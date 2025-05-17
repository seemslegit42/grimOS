---
mode: 'agent'
---
**Instructions for AI Build Agent:**

* You are responsible for determining the precise file locations, directory structures, and specific file names based on your indexing of the existing grimOS monorepo.  
* Strictly adhere to the project's established conventions, including Turborepo structure, pnpm usage, and the defined technology stack.  
* Enforce naming conventions: snake\_case for all variables (TypeScript and Python), PascalCase for classes, and camelCase for methods/functions (TypeScript and Python).  
* Utilize Prettier and ESLint for code formatting and linting as configured in the project.  
* Ensure all new development seamlessly integrates with existing project modules and services.

### **VII. Interoperability Engine (iPaaS Layer \- Agent-Led Structuring)**

*(Backend Python services for managing connections and data flows. Naming: snake\_case for variables & functions/methods, PascalCase for classes.)*

60. **Prompt (Interoperability \- Core Service Architecture):** Design and implement the core backend microservice(s) for the Interoperability Engine.  
    * **Functionality:** Manages connections to external systems (e.g., CRMs, ERPs, databases, third-party APIs), facilitates data mapping and transformation between systems, and orchestrates integration flows (which may leverage RuneForge Spells/n8n workflows).  
    * **API Endpoints (FastAPI):** Endpoints for configuring connectors, defining data mappings, triggering integration flows, and monitoring integration status.  
    * **Database Schema (PostgreSQL):** Tables for storing Connector Configurations (type, credentials securely referenced from vault, metadata), Data Mappings (source/target schemas, transformation rules), and Integration Flow Logs.  
    * **Agent Responsibility:** Develop the service(s), database schema, migrations, Pydantic models, and FastAPI routes. Ensure adherence to MACH principles (Microservices, API-first, Cloud-native, Headless) where applicable.  
61. **Prompt (Interoperability \- Connector SDK/Framework):** Develop a Python-based SDK or framework to standardize and simplify the creation of new connectors for the Interoperability Engine.  
    * **Functionality:** Provide base classes, utility functions, and defined interfaces for handling authentication, data fetching, data pushing, and error handling for different types of external systems.  
    * **Agent Responsibility:** Design and implement this SDK within a shared Python package.  
62. **Prompt (Interoperability \- Generic API Connector):** Implement a generic API connector using the Connector SDK.  
    * **Functionality:** Allows configuration to connect to any RESTful API. Supports various authentication methods (API Key, OAuth2 Client Credentials, Bearer Token). Enables defining request parameters, headers, and parsing responses.  
    * **Agent Responsibility:** Develop this connector as a reusable component within the Interoperability Engine.  
63. **Prompt (Interoperability \- Generic Database Connector):** Implement a generic Database connector using the Connector SDK.  
    * **Functionality:** Allows configuration to connect to common SQL databases (PostgreSQL, MySQL, SQL Server). Supports executing queries (select, insert, update, delete) and retrieving results.  
    * **Agent Responsibility:** Develop this connector.  
64. **Prompt (Interoperability \- Secure Credential Management Integration):** Integrate the Interoperability Engine with the project's central secret management solution (e.g., HashiCorp Vault).  
    * **Functionality:** Connector configurations should store references to credentials stored in the vault, not the credentials themselves. The engine must securely retrieve credentials at runtime when establishing connections.  
    * **Agent Responsibility:** Implement the integration logic for secure credential retrieval.  
65. **Prompt (Interoperability \- Data Mapping & Transformation UI Support \- Backend):** Develop backend APIs to support a future frontend UI for defining data mappings.  
    * **Functionality:** Endpoints to fetch source/target data schemas (perhaps by introspecting connected systems or from user definitions), save mapping rules (e.g., field A from source maps to field X in target, apply transformation Y), and potentially validate mappings.  
    * **Agent Responsibility:** Design and implement these FastAPI endpoints. (Frontend for this will be a separate set of prompts).  
