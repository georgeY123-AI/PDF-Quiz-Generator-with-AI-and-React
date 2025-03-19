import React, { useState } from 'react';
import PDFUploader from './components/PDFUploader';
import QuizDisplay from './components/QuizDisplay';
import axios from 'axios';
import './App.css';

function App() {
  const [quizData, setQuizData] = useState(null);
  const [pdfFile, setPdfFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateQuiz = async (file) => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/generate-quiz', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      console.log('API Response:', response.data); // Log the response for debugging
      if (response.data.error) {
        alert(response.data.error);
      } else {
        setQuizData(response.data);
      }
    } catch (error) {
      console.error('Error details:', error.response ? error.response.data : error.message);
      alert('Failed to generate quiz. Please ensure the server is running and try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = (file) => {
    setPdfFile(file);
    generateQuiz(file);
  };

  return (
    <div className="App">
      <h1>PDF Quiz Generator</h1>
      <PDFUploader onFileUpload={handleFileUpload} />
      {loading && <p className="loading">Generating quiz, please wait...</p>}
      {quizData && !loading && <QuizDisplay quizData={quizData} />}
    </div>
  );
}

export default App;