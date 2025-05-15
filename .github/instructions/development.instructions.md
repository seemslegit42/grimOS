---
applyTo: 'grimOS: Brand & Development Guide for AI Coding Agent
Document Purpose: This document provides essential brand, design, and technical guidelines for an AI coding agent assisting in the development of grimOS and its associated components. It incorporates information from the Grimoire™ (grimOS) Comprehensive Blueprint, Requirements Specification, and OS Playbook.
1. Core Product Suite Overview
Company: BitBrew Inc.
Main Platform: grimOS
Concept: A "Unified Intelligence Layer" or "Digital Grimoire." A sentient, AI-powered enterprise operating system (Digital Operations Platform - DOP).
Purpose: To integrate security, operations, and strategic decision-making for mid-market to large enterprises, enabling them to design, automate, manage, and optimize business processes and workflows.
Core Values (Inspired by Blueprints & OS Playbook): Innovation, Intelligence, Unification, Security, Scalability, Extensibility, User Empowerment, Ethical Responsibility, People-Centricity, Results-Driven, Collaboration, Adaptability (Pivoting), Transparency, Agency, Flow.
Future Cybersecurity Expansion: Command & Cauldron™
Concept: A sentient Command & Control (C2) and Cyber Operations Framework built on grimOS.
Purpose: To serve elite red/blue teams, cybersecurity analysts, and autonomous security agents.
2. Target Audience (Context for Development)
Primary Users of grimOS (from Comprehensive Blueprint):
Mid-Market Enterprises (500-5000 employees)
Large Enterprises (5000+ employees)
Specific Industry Focus (Phase 2 onwards): Finance, Healthcare, Manufacturing.
Key User Roles: Security Analysts, Engineers, Architects, Operations Managers, Business Analysts, CEOs, Strategic Leaders, IT Administrators, Internal and Third-Party Developers.
Broader User Categories (from Requirements Specification, for context):
Developers & Technical Innovators (Solo hackers, indie dreamers, small teams building AI-powered tools).
Small to Medium-sized Businesses (SMBs seeking automation and insights).
Forward-Thinking Operational Sorcerers (Individuals in larger companies implementing agile, AI-native solutions).
Future Users of Command & Cauldron™:
Elite Red/Blue Teams
Cybersecurity Analysts
Autonomous Security Agents
3. Core Architectural Principles (for grimOS)
Microservices Architecture: Independent, deployable services.
Event-Driven Architecture (EDA): Asynchronous communication (e.g., Kafka) for scalability and resilience.
API-First Design: All functionalities exposed via a Universal API Fabric. (MACH compliance)
Data Mesh Architecture: Decentralized data ownership, domain-oriented data products.
AI-Powered Core: ML/DL/Reinforcement Learning integrated throughout.
Security by Design: Security embedded at every layer.
Composable Architecture: Flexible assembly of features and integrations. (MACH compliance, Composable Enterprise approach)
Cloud-Native: Designed for cloud deployment. (MACH compliance)
Headless: Decoupled frontend and backend. (MACH compliance)
4. Key Modules & Features (grimOS - Based on Requirements Specification)
4.1 Cognitive Core (AI/Agents)
4.1.1 Agent Orchestration: Embed, orchestrate, manage autonomous AI agents (e.g., SuperAGI, AutoGen, LangGraph). Enable agent collaboration.
4.1.2 Natural Language Workflow Creation (ScrollWeaver): GenAI co-pilot for generating operational workflows from natural language descriptions.
4.1.3 Predictive Intelligence (Omens): Anomaly detection, predictive insights, proactive suggestions from operational data.
4.1.4 AI Assistant (Familiar): Context-aware AI assistant in UI for guidance, commands, suggestions.
4.1.5 Agent Management: Create, modify, manage custom agents; define agent permissions/access controls; monitor agent activity/performance.
4.2 Composable Runes (Low-Code Logic Builder)
4.2.1 Visual Workflow Designer (RuneForge): Drag-and-drop interface. Library of pre-built logic blocks ("Runes"): conditionals, triggers, webhooks, API calls, agent tasks, GenAI actions.
4.2.2 Workflow Version Control (Spells): Track changes, allow forking/modification of workflows.
4.2.3 Reusable Components (Runes/Spell Scrolls): Save complex multi-agent workflows as reusable modules.
4.2.4 Rune Marketplace: Publish, share, search, discover custom Runes. Versioning and dependency management.
4.3 Interoperability Engine (iPaaS Layer)
4.3.1 Built-in iPaaS: Pre-built connectors (ERPs, CRMs, Stripe, Slack, GSuite, etc.).
4.3.2 MACH Compliance: Adherence to Microservices, API-first, Cloud-native, Headless principles.
4.3.3 API Management: Define, publish, manage custom APIs. Versioning, lifecycle management, security (authN/authZ).
4.4 Observability Dashboards
4.4.1 Functional Dashboards (Grimoires): Real-time dashboards for Sales, Operations, Finance, etc. (metrics, analytics, summaries).
4.4.2 Unified Observability (SigilSight): Monitor agent behavior, workflow execution, system performance. Features: playback, logging, audit trails.
4.4.3 Process Mining: Visualize, analyze process flows. Identify bottlenecks, optimization areas.
4.5 Governance + Trust Layer
4.5.1 Access Control: Fine-grained RBAC for users and agents.
4.5.2 Audit Logging: Immutable audit logs for all system activity and user actions.
4.5.3 Approval Flows: Human-in-the-loop approval for critical operations.
4.5.4 Agent Sandboxing: Restrict agent capabilities, prevent unintended actions.
4.5.5 Data Loss Prevention (DLP): Prevent unauthorized data access/transmission by agents.
4.5.6 Explainability (XAI): Tools for understanding/visualizing agent decision-making.
4.6 Persistent Memory & Identity (Cauldron Core)
4.6.1 User Authentication: Robust user identity verification.
4.6.2 Session Management: Maintain user sessions and context.
4.6.3 Memory System: Recognize users, retain context, remember project details/history, learn preferences. Differentiate short-term (working) and long-term (episodic, semantic, procedural) memory.
4.6.4 Data Management: Tools for storage, retrieval, organization of data used by agents/workflows. Support various data formats/sources.
4.7 Conversational Operating System (CoS)
4.7.1 Natural Language Interface: Input commands, queries, requests via natural language.
4.7.2 Proactive Assistance: Suggestions/recommendations based on user context/system data.
4.7.3 Task Automation: Trigger agentic workflows from natural language input.
4.7.4 Communication Features: Agent-user communication via CoS (text, voice channels).
4.7.5 Morning Briefs: Daily summaries of relevant info/upcoming tasks.
4.7.6 Decision Queue: Queue of pending decisions/recommendations for users.
4.7.7 Agent Recommendations: Suggest relevant agents for tasks/workflows.
5. Technology Stack (Prioritizing Requirements Specification & Blueprints)
Primary Languages: Python (Backend), TypeScript (Frontend)
Supporting Languages: Java, Go (for specific microservices as needed, per Comprehensive Blueprint)
Frontend:
Framework: Next.js (Leveraging next-enterprise boilerplate for structure, internationalization, testing, etc.)
UI Library: React
Component Library: shadcn/ui
Styling: Tailwind CSS
Backend:
Frameworks/Libraries: Python, LangGraph
AI SDK: AI SDK for TypeScript (for developer ecosystem, per Comprehensive Blueprint)
Message Queue: Apache Kafka
Databases:
Relational (Structured Data): PostgreSQL
Caching/Message Queuing (can also be used by Kafka): Redis
Vector Database (AI Memory):
MVP/Local: ChromaDB
Scale: Redis (with vector search), Zilliz Cloud, or Qdrant
NoSQL (from Comprehensive Blueprint, if specific needs arise): MongoDB, Cassandra
Graph (from Comprehensive Blueprint, if specific needs arise): Neo4j
Time-Series (from Comprehensive Blueprint, if specific needs arise): TimescaleDB
Cloud Platform: AWS, Azure, or GCP (design for cloud-agnostic principles where feasible)
Containerization & Orchestration: Docker, Kubernetes
AI/ML Libraries: TensorFlow, PyTorch, scikit-learn, MLflow, Kubeflow
Large Language Models (LLMs): Integration capability for models like OpenAI GPT series, Anthropic Claude, Google Gemini.
AI Acceleration (Inference): Groq (mentioned in Comprehensive Blueprint)
Monitoring & Logging: Prometheus, Grafana, OpenTelemetry
API Gateway: Kong (or cloud-native equivalent like AWS API Gateway, Azure API Management)
Deployment Model: Multi-tenant SaaS. Consider hybrid tenancy for sensitive AI agent operations.
6. Visual Identity: "Corporate Cyberpunk" - Digital Weave Palette
Theme: High-tech, sleek, professional, energetic, secure, intelligent, efficient.
Selected Palette: Digital Weave
Primary Green (Lime): #7ED321
Usage: Key branding (logo accents), primary CTAs, active states, highlights, positive trends/status, progress indicators.
Secondary 1 (Near Black): #121212
Usage: Main UI backgrounds, containers, large surfaces. Foundation of the dark theme. Provides strong contrast.
Secondary 2 (Electric Blue): #00BFFF
Usage: Secondary highlights, informational icons, inactive but important elements, data visualizations, differentiating UI sections, subtle gradients.
Accent 1 (Hot Pink): #FF1D58
Usage: Critical alerts, error messages, urgent notifications, destructive action confirmations. Use sparingly for maximum impact.
Accent 2 (White): #FFFFFF
Usage: All primary text content, standard icons, borders, subtle UI dividers. Ensure high readability against dark backgrounds.
Implementation Notes:
Maintain high contrast for readability (WCAG AA/AAA minimum).
Use gradients subtly (e.g., Green-to-Blue, Color-to-Black) to enhance futuristic feel without sacrificing clarity.
Digital motifs (e.g., fine grids, subtle circuit patterns, flowing data lines) can be used as background textures or decorative elements if they don't clutter the UI.
7. UI/UX Design Principles (for grimOS Interface)
Clarity & Intuitiveness (OS Playbook: Transparency): Users should understand status and navigate easily. Information should be accessible.
Efficiency & Flow (OS Playbook: Flow): Streamline common tasks; minimize clicks. Support users in achieving their goals without friction.
Information Density & Visualization (Data as Light): Present complex data clearly through well-designed dashboards and dynamic visualizations.
Responsiveness: Fast load times and interactions.
Consistency: Uniform design language (via shadcn/ui components) and interaction patterns across all modules.
Customization & Agency (OS Playbook: Agency): Allow users to tailor views/dashboards where appropriate, giving them control over their workspace.
Accessibility: Adhere to WCAG standards (color contrast, keyboard navigation, screen reader compatibility).
Aesthetic: Modern, clean, professional, aligning with "Corporate Cyberpunk" and the Digital Weave palette.
People-Centric (OS Playbook: People Over Process): Design for human users first, making the system supportive and enabling.
Results-Oriented (OS Playbook: Results Over Reports): UI should help users achieve and track meaningful outcomes.
Specific UI Elements (from grimOS Dev Blueprint): Unified Dashboard, Context-Aware Navigation, Natural Language Interaction (CoS), Predictive Insights Overlay, Process Cartography (visualization of processes), Subtle Security Awareness cues.
8. API Design Principles (Universal API Fabric)
RESTful & GraphQL: Offer both for flexibility.
Clear & Consistent Naming Conventions.
Well-defined Request/Response Formats: JSON primary.
Comprehensive Documentation: OpenAPI/Swagger for REST, schema for GraphQL. Auto-generate where possible.
Secure Authentication & Authorization: OAuth 2.0 / OpenID Connect, Role-Based Access Control (RBAC).
Versioning: Clear API versioning strategy (e.g., URI path versioning).
Robust Error Handling: Standardized, informative error codes and messages.
Statelessness (for REST).
Performance: Optimized for low latency and high throughput. Idempotency for relevant operations.
Discoverability: APIs should be easily discoverable and understandable.
9. Ethical AI Considerations (for Development)
Fairness & Non-Discrimination: Design and rigorously test AI models to identify and mitigate biases.
Transparency/Explainability (XAI): Implement XAI features (as per 4.5.6). Log AI-driven actions and decisions.
Accountability & Auditability: Enable comprehensive audit trails for all AI operations and decisions.
Privacy & Data Protection: Implement strong data encryption (at rest, in transit), anonymization/pseudonymization where appropriate. Adhere to GDPR, CCPA, etc.
Human Agency & Oversight (OS Playbook: Dignity, Agency): Ensure critical AI-driven decisions can be reviewed, overridden, or require human approval (as per 4.5.3). AI should augment, not replace, human judgment in high-stakes scenarios.
Security & Robustness: Protect AI models and data from adversarial attacks (e.g., data poisoning, model evasion). Ensure resilience.
Beneficence: Strive for AI applications within grimOS to genuinely benefit users and their organizations.
10. Development Phases & Priorities (High-Level Context - Aligned with Blueprints)
Phase 1 (MVP): Core Foundation
Security: Threat Intelligence, UBA (as per Comprehensive Blueprint).
Operations: Workflow Automation, Data Integration (as per Comprehensive Blueprint).
Cognitive Core: Basic AI capabilities, initial agent management, Natural Language Workflow Creation (ScrollWeaver MVP).
Platform: Universal API Fabric, Core Data Management (PostgreSQL, Redis, ChromaDB), Initial UI (Next.js with next-enterprise boilerplate, shadcn/ui, Digital Weave palette).
Key Modules from Req Spec to consider for MVP: Basic RuneForge, SigilSight (logging), Cauldron Core (Auth, Session, Basic Memory), CoS (basic NL input).
Phase 2: Expansion
Enhance Cognitive Core (Predictive Modeling - Omens, Gemini integration, full Agent Orchestration).
Develop Rune Marketplace, full Process Mining.
Expand Interoperability Engine (more connectors).
Mature Governance + Trust Layer (DLP, full XAI).
Industry-specific modules.
Developer Ecosystem (AI SDK for TypeScript).
Phase 3: Growth & Advanced Features
Autonomous capabilities (as per Comprehensive Blueprint).
Full CoS features (Morning Briefs, Decision Queue).
Begin Command & Cauldron™ development.
This guide should serve as a foundational reference for the AI coding agent. Refer to the full "Grimoire™ (grimOS) Comprehensive Blueprint" and "Detailed Requirements Specification for Grimoire™" for more granular details.
'
---

Coding standards, domain knowledge, and preferences that AI should follow.