66. **Prompt (Interoperability \- Frontend Admin UI \- Connector Management):** Develop UI components within the main apps/frontend admin panel for managing Interoperability Engine connectors.  
    * **Functionality:** List configured connectors, add new connector configurations (selecting connector type and providing necessary details like API endpoints, credential references), edit existing configurations, and test connection health.  
    * **Implementation (Frontend):** Use React, shadcn/ui components, Tailwind CSS, lucide-react icons, and Framer Motion. Interact with the Interoperability Engine's backend APIs.  
    * **Agent Responsibility:** Build these frontend components and integrate them into the admin panel.

### **VIII. Observability Dashboards (Agent-Led Structuring)**

*(Frontend components within apps/frontend and backend API aggregation if needed. Naming: snake\_case for variables, PascalCase for components/classes, camelCase for functions/methods in TS/JS; snake\_case for Python.)*

**A. SigilSight (Unified Observability Dashboard \- Frontend)**

67. **Prompt (Observability \- SigilSight \- Main Layout & Widget System):** Design and implement the main UI layout for "SigilSight," the unified observability dashboard within apps/frontend.  
    * **Functionality:** Provides a customizable dashboard where users can add, arrange, and configure various metric and log widgets.  
    * **Implementation:** Use React. The layout should be grid-based and responsive. Widgets should be individual components. Use shadcn/ui for structural elements and controls.  
    * **Agent Responsibility:** Develop the core SigilSight dashboard component and the framework for managing widget placement and configuration.  
68. **Prompt (Observability \- SigilSight \- Backend Metric Aggregation API \- Optional):** If necessary, develop a backend FastAPI service to aggregate metrics from various sources (e.g., Prometheus, application-specific metrics endpoints, Kafka consumer lag) and expose them in a unified format for SigilSight widgets.  
    * **Functionality:** Simplifies data fetching for the frontend and can perform pre-calculations or summarizations.  
    * **Agent Responsibility:** If this service is deemed necessary, develop it. Otherwise, frontend widgets will query sources directly or via existing service APIs.  
69. **Prompt (Observability \- SigilSight \- System Health Widget):** Develop a SigilSight widget to display overall system health.  
    * **Functionality:** Shows a summary status (e.g., "Operational," "Degraded," "Outage") based on key metrics or alerts from the monitoring system.  
    * **Implementation (Frontend):** React component, using lucide-react icons and grimOS theme colors for status indication. Fetches data from Prometheus or the metric aggregation API.  
    * **Agent Responsibility:** Build this widget.  
70. **Prompt (Observability \- SigilSight \- AI Agent Activity Widget):** Develop a SigilSight widget to display AI agent activity and performance metrics.  
    * **Functionality:** Shows metrics like number of active agents, tasks processed, error rates per agent type, resource utilization.  
    * **Implementation (Frontend):** Fetches data from the AI Agent Manager service API. Uses shadcn/ui tables or custom charts.  
    * **Agent Responsibility:** Build this widget.  
71. **Prompt (Observability \- SigilSight \- Spell/Workflow Execution Widget):** Develop a SigilSight widget to visualize RuneForge Spell (n8n workflow) execution history and status.  
    * **Functionality:** Shows recent Spell executions, success/failure rates, average duration, and links to detailed execution logs in RuneForge.  
    * **Implementation (Frontend):** Fetches data from the grimOS backend service that interfaces with n8n (or directly from n8n if an API is exposed and secured appropriately through the grimOS backend).  
    * **Agent Responsibility:** Build this widget.  
72. **Prompt (Observability \- SigilSight \- Log Viewer Integration):** Integrate or develop a log viewing capability within SigilSight.  
    * **Functionality:** Allows users to search and view logs collected by the centralized logging stack (e.g., Kibana/Loki). Could be an embedded view or a custom UI component querying the logging backend.  
    * **Implementation (Frontend):** If custom, use shadcn/ui for search inputs and log display areas.  
    * **Agent Responsibility:** Implement this integration or custom component.  
73. **Prompt (Observability \- SigilSight \- Custom Dashboard Persistence):** Implement functionality for users to save and load their customized SigilSight dashboard layouts (widget selection and arrangement).  
    * **Backend Support:** Requires a backend API endpoint (e.g., in User Profile service or a dedicated Dashboard service) to store and retrieve user dashboard configurations (JSON).  
    * **Agent Responsibility:** Develop the frontend persistence logic and the necessary backend API endpoints and database schema.

