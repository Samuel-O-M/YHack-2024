import { useState } from 'react';
import './App.css';
import JSZip from 'jszip';

function App() {
  const [selectedImages, setSelectedImages] = useState([]);
  const [latexCode, setLatexCode] = useState('');

  const handleZipFileSelection = async (e) => {
    const zip = new JSZip();
    const file = e.target.files[0];

    if (file) {
      try {
        const zipContent = await zip.loadAsync(file);
        const images = [];
        const entries = Object.values(zipContent.files);
        for (const zipEntry of entries) {
          if (zipEntry.name.match(/\.(jpg|jpeg|png|gif)$/i)) {
            const imageBlob = await zipEntry.async('blob');
            images.push(new File([imageBlob], zipEntry.name));
          }
        }
        setSelectedImages(images);
      } catch (error) {
        console.error('Error reading zip file:', error);
      }
    }
  };

  const handleLatexFileSelection = async (e) => {
    const file = e.target.files[0];
    if (file) {
      try {
        const text = await file.text();
        setLatexCode(text);
      } catch (error) {
        console.error('Error reading txt file:', error);
      }
    }
  };

  const handleSubmit = () => {
    if (selectedImages.length === 0 || !latexCode) {
      alert('Please select both a ZIP file with images and a LaTeX code file.');
      return;
    }

    const data = new FormData();
    selectedImages.forEach((image) => {
      data.append('images', image);
    });
    const latexBlob = new Blob([latexCode], { type: 'text/plain' });
    const latexFile = new File([latexBlob], 'latex_code.txt', { type: 'text/plain' });
    data.append('textfile', latexFile);

    fetch('http://localhost:5173/upload', {
      method: 'POST',
      body: data,
    })
      .then((response) => {
        if (response.ok) {
          return response.blob();
        } else {
          return response.text().then((text) => {
            throw new Error(text);
          });
        }
      })
      .then((pdfBlob) => {
        const url = window.URL.createObjectURL(pdfBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'output.pdf';
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      })
      .catch((error) => {
        console.error('Error uploading files:', error);
      });
  };

  return (
    <div className='landing-page'>
      <div className="logo-container">
        <img src="./image1.png" alt="Your Logo" className="logo" />
      </div>
      <div className="upload-section-container">
        <div className="zip-upload-section-unique">
          <h2 className="section-title">Select Zip File with Images</h2>
          <input
            type="file"
            accept=".zip"
            onChange={handleZipFileSelection}
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
