# grimOS Stats Service

This service provides statistics and metrics for the grimOS platform.

## API Endpoints

### `/api/stats/demo`

Returns mock dashboard statistics for grimOS.

**Method**: GET

**Response**:
```json
{
  "metrics": {
    "total_users": 3500,
    "active_sessions": 250,
    "ai_jobs_completed": 12000,
    "system_status": "OK"
  },
  "charts": {
    "weekly_jobs": [
      {
        "date": "2025-05-10",
        "nlp_jobs": 30,
        "vision_jobs": 20,
        "codegen_jobs": 25
      },
      // ... more data points
    ],
    "job_distribution": [
      {
        "name": "NLP",
        "value": 200
      },
      // ... more data points
    ]
  },
  "updated_at": "2025-05-17T12:34:56.789Z"
}
```

## Running the Service

```bash
# Navigate to the service directory
cd services/stats

# Install dependencies
pip install -r requirements.txt

# Run the service
uvicorn app.main:app --reload --port 8000
```

## Development

This service is built with FastAPI and provides mock data for the grimOS dashboard. In a production environment, this would be connected to real data sources.