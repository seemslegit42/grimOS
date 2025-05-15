from typing import List, Optional, Dict, Any
import httpx
from sqlalchemy.orm import Session
import asyncio
import re
import json
import logging
from datetime import datetime

# Import spaCy for NLP
try:
    import spacy
    import en_core_web_sm
    nlp = en_core_web_sm.load()
except ImportError:
    # Fallback if spaCy is not available
    nlp = None

from app.repositories.base import BaseRepository
from app.models.cognitive import ScrollWeaverRequest as ScrollWeaverRequestModel, AnalysisTrend
from app.schemas.cognitive import ScrollWeaverRequest, ScrollWeaverResponse, ScrollWeaverStep
from app.core.config import settings

logger = logging.getLogger(__name__)

class ScrollWeaverRepository:
    async def process_request(self, db: Session, *, user_id: str, request: ScrollWeaverRequest) -> ScrollWeaverResponse:
        """Process a ScrollWeaver request"""
        # Save the request
        db_obj = ScrollWeaverRequestModel(
            natural_language_input=request.natural_language_input,
            user_id=user_id,
            processing_status="processing",
        )
        db.add(db_obj)
        db.commit()
        
        try:
            # Parse the natural language input
            if nlp:
                # Use spaCy if available
                interpreted_steps = await self._parse_with_spacy(request.natural_language_input)
                confidence_score = 0.85  # Higher confidence with spaCy
            else:
                # Fallback to rule-based approach
                interpreted_steps = self._parse_with_rules(request.natural_language_input)
                confidence_score = 0.7  # Lower confidence with rules
            
            # Create warnings for ambiguous terms or unsupported actions
            warnings = self._generate_warnings(request.natural_language_input, interpreted_steps)
            
            # Create the response
            response = ScrollWeaverResponse(
                original_input=request.natural_language_input,
                interpreted_steps=interpreted_steps,
                confidence_score=confidence_score,
                warnings=warnings,
            )
            
            # Update the request with the response
            db_obj.response = response.dict()
            db_obj.processing_status = "completed"
            db_obj.confidence_score = confidence_score
            db.add(db_obj)
            db.commit()
            
            return response
        except Exception as e:
            # Handle errors
            logger.error(f"Error processing ScrollWeaver request: {str(e)}")
            db_obj.processing_status = "failed"
            db_obj.error = str(e)
            db.add(db_obj)
            db.commit()
            raise
    
    async def _parse_with_spacy(self, text: str) -> List[ScrollWeaverStep]:
        """Parse natural language using spaCy NLP"""
        steps = []
        step_number = 1
        
        # Process the text with spaCy
        doc = nlp(text)
        
        # Split text into sentences
        sentences = list(doc.sents)
        
        for i, sent in enumerate(sentences):
            sent_text = sent.text.strip()
            
            # Skip if empty
            if not sent_text:
                continue
                
            # Extract verbs, subjects and objects
            verbs = [token for token in sent if token.pos_ == "VERB"]
            
            if verbs:
                main_verb = verbs[0]
                action = None
                description = sent_text
                parameters = {}
                
                # Check for common workflow verbs
                if main_verb.lemma_ in ["assign", "allocate", "delegate"]:
                    action = "Assign Manual Task"
                    # Extract what is being assigned to whom
                    task = None
                    assignee = None
                    
                    # Find direct object (what is being assigned)
                    for child in main_verb.children:
                        if child.dep_ in ["dobj", "attr"]:
                            task = ' '.join([w.text for w in child.subtree])
                    
                    # Find indirect object (to whom it's assigned)
                    to_parts = []
                    found_to = False
                    for token in sent:
                        if token.text.lower() == "to":
                            found_to = True
                        elif found_to:
                            to_parts.append(token.text)
                    
                    if to_parts:
                        assignee = ' '.join(to_parts)
                    
                    parameters = {
                        "task_name": task if task else "Unspecified Task",
                        "assignee": assignee if assignee else "Unspecified Person"
                    }
                    
                elif main_verb.lemma_ in ["notify", "alert", "inform", "send"]:
                    action = "Send Notification"
                    # Extract message and recipient
                    message = None
                    recipient = None
                    
                    # Simple extraction logic - everything after "send" until "to"
                    verb_idx = sent_text.lower().find(main_verb.text.lower())
                    to_idx = sent_text.lower().find("to", verb_idx)
                    
                    if to_idx > verb_idx:
                        message = sent_text[verb_idx + len(main_verb.text):to_idx].strip()
                        recipient = sent_text[to_idx + 2:].strip()
                    
                    parameters = {
                        "message": message if message else "Unspecified Message",
                        "recipient": recipient if recipient else "Unspecified Recipient"
                    }
                
                elif main_verb.lemma_ in ["check", "verify", "validate"]:
                    action = "Validation Step"
                    condition = ' '.join([w.text for w in list(main_verb.children)])
                    parameters = {
                        "condition": condition if condition else "Unspecified Condition"
                    }
                
                else:
                    # Generic action for any other verb
                    action = f"{main_verb.lemma_.capitalize()} Action"
            
            else:
                # If no verb found, use generic action
                action = "Process Step"
            
            steps.append(ScrollWeaverStep(
                step_number=step_number,
                action=action,
                description=description,
                parameters=parameters
            ))
            
            step_number += 1
        
        # If no steps were generated, create a generic one
        if not steps:
            steps.append(ScrollWeaverStep(
                step_number=1,
                action="Process Step",
                description=text,
                parameters={}
            ))
        
        return steps
    
    def _parse_with_rules(self, text: str) -> List[ScrollWeaverStep]:
        """Simple rule-based parsing fallback"""
        steps = []
        
        # Split by keywords like "then" or "next" or periods
        parts = re.split(r'\s+then\s+|\s+next\s+|\.', text.lower())
        parts = [p.strip() for p in parts if p.strip()]
        
        for i, part in enumerate(parts):
            step_number = i + 1
            action = "Process Step"
            description = part
            parameters = {}
            
            # Try to extract action and target
            if re.search(r'\bassign\b', part) and re.search(r'\bto\b', part):
                # Extract task and assignee
                match = re.search(r'\bassign\s+(.*?)\s+to\s+(.*?)(?:$|\.)', part)
                if match:
                    task = match.group(1).strip()
                    assignee = match.group(2).strip()
                    
                    action = "Assign Manual Task"
                    parameters = {
                        "task_name": task,
                        "assignee": assignee,
                    }
                    
            elif any(verb in part for verb in ["send", "notify", "alert"]) and "to" in part:
                # Extract message and recipient
                for verb in ["send", "notify", "alert"]:
                    if verb in part:
                        match = re.search(f'\\b{verb}\\s+(.*?)\\s+to\\s+(.*?)(?:$|\\.)', part)
                        if match:
                            message = match.group(1).strip()
                            recipient = match.group(2).strip()
                            
                            action = "Send Notification"
                            parameters = {
                                "message": message,
                                "recipient": recipient,
                            }
                            break
                        
            elif any(verb in part for verb in ["check", "verify", "validate"]):
                # Extract condition
                for verb in ["check", "verify", "validate"]:
                    if verb in part:
                        match = re.search(f'\\b{verb}\\s+(.*?)(?:$|\\.)', part)
                        if match:
                            condition = match.group(1).strip()
                            
                            action = "Validation Step"
                            parameters = {
                                "condition": condition,
                            }
                            break
            
            steps.append(ScrollWeaverStep(
                step_number=step_number,
                action=action,
                description=description,
                parameters=parameters
            ))
        
        return steps
    
    def _generate_warnings(self, text: str, steps: List[ScrollWeaverStep]) -> List[str]:
        """Generate warnings for potential issues in the request"""
        warnings = []
        
        # Check for potential ambiguities
        if text.count("it") > 0 or text.count("this") > 0:
            warnings.append("Ambiguous references detected ('it' or 'this'). Consider being more specific.")
        
        # Check for complex conditions
        if "if" in text and ("and" in text or "or" in text):
            warnings.append("Complex conditional logic detected. Consider breaking into multiple steps.")
        
        # Check for steps without clear parameters
        for step in steps:
            if step.action != "Process Step" and not step.parameters:
                warnings.append(f"Step {step.step_number} ({step.action}) lacks clear parameters.")
        
        return warnings


