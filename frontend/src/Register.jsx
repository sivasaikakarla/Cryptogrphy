import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Register() {
  const [identity, setIdentity] = useState('');
  const [response, setResponse] = useState(null);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const result = await axios.post('http://localhost:5000/register', { identity });
      setResponse(result.data);
    } catch (error) {
      setResponse({ message: 'Registration failed. Please try again.' });
    }
  };

  const handleNavigate = () => {
    navigate('/authenticate'); 
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <label>Identity:</label>
        <input
          type="text"
          value={identity}
          onChange={(e) => setIdentity(e.target.value)}
          required
        />
        <button type="submit">Register</button>
      </form>
      {response && (
        <div>
          <p>{response.message}</p>
          {response.alias_identity && (
            <div>
              <p><strong>Alias Identity:</strong> {response.alias_identity}</p>
              <p><strong>A_i:</strong> {response.A_i}</p>
              <p><strong>B_i:</strong> {response.B_i}</p>
              <p><strong>T:</strong> {response.T}</p>
            </div>
          )}
          <button onClick={handleNavigate}>Go to Authentication Page</button>
        </div>
      )}
    </div>
  );
}

export default Register;
