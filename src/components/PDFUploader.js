import React from 'react';
import { motion } from 'framer-motion';

function PDFUploader({ onFileUpload }) {
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      onFileUpload(file);
    } else {
      alert('Please upload a valid PDF file.');
    }
  };

  return (
    <motion.div
      className="pdf-uploader"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h3>Upload Your PDF</h3>
      <label className="upload-button">
        <input type="file" accept="application/pdf" onChange={handleFileChange} />
        Choose PDF
      </label>
    </motion.div>
  );
}

export default PDFUploader;