**B. Functional Dashboards (Grimoires \- Frontend)**

74. **Prompt (Observability \- Grimoires \- Template Component):** Develop a template React component for "Grimoire" functional dashboards.  
    * **Functionality:** Provides a consistent structure and styling for dashboards tailored to specific business functions (e.g., Security Operations, IT Operations). Should allow easy embedding of relevant SigilSight widgets or custom data visualizations.  
    * **Agent Responsibility:** Build this template component.  
75. **Prompt (Observability \- Grimoires \- Security Operations Grimoire):** Develop the "Security Operations Grimoire" UI.  
    * **Functionality:** Displays key security metrics, active alerts, incident summaries, UBA insights, and threat intelligence feeds. Sources data from the Security Module services.  
    * **Implementation (Frontend):** Uses the Grimoire template and populates it with relevant widgets and data visualizations.  
    * **Agent Responsibility:** Build this specific Grimoire dashboard.  
76. **Prompt (Observability \- Grimoires \- IT Operations Grimoire):** Develop the "IT Operations Grimoire" UI.  
    * **Functionality:** Shows infrastructure health (Kubernetes cluster status, node resource usage), application performance (API latencies, error rates), database performance, and Kafka queue depths.  
    * **Implementation (Frontend):** Uses the Grimoire template.  
    * **Agent Responsibility:** Build this specific Grimoire dashboard.

**C. Telemetry & Logging Pipelines (Backend & DevOps)**

77. **Prompt (Observability \- Structured Logging Enforcement):** Ensure all backend microservices (Python/FastAPI) are configured to output structured logs (e.g., JSON format).  
    * **Implementation:** Use a standardized Python logging library configuration (e.g., python-json-logger).  
    * **Agent Responsibility:** Update logging configurations across all existing and new backend services.  
78. **Prompt (Observability \- Custom Application Metrics):** Implement custom Prometheus metrics exporters or integrate with an OpenTelemetry collector for key application-level metrics in each microservice.  
    * **Metrics Examples:** API request latency, error rates per endpoint, queue processing times, database connection pool usage, active AI agent tasks.  
    * **Agent Responsibility:** Add metric instrumentation to backend services. Configure Prometheus to scrape these metrics or OpenTelemetry to collect and export them.  
