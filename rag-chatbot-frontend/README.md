# RAG Chatbot Frontend

A modern React.js frontend for the RAG (Retrieval-Augmented Generation) chatbot backend.

## Features

- **Chat Interface**: Clean, responsive chat UI with real-time messaging
- **PDF Upload**: Drag-and-drop PDF ingestion with progress tracking
- **Chat History**: View last 10 conversations with timestamps
- **System Metrics**: Modal displaying similarity scores and system stats
- **Responsive Design**: Mobile-friendly interface

## Tech Stack

- **React 18** - Modern React with hooks
- **Axios** - HTTP client for API calls
- **CSS3** - Custom styling with flexbox and grid
- **Create React App** - Build tooling

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- RAG Chatbot Backend running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm start
```

The app will open at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

## API Integration

The frontend connects to these backend endpoints:

- `POST /api/v1/query` - Send chat messages
- `GET /api/v1/history` - Fetch chat history
- `GET /api/v1/metrics` - Get system metrics
- `POST /api/v1/ingest` - Upload PDF files
- `GET /api/v1/documents` - List uploaded documents

## Component Structure

```
src/
├── App.js              # Main app with tab navigation
├── components/
│   ├── ChatBox.js      # Chat interface
│   ├── HistoryPanel.js # Chat history display
│   ├── MetricsPanel.js # System metrics modal
│   └── FileUpload.js   # PDF upload component
├── api.js              # Axios API client
└── App.css             # Styling
```

## Usage

1. **Chat**: Type questions and get AI responses with source citations
2. **Upload PDFs**: Add documents to the knowledge base
3. **View History**: Check previous conversations
4. **Monitor Metrics**: Track system performance

## Configuration

Set backend URL in `.env`:

```
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## Development

- Components use React hooks (useState, useEffect)
- Modular architecture with clear separation of concerns
- Error handling and loading states
- Responsive CSS with mobile support