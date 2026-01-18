import React, { useState, useEffect } from 'react';
import { chatAPI } from '../api';

/**
 * MetricsPanel Component - Displays system metrics
 * Shows similarity scores and clustering information
 */
const MetricsPanel = ({ isOpen, onClose }) => {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch metrics from backend
  const fetchMetrics = async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await chatAPI.getMetrics();
      setMetrics(data);
    } catch (err) {
      setError('Failed to load metrics');
      console.error('Metrics fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Load metrics when panel opens
  useEffect(() => {
    if (isOpen) {
      fetchMetrics();
    }
  }, [isOpen]);

  // Don't render if panel is closed
  if (!isOpen) return null;

  return (
    <div className="metrics-modal-overlay" onClick={onClose}>
      <div className="metrics-panel" onClick={(e) => e.stopPropagation()}>
        <div className="metrics-header">
          <h3>System Metrics</h3>
          <button onClick={onClose} className="close-button">×</button>
        </div>

        <div className="metrics-content">
          {loading ? (
            <div className="loading-message">Loading metrics...</div>
          ) : error ? (
            <div className="error-message">{error}</div>
          ) : metrics ? (
            <div className="metrics-data">
              {metrics.message ? (
                <div className="metrics-message">{metrics.message}</div>
              ) : (
                <>
                  <div className="metric-item">
                    <label>Total Queries:</label>
                    <span>{metrics.total_queries || 0}</span>
                  </div>
                  
                  <div className="metric-item">
                    <label>Average Similarity:</label>
                    <span>{metrics.avg_similarity ? metrics.avg_similarity.toFixed(3) : 'N/A'}</span>
                  </div>
                  
                  <div className="metric-item">
                    <label>Min Similarity:</label>
                    <span>{metrics.min_similarity ? metrics.min_similarity.toFixed(3) : 'N/A'}</span>
                  </div>
                  
                  <div className="metric-item">
                    <label>Max Similarity:</label>
                    <span>{metrics.max_similarity ? metrics.max_similarity.toFixed(3) : 'N/A'}</span>
                  </div>
                  
                  <div className="metric-item">
                    <label>Similarity Std Dev:</label>
                    <span>{metrics.similarity_std ? metrics.similarity_std.toFixed(3) : 'N/A'}</span>
                  </div>
                  
                  {metrics.clusters && (
                    <div className="metric-item">
                      <label>Clusters:</label>
                      <span>{metrics.clusters}</span>
                    </div>
                  )}
                </>
              )}
            </div>
          ) : (
            <div className="no-data">No metrics available</div>
          )}
        </div>

        <div className="metrics-footer">
          <button onClick={fetchMetrics} disabled={loading} className="refresh-button">
            Refresh
          </button>
        </div>
      </div>
    </div>
  );
};

export default MetricsPanel;