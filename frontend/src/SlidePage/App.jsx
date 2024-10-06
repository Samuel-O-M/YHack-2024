import React, { useState } from 'react';
import './SlidePage.css';

const SlidePage = () => {
  const [slides, setSlides] = useState(['Slide 1', 'Slide 2', 'Slide 3']);
  const [images, setImages] = useState(['Image 1', 'Image 2', 'Image 3']);
  const [paragraphs, setParagraphs] = useState(['Paragraph 1', 'Paragraph 2', 'Paragraph 3']);
  const [currentSlide, setCurrentSlide] = useState(0);
  const [currentImage, setCurrentImage] = useState(0);
  const [currentParagraph, setCurrentParagraph] = useState(0);

  const navigate = (setter, current, items, increment) => {
    setter((current + increment + items.length) % items.length);
  };

  const addSlide = () => {
    setSlides([...slides, `Slide ${slides.length + 1}`]);
    setCurrentSlide(slides.length);
  };

  return (
    <div className="slide-page">
      <div className="main-content">
        <div className="slide-section">
          <div className="content">
            <h2>{slides[currentSlide]}</h2>
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
            <p>{images[currentImage]}</p>
          </div>
          <div className="navigation">
            <button onClick={() => navigate(setCurrentImage, currentImage, images, -1)}>&lt;</button>
            <button>+</button>
            <button onClick={() => navigate(setCurrentImage, currentImage, images, 1)}>&gt;</button>
          </div>
        </div>
        <div className="paragraph-section">
          <div className="content">
            <p>{paragraphs[currentParagraph]}</p>
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