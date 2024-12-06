import React, { useState } from 'react';
import axios from 'axios';

const Chatbot = () => {
  const [pdfs, setPdfs] = useState([]);
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const handleFileChange = (e) => {
    setPdfs(e.target.files);
  };

  const handleQueryChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    for (let i = 0; i < pdfs.length; i++) {
      formData.append('documents', pdfs[i]);
    }
    formData.append('query', query);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setChatHistory(response.data.chat_history);
    } catch (error) {
      console.error('Error querying the chatbot:', error);
    }
  };

  return (
    <div>
      <h1>Chat with PDFs</h1>
      <input type="file" multiple onChange={handleFileChange} />
      <textarea value={query} onChange={handleQueryChange} placeholder="Ask a question..." />
      <button onClick={handleSubmit}>Submit</button>

      <div>
        {chatHistory.map((message, index) => (
          <div key={index}>
            <p>{message.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Chatbot;
