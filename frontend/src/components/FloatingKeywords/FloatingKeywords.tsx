import React from 'react';
import './FloatingKeywords.css';

interface FloatingKeywordsProps {
  keywords: string[];
}

const FloatingKeywords: React.FC<FloatingKeywordsProps> = ({ keywords }) => {
  return (
    <div className="floating-keywords-container">
      <h3>✨ Key Topics Detected</h3>
      <div className="keywords-cloud">
        {keywords.map((word, index) => (
          <span key={index} className="floating-keyword">
            {word}
          </span>
        ))}
      </div>
    </div>
  );
};

export default FloatingKeywords;
