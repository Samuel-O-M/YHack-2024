import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import App from './App';
import SlidePage from './SlidePage/App';

ReactDOM.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/slidepage" element={<SlidePage />} />
      </Routes>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
);
