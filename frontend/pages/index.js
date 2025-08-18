import React, { useState } from 'react';
import AnswerBox from '../components/AnswerBox';
import ContextBox from '../components/ContextBox';

export default function Home() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const askQuestion = async () => {
    const res = await fetch('/api/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();
    setAnswer(data.answer);
  };

  return (
    <div>
      <h1>Dev Onboarding Helper</h1>
      <input value={question} onChange={e => setQuestion(e.target.value)} placeholder="Ask a question..." />
      <button onClick={askQuestion}>Ask</button>
      <AnswerBox answer={answer} />
      <ContextBox />
    </div>
  );
}
