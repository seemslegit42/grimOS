---
mode: 'agent'
---
## **grimOS Revised Build Prompts**

**Instructions for AI Build Agent:**

* You are responsible for determining the precise file locations, directory structures, and specific file names based on your indexing of the existing grimOS monorepo.  
* Strictly adhere to the project's established conventions, including Turborepo structure, pnpm usage, and the defined technology stack.  
* Enforce naming conventions: snake\_case for all variables (TypeScript and Python), PascalCase for classes, and camelCase for methods/functions (TypeScript and Python).  
* Utilize Prettier and ESLint for code formatting and linting as configured in the project.  
* Ensure all new development seamlessly integrates with existing project modules and services.

### **I. Foundation & DevOps (Agent-Led Structuring)**

1. **Prompt (Foundation \- Monorepo Core):** Establish and manage the grimOS monorepo using Turborepo and pnpm.  
   * **Core Requirement:** The monorepo must effectively organize distinct applications (e.g., the main frontend application, various backend microservices) and shared internal packages (e.g., for UI elements, common types, utility functions), enabling efficient build and development workflows.  
   * **Tooling Integration:** Integrate and configure ESLint and Prettier for automated code formatting and linting across all relevant codebases (TypeScript, Python). Set up robust type-checking mechanisms (TypeScript compiler for frontend/shared packages, MyPy for Python backend services).  
   * **Agent Responsibility:** Verify this foundational setup or perform necessary initialization, strictly adhering to any existing monorepo structure, conventions, and the established technology stack.  
2. **Prompt (Foundation \- Shared Types Package):** Develop a shared TypeScript package for common data models, interfaces, and type definitions used across multiple frontend applications or packages and potentially for API contracts with backend services.  
   * **Functionality:** This package should centralize types to ensure consistency and type safety.  
   * **Agent Responsibility:** Create or identify the appropriate shared package within the Turborepo structure for these types.  
