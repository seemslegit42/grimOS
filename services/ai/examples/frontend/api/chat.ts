import { NextRequest, NextResponse } from 'next/server';

// This is a Next.js API route that forwards requests to the AI service
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    
    // Extract provider and model from the request
    const { provider = 'openai', model, messages, stream = false } = body;
    
    // Determine the appropriate model if not specified
    let actualModel = model;
    if (!actualModel) {
      if (provider === 'openai') {
        actualModel = 'gpt-4o';
      } else if (provider === 'gemini') {
        actualModel = 'gemini-1.5-pro';
      } else if (provider === 'groq') {
        actualModel = 'llama3-70b-8192';
      }
    }
    
    // Forward the request to the AI service
    const aiServiceUrl = process.env.AI_SERVICE_URL || 'http://localhost:8000';
    
    // Use the Vercel AI SDK compatible endpoint
    const endpoint = `${aiServiceUrl}/vercel-ai/v1/chat/completions`;
    
    // If streaming is requested, handle it differently
    if (stream) {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: actualModel,
          messages,
          stream: true,
        }),
      });
      
      // Return the streaming response
      return new Response(response.body, {
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
        },
      });
    }
    
    // For non-streaming requests
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: actualModel,
        messages,
        stream: false,
      }),
    });
    
    const data = await response.json();
    
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error in chat API route:', error);
    return NextResponse.json(
      { error: 'Failed to process chat request' },
      { status: 500 }
    );
  }
}

// Configure the route to handle streaming responses
export const config = {
  runtime: 'edge',
};