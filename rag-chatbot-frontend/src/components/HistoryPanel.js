import React, { useState, useEffect } from 'react';
import { chatAPI } from '../api';

/**
 * HistoryPanel Component - Displays chat history
 * Shows last 10 Q&A pairs from the backend
 */
const HistoryPanel = ({ refreshTrigger }) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch chat history from backend
  const fetchHistory = async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await chatAPI.getHistory();
      setHistory(Array.isArray(data) ? data : []);
    } catch (err) {
      setError('Failed to load history');
      console.error('History fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Load history on component mount and when refreshTrigger changes
  useEffect(() => {
    fetchHistory();
  }, [refreshTrigger]);

  // Format timestamp for display
  const formatTimestamp = (timestamp) => {
    try {
      return new Date(timestamp).toLocaleString();
    } catch {
      return 'Unknown time';
    }
  };

  return (
    <div className="history-panel">
      <div className="history-header">
        <h3>Chat History</h3>
        <button onClick={fetchHistory} className="refresh-button" disabled={loading}>
          {loading ? '⟳' : '↻'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {loading && history.length === 0 ? (
        <div className="loading-message">Loading history...</div>
      ) : (
        <div className="history-list">
          {history.length === 0 ? (
            <div className="empty-history">No chat history yet</div>
          ) : (
            history.map((item, index) => (
              <div key={item.id || index} className="history-item">
                <div className="history-question">
                  <strong>Q:</strong> {item.query || item.question}
                </div>
                <div className="history-answer">
                  <strong>A:</strong> {item.response || item.answer}
                </div>
                <div className="history-timestamp">
                  {formatTimestamp(item.timestamp)}
                </div>
                {item.similarity && (
                  <div className="history-similarity">
                    Similarity: {item.similarity.toFixed(3)}
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default HistoryPanel;