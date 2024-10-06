import React, { useState } from 'react';
import './SlidePage.css';

// Import your images
import slideImage1 from '../assets/images/slide1.png'; // Replace with actual path
import slideImage2 from '../assets/images/slide2.png';
import slideImage3 from '../assets/images/slide3.png';

import sideImage1 from '../assets/images/slide1.png';
import sideImage2 from '../assets/images/slide2.png';
import sideImage3 from '../assets/images/slide3.png';

import paragraphImage1 from '../assets/images/slide1.png';
import paragraphImage2 from '../assets/images/slide2.png';
import paragraphImage3 from '../assets/images/slide3.png';

const SlidePage = () => {
  const [slides, setSlides] = useState([slideImage1, slideImage2, slideImage3]);
  const [images, setImages] = useState([sideImage1, sideImage2, sideImage3]);
  const [paragraphs, setParagraphs] = useState([paragraphImage1, paragraphImage2, paragraphImage3]);

  const [currentSlide, setCurrentSlide] = useState(0);
  const [currentImage, setCurrentImage] = useState(0);
  const [currentParagraph, setCurrentParagraph] = useState(0);

  const navigate = (setter, current, items, increment) => {
    setter((current + increment + items.length) % items.length);
  };

  const addSlide = () => {
    setSlides([...slides, slideImage1]); // Add a placeholder or new slide image
    setCurrentSlide(slides.length);
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
            <button onClick={addSlide}>+</button>
            <button onClick={() => navigate(setCurrentSlide, currentSlide, slides, 1)}>&gt;</button>
          </div>
        </div>
      </div>
      <div className="side-content">
        <div className="image-section">
          <div className="content">
            <img src={images[currentImage]} alt={`Image ${currentImage + 1}`} />
          </div>
          <div className="navigation">
            <button onClick={() => navigate(setCurrentImage, currentImage, images, -1)}>&lt;</button>
            <button>+</button>
            <button onClick={() => navigate(setCurrentImage, currentImage, images, 1)}>&gt;</button>
          </div>
        </div>
        <div className="paragraph-section">
          <div className="content">
            <img src={paragraphs[currentParagraph]} alt={`Paragraph ${currentParagraph + 1}`} />
          </div>
          <div className="navigation">
            <button onClick={() => navigate(setCurrentParagraph, currentParagraph, paragraphs, -1)}>&lt;</button>
            <button>+</button>
            <button onClick={() => navigate(setCurrentParagraph, currentParagraph, paragraphs, 1)}>&gt;</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SlidePage;
