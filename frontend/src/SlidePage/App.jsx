import React, { useState, useEffect } from 'react';
import './SlidePage.css';

// Import your images
import slideImage1 from '../assets/images/slide1.png';
import slideImage2 from '../assets/images/slide2.png';
import slideImage3 from '../assets/images/slide3.png';

const SlidePage = () => {
  const [slides, setSlides] = useState([slideImage1, slideImage2, slideImage3]);
  const [currentSlide, setCurrentSlide] = useState(0);
  const [latexFunctions, setLatexFunctions] = useState('');  // New state for LaTeX functions

  // Function to fetch LaTeX functions from API
  const fetchLatexFunctions = async () => {
    const latexContent = `Your LaTeX content here`;  // Replace with actual LaTeX content
    const apiKey = 'your-api-key-here';
    const functions = await getFunctionsFromLatex(latexContent, apiKey);
    setLatexFunctions(functions);  // Store LaTeX functions in state
  };

  useEffect(() => {
    fetchLatexFunctions();  // Fetch LaTeX functions when the component mounts
  }, []);

  const navigate = (setter, current, items, increment) => {
    setter((current + increment + items.length) % items.length);
  };

  return (
    <div className="slide-page">
      <div className="main-content">
        <div className="slide-section">
          <div className="content">
            <img src={slides[currentSlide]} alt={`Slide ${currentSlide + 1}`} />
          </div>
          <div className="navigation">
            <button onClick={() => navigate(setCurrentSlide, currentSlide, slides, -1)}>&lt;</button>
            <button>+</button>
            <button onClick={() => navigate(setCurrentSlide, currentSlide, slides, 1)}>&gt;</button>
          </div>
        </div>
      </div>
      <div className="side-content">
        <div className="paragraph-section">
          <div className="content">
            {/* Display extracted LaTeX functions */}
            <p className="latex-functions">{latexFunctions}</p>  
          </div>
        </div>
      </div>
    </div>
  );
};

export default SlidePage;
