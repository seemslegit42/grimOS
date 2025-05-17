# **Grimoire™ (grimOS) \- API Design Specification for MVP**

Version: 1.0  
Date: May 15, 2025  
**Table of Contents:**

1. Introduction  
   1.1 Purpose  
   1.2 Scope  
   1.3 Definitions, Acronyms, and Abbreviations  
   1.4 References  
2. API Design Principles & Conventions  
   2.1 General Principles  
   2.2 Naming Conventions  
   2.3 Versioning Strategy  
   2.4 Authentication & Authorization  
   2.5 Error Handling  
   2.6 Pagination, Sorting, and Filtering  
   2.7 Data Formats  
3. Global API Elements  
   3.1 Base URL  
   3.2 Authentication Endpoints (Conceptual for MVP)  
4. Security Module MVP APIs  
   4.1 Threat Intelligence API  
   4.2 User Behavior Analytics (UBA) API  
5. Operations Module MVP APIs  
   5.1 Workflow Management API (RuneForge POC Backend)  
   5.2 Data Integration (Connector Interaction) API  
6. Cognitive Core MVP APIs  
   6.1 Basic AI Data Analysis API (Internal/Display)  
   6.2 ScrollWeaver POC API (NL to Workflow Stub)  
7. Data Models (Request/Response Schemas \- JSON)  
   7.1 Common Data Types  
   7.2 ThreatIndicator Object  
   7.3 UBALoginAnomalyAlert Object  
   7.4 WorkflowDefinition Object  
   7.5 WorkflowInstance Object  
   7.6 Rune Object (Simplified for MVP)  
   7.7 ScrollWeaverRequest Object  
   7.8 ScrollWeaverResponse Object  
8. Future Considerations

## **1\. Introduction**

### **1.1 Purpose**

This document specifies the design of the Application Programming Interfaces (APIs) for the Minimum Viable Product (MVP) of Grimoire™ (grimOS). These APIs will be exposed via the Universal API Fabric and will serve as the primary means of interaction between the frontend, backend microservices, and potentially early third-party integrations.

### **1.2 Scope**

This specification covers the RESTful API endpoints for the core MVP functionalities of the Security, Operations, and Cognitive Core modules, as defined in the "grimOS \- MVP Core Module Feature Specifications." It includes endpoint definitions, request/response formats, authentication mechanisms, and error handling. GraphQL API specifications will be detailed in a separate document or a later version of this one.

### **1.3 Definitions, Acronyms, and Abbreviations**

(Refer to Section 1.3 of the "Grimoire™ (grimOS) \- Detailed Requirements Specification")

* **CRUD:** Create, Read, Update, Delete  
* **JWT:** JSON Web Token  
* **HAL:** Hypertext Application Language

### **1.4 References**

* Grimoire™ (grimOS) \- Detailed Requirements Specification (DRS) V1.0  
* Grimoire™ (grimOS) \- System Architecture Document (SAD) V1.0  
* Grimoire™ (grimOS) \- MVP Core Module Feature Specifications V1.0  
* OpenAPI Specification (Version 3.x)

## **2\. API Design Principles & Conventions**

### **2.1 General Principles**

* **API-First:** Design APIs before implementation.  
* **Statelessness:** APIs will be stateless; each request from a client will contain all information needed to understand the request.  
* **Resource-Oriented:** Design APIs around resources that can be created, retrieved, updated, and deleted.  
* **Standard HTTP Methods:** Use HTTP methods (GET, POST, PUT, PATCH, DELETE) appropriately.  
* **Idempotency:** Ensure PUT and DELETE operations are idempotent. Consider idempotency for POST where applicable (e.g., using an Idempotency-Key header).  
* **Consistency:** Maintain consistency in naming, data formats, and error responses across all APIs.  
* **Discoverability (Future):** While not fully implemented in MVP, design with HATEOAS principles (e.g., HAL) in mind for future discoverability.

### **2.2 Naming Conventions**

* **Endpoints:** Use plural nouns for resource collections (e.g., /workflows, /alerts). Use lowercase and hyphens (kebab-case) for path segments.  
* **Query Parameters:** Use camelCase.  
* **JSON Properties:** Use camelCase for request and response body properties.