class AnalysisTrendRepository:
    def get_operational_trends(
        self, 
        db: Session, 
        *, 
        trend_type: Optional[str] = None, 
        time_period: Optional[str] = None,
        severity: Optional[str] = None
    ) -> List[AnalysisTrend]:
        """Get operational trends with various filtering options"""
        # Query base
        query = db.query(AnalysisTrend)
        
        # Apply filters
        if trend_type:
            query = query.filter(AnalysisTrend.trend_type == trend_type)
        
        if severity:
            query = query.filter(AnalysisTrend.severity == severity)
            
        # Time period filtering
        if time_period:
            now = datetime.utcnow()
            
            if time_period == "today":
                start_date = datetime(now.year, now.month, now.day)
                query = query.filter(AnalysisTrend.created_at >= start_date)
            elif time_period == "week":
                # Last 7 days
                from datetime import timedelta
                start_date = now - timedelta(days=7)
                query = query.filter(AnalysisTrend.created_at >= start_date)
            elif time_period == "month":
                # Last 30 days
                from datetime import timedelta
                start_date = now - timedelta(days=30)
                query = query.filter(AnalysisTrend.created_at >= start_date)
        
        # Sort by severity and creation date
        query = query.order_by(
            AnalysisTrend.severity.desc(),  # Critical first
            AnalysisTrend.created_at.desc()  # Newest first
        )
        
        return query.all()

    async def generate_mock_trends(self, db: Session) -> List[AnalysisTrend]:
        """Generate mock trends for development purposes"""
        from uuid import uuid4
        
        # Mock data for development
        mock_trends = [
            {
                "trend_type": "workflow_duration_anomaly",
                "resource_id": str(uuid4()),
                "resource_type": "workflow_definition",
                "message": "Workflow 'Approval Process' average completion time increased by 25% this week.",
                "severity": "warning",
                "details": {
                    "average_time_previous": 24.5,  # hours
                    "average_time_current": 30.6,   # hours
                    "percent_change": 25,
                    "affected_workflow_name": "Approval Process"
                }
            },
            {
                "trend_type": "login_failures",
                "resource_id": None,
                "resource_type": "security",
                "message": "Unusual spike in failed login attempts detected from IP range 192.168.1.x",
                "severity": "critical",
                "details": {
                    "ip_range": "192.168.1.0/24",
                    "failure_count": 45,
                    "time_window": "1 hour",
                    "normal_baseline": 5
                }
            },
            {
                "trend_type": "workflow_start_anomaly",
                "resource_id": str(uuid4()),
                "resource_type": "workflow_definition",
                "message": "Significant decrease in 'Customer Onboarding' workflow initiations today.",
                "severity": "info",
                "details": {
                    "current_count": 3,
                    "average_daily_count": 12,
                    "percent_change": -75,
                    "affected_workflow_name": "Customer Onboarding"
                }
            }
        ]
        
        # Create and add to database
        db_trends = []
        for trend_data in mock_trends:
            details = trend_data.pop("details")
            
            db_trend = AnalysisTrend(
                **trend_data,
                details=details
            )
            db.add(db_trend)
            db_trends.append(db_trend)
        
        db.commit()
        
        return db_trends


scrollweaver_repository = ScrollWeaverRepository()
analysis_trend_repository = AnalysisTrendRepository()
