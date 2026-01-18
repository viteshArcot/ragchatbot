import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api/v1', // Use proxy from package.json
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API functions for all backend endpoints
export const chatAPI = {
  // Send query to chatbot
  sendQuery: async (question) => {
    const response = await api.post('/query', { question });
    return response.data;
  },

  // Get chat history
  getHistory: async () => {
    const response = await api.get('/history');
    return response.data;
  },

  // Get metrics
  getMetrics: async () => {
    const response = await api.get('/metrics');
    return response.data;
  },

  // Upload PDF file
  uploadPDF: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/ingest', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get ingested documents
  getDocuments: async () => {
    const response = await api.get('/documents');
    return response.data;
  },
};

export default api;