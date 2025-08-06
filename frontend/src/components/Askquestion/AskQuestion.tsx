import React, { useState } from 'react';
import './AskQuestion.css';

const AskQuestion: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const sessionId = 'test-session-1'; // Replace with dynamic ID if needed

  const handleSubmit = async () => {
    if (!question.trim()) {
      alert('Please enter a question');
      return;
    }
    setLoading(true);
    setAnswer('');
    try {
      const response = await fetch('http://127.0.0.1:5000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, session_id: sessionId }),
      });
      const data = await response.json();
      if (response.ok) {
        const fullText = data.answer;
        let i = 0;
        setAnswer('');
        const interval = setInterval(() => {
          setAnswer(prev => prev + fullText.charAt(i));
          i++;
          if (i >= fullText.length) clearInterval(interval);
        }, 25);
      } else {
        setAnswer(`Error: ${data.error || 'Unknown error'}`);
      }
    } catch (err: any) {
      setAnswer(`Error: ${err.message}`);
    }
    setLoading(false);
  };

  return (
    <div className="ask-question-container">
      <h2>Ask a Question</h2>
      <div className="ask-form">
        <input
          type="text"
          value={question}
          onChange={e => setQuestion(e.target.value)}
          placeholder="Type your question here..."
          disabled={loading}
        />
        <button onClick={handleSubmit} disabled={loading || !question.trim()}>
          {loading ? <div className="spinner" /> : 'Ask'}
        </button>
      </div>

      <div className="example-box">
        <p className="example-title">💡 Example Questions</p>
        <ul className="example-list">
          <li>🧠 What is the main idea of Chapter 3?</li>
          <li>📊 Summarize the topic on neural networks.</li>
          <li>🔍 Explain the difference between supervised and unsupervised learning.</li>
          <li>📚 What are the key takeaways from the conclusion?</li>
        </ul>
      </div>

      {answer && (
        <div className="ask-answer">
          <strong>Answer:</strong>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
};

export default AskQuestion;
