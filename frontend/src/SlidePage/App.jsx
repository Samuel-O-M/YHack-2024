import { useEffect, useState } from 'react';
import './SlidePage.css';  // Ensure the correct CSS file is linked

function SlidePage() {
    const [slides, setSlides] = useState([]);
    const [images, setImages] = useState([]);
    const [formulas, setFormulas] = useState([]);

    useEffect(() => {
        // Fetch images and formulas from the backend
        fetch('http://localhost:5000/images.json')  // Adjust the endpoint if necessary
            .then((response) => response.json())
            .then((data) => {
                // Assuming the response contains base64 image data
                const imageArray = data.pngfiles.map(file => ({
                    name: file.file_name, 
                    data: file.image_data
                }));
                setImages(imageArray);
            })
            .catch((error) => console.error('Error fetching images:', error));

        fetch('http://localhost:5000/formulas.json')  // Adjust the endpoint if necessary
            .then((response) => response.json())
            .then((data) => setFormulas(data.formulas))
            .catch((error) => console.error('Error fetching formulas:', error));

        // Optionally, fetch slides if they exist as a separate resource
        fetch('http://localhost:5000/slide_data')  // Example endpoint for slides
            .then((response) => response.json())
            .then((data) => setSlides(data.slides))
            .catch((error) => console.error('Error fetching slides:', error));
    }, []);

    return (
        <div className="slide-page">
            {/* Slides Section */}
            <div className="slide-section">
                <h2>Slides</h2>
                {slides.length > 0 ? (
                    slides.map((slide, index) => (
                        <div key={index} className="slide-item">
                            <h3>{`Slide ${index + 1}`}</h3>
                            <p>{slide}</p>
                        </div>
                    ))
                ) : (
                    <div className="slide-placeholder">
                        <h3>Slides</h3>
                        <p>No slides available yet. Please upload or check back later.</p>
                    </div>
                )}
            </div>

            {/* Images Section */}
            <div className="image-section">
                <h2>Images</h2>
                {images.length > 0 ? (
                    images.map((image, index) => (
                        <div key={index} className="image-item">
                            <img
                                src={`data:image/png;base64,${image.data}`}  // Display base64 image data
                                alt={`Slide Image ${index + 1}`}
                            />
                        </div>
                    ))
                ) : (
                    <div className="image-placeholder">
                        <h3>Images</h3>
                        <p>No images available yet. Please upload or check back later.</p>
                    </div>
                )}
            </div>

            {/* Formulas Section */}
            <div className="formula-section">
                <h2>Formulas</h2>
                {formulas.length > 0 ? (
                    formulas.map((formula, index) => (
                        <div key={index} className="formula-item">
                            <p>{formula}</p>
                        </div>
                    ))
                ) : (
                    <div className="formula-placeholder">
                        <h3>Formulas</h3>
                        <p>No formulas available yet. Please upload or check back later.</p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default SlidePage;
