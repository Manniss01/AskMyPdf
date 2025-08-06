import React, { useState } from 'react';
import './UploadPDF.css';

interface UploadPDFProps {
  onTopicsExtracted?: (topics: string[]) => void;
}

const UploadPDF: React.FC<UploadPDFProps> = ({ onTopicsExtracted }) => {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState('');
  const [pdfInfo, setPdfInfo] = useState<null | {
    pages: number;
    words: number;
    summary: string;
    pdf_type: string;
  }>(null);
  const [classification, setClassification] = useState<string[]>([]);
  const [topics, setTopics] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setStatus('');
      setPdfInfo(null);
      setClassification([]);
      setTopics([]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setStatus('Please select a PDF file first.');
      return;
    }

    setLoading(true);
    setStatus('Processing PDF...');

    const formData = new FormData();
    formData.append('pdf', file);

    try {
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setStatus('Upload successful!');
        setPdfInfo(data.pdf_info);
        setClassification(data.classification || []);

        if (onTopicsExtracted && data.topics) {
          onTopicsExtracted(data.topics);
        }
        if (data.topics) {
          setTopics(data.topics);
        }
      } else {
        setStatus('Upload failed: ' + (data.error || 'Unknown error'));
      }
    } catch (error: any) {
      setStatus('Upload error: ' + error.message);
    }

    setLoading(false);
  };

  return (
    <div className="upload-pdf-container">
      <h2>📄 Upload PDF</h2>

      <input
        type="file"
        accept=".pdf"
        onChange={handleFileChange}
        disabled={loading}
        className="file-input"
      />

      <button onClick={handleUpload} disabled={loading || !file}>
        {loading ? <div className="spinner" /> : 'Upload & Analyze'}
      </button>

      {status && <p className="status-text">{status}</p>}

      {pdfInfo && (
        <div className="pdf-info">
          <h3>📊 PDF Details</h3>
          <p><strong>Total Pages:</strong> {pdfInfo.pages}</p>
          <p><strong>Total Words:</strong> {pdfInfo.words}</p>
          <p><strong>PDF Type:</strong> {pdfInfo.pdf_type}</p>
          <p><strong>Classification:</strong> {classification.join(', ')}</p>
          <p><strong>🧠 Summary:</strong> {pdfInfo.summary}</p>

        </div>
      )}
    </div>
  );
};

export default UploadPDF;
