FROM python:3.11-slim

WORKDIR /app/

# Install Poetry
RUN pip install poetry==1.6.1 && \
    poetry config virtualenvs.create false

# Copy poetry configuration files
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root --no-dev

# Copy application code
COPY . /app/

# Run with uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
