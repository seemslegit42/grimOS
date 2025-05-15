FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . /app/

# Expose the port
EXPOSE 8080

# Start the API Gateway
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]
