import { useState } from 'react';
import PropTypes from 'prop-types';
import './PDFUploader.css';

/**
 * PDFUploader Component
 * 
 * Handles PDF file upload before starting the voice conversation.
 * Provides drag-and-drop interface and file validation.
 * 
 * @param {Object} props - Component properties
 * @param {Function} props.onUploadSuccess - Callback when upload succeeds
 * @param {Function} props.onUploadError - Callback when upload fails
 * @param {string} props.roomId - Current room ID for context association
 */
const PDFUploader = ({ onUploadSuccess, onUploadError, roomId }) => {
  const [isUploading, setIsUploading] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);

  const handleFileUpload = async (file) => {
    if (!file) return;

    // Validate file type
    if (!file.type.includes('pdf')) {
      const error = 'Please select a PDF file only.';
      setUploadStatus({ type: 'error', message: error });
      onUploadError?.(error);
      return;
    }

    // Validate file size (10MB limit)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      const error = 'File size must be less than 10MB.';
      setUploadStatus({ type: 'error', message: error });
      onUploadError?.(error);
      return;
    }

    setIsUploading(true);
    setUploadStatus({ type: 'info', message: 'Processing PDF...' });

    try {
      const formData = new FormData();
      formData.append('pdf_file', file);
      formData.append('room_id', roomId || 'default');

      const response = await fetch('http://localhost:5001/upload-pdf', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();

      if (result.success) {
        setUploadStatus({ 
          type: 'success', 
          message: `✅ PDF processed successfully! (${result.metadata.num_pages} pages)` 
        });
        onUploadSuccess?.(result);
      } else {
        throw new Error(result.error || 'Upload failed');
      }
    } catch (error) {
      console.error('Upload error:', error);
      const errorMessage = error.message || 'Failed to upload PDF. Please try again.';
      setUploadStatus({ type: 'error', message: errorMessage });
      onUploadError?.(errorMessage);
    } finally {
      setIsUploading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileUpload(files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const resetUpload = () => {
    setUploadStatus(null);
  };

  return (
    <div className="pdf-uploader">
      <h3>📄 Upload a PDF for Context</h3>
      <p className="upload-description">
        Upload a PDF document to enhance our conversation with relevant context.
        The AI will reference the document content during our discussion.
      </p>

      <div
        className={`upload-zone ${isDragOver ? 'drag-over' : ''} ${isUploading ? 'uploading' : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        {isUploading ? (
          <div className="upload-progress">
            <div className="spinner"></div>
            <p>Processing your PDF...</p>
          </div>
        ) : (
          <>
            <div className="upload-icon">📁</div>
            <p className="upload-text">
              Drag and drop your PDF here, or{' '}
              <label className="file-select-label">
                click to browse
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileSelect}
                  className="file-input"
                  disabled={isUploading}
                />
              </label>
            </p>
            <p className="upload-limits">Maximum file size: 10MB</p>
          </>
        )}
      </div>

      {uploadStatus && (
        <div className={`upload-status ${uploadStatus.type}`}>
          <span className="status-message">{uploadStatus.message}</span>
          {uploadStatus.type !== 'info' && (
            <button className="reset-button" onClick={resetUpload}>
              ✕
            </button>
          )}
        </div>
      )}

      <div className="upload-benefits">
        <h4>💡 What happens when you upload a PDF?</h4>
        <ul>
          <li>🔍 AI extracts and analyzes the document content</li>
          <li>💬 Conversations become more personalized and relevant</li>
          <li>📊 AI can reference specific information from your document</li>
          <li>🎯 Better recommendations based on document context</li>
        </ul>
      </div>
    </div>
  );
};

PDFUploader.propTypes = {
  onUploadSuccess: PropTypes.func,
  onUploadError: PropTypes.func,
  roomId: PropTypes.string
};

export default PDFUploader;
