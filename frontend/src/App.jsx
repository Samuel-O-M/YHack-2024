import { useState } from 'react';
import './App.css';

function App() {
  const [selectedImages, setSelectedImages] = useState([]);
  const [latexCode, setLatexCode] = useState('');

  // Handle PNG image file selection
  const handleImageFileSelection = (e) => {
    const files = Array.from(e.target.files);  // Convert file list to array
    const pngImages = files.filter(file => file.type === 'image/png');  // Only accept PNG files

    if (pngImages.length === 0) {
      alert('Please select PNG images only.');
    } else {
      setSelectedImages(pngImages);  // Store selected images in state
    }
  };

  // Handle LaTeX file selection
  const handleLatexFileSelection = async (e) => {
    const file = e.target.files[0];
    if (file) {
      try {
        const text = await file.text();
        setLatexCode(text);  // Store LaTeX code in state
      } catch (error) {
        console.error('Error reading txt file:', error);
      }
    }
  };

  // Handle form submission
  const handleSubmit = () => {
    if (selectedImages.length === 0 || !latexCode) {
      alert('Please select both PNG images and a LaTeX code file.');
      return;
    }

    const data = new FormData();
    selectedImages.forEach((image) => {
      data.append('images[]', image);  // Append each image to FormData
    });

    const latexBlob = new Blob([latexCode], { type: 'text/plain' });
    const latexFile = new File([latexBlob], 'latex_code.txt', { type: 'text/plain' });
    data.append('tex_file', latexFile);  // Append LaTeX code to FormData

    // Post request to backend Flask server
    fetch('http://localhost:5000/initialize', {
      method: 'POST',
      body: data,
    })
      .then((response) => {
        if (response.ok) {
          return response.json();  // Parse response from backend
        } else {
          return response.text().then((text) => {
            throw new Error(text);
          });
        }
      })
      .then((jsonResponse) => {
        console.log('Backend response:', jsonResponse);
        // Redirect to the SlidePage with the data if needed
        // You can use a router (e.g., React Router) to move to SlidePage
      })
      .catch((error) => {
        console.error('Error uploading files:', error);
      });
  };

  return (
    <div className="landing-page">
      <div className="logo-container">
        <img src="./image1.png" alt="Your Logo" className="logo" />
      </div>
      <div className="upload-section-container">
        <div className="zip-upload-section-unique">
          <h2 className="section-title">Select PNG Image Files</h2>
          <input
            type="file"
            accept="image/png"
            multiple
            onChange={handleImageFileSelection}
            className="file-input"
          />
        </div>

        <div className="latex-upload-section-unique">
          <h2 className="section-title">Select LaTeX Code File (.txt)</h2>
          <input
            type="file"
            accept=".txt"
            onChange={handleLatexFileSelection}
            className="file-input"
          />
        </div>
      </div>
      <div className="submit-button-container-unique">
        <button className="submit-button-modern" onClick={handleSubmit}>
          Submit
        </button>
      </div>
    </div>
  );
}

export default App;
