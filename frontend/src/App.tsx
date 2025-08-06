import React, { useState, useEffect } from 'react';
import UploadPDF from './components/Upload/UploadPDF';
import AskQuestion from './components/AskQuestion/AskQuestion';
import FloatingKeywords from './components/FloatingKeywords/FloatingKeywords';
import './App.css';

const App: React.FC = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [showHelper, setShowHelper] = useState(false);
  const [keywords, setKeywords] = useState<string[]>([]);

  useEffect(() => {
    document.body.classList.toggle('dark', darkMode);
  }, [darkMode]);

  const handleTopicsExtracted = (topics: string[]) => {
    setKeywords(topics);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>AskMyPDF</h1>
        <button
          className="toggle-btn"
          onClick={() => setDarkMode(!darkMode)}
          aria-label="Toggle Dark Mode"
          title="Toggle Dark Mode"
        >
          {darkMode ? '🌞' : '🌙'}
        </button>
      </header>

      <main className="main-content">
        <div className="card unified-card">
          <h2>📘 Your Smart PDF Assistant</h2>
          <UploadPDF onTopicsExtracted={handleTopicsExtracted} />
          <AskQuestion />
        </div>

        {keywords.length > 0 && <FloatingKeywords keywords={keywords} />}

        <section className="about-section section">
          <h2>About AskMyPDF</h2>
          <p>
            <strong>AskMyPDF</strong> is your intelligent assistant for extracting knowledge from PDFs.
            Upload your study material, and the app will:
          </p>
          <ul>
            <li>📄 Analyze and summarize the content</li>
            <li>📌 Detect key topics using machine learning</li>
            <li>❓ Allow you to ask context-aware questions</li>
            <li>🧠 Provide smart answers using LLM-based understanding</li>
          </ul>
          <p>
            Powered by <strong>transformers</strong>, <strong>vector search</strong>, and <strong>custom agents</strong>,
            it’s built to support your learning journey!
          </p>
        </section>
      </main>

      {/* Floating Helper Icon */}
      <button
        className="chatbot-fab"
        onClick={() => setShowHelper(prev => !prev)}
        title="Need help?"
      >
        💬
      </button>

      {showHelper && (
        <div className="chatbot-popup">
          <p>Hi there! 👋</p>
          <p>• Upload a PDF to get started</p>
          <p>• Ask questions about the content</p>
          <p>• AI will assist you in real time!</p>
        </div>
      )}
    </div>
  );
};

export default App;
