import { useState } from 'react';
import './App.css';
import JSZip from 'jszip';

function App() {
  const [count, setCount] = useState(0);
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
        
        //Trying to read the Zip File
        zipContent.forEach(async (relativePath, zipEntry) => {
          if (zipEntry.name.match(/\.(jpg|jpeg|png|gif)$/i)) {
            const imageBlob = await zipEntry.async('blob');
            images.push(new File([imageBlob], zipEntry.name));
          }
        });
        
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
    // Here you can handle the submission of images and LaTeX code.
    console.log('Submitted Images:', selectedImages);
    console.log('Submitted LaTeX Code:', latexCode);
  };

  return (
    <>
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
      <button className="submit-button" onClick={handleSubmit}>
        Submit
      </button>
    </>
  );
}

export default App;