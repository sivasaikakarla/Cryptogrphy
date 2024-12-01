import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Register from './Register';
import Authenticate from './Authenticate';

function App() {
  return (
    <Router>
      <div>
        <h1>Secure Authentication System</h1>
        <Routes>
          <Route path="/" element={<Register />} />
          <Route path="/authenticate" element={<Authenticate />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
