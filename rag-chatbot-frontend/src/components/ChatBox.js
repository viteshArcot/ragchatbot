import React, { useState } from 'react';
import { chatAPI } from '../api';

/**
 * ChatBox Component - Main chat interface
 * Handles user input, sends queries, and displays responses
 */
const ChatBox = ({ onNewMessage }) => {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const result = await chatAPI.sendQuery(question);
      setResponse(result);
      
      // Notify parent component of new message for history update
      if (onNewMessage) {
        onNewMessage();
      }
      
      setQuestion(''); // Clear input
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get response');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-box">
      <h2>RAG Chatbot</h2>
      
      {/* Query Form */}
      <form onSubmit={handleSubmit} className="query-form">
        <div className="input-group">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask me anything..."
            disabled={loading}
            className="question-input"
          />
          <button 
            type="submit" 
            disabled={loading || !question.trim()}
            className="send-button"
          >
            {loading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </form>

      {/* Error Display */}
      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Response Display */}
      {response && (
        <div className="response-container">
          <div className="response-message">
            <h3>Response:</h3>
            <p>{response.answer}</p>
            
            {/* Similarity Score */}
            {response.similarity_score && (
              <div className="similarity-score">
                <small>Similarity Score: {response.similarity_score.toFixed(3)}</small>
              </div>
            )}
          </div>

          {/* Sources */}
          {response.sources && response.sources.length > 0 && (
            <div className="sources-container">
              <h4>Sources:</h4>
              <ul className="sources-list">
                {response.sources.map((source, index) => (
                  <li key={index} className="source-item">
                    {source}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ChatBox;