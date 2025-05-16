from fastapi import APIRouter, Depends
from typing import Dict, List, Any
import random
from datetime import datetime, timedelta

router = APIRouter()

# Mock data generation functions
def generate_weekly_data() -> List[Dict[str, Any]]:
    """Generate mock data for weekly AI jobs"""
    today = datetime.now()
    data = []
    
    for i in range(7):
        date = today - timedelta(days=6-i)
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "nlp_jobs": random.randint(10, 50),
            "vision_jobs": random.randint(5, 30),
            "codegen_jobs": random.randint(15, 45)
        })
    
    return data

def generate_job_distribution() -> List[Dict[str, Any]]:
    """Generate mock data for job type distribution"""
    return [
        {"name": "NLP", "value": random.randint(100, 300)},
        {"name": "Vision", "value": random.randint(50, 200)},
        {"name": "Codegen", "value": random.randint(150, 250)},
        {"name": "Other", "value": random.randint(20, 100)}
    ]

@router.get("/demo", response_model=Dict[str, Any])
async def get_dashboard_stats():
    """
    Get mock dashboard statistics for grimOS
    
    Returns:
        Dict containing various metrics and chart data for the dashboard
    """
    # Determine system status based on random value
    status_value = random.random()
    if status_value > 0.8:
        system_status = "ERROR"
    elif status_value > 0.6:
        system_status = "WARN"
    else:
        system_status = "OK"
    
    # Generate mock data
    return {
        "metrics": {
            "total_users": random.randint(1000, 5000),
            "active_sessions": random.randint(50, 500),
            "ai_jobs_completed": random.randint(5000, 20000),
            "system_status": system_status
        },
        "charts": {
            "weekly_jobs": generate_weekly_data(),
            "job_distribution": generate_job_distribution()
        },
        "updated_at": datetime.now().isoformat()
    }