3. **Prompt (Foundation \- CI/CD Pipeline Basics):** Implement a foundational CI/CD pipeline (e.g., using GitHub Actions, GitLab CI, or the project's standard).  
   * **Initial Functionality:** The pipeline should automatically trigger on code pushes to main branches and merge/pull requests. It must run linters, type-checkers, and any existing basic test suites for frontend and backend code.  
   * **Agent Responsibility:** Configure the CI/CD workflow files, ensuring they correctly build and test applications and packages within the Turborepo environment.  
4. **Prompt (Foundation \- Standardized Backend Service Dockerization):** Define a standardized approach for Dockerizing Python FastAPI microservices.  
   * **Requirements:** Dockerfiles should incorporate multi-stage builds for optimized image size and security. Include common dependencies, environment variable configurations, and a consistent entry point.  
   * **Agent Responsibility:** Create a template Dockerfile or establish the convention to be used for all new backend services, ensuring it integrates with the project's containerization strategy.  
5. **Prompt (Foundation \- Standardized Frontend App Dockerization):** Define a standardized approach for Dockerizing the React (Vite) frontend application(s).  
   * **Requirements:** Dockerfiles should handle building the static assets and serving them efficiently (e.g., via a lightweight web server like Nginx). Include multi-stage builds.  
   * **Agent Responsibility:** Create a template Dockerfile or establish the convention for frontend application containerization.  
6. **Prompt (Foundation \- Kubernetes Deployment Configuration):** Establish a standardized method (e.g., Helm charts, Kustomize overlays) for configuring deployments of grimOS microservices and frontend applications to Kubernetes.  
   * **Requirements:** Configurations should be parameterizable for common settings (replica counts, resource limits, image tags, environment-specific variables).  
   * **Agent Responsibility:** Develop templates or define the structure for these deployment configurations.  
7. **Prompt (Foundation \- Service Discovery):** Ensure a service discovery mechanism is configured and utilized within the Kubernetes environment for internal microservice communication.  
   * **Typical Solution:** Kubernetes DNS.  
   * **Agent Responsibility:** Verify or configure this, ensuring services can resolve each other by name.  
8. **Prompt (Foundation \- Container Registry):** Integrate with the project's designated private Docker registry for storing and pulling grimOS service images.  
   * **Agent Responsibility:** Ensure CI/CD pipelines and deployment scripts are configured to use this registry.  
9. **Prompt (Foundation \- Local Development Environment):** Define and document a streamlined process for local development and iteration of microservices and frontend applications, ideally leveraging the containerization setup (e.g., using Docker Compose, Skaffold, or Minikube/Kind with local registry).  
   * **Agent Responsibility:** Provide scripts or configuration to simplify the local development experience.  
10. **Prompt (Foundation \- Centralized Logging):** Implement or integrate with a centralized logging stack (e.g., ELK stack, Grafana Loki, or cloud provider's logging service).  
    * **Requirement:** All applications (frontend and backend) and services running in Kubernetes should forward their logs to this central system. Logs should be structured (e.g., JSON) for easier parsing and searching.  
    * **Agent Responsibility:** Configure log collection and ensure services are set up to output logs in the required format.  
11. **Prompt (Foundation \- Monitoring & Alerting Basics):** Implement or integrate with a monitoring solution (e.g., Prometheus, Grafana, or cloud provider's monitoring service).  
    * **Initial Scope:** Monitor Kubernetes cluster resources and basic application metrics (e.g., CPU/memory usage, HTTP request rates, error rates). Set up basic alerting for critical issues.  
    * **Agent Responsibility:** Configure metric collection and dashboards.  
12. **Prompt (Foundation \- Infrastructure as Code (IaC) Setup):** If not already in place, establish the use of an IaC tool (e.g., Terraform, Pulumi, CloudFormation) for provisioning and managing cloud infrastructure resources (like Kubernetes clusters, databases, message queues).  
    * **Agent Responsibility:** Create initial IaC scripts or modules for core infrastructure components.  
13. **Prompt (Foundation \- Secret Management):** Implement or integrate with a secure secret management solution (e.g., HashiCorp Vault, Kubernetes Secrets with SOPS, cloud provider's KMS).  
    * **Requirement:** Securely store and manage sensitive information like API keys, database credentials, and certificates. Ensure applications can securely access these secrets.  
    * **Agent Responsibility:** Configure the chosen solution and integrate it into the deployment process.  
14. **Prompt (Foundation \- Shared Python Utilities Package):** Develop a shared Python package for common utilities, custom FastAPI middleware, error handling classes, and API client generation logic used across backend microservices.  
    * **Agent Responsibility:** Create or identify the appropriate shared package within the Turborepo structure.  
15. **Prompt (Foundation \- API Gateway):** Configure an API Gateway (e.g., Kong, Traefik, or cloud provider's native gateway) at the edge of the Kubernetes cluster.  
    * **Functionality:** Route external traffic to the appropriate frontend applications and backend API services. Handle concerns like SSL termination, request routing, and potentially initial rate limiting or authentication.  
    * **Agent Responsibility:** Implement or configure the API Gateway.

### **II. Backend Microservices (Agent-Led Structuring)**

*(All backend services to be built with Python 3.11+ and FastAPI, adhering to snake\_case for variables and functions/methods, PascalCase for classes.)*

**A. User Authentication & Authorization Service (Cauldron Core \- Identity Module)**

16. **Prompt (Backend \- User Auth \- Schema Design):** Design the database schema for the User Authentication service.  
    * **Entities:** Users (with fields for ID, email, hashed password, first name, last name, active status, timestamps), Roles, Permissions, and tables for User-Role and Role-Permission mappings.  
    * **Database:** Assume PostgreSQL or the project's standard relational database.  
    * **Agent Responsibility:** Generate schema migration scripts (e.g., using Alembic) based on this design.  
17. **Prompt (Backend \- User Auth \- Registration API):** Implement a FastAPI endpoint for user registration.  
    * **Functionality:** Accepts user details (email, password, name). Hashes the password securely (e.g., bcrypt, Argon2). Creates a new user record. Handles potential errors like duplicate email addresses.  
    * **Agent Responsibility:** Develop the FastAPI route, Pydantic models for request/response, and service logic.  
18. **Prompt (Backend \- User Auth \- Login API):** Implement a FastAPI endpoint for user login.  
    * **Functionality:** Accepts email and password. Validates credentials against stored hashed passwords. Issues JWTs (access and refresh tokens) upon successful authentication.  
    * **Agent Responsibility:** Develop the FastAPI route, Pydantic models, and service logic for token generation and credential validation.  
19. **Prompt (Backend \- User Auth \- Token Refresh API):** Implement a FastAPI endpoint for refreshing access tokens.  
    * **Functionality:** Accepts a valid refresh token. Issues a new access token.  
    * **Agent Responsibility:** Develop the FastAPI route and token validation/refresh logic.  
20. **Prompt (Backend \- User Auth \- JWT Validation Middleware):** Develop FastAPI middleware for validating JWTs.  
    * **Functionality:** Inspects Authorization headers. Verifies token signature and expiry. Populates request state with authenticated user information if valid. Protects specified routes.  
    * **Agent Responsibility:** Implement the middleware and integrate it into relevant FastAPI applications/routers.  
21. **Prompt (Backend \- User Auth \- RBAC Management APIs):** Implement FastAPI endpoints for managing Roles and Permissions.  
    * **Functionality:** CRUD operations for Roles. CRUD operations for Permissions. Endpoints to assign/revoke permissions from roles, and assign/revoke roles from users. Ensure these are admin-protected.  
    * **Agent Responsibility:** Develop the necessary FastAPI routes, Pydantic models, and service logic.  
22. **Prompt (Backend \- User Auth \- User Profile API \- "Me"):** Implement a FastAPI endpoint (e.g., /users/me) that returns the profile and permissions of the currently authenticated user (derived from their JWT).  
    * **Agent Responsibility:** Develop the FastAPI route and logic to fetch user details and their effective permissions.  
23. **Prompt (Backend \- User Auth \- OAuth 2.0 Integration):** Implement OAuth 2.0 / OpenID Connect provider integration (e.g., for Google, Microsoft Entra ID) for user login/registration.  
    * **Functionality:** Handle OAuth callbacks, create/link user accounts, and issue JWTs.  
    * **Agent Responsibility:** Implement the necessary routes and service logic for OAuth integration.

### **III. Frontend Components & UI/UX (Agent-Led Structuring)**

*(All frontend development with React (TypeScript), Vite, TailwindCSS, shadcn/ui, glasscn-ui, Framer Motion, lucide-react. Adhere to snake\_case for variables, PascalCase for components/classes, camelCase for functions/methods.)*

**A. Core UI Shell & Layout**

24. **Prompt (Frontend \- Core UI \- Main Application Shell):** Develop the main application layout component for the apps/frontend application.  
    * **Functionality:** Defines the primary structure (e.g., sidebar navigation, top bar for user profile/notifications, main content area).  
    * **Implementation:** Use React components, styled with Tailwind CSS. Integrate shadcn/ui components for structural elements where appropriate.  
    * **Agent Responsibility:** Create or modify the root layout component.  
25. **Prompt (Frontend \- Core UI \- Theme Integration):** Ensure the grimOS "Corporate Cyberpunk" visual identity and "Digital Weave" color palette are implemented globally.  
    * **Implementation:** Configure Tailwind CSS theme extensions. Define and apply CSS variables for shadcn/ui theming (backgrounds, foregrounds, primary, accent colors, card styles, borders, inputs, rings) to match the grimOS palette. Implement a theme switcher (light/dark modes, if applicable, based on the palette).  
    * **Agent Responsibility:** Set up the Tailwind configuration and global CSS for theming.  
26. **Prompt (Frontend \- Core UI \- Shared UI Package):** Establish or utilize a shared UI package (e.g., packages/ui) for common, reusable React components styled with shadcn/ui, glasscn-ui, Tailwind CSS, and lucide-react icons, adhering to the grimOS theme.  
    * **Examples:** Custom styled buttons, inputs, modals, cards, layout primitives.  
    * **Agent Responsibility:** Create or identify this package and populate it with initial core components.  
27. **Prompt (Frontend \- Core UI \- Global State Management):** Implement or configure a global state management solution (e.g., Zustand, Redux Toolkit) for the apps/frontend application.  
    * **Initial Scope:** Manage global user authentication state, user profile information, and potentially global UI states (e.g., loading indicators, notifications).  
    * **Agent Responsibility:** Set up the chosen state management library and define initial stores/slices.  
28. **Prompt (Frontend \- Core UI \- Routing & Auth Guards):** Implement client-side routing (e.g., using React Router) and navigation guards.  
    * **Functionality:** Protect routes that require authentication. Redirect unauthenticated users to a login page.  
    * **Agent Responsibility:** Configure routing and implement authentication guards.

**B. Authentication & User Profile Pages**

29. **Prompt (Frontend \- Auth \- Login Page):** Develop the Login page UI component.  
    * **Functionality:** Provides form fields for email and password. Interacts with the User Authentication service's login API endpoint. Handles successful login (e.g., storing tokens, redirecting) and login errors (displaying messages).  
    * **Implementation:** Use shadcn/ui form components, styled with Tailwind. Integrate lucide-react icons. Use Framer Motion for subtle animations.  
    * **Agent Responsibility:** Create the component and its associated logic.  
30. **Prompt (Frontend \- Auth \- Registration Page):** Develop the Registration page UI component.  
    * **Functionality:** Provides form fields for registration (name, email, password). Interacts with the User Authentication service's registration API. Handles success and error responses.  
    * **Implementation:** Similar to the Login page, using shadcn/ui, Tailwind, Lucide, Framer Motion.  
    * **Agent Responsibility:** Create the component and its logic.  
31. **Prompt (Frontend \- User Profile \- Profile Page):** Develop a User Profile page UI component.  
    * **Functionality:** Displays user information (name, email). Allows users to edit their profile details (e.g., name, password change). Interacts with relevant backend API endpoints.  
    * **Implementation:** Use shadcn/ui components for display and forms.  
    * **Agent Responsibility:** Create the component and its logic.  
32. **Prompt (Frontend \- Core UI \- User Dropdown Menu):** Implement a user dropdown menu in the application's top bar.  
    * **Functionality:** Displays the authenticated user's name or avatar. Provides links to Profile, Settings, and a Logout action.  
    * **Implementation:** Use shadcn/ui \<DropdownMenu /\>. Logout should clear authentication state and redirect to login.  
    * **Agent Responsibility:** Integrate this into the main layout.

### **VI. RuneForge Canvas (Frontend for n8n Integration \- Agent-Led Structuring)**

*(Continuing with the revised, agent-led approach for the RuneForge Canvas components within apps/frontend)*

33. **Prompt (RuneForge \- State \- Store Definition):** Define the Zustand store specifically for the RuneForge canvas feature.  
    * **Functionality:** Manages all reactive state for creating, viewing, and interacting with "Spells" (n8n workflows) and "Runes" (n8n nodes).  
    * **State Properties (TS camelCase):** current\_spell\_id: string | null, current\_spell\_name: string, flow\_nodes: Node\[\], flow\_edges: Edge\[\], available\_runes: AvailableRuneType\[\], selected\_node\_id: string | null, is\_loading\_spell: boolean, is\_saving\_spell: boolean, canvas\_error: string | null.  
    * **Types (ensure these are defined in a shared or local types location):** AvailableRuneType (id, displayName, category, iconName from lucide-react, parametersSchema: FormFieldDefinitionType\[\]), FormFieldDefinitionType (name, label, fieldType: 'text'|'select'|'textarea'|'boolean'|'json', options, defaultValue).  
    * **Core Actions (TS camelCase):** setSpellData, addFlowNode, deleteFlowNode, updateFlowNodePosition, updateRuneParameters, addFlowEdge, deleteFlowEdge, setSelectedNodeId, setAvailableRunesList, initiateLoadSpell, initiateSaveCurrentSpell.  
    * **Agent Responsibility:** Create or update the store file, ensuring it follows project conventions for state management.  
34. **Prompt (RuneForge \- Canvas \- Main View Component):** Develop the primary React component for the RuneForge canvas view.  
    * **Functionality:** Renders the interactive workflow graph using react-flow.  
    * **Implementation:**  
      * Integrate with the RuneForgeStore for state and actions.  
      * Configure \<ReactFlow\> with flow\_nodes, flow\_edges, event handlers (onNodesChange, onEdgesChange, onConnect, onNodeClick, etc.) that dispatch actions to the store.  
      * Specify custom nodeTypes (pointing to GrimOSRuneNodeComponent) and edgeTypes (pointing to GrimOSConnectionLineComponent).  
      * Style the canvas background and controls (e.g., zoom/pan from react-flow or custom shadcn/ui buttons) according to grimOS theme. Use lucide-react icons for controls.  
    * **Agent Responsibility:** Build this core canvas rendering component.  
35. **Prompt (RuneForge \- Canvas \- Custom Rune Node Component):** Create the GrimOSRuneNodeComponent.  
    * **Functionality:** Visually represents a "Rune" (n8n node) on the canvas.  
    * **Implementation:**  
      * Receive data (label, lucide-react iconName, status, n8nNodeType, parameters) and selected props.  
      * Style with Tailwind CSS, glasscn-ui for card effects, and grimOS theme colors. Use Framer Motion for animations (e.g., selection emphasis, entry).  
      * Render Handle components from react-flow for connection ports, styled to match.  
    * **Agent Responsibility:** Build this custom node component.  
36. **Prompt (RuneForge \- Canvas \- Custom Connection Line Component):** Create the GrimOSConnectionLineComponent.  
    * **Functionality:** Visually represents a connection between "Runes."  
    * **Implementation:**  
      * Render an SVG path using react-flow utility functions.  
      * Style with grimOS theme colors. Use Framer Motion for drawing animations or a "data flow" pulse effect.  
    * **Agent Responsibility:** Build this custom edge component.  
37. **Prompt (RuneForge \- UI \- Rune Palette Panel):** Develop the UI module for the Rune Palette.  
    * **Functionality:** Displays available "Runes" that can be dragged onto the canvas.  
    * **Implementation:**  
      * Fetch available\_runes from the RuneForgeStore.  
      * Render each Rune using a shadcn/ui \<Card\> or similar, styled with grimOS theme, lucide-react icon, and Framer Motion for hover effects.  
      * Implement drag-to-canvas functionality, creating a new flow\_node in the store on drop.  
      * Panel itself styled with Tailwind and potentially glasscn-ui.  
    * **Agent Responsibility:** Build this panel module.  
38. **Prompt (RuneForge \- UI \- Rune Properties Panel):** Develop the UI module for Rune Properties.  
    * **Functionality:** Allows configuration of the selected "Rune's" parameters.  
    * **Implementation:**  
      * Dynamically render a form using shadcn/ui components (\<Input\>, \<Select\>, \<Switch\>, \<Textarea\>, \<Label\>) based on the parametersSchema of the selected Rune.  
      * Panel styled with Tailwind, glasscn-ui, and Framer Motion for transitions.  
      * Form changes update the RuneForgeStore via the updateRuneParameters action.  
    * **Agent Responsibility:** Build this panel module.  
39. **Prompt (RuneForge \- UI \- Canvas Toolbar):** Develop the UI module for the Canvas Toolbar.  
    * **Functionality:** Provides actions like save, zoom, fit view.  
    * **Implementation:**  
      * Use shadcn/ui \<Button\> components with lucide-react icons.  
      * Styled with Tailwind and glasscn-ui.  
      * Actions trigger store functions (e.g., initiateSaveCurrentSpell) or react-flow controls.  
    * **Agent Responsibility:** Build this toolbar module.  
40. **Prompt (RuneForge \- Util \- n8n JSON Transformer):** Develop or integrate the N8NJsonTransformerUtil module.  
    * **Functionality:** Converts data between the canvas's React Flow state (flow\_nodes, flow\_edges) and n8n-compatible workflow JSON.  
    * **Implementation:** Provide transformToN8nJson and transformFromN8nJson functions (camelCase). Ensure strict adherence to n8n's JSON schema for nodes and connections.  
    * **Types (ensure defined in shared/local types location):** N8nWorkflowJsonType, N8nNodeType, N8nConnectionType.  
    * **Agent Responsibility:** Build or integrate this utility, ensuring correct data mapping.  
41. **Prompt (RuneForge \- Service \- Spell API Client):** Develop or integrate the SpellApiServiceClient.  
    * **Functionality:** Communicates with grimOS backend FastAPI services for loading/saving Spells.  
    * **Implementation:** Provide async fetchSpellFromBackend(spell\_id: string) and async saveSpellToBackend(workflow\_json: N8nWorkflowJsonType) functions (camelCase). These will call the Python backend.  
    * **Agent Responsibility:** Build or integrate this service client.

### **IV. Data Layer & Management (Agent-Led Structuring)**

*(Focus on backend Python services and infrastructure. Naming: snake\_case for variables & functions/methods, PascalCase for classes.)*

42. **Prompt (Data \- Primary Database Setup):** Provision and configure the primary relational database instance (e.g., PostgreSQL via managed cloud service like AWS RDS/Google Cloud SQL, or a robust Kubernetes deployment using a StatefulSet).  
    * **Requirements:** Ensure high availability, automated backups, and point-in-time recovery (PITR) capabilities are configured. Secure access credentials.  
    * **Agent Responsibility:** Implement IaC scripts for provisioning or configure the Kubernetes deployment. Ensure connection details are securely managed.  
43. **Prompt (Data \- Database Migration Strategy):** Implement and enforce a database migration strategy for all services using a relational database.  
    * **Tooling:** Utilize Alembic for Python/SQLAlchemy-based services.  
    * **Process:** Migrations should be version-controlled and integrated into the CI/CD pipeline to apply automatically to different environments.  
    * **Agent Responsibility:** Set up Alembic for existing and new services. Ensure migration scripts are generated for schema changes (like those in prompt 16).  
44. **Prompt (Data \- Centralized Audit Log Service & Schema):** Design and implement a dedicated backend microservice for centralized audit logging.  
    * **Functionality:** Provides an API endpoint (e.g., FastAPI) to receive audit event data from other microservices. Stores audit events in a dedicated, immutable (or append-only) manner in a PostgreSQL table.  
    * **Schema:** The audit log table should include fields for event ID, timestamp, service name, user ID (if applicable), action performed, target resource, event details (JSONB), and event status.  
    * **Agent Responsibility:** Develop the Audit Log service, its database schema, and migration scripts. Define a clear contract for audit event submission.  
45. **Prompt (Data \- Caching Layer Setup):** Provision and configure a caching layer (e.g., Redis via managed service or Kubernetes deployment).  
    * **Functionality:** Used for caching frequently accessed data, session management (if applicable beyond stateless JWTs), and potentially as a message broker for simple tasks or rate limiting counters.  
    * **Agent Responsibility:** Implement IaC or Kubernetes configurations for Redis. Ensure services can connect securely.  
46. **Prompt (Data \- Vector Database Setup):** Provision and configure a vector database (e.g., ChromaDB, Qdrant, Weaviate, or a managed cloud equivalent) for AI-related features.  
    * **Functionality:** Store and query embeddings for Retrieval Augmented Generation (RAG), semantic search, and other AI capabilities.  
    * **Agent Responsibility:** Deploy the chosen vector database (e.g., via Helm chart in Kubernetes) or configure access to a managed service.  
47. **Prompt (Data \- Message Queue/Streaming Platform Setup):** Provision and configure a robust message queue or event streaming platform (e.g., Apache Kafka, RabbitMQ, or cloud provider's equivalent like AWS SQS/Kinesis).  
    * **Functionality:** Facilitate asynchronous communication between microservices, event-driven architectures, and data ingestion pipelines for modules like Omens or UBA.  
    * **Agent Responsibility:** Deploy the platform (e.g., Kafka with Zookeeper via Helm charts) or configure access to a managed service. Define topic naming conventions and initial topics.  
48. **Prompt (Data \- Schema Registry for Kafka):** Implement or integrate a schema registry (e.g., Confluent Schema Registry) if using Kafka with structured event data.  
    * **Functionality:** Enforce schema validation for Kafka messages (e.g., using Avro or Protobuf) to ensure data consistency between producers and consumers.  
    * **Agent Responsibility:** Set up the schema registry and configure services to use it.  
49. **Prompt (Data \- Object Storage Setup):** Provision and configure object storage (e.g., MinIO deployed in Kubernetes, or a cloud provider's service like AWS S3, Google Cloud Storage).  
    * **Functionality:** Store large binary objects, user uploads (like avatars), AI model artifacts, backups, and potentially intermediate data from workflows.  
    * **Agent Responsibility:** Deploy MinIO or configure access to cloud object storage. Create initial buckets with appropriate access policies.  
50. **Prompt (Data \- Data Access Layer (DAL) Pattern):** Establish a convention or implement a shared library for Data Access Layers (DALs) or repositories in backend services.  
    * **Functionality:** Abstract database interactions (e.g., using SQLAlchemy with helper classes/functions) to keep service logic cleaner and make data source changes easier.  
    * **Agent Responsibility:** Define this pattern or create initial DAL components in the shared Python utilities package.  
51. **Prompt (Data \- Data Retention & Archival Policies):** Define and document initial data retention and archival policies for all major data stores (PostgreSQL, Kafka topics, audit logs, object storage).  
    * **Considerations:** Compliance requirements, storage costs, performance implications.  
    * **Agent Responsibility:** Document these policies. Implement basic mechanisms or stubs for future automated enforcement where feasible (e.g., TTLs for Kafka, partitioning for PostgreSQL).

### **V. Cognitive Core (AI/Agents \- Agent-Led Structuring)**

*(Backend Python services, AI model integration. Naming: snake\_case for variables & functions/methods, PascalCase for classes.)*

52. **Prompt (Cognitive Core \- AI Agent Manager Service \- Architecture & API):** Design and implement the core backend microservice for AI Agent Management.  
    * **Functionality:** Responsible for registering, configuring, orchestrating, and monitoring AI agents within grimOS. Exposes FastAPI endpoints for these operations.  
    * **Core Entities (Database Schema):** Agent Definitions (type, capabilities, configuration schema), Agent Instances (running state, current task, resource allocation).  
    * **API Endpoints:** Register new agent types, instantiate agents, assign tasks to agents, get agent status, list available agent skills.  
    * **Agent Responsibility:** Develop the service, its database schema (PostgreSQL), migrations, Pydantic models, and FastAPI routes.  
53. **Prompt (Cognitive Core \- Agent Communication Protocol):** Define and implement the communication protocol between the AI Agent Manager and individual AI agents.  
    * **Options:** Asynchronous messaging via Kafka, gRPC for direct calls, or a combination.  
    * **Requirements:** Must support task assignment, status updates, result reporting, and health checks.  
    * **Agent Responsibility:** Implement the chosen protocol components in the Agent Manager and provide a client library or template for AI agents to use.  
54. **Prompt (Cognitive Core \- Familiar AI Assistant \- Backend Logic):** Develop the backend logic for the "Familiar" context-aware AI assistant.  
    * **Functionality:** Consumes user context (e.g., current UI view, recent activity provided by frontend via API). Integrates with a foundational LLM (e.g., GPT series, Claude, Gemini via their APIs – manage keys securely). Implements a basic RAG pipeline using the vector database to fetch relevant grimOS documentation or knowledge base articles to augment LLM responses. Provides proactive suggestions or answers user queries via an API (e.g., WebSocket or REST) for the frontend.  
    * **Agent Responsibility:** Develop this as a distinct AI agent or a module within a core AI service. Implement LLM integration, RAG pipeline, and API endpoints.  
55. **Prompt (Cognitive Core \- ScrollWeaver \- Backend Logic):** Develop the backend AI logic for "ScrollWeaver" (natural language workflow creation).  
    * **Functionality:** Translates natural language descriptions of desired workflows into a structured format compatible with n8n JSON (which RuneForge consumes). Integrates with an LLM with strong instruction-following capabilities.  
    * **API:** Expose an endpoint for the frontend to submit natural language descriptions and receive structured workflow drafts.  
    * **Agent Responsibility:** Develop this AI agent/service. Consider initial fine-tuning or prompt engineering strategies for the LLM.  
56. **Prompt (Cognitive Core \- Omens \- Data Ingestion & Prediction Service):** Design and implement the backend service for "Omens" (predictive intelligence).  
    * **Data Ingestion:** Consume relevant operational data (system logs, performance metrics, business KPIs) from Kafka topics.  
    * **Prediction Models:** Implement initial time-series forecasting models (e.g., ARIMA, Prophet using Python libraries) or anomaly detection algorithms for key metrics.  
    * **Model Management:** Integrate with MLflow (or project's standard MLOps tool) for experiment tracking and model versioning.  
    * **API:** Expose endpoints to serve predictions, anomalies, and insights to frontend dashboards (SigilSight).  
    * **Agent Responsibility:** Develop the service, data ingestion consumers, initial predictive models, and APIs.  
57. **Prompt (Cognitive Core \- Generic AI Agent Task Executor Template):** Create a Python template for a generic AI agent.  
    * **Functionality:** Provides a base structure for developing new AI agents. Includes boilerplate for connecting to the Agent Manager, receiving tasks, reporting status/results, and basic error handling.  
    * **Agent Responsibility:** Develop this template to accelerate new agent creation.  
58. **Prompt (Cognitive Core \- AI Agent Skill \- Web Scraping):** Implement a web scraping skill for AI agents.  
    * **Functionality:** Takes a URL and selectors/instructions as input. Scrapes content from the web page.  
    * **Tooling:** Use Python libraries like Scrapy or BeautifulSoup.  
    * **Integration:** Make this skill discoverable and callable by the AI Agent Manager.  
    * **Agent Responsibility:** Develop and register this skill.  
59. **Prompt (Cognitive Core \- AI Agent Skill \- Document Processing):** Implement a document processing skill for AI agents.  
    * **Functionality:** Handles tasks like PDF text extraction (e.g., using PyMuPDF), document summarization (using an LLM), and potentially basic information extraction.  
    * **Integration:** Callable via the AI Agent Manager.  
    * **Agent Responsibility:** Develop and register this skill.