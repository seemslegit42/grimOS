import { useChat, useCompletion } from 'ai/react';
import { useState } from 'react';

// Example component showing both completion and chat interfaces
export default function VercelAIExample() {
  const [activeTab, setActiveTab] = useState<'completion' | 'chat'>('chat');
  
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Vercel AI SDK Example</h1>
      
      <div className="flex space-x-4 mb-6">
        <button
          onClick={() => setActiveTab('completion')}
          className={`px-4 py-2 rounded-md ${
            activeTab === 'completion' 
              ? 'bg-indigo-600 text-white' 
              : 'bg-gray-200 text-gray-800'
          }`}
        >
          Text Completion
        </button>
        <button
          onClick={() => setActiveTab('chat')}
          className={`px-4 py-2 rounded-md ${
            activeTab === 'chat' 
              ? 'bg-indigo-600 text-white' 
              : 'bg-gray-200 text-gray-800'
          }`}
        >
          Chat Interface
        </button>
      </div>
      
      {activeTab === 'completion' ? <CompletionExample /> : <ChatExample />}
    </div>
  );
}

// Text Completion Example
function CompletionExample() {
  const { completion, input, handleInputChange, handleSubmit, isLoading } = useCompletion({
    api: '/api/completion',
    body: {
      provider: 'openai',
      model: 'gpt-4o',
    },
  });
  
  return (
    <div className="border border-gray-300 rounded-lg p-6 bg-white shadow-sm">
      <h2 className="text-xl font-semibold mb-4">Text Completion</h2>
      
      <form onSubmit={handleSubmit} className="mb-6">
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Prompt
          </label>
          <textarea
            value={input}
            onChange={handleInputChange}
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="Enter your prompt here..."
          />
        </div>
        
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="w-full px-4 py-2 bg-indigo-600 text-white rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {isLoading ? 'Generating...' : 'Generate Completion'}
        </button>
      </form>
      
      {completion && (
        <div className="mt-6">
          <h3 className="text-lg font-medium mb-2">Completion:</h3>
          <div className="bg-gray-50 p-4 rounded-md border border-gray-200 whitespace-pre-wrap">
            {completion}
          </div>
        </div>
      )}
    </div>
  );
}

// Chat Interface Example
function ChatExample() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',
    body: {
      provider: 'gemini',
      model: 'gemini-1.5-pro',
    },
  });
  
  return (
    <div className="border border-gray-300 rounded-lg p-6 bg-white shadow-sm">
      <h2 className="text-xl font-semibold mb-4">Chat Interface</h2>
      
      <div className="h-96 overflow-y-auto mb-4 border border-gray-200 rounded-md p-4 bg-gray-50">
        {messages.length === 0 ? (
          <div className="text-gray-500 text-center py-8">
            Start a conversation with the AI
          </div>
        ) : (
          messages.map((message) => (
            <div 
              key={message.id} 
              className={`mb-4 p-3 rounded-lg ${
                message.role === 'user' 
                  ? 'bg-blue-100 ml-auto max-w-[80%]' 
                  : 'bg-white border border-gray-200 max-w-[80%]'
              }`}
            >
              <div className="font-semibold mb-1">
                {message.role === 'user' ? 'You' : 'AI'}
              </div>
              <div className="whitespace-pre-wrap">{message.content}</div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="bg-white border border-gray-200 p-3 rounded-lg max-w-[80%] animate-pulse">
            <div className="font-semibold mb-1">AI</div>
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        )}
      </div>
      
      <form onSubmit={handleSubmit} className="flex space-x-2">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Type your message..."
          className="flex-1 px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="px-4 py-2 bg-indigo-600 text-white rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </div>
  );
}