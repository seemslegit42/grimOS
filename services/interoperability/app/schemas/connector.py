"""
Schemas for integration connectors
"""
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Any, Optional, Literal
import uuid
from datetime import datetime
from enum import Enum


class ConnectorType(str, Enum):
    """Types of connectors supported by the Interoperability Engine"""
    REST_API = "rest_api"
    SOAP = "soap"
    DATABASE = "database"
    FILE = "file"
    EVENT = "event"
    MESSAGE_QUEUE = "message_queue"
    CUSTOM = "custom"


class AuthType(str, Enum):
    """Authentication types for connectors"""
    NONE = "none"
    API_KEY = "api_key"
    BASIC = "basic"
    OAUTH2 = "oauth2"
    JWT = "jwt"
    CERTIFICATE = "certificate"
    CUSTOM = "custom"


class ConnectorStatus(str, Enum):
    """Status of a connector"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class FieldType(str, Enum):
    """Field types for data mappings"""
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    OBJECT = "object"
    ARRAY = "array"
    ANY = "any"


class OperationType(str, Enum):
    """Operation types for connectors"""
    READ = "read"
    WRITE = "write"
    UPDATE = "update"
    DELETE = "delete"
    CUSTOM = "custom"


class AuthConfig(BaseModel):
    """Authentication configuration for a connector"""
    type: AuthType
    config: Dict[str, Any] = Field(default_factory=dict)
    credential_id: Optional[uuid.UUID] = None  # Reference to securely stored credentials


class FieldDefinition(BaseModel):
    """Definition of a field for schema mappings"""
    name: str
    type: FieldType
    description: Optional[str] = None
    required: bool = False
    default_value: Optional[Any] = None
    constraints: Optional[Dict[str, Any]] = None


class SchemaDefinition(BaseModel):
    """Schema definition for a connector"""
    fields: List[FieldDefinition]
    metadata: Optional[Dict[str, Any]] = None


class OperationDefinition(BaseModel):
    """Definition of an operation supported by a connector"""
    id: str
    type: OperationType
    name: str
    description: Optional[str] = None
    input_schema: Optional[SchemaDefinition] = None
    output_schema: Optional[SchemaDefinition] = None
    config: Dict[str, Any] = Field(default_factory=dict)


class ConnectorBase(BaseModel):
    """Base schema for a connector"""
    name: str = Field(..., description="Name of the connector")
    description: Optional[str] = Field(None, description="Description of the connector")
    type: ConnectorType = Field(..., description="Type of the connector")
    system_name: str = Field(..., description="Name of the external system (e.g., 'Salesforce', 'SAP')")
    auth_config: AuthConfig = Field(..., description="Authentication configuration")
    base_config: Dict[str, Any] = Field(default_factory=dict, description="Base configuration parameters")
    operations: List[OperationDefinition] = Field(default_factory=list, description="Operations supported by this connector")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")
    is_custom: bool = Field(default=False, description="Whether this is a custom connector")


class ConnectorCreate(ConnectorBase):
    """Schema for creating a new connector"""
    pass


class ConnectorUpdate(BaseModel):
    """Schema for updating a connector"""
    name: Optional[str] = None
    description: Optional[str] = None
    auth_config: Optional[AuthConfig] = None
    base_config: Optional[Dict[str, Any]] = None
    operations: Optional[List[OperationDefinition]] = None
    tags: Optional[List[str]] = None
    status: Optional[ConnectorStatus] = None


class ConnectorResponse(ConnectorBase):
    """Schema for connector response"""
    id: uuid.UUID
    owner_id: uuid.UUID
    status: ConnectorStatus
    created_at: datetime
    updated_at: datetime
    last_connection_time: Optional[datetime] = None
    
    class Config:
        orm_mode = True


class CredentialBase(BaseModel):
    """Base schema for credentials"""
    name: str = Field(..., description="Name of the credential")
    description: Optional[str] = Field(None, description="Description of the credential")
    type: AuthType = Field(..., description="Type of authentication")
    data: Dict[str, Any] = Field(..., description="Encrypted credential data")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")


class CredentialCreate(CredentialBase):
    """Schema for creating a new credential"""
    pass


class CredentialUpdate(BaseModel):
    """Schema for updating a credential"""
    name: Optional[str] = None
    description: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None


class CredentialResponse(BaseModel):
    """Schema for credential response (without sensitive data)"""
    id: uuid.UUID
    name: str
    description: Optional[str]
    type: AuthType
    owner_id: uuid.UUID
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class DataMapping(BaseModel):
    """Schema for data mapping between systems"""
    source_field: str
    target_field: str
    transformation: Optional[str] = None  # Can be a formula or transformation function name


class IntegrationConfig(BaseModel):
    """Configuration for an integration between systems"""
    name: str
    description: Optional[str] = None
    source_connector_id: uuid.UUID
    target_connector_id: uuid.UUID
    source_operation_id: str
    target_operation_id: str
    mappings: List[DataMapping]
    schedule: Optional[str] = None  # Cron expression for scheduled execution
    triggers: Optional[Dict[str, Any]] = None  # Event-based triggers
    error_handling: Optional[Dict[str, Any]] = None  # Error handling configuration
    filters: Optional[Dict[str, Any]] = None  # Data filters


class ConnectorTestRequest(BaseModel):
    """Request to test a connector"""
    connector_id: Optional[uuid.UUID] = None  # For existing connectors
    connector_config: Optional[ConnectorBase] = None  # For testing before saving
    operation_id: Optional[str] = None  # Specific operation to test
    test_input: Optional[Dict[str, Any]] = None  # Test input data
