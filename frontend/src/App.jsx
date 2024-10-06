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
        //load the zip file
        const zipContent = await zip.loadAsync(file);
        const images = [];
        
        // Read the Zip File entries
        const entries = Object.values(zipContent.files);
        for (const zipEntry of entries) {
          if (zipEntry.name.match(/\.(jpg|jpeg|png|gif)$/i)) {
            const imageBlob = await zipEntry.async('blob');
            images.push(new File([imageBlob], zipEntry.name));
          }
        }
        
      //If the Zip FIle is not readable then we just return an Error
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
        //catch if the txt file is not readable
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
  
    // Append images to FormData
    selectedImages.forEach((image) => {
      data.append('images', image);
    });
  
    // Create a Blob from the LaTeX code and append it as a file
    const latexBlob = new Blob([latexCode], { type: 'text/plain' });
    const latexFile = new File([latexBlob], 'latex_code.txt', { type: 'text/plain' });
    data.append('textfile', latexFile);
  
    // Send the data to the backend
    fetch('http://localhost:5173/upload', {
      method: 'POST',
      body: data,
    })
      .then((response) => {
        if (response.ok) {
          return response.blob(); // Assuming the backend returns a PDF file
        } else {
          return response.text().then((text) => {
            throw new Error(text);
          });
        }
      })
      .then((pdfBlob) => {
        // Handle the PDF blob, e.g., download it
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
    <>
    <div className='landing-page'>
      <div className="zip-upload-section">
        <h2>Select Zip File with Images</h2>
        <input
          type="file"
          accept=".zip"
          onChange={handleZipFileSelection}
        />
        <div className="selected-images">
          {selectedImages.length > 0 &&
            selectedImages.map((image, index) => (
              <p key={index}>{image.name}</p>
            ))}
        </div>
      </div>

      <div className="latex-upload-section">
        <h2>Select LaTeX Code File (.txt)</h2>
        <input
          type="file"
          accept=".txt"
          onChange={handleLatexFileSelection}
        />
      </div>
      <div className="submit-button-container">
        <button className="submit-button" onClick={handleSubmit}>
          Submit
        </button>
      </div>
    </div>
    </>
  );
}

export default App;