### **2.3 Versioning Strategy**

* **URI Path Versioning:** APIs will be versioned using /v1/ in the base path (e.g., https://api.grimoire.com/v1/resource). MVP will start with v1.

### **2.4 Authentication & Authorization**

* **Authentication:** All protected API endpoints will require authentication. For MVP, this will likely be a Bearer Token (e.g., JWT) obtained via a separate authentication flow (conceptualized in 3.2).  
  * Authorization: Bearer \<token\>  
* **Authorization:** Role-Based Access Control (RBAC) will be enforced. API endpoints will check if the authenticated user/service has the necessary permissions for the requested resource and operation. Specific permissions will be tied to defined roles.

### **2.5 Error Handling**

* **Standard HTTP Status Codes:** Use standard HTTP status codes to indicate success or failure (e.g., 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error).  
* **Error Response Body:** Errors will return a JSON object with a consistent structure:  
  {  
    "error": {  
      "code": "ERROR\_CODE\_STRING", // e.g., "VALIDATION\_ERROR", "RESOURCE\_NOT\_FOUND"  
      "message": "A human-readable description of the error.",  
      "details": \[ // Optional array for more specific error details  
        {  
          "field": "fieldName", // If applicable to a specific field  
          "issue": "Description of the issue with the field."  
        }  
      \],  
      "timestamp": "ISO8601\_TIMESTAMP"  
    }  
  }

### **2.6 Pagination, Sorting, and Filtering**

* **Pagination (for collections):**  
  * GET /resource?limit=25\&offset=0 or GET /resource?page=1\&pageSize=25  
  * Responses for paginated collections should include pagination metadata (e.g., totalItems, totalPages, currentPage, nextPageLink, prevPageLink).  
* **Sorting (for collections):**  
  * GET /resource?sortBy=fieldName\&sortOrder=asc (or desc)  
* **Filtering (for collections):**  
  * GET /resource?filterField=value\&anotherField=anotherValue  
  * Specific filterable fields will be documented per endpoint.

### **2.7 Data Formats**

* **Request Body:** JSON (Content-Type: application/json)  
* **Response Body:** JSON (Content-Type: application/json)

## **3\. Global API Elements**

### **3.1 Base URL**

* **Production (Example):** https://api.grimoire.com/v1  
* **Staging (Example):** https://api.staging.grimoire.com/v1  
* **Development (Example):** http://localhost:PORT/api/v1

### **3.2 Authentication Endpoints (Conceptual for MVP)**

*(Detailed specification for auth endpoints (e.g., /auth/login, /auth/refresh) will be in a dedicated Auth API Spec. For MVP, assume a token is acquired and used.)*

* **POST /auth/token:** Obtain an access token (e.g., using client credentials or user credentials).  
* **POST /auth/refresh:** Refresh an expired access token.

## **4\. Security Module MVP APIs**

### **4.1 Threat Intelligence API**

* **Resource:** /security/threat-intelligence/indicators  
* **Description:** Provides access to aggregated threat intelligence indicators.  
* **Endpoints:**  
  * **GET /indicators**  
    * **Description:** Retrieve a list of threat indicators.  
    * **Permissions:** security:threat-intel:read  
    * **Query Parameters:**  
      * limit (int, optional, default: 25): Number of items per page.  
      * offset (int, optional, default: 0): Offset for pagination.  
      * source (string, optional): Filter by threat feed source.  
      * type (string, optional): Filter by indicator type (e.g., ip, domain, hash).  
      * severity (string, optional): Filter by severity level.  
      * sortBy (string, optional, default: timestamp): Field to sort by.  
      * sortOrder (string, optional, default: desc): asc or desc.  
    * **Successful Response (200 OK):**  
      {  
        "data": \[ /\* Array of ThreatIndicator objects \*/ \],  
        "pagination": { /\* Pagination metadata \*/ }  
      }

    * **Error Responses:** 400, 401, 403, 500\.

### **4.2 User Behavior Analytics (UBA) API**

* **Resource:** /security/uba/login-anomalies  
* **Description:** Provides access to detected anomalous login alerts.  
* **Endpoints:**  
  * **GET /login-anomalies**  
    * **Description:** Retrieve a list of login anomaly alerts.  
    * **Permissions:** security:uba:read  
    * **Query Parameters:**  
      * limit (int, optional, default: 25\)  
      * offset (int, optional, default: 0\)  
      * userId (string, optional): Filter by user ID.  
      * alertType (string, optional): Filter by anomaly type (e.g., impossible\_travel, multiple\_failed\_logins).  
      * status (string, optional, default: new): Filter by alert status (e.g., new, reviewed, false\_positive).  
      * startDate (ISO8601, optional): Filter by start date.  
      * endDate (ISO8601, optional): Filter by end date.  
      * sortBy (string, optional, default: timestamp)  
      * sortOrder (string, optional, default: desc)  
    * **Successful Response (200 OK):**  
      {  
        "data": \[ /\* Array of UBALoginAnomalyAlert objects \*/ \],  
        "pagination": { /\* Pagination metadata \*/ }  
      }

    * **Error Responses:** 400, 401, 403, 500\.  
  * **PATCH /login-anomalies/{alertId}**  
    * **Description:** Update the status of a login anomaly alert (e.g., mark as reviewed).  
    * **Permissions:** security:uba:update  
    * **Request Body:**  
      {  
        "status": "reviewed" // or "false\_positive", "investigating"  
      }

    * **Successful Response (200 OK):**  
      {  
        "data": { /\* Updated UBALoginAnomalyAlert object \*/ }  
      }

    * **Error Responses:** 400, 401, 403, 404, 500\.

## **5\. Operations Module MVP APIs**

### **5.1 Workflow Management API (RuneForge POC Backend)**

* **Resource:** /operations/workflows  
* **Description:** Manage workflow definitions and instances.  
* **Endpoints:**  
  * **POST /workflows/definitions**  
    * **Description:** Create a new workflow definition (from RuneForge POC).  
    * **Permissions:** operations:workflow-definition:create  
    * **Request Body:** WorkflowDefinition object (simplified for MVP, e.g., name, description, array of Rune stubs).  
    * **Successful Response (201 Created):**  
      {  
        "data": { /\* Created WorkflowDefinition object \*/ }  
      }

    * **Error Responses:** 400, 401, 403, 500\.  
  * **GET /workflows/definitions**  
    * **Description:** Retrieve a list of workflow definitions.  
    * **Permissions:** operations:workflow-definition:read  
    * **Query Parameters:** limit, offset, sortBy, sortOrder.  
    * **Successful Response (200 OK):**  
      {  
        "data": \[ /\* Array of WorkflowDefinition objects \*/ \],  
        "pagination": { /\* Pagination metadata \*/ }  
      }

  * **GET /workflows/definitions/{definitionId}**  
    * **Description:** Retrieve a specific workflow definition.  
    * **Permissions:** operations:workflow-definition:read  
    * **Successful Response (200 OK):** WorkflowDefinition object.  
  * **PUT /workflows/definitions/{definitionId}** (For MVP, might be limited to updating basic fields like name/description)  
    * **Description:** Update an existing workflow definition.  
    * **Permissions:** operations:workflow-definition:update  
    * **Request Body:** WorkflowDefinition object.  
    * **Successful Response (200 OK):** Updated WorkflowDefinition object.  
  * **POST /workflows/instances**  
    * **Description:** Create and start a new workflow instance from a definition.  
    * **Permissions:** operations:workflow-instance:create  
    * **Request Body:**  
      {  
        "definitionId": "string",  
        "name": "string (optional)",  
        "initialPayload": { /\* Optional JSON object \*/ }  
      }

    * **Successful Response (201 Created):** WorkflowInstance object.  
  * **GET /workflows/instances**  
    * **Description:** Retrieve a list of workflow instances.  
    * **Permissions:** operations:workflow-instance:read  
    * **Query Parameters:** limit, offset, status (e.g., running, completed, failed), definitionId, sortBy, sortOrder.  
    * **Successful Response (200 OK):**  
      {  
        "data": \[ /\* Array of WorkflowInstance objects \*/ \],  
        "pagination": { /\* Pagination metadata \*/ }  
      }

  * **GET /workflows/instances/{instanceId}**  
    * **Description:** Retrieve a specific workflow instance and its current state/logs (basic for MVP).  
    * **Permissions:** operations:workflow-instance:read  
    * **Successful Response (200 OK):** WorkflowInstance object (with execution log stubs).  
  * **POST /workflows/instances/{instanceId}/tasks/{taskId}/complete** (For Manual Task Rune MVP)  
    * **Description:** Mark a manual task within a workflow instance as complete.  
    * **Permissions:** operations:workflow-task:update (or specific task assignee permission)  
    * **Request Body:**  
      {  
        "outcome": "string (e.g., approved, rejected)",  
        "notes": "string (optional)"  
      }

    * **Successful Response (200 OK):** Updated WorkflowInstance object.

### **5.2 Data Integration (Connector Interaction) API**

*(For MVP, this is primarily internal for the "Basic API Call" Rune and "Slack Notification" Rune. No direct user-facing API to manage connectors in MVP, configuration happens within RuneForge.)*

* **Internal Endpoint (Example, called by Workflow Engine):**  
  * **POST /internal/connectors/execute**  
    * **Description:** Used by the workflow engine to trigger a configured connector action (e.g., an API call, a Slack message).  
    * **Request Body (Example for a generic API call):**  
      {  
        "connectorType": "REST\_API\_CALL", // or "SLACK\_NOTIFICATION"  
        "config": { // Connector-specific configuration  
          "url": "https://api.example.com/data",  
          "method": "GET", // MVP: GET only  
          "headers": { "X-API-Key": "secret" }, // Securely managed  
          // ... other params  
        },  
        "payload": { /\* Optional payload for POST/PUT \*/ }  
      }

    * **Successful Response (200 OK):**  
      {  
        "status": "success", // or "failed"  
        "response": { /\* Response from the external system, if any \*/ },  
        "error": "string (if failed)"  
      }

## **6\. Cognitive Core MVP APIs**

### **6.1 Basic AI Data Analysis API (Internal/Display)**

*(This API might be internal, consumed by dashboard widgets, rather than a public API for MVP.)*

* **Resource (Example):** /cognitive/analysis/operational-trends  
* **Endpoints:**  
  * **GET /operational-trends**  
    * **Description:** Retrieve basic AI-analyzed trends (e.g., workflow completion time anomalies, login attempt spikes).  
    * **Permissions:** cognitive:analysis:read  
    * **Query Parameters:** trendType (e.g., workflow\_duration, login\_failures), timePeriod (e.g., last\_7\_days).  
    * **Successful Response (200 OK):**  
      {  
        "data": \[  
          {  
            "trendType": "workflow\_duration\_anomaly",  
            "workflowDefinitionId": "abc",  
            "message": "Workflow 'X' average completion time increased by Y% this week.",  
            "severity": "warning",  
            "timestamp": "ISO8601\_TIMESTAMP"  
          }  
          // ... other trend objects  
        \]  
      }

### **6.2 ScrollWeaver POC API (NL to Workflow Stub)**

* **Resource:** /cognitive/scrollweaver/generate-stub  
* **Description:** Accepts natural language input and returns a textual stub of a simple workflow.  
* **Endpoints:**  
  * **POST /generate-stub**  
    * **Description:** Generate a workflow stub from natural language.  
    * **Permissions:** cognitive:scrollweaver:create  
    * **Request Body:** ScrollWeaverRequest object.  
    * **Successful Response (200 OK):** ScrollWeaverResponse object.  
    * **Error Responses:** 400 (if input is unparsable for MVP), 401, 403, 500\.

## **7\. Data Models (Request/Response Schemas \- JSON)**

### **7.1 Common Data Types**

* **timestamp**: ISO 8601 string (e.g., "2025-05-15T14:30:00Z")  
* **uuid**: String representing a UUID.

### **7.2 ThreatIndicator Object**

{  
  "id": "uuid",  
  "indicatorValue": "string", // e.g., "1.2.3.4", "evil.com"  
  "indicatorType": "string", // "ip", "domain", "hash\_md5", "hash\_sha256", "url"  
  "source": "string", // Name of the threat feed  
  "severity": "string", // "low", "medium", "high", "critical" (optional)  
  "description": "string (optional)",  
  "tags": \["string"\], // (optional)  
  "firstSeen": "timestamp (optional)",  
  "lastSeen": "timestamp",  
  "createdAt": "timestamp",  
  "updatedAt": "timestamp"  
}

### **7.3 UBALoginAnomalyAlert Object**

{  
  "id": "uuid",  
  "userId": "uuid",  
  "username": "string",  
  "alertType": "string", // "impossible\_travel", "multiple\_failed\_logins", "new\_location"  
  "description": "string",  
  "ipAddress": "string",  
  "location": { // (optional)  
    "city": "string",  
    "country": "string",  
    "latitude": "float",  
    "longitude": "float"  
  },  
  "timestamp": "timestamp",  
  "status": "string", // "new", "reviewed", "false\_positive", "investigating"  
  "severity": "string", // "low", "medium", "high"  
  "details": {}, // JSON object with specific details about the anomaly  
  "createdAt": "timestamp"  
}

### **7.4 WorkflowDefinition Object (Simplified for MVP)**

{  
  "id": "uuid",  
  "name": "string",  
  "description": "string (optional)",  
  "version": "integer",  
  "runes": \[ /\* Array of simplified Rune objects or stubs \*/ \],  
  "createdAt": "timestamp",  
  "updatedAt": "timestamp",  
  "createdBy": "uuid"  
}

### **7.5 WorkflowInstance Object (Simplified for MVP)**

{  
  "id": "uuid",  
  "definitionId": "uuid",  
  "definitionName": "string",  
  "name": "string (optional)",  
  "status": "string", // "pending", "running", "completed", "failed", "paused"  
  "currentStepId": "string (optional)",  
  "payload": {}, // JSON object with instance data  
  "result": {}, // JSON object with final result (if any)  
  "error": "string (if failed)",  
  "startTime": "timestamp (optional)",  
  "endTime": "timestamp (optional)",  
  "createdAt": "timestamp",  
  "executionLog": \[ // Basic log entries for MVP  
    { "stepId": "string", "status": "string", "message": "string", "timestamp": "timestamp" }  
  \]  
}

### **7.6 Rune Object (Simplified for MVP \- as part of WorkflowDefinition)**

{  
  "id": "string", // Unique within the workflow definition  
  "type": "string", // "START", "END", "MANUAL\_TASK", "SIMPLE\_CONDITION", "BASIC\_API\_CALL", "AGENT\_TASK\_STUB"  
  "name": "string",  
  "config": { // Rune-specific configuration  
    // Example for MANUAL\_TASK:  
    // "assigneeRole": "string", "instructions": "string"  
    // Example for BASIC\_API\_CALL:  
    // "url": "string", "method": "GET"  
  },  
  "nextStepId": "string (optional)", // For linear MVP workflows  
  "conditionTrueNextStepId": "string (optional)", // For SIMPLE\_CONDITION  
  "conditionFalseNextStepId": "string (optional)" // For SIMPLE\_CONDITION  
}

### **7.7 ScrollWeaverRequest Object**

{  
  "naturalLanguageInput": "string"  
}

### **7.8 ScrollWeaverResponse Object (MVP: Textual Stub)**

{  
  "originalInput": "string",  
  "interpretedSteps": \[  
    {  
      "stepNumber": "integer",  
      "action": "string", // e.g., "Assign Manual Task", "Send Notification"  
      "description": "string", // e.g., "'Review Q1 Report' to John Doe"  
      "parameters": {} // Key-value pairs of identified parameters  
    }  
  \],  
  "confidenceScore": "float (optional, for future)",  
  "warnings": \["string"\] // (optional, e.g., "Could not identify assignee for task X")  
}

## **8\. Future Considerations**

* **GraphQL API:** Detailed specification for GraphQL queries, mutations, and subscriptions.  
* **Webhook Support:** Inbound webhooks for triggering workflows.  
* **Real-time APIs (WebSockets):** For live dashboard updates, agent communication.  
* **API Throttling and Quotas:** More granular controls.  
* **Developer Portal:** Interactive API documentation, sandbox, SDKs.  
* **More granular permissions and OAuth scopes.**

This API Design Specification for MVP provides a foundational set of interfaces for grimOS. It will be expanded and refined in subsequent development phases.