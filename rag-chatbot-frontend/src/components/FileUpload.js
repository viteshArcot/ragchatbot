import React, { useState } from 'react';
import { chatAPI } from '../api';

/**
 * FileUpload Component - Handles PDF file uploads
 * Allows users to upload PDFs for ingestion into the RAG system
 */
const FileUpload = ({ onUploadSuccess }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState(null);

  // Handle file selection
  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file type
      if (file.type !== 'application/pdf') {
        setError('Please select a PDF file');
        return;
      }
      
      // Validate file size (10MB limit)
      if (file.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB');
        return;
      }
      
      setSelectedFile(file);
      setError(null);
      setUploadResult(null);
    }
  };

  // Handle file upload
  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setError(null);

    try {
      const result = await chatAPI.uploadPDF(selectedFile);
      setUploadResult(result);
      setSelectedFile(null);
      
      // Reset file input
      const fileInput = document.getElementById('pdf-upload');
      if (fileInput) fileInput.value = '';
      
      // Notify parent component of successful upload
      if (onUploadSuccess) {
        onUploadSuccess(result);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  // Clear selection
  const clearSelection = () => {
    setSelectedFile(null);
    setError(null);
    setUploadResult(null);
    const fileInput = document.getElementById('pdf-upload');
    if (fileInput) fileInput.value = '';
  };

  return (
    <div className="file-upload">
      <h3>Upload PDF Document</h3>
      
      <div className="upload-section">
        <div className="file-input-container">
          <input
            id="pdf-upload"
            type="file"
            accept=".pdf"
            onChange={handleFileSelect}
            disabled={uploading}
            className="file-input"
          />
          <label htmlFor="pdf-upload" className="file-input-label">
            {selectedFile ? selectedFile.name : 'Choose PDF file...'}
          </label>
        </div>

        {selectedFile && (
          <div className="file-actions">
            <button
              onClick={handleUpload}
              disabled={uploading}
              className="upload-button"
            >
              {uploading ? 'Uploading...' : 'Upload PDF'}
            </button>
            <button
              onClick={clearSelection}
              disabled={uploading}
              className="clear-button"
            >
              Clear
            </button>
          </div>
        )}
      </div>

      {/* File info */}
      {selectedFile && (
        <div className="file-info">
          <small>
            Size: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
          </small>
        </div>
      )}

      {/* Error message */}
      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Success message */}
      {uploadResult && (
        <div className="success-message">
          <h4>Upload Successful!</h4>
          <p><strong>File:</strong> {uploadResult.filename}</p>
          <p><strong>Chunks created:</strong> {uploadResult.num_chunks}</p>
          <p><strong>Document ID:</strong> {uploadResult.doc_id}</p>
          {uploadResult.total_text_length && (
            <p><strong>Text length:</strong> {uploadResult.total_text_length} characters</p>
          )}
        </div>
      )}

      {/* Upload progress */}
      {uploading && (
        <div className="upload-progress">
          <div className="progress-bar">
            <div className="progress-fill"></div>
          </div>
          <p>Processing PDF and creating embeddings...</p>
        </div>
      )}
    </div>
  );
};

export default FileUpload;