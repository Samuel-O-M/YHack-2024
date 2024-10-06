import React from 'react';
import { createRoot } from 'react-dom/client';  // Import createRoot
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import App from './App';
import SlidePage from './SlidePage/App';

const container = document.getElementById('root'); // Get the root element
const root = createRoot(container); // Create the root for concurrent features

root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/slidepage" element={<SlidePage />} />
      </Routes>
    </Router>
  </React.StrictMode>
);
