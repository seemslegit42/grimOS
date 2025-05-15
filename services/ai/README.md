# grimOS AI Service

This service integrates multiple AI providers (OpenAI, Google Gemini, and Groq) using the Vercel AI SDK, providing a unified API for AI capabilities.

## Features

- Chat completions with streaming support
- Text completions with streaming support
- Embeddings generation
- Vercel AI SDK compatibility
- Provider-agnostic API

## Supported Providers

- **OpenAI**: GPT-4o, GPT-4 Turbo, GPT-3.5 Turbo, and embedding models
- **Google Gemini**: Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini 1.0 Pro, and embedding models
- **Groq**: Llama 3 70B, Llama 3 8B, Mixtral 8x7B

## API Endpoints

### Native API

- `/api/v1/chat`: Chat completions
- `/api/v1/completion`: Text completions
- `/api/v1/embeddings`: Embeddings generation
- `/api/v1/health`: Service health check

### Vercel AI SDK Compatibility

- `/vercel-ai/v1/chat/completions`: Compatible with Vercel AI SDK chat completions
- `/vercel-ai/v1/completions`: Compatible with Vercel AI SDK text completions
- `/vercel-ai/v1/embeddings`: Compatible with Vercel AI SDK embeddings
- `/vercel-ai/v1/models`: List available models

## Configuration

Set the following environment variables in the `.env` file:

```
# API Keys
OPENAI_API_KEY=your-openai-api-key
GEMINI_API_KEY=your-gemini-api-key
GROQ_API_KEY=your-groq-api-key

# Default Models
DEFAULT_OPENAI_MODEL=gpt-4o
DEFAULT_GEMINI_MODEL=gemini-1.5-pro
DEFAULT_GROQ_MODEL=llama3-70b-8192
```

## Development

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```
   uvicorn app.main:app --reload
   ```

## Docker Deployment

Build and run the Docker container:

```
docker build -t grimos-ai-service .
docker run -p 8000:8000 --env-file .env grimos-ai-service
```

## Client Usage with Vercel AI SDK

```typescript
import { createAI } from 'ai';
import { useChat } from 'ai/react';

// Configure the AI SDK
const ai = createAI({
  apiKey: process.env.AI_API_KEY,
  baseURL: 'https://ai-service.grimos.app/vercel-ai',
});

// In your React component
function ChatComponent() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: '/api/chat',
    model: 'gemini-1.5-pro', // or 'gpt-4o' or 'llama3-70b-8192'
  });

  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>
          {m.role === 'user' ? 'User: ' : 'AI: '}
          {m.content}
        </div>
      ))}
      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Say something..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
```