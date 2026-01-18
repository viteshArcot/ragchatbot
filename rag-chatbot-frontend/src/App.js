import React, { useState } from 'react';
import ChatBox from './components/ChatBox';
import HistoryPanel from './components/HistoryPanel';
import MetricsPanel from './components/MetricsPanel';
import FileUpload from './components/FileUpload';
import './App.css';

/**
 * Main App Component - RAG Chatbot Frontend
 * Orchestrates all components and manages global state
 */
function App() {
  // State for triggering history refresh
  const [historyRefreshTrigger, setHistoryRefreshTrigger] = useState(0);
  
  // State for metrics modal
  const [showMetrics, setShowMetrics] = useState(false);
  
  // State for active tab
  const [activeTab, setActiveTab] = useState('chat');

  // Handle new message - refresh history
  const handleNewMessage = () => {
    setHistoryRefreshTrigger(prev => prev + 1);
  };

  // Handle successful upload - refresh history
  const handleUploadSuccess = (result) => {
    console.log('Upload successful:', result);
    // Could trigger a notification or refresh here
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <h1>RAG Chatbot</h1>
        <div className="header-actions">
          <button 
            onClick={() => setShowMetrics(true)}
            className="metrics-button"
          >
            📊 Metrics
          </button>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="tab-navigation">
        <button 
          className={`tab-button ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveTab('chat')}
        >
          💬 Chat
        </button>
        <button 
          className={`tab-button ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          📄 Upload PDF
        </button>
        <button 
          className={`tab-button ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          📋 History
        </button>
      </nav>

      {/* Main Content */}
      <main className="main-content">
        {activeTab === 'chat' && (
          <div className="chat-layout">
            <div className="chat-main">
              <ChatBox onNewMessage={handleNewMessage} />
            </div>
          </div>
        )}

        {activeTab === 'upload' && (
          <div className="upload-layout">
            <FileUpload onUploadSuccess={handleUploadSuccess} />
          </div>
        )}

        {activeTab === 'history' && (
          <div className="history-layout">
            <HistoryPanel refreshTrigger={historyRefreshTrigger} />
          </div>
        )}
      </main>

      {/* Metrics Modal */}
      <MetricsPanel 
        isOpen={showMetrics} 
        onClose={() => setShowMetrics(false)} 
      />

      {/* Footer */}
      <footer className="app-footer">
        <p>RAG Chatbot Frontend - Powered by FastAPI & React</p>
      </footer>
    </div>
  );
}

export default App;