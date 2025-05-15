"""Schema registry and validators for Kafka messages."""
import json
import logging
import os
from typing import Any, Dict, Optional, Union

import fastavro
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)

# Constants
SCHEMAS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schemas")


def load_avro_schema(schema_file: str) -> Dict[str, Any]:
    """Load Avro schema from file.
    
    Args:
        schema_file: Schema file name
        
    Returns:
        Dict[str, Any]: Avro schema
    """
    schema_path = os.path.join(SCHEMAS_DIR, schema_file)
    
    try:
        with open(schema_path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load schema from {schema_path}: {e}")
        raise


class SchemaValidator:
    """Schema validator using Avro schemas."""
    
    def __init__(self):
        """Initialize schema validator."""
        self._schemas = {}
        self._parsed_schemas = {}
        self._load_schemas()
    
    def _load_schemas(self):
        """Load all schemas from the schemas directory."""
        try:
            if not os.path.exists(SCHEMAS_DIR):
                os.makedirs(SCHEMAS_DIR)
                logger.warning(f"Created schemas directory: {SCHEMAS_DIR}")
                return
            
            # Load all .avsc files in the schemas directory
            for filename in os.listdir(SCHEMAS_DIR):
                if filename.endswith(".avsc"):
                    schema_name = os.path.splitext(filename)[0]
                    self._schemas[schema_name] = load_avro_schema(filename)
                    # Parse schema for validation
                    self._parsed_schemas[schema_name] = fastavro.parse_schema(
                        self._schemas[schema_name]
                    )
                    logger.info(f"Loaded schema: {schema_name}")
        except Exception as e:
            logger.error(f"Failed to load schemas: {e}")
    
    def validate(self, schema_name: str, data: Dict[str, Any]) -> bool:
        """Validate data against a schema.
        
        Args:
            schema_name: Schema name (without extension)
            data: Data to validate
            
        Returns:
            bool: True if validation succeeds, False otherwise
        """
        if schema_name not in self._parsed_schemas:
            logger.warning(f"Schema not found: {schema_name}")
            return False
        
        try:
            # Validate data against schema
            fastavro.validate(data, self._parsed_schemas[schema_name])
            return True
        except Exception as e:
            logger.error(f"Schema validation failed for {schema_name}: {e}")
            return False
    
    def get_schema(self, schema_name: str) -> Optional[Dict[str, Any]]:
        """Get schema by name.
        
        Args:
            schema_name: Schema name (without extension)
            
        Returns:
            Optional[Dict[str, Any]]: Schema or None if not found
        """
        return self._schemas.get(schema_name)


# Global schema validator instance
validator = SchemaValidator()
