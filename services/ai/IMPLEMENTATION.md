# grimOS AI Service Implementation

This document outlines the implementation of the AI service that integrates Gemini, Groq, and OpenAI using the Vercel AI SDK.

## Architecture

The AI service follows a microservices architecture and is built with FastAPI. It provides a unified API for interacting with multiple AI providers:

1. **OpenAI**: For GPT models and embeddings
2. **Google Gemini**: For Gemini models and embeddings
3. **Groq**: For fast inference on Llama and Mixtral models

## Core Components

### 1. Provider Implementations

- `OpenAIProvider`: Integrates with OpenAI's API
- `GeminiProvider`: Integrates with Google's Generative AI API
- `GroqProvider`: Integrates with Groq's API

### 2. Unified AI Service

The `AIService` class provides a unified interface for all providers, handling:
- Provider initialization and management
- Request formatting
- Response normalization
- Error handling

### 3. Vercel AI SDK Compatibility

The `VercelAISDK` class provides endpoints compatible with the Vercel AI SDK:
- `/vercel-ai/v1/chat/completions`
- `/vercel-ai/v1/completions`
- `/vercel-ai/v1/embeddings` # Corrected path
- `/vercel-ai/v1/models`

### 4. Native API

The native API provides more control and explicit provider selection:
- `/api/v1/chat`
- `/api/v1/completion`
- `/api/v1/embeddings`
- `/api/v1/health`

## Features

- **Chat Completions**: Generate conversational responses
- **Text Completions**: Generate text based on prompts
- **Embeddings**: Generate vector embeddings for text
- **Streaming**: Support for streaming responses
- **Provider Selection**: Explicitly choose which AI provider to use
- **Model Selection**: Choose specific models for each provider
- **Health Checks**: Monitor the status of each provider

## Integration Examples

### Frontend Integration

The service includes examples for integrating with frontend applications:
- React components using the Vercel AI SDK
- Next.js API routes for proxying requests

### Python Client

A Python client is provided for easy integration with other Python services.

## Configuration

The service is configured via environment variables in the `.env` file:
- API keys for each provider
- Default models
- Rate limiting settings
- CORS settings

## Deployment

The service can be deployed using Docker and integrated into the grimOS microservices architecture.