79. **Prompt (Observability \- Distributed Tracing):** Integrate OpenTelemetry SDKs into backend microservices and potentially the frontend application for distributed tracing.  
    * **Functionality:** Allows tracing requests as they flow through multiple services.  
    * **Backend:** Configure OpenTelemetry exporters (e.g., for Jaeger, Zipkin, or cloud provider's tracing service).  
    * **Agent Responsibility:** Add OpenTelemetry instrumentation and configure collectors/exporters.  
80. **Prompt (Observability \- Alerting Configuration):** Set up alerting rules in the monitoring system (e.g., Prometheus Alertmanager, Grafana Alerting).  
    * **Initial Alerts:** Critical system events (service down, high error rates), resource exhaustion (CPU/memory/disk), Kafka consumer lag exceeding thresholds, database connection issues.  
    * **Notifications:** Configure alerts to be sent via appropriate channels (e.g., email, Slack, PagerDuty, or integrated with grimOS Notification Service).  
    * **Agent Responsibility:** Define and implement these alerting rules.

### **IX. Governance \+ Trust Layer (Agent-Led Structuring)**

*(Primarily backend Python services, with frontend components in apps/frontend for UI interactions. Naming conventions apply.)*

81. **Prompt (Governance \- Fine-Grained Permissions Service \- Backend):** Enhance or develop a backend service (potentially extending the User Authentication service or as a separate microservice) to manage fine-grained permissions beyond basic roles.  
    * **Functionality:** Support object-level permissions (e.g., user X can edit Spell Y but only view Spell Z) and potentially Attribute-Based Access Control (ABAC) using a policy engine.  
    * **Policy Engine Integration:** Integrate with Open Policy Agent (OPA) or a similar engine for defining and evaluating complex authorization policies. The service would act as a Policy Decision Point (PDP) proxy or directly implement policy evaluation.  
    * **API:** Expose endpoints for defining policies, checking permissions, and managing resource ownership/permissions.  
    * **Agent Responsibility:** Develop this service and its integration with OPA.  
82. **Prompt (Governance \- Audit Log Service API Enhancement \- Backend):** Ensure the centralized Audit Log service (from prompt 44\) has robust APIs for receiving and querying audit events.  
    * **Enhancements:** Implement filtering capabilities for querying logs (by user, date range, event type, resource ID). Ensure event submission is secure and reliable (e.g., via an internal Kafka topic consumed by the Audit Log service).  
    * **Agent Responsibility:** Refine the Audit Log service APIs and event ingestion mechanism.  
83. **Prompt (Governance \- Audit Log Viewer UI \- Frontend):** Develop UI components within the apps/frontend admin panel for viewing and searching immutable audit logs.  
    * **Functionality:** Allows administrators to query the Audit Log service, display results in a readable format (e.g., shadcn/ui \<Table /\>), and apply filters.  
    * **Implementation (Frontend):** React components, using shadcn/ui for tables and form inputs.  
    * **Agent Responsibility:** Build these frontend components.  
84. **Prompt (Governance \- Human-in-the-Loop Approval Service \- Backend):** Design and implement a backend microservice for "Human-in-the-Loop" approval flows.  
    * **Functionality:** Allows AI agents or automated Spells/workflows to request manual approval for sensitive operations. Creates approval tasks, assigns them to users/roles, tracks approval status, and notifies initiating systems upon completion.  
    * **Integration:** Integrates with the grimOS Task Management service (to be defined later) for task creation and user notification.  
    * **API:** Endpoints to submit approval requests, query approval status, and for approvers to submit their decisions.  
    * **Agent Responsibility:** Develop this service, its database schema (for approval requests), and APIs.  
85. **Prompt (Governance \- AI Agent Sandboxing Strategy \- DevOps/Platform):** Define and document the strategy for sandboxing AI agents that execute potentially untrusted code or access external resources.  
    * **Options:** Container-based sandboxing (e.g., gVisor, Kata Containers), separate Kubernetes namespaces with strict network policies, or function-as-a-service environments with limited permissions.  
    * **Agent Responsibility:** Research and document the chosen sandboxing approach. Implement initial configurations or tooling to support this.  
86. **Prompt (Governance \- Data Loss Prevention (DLP) Mechanisms \- Backend):** Implement basic DLP mechanisms within relevant backend services or as a dedicated DLP service.  
    * **Initial Scope:** Pattern matching (regex) for common sensitive data types (e.g., credit card numbers, social security numbers, API keys) in AI agent outputs, Spell results, or data being exfiltrated via connectors.  
    * **Actions:** Log, alert, or redact/block based on policy.  
    * **Agent Responsibility:** Develop these DLP capabilities.  
87. **Prompt (Governance \- Explainable AI (XAI) API Support \- Backend):** For AI services making critical decisions (e.g., Omens, UBA), implement API endpoints to expose explanations or contributing factors for those decisions.  
    * **Functionality:** If models support it (e.g., using SHAP, LIME, or attention mechanisms), provide data that helps users understand *why* a particular prediction or decision was made.  
    * **Agent Responsibility:** Add these XAI-supportive API endpoints to relevant AI services. (Frontend for displaying this will be separate).  
88. **Prompt (Governance \- Data Encryption at Rest & In Transit \- Platform/DevOps):** Ensure data encryption at rest is configured for all sensitive data stores (e.g., PostgreSQL using pgcrypto or Transparent Data Encryption, object storage server-side encryption). Ensure data encryption in transit (TLS/SSL) is enforced for all inter-service communication and external connections.  
    * **Agent Responsibility:** Verify and configure encryption settings across the platform.

This covers the next three major sections. I'll continue with Persistent Memory & Identity, Conversational OS, and the Security Module in the subsequent part.