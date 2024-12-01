import React, { useState } from 'react';
import axios from 'axios';

function Authenticate() {
  const [aliasIdentity, setAliasIdentity] = useState('');
  const [A_i, setA_i] = useState('');
  const [B_i, setB_i] = useState('');
  const [T, setT] = useState('');
  const [authMessage, setAuthMessage] = useState('');

  const handleAuthenticate = async (e) => {
    e.preventDefault();
    try {
      if (!aliasIdentity || !A_i || !B_i || !T) {
        setAuthMessage('Please fill all required fields');
        return;
      }

      const authRequest = await axios.post('http://localhost:5000/generate_auth_request', {
        alias_identity: aliasIdentity,
        A_i,
        B_i,
        T,
      });

      const { m1, m2, m3, ti, B_i: serverBi, T: serverT } = authRequest.data;

      const authResponse = await axios.post('http://localhost:5000/verify_authentication', {
        ti,
        m1,
        m2,
        m3,
        B_i: serverBi,
        T: serverT,
      });

      setAuthMessage(authResponse.data.message);
    } catch (error) {
      setAuthMessage('Authentication failed. Please try again.');
    }
  };

  return (
    <div>
      <h2>Authenticate</h2>
      <form onSubmit={handleAuthenticate}>
        <div>
          <label>Alias Identity:</label>
          <input
            type="text"
            value={aliasIdentity}
            onChange={(e) => setAliasIdentity(e.target.value)}
            required
          />
        </div>
        <div>
          <label>A_i:</label>
          <input
            type="text"
            value={A_i}
            onChange={(e) => setA_i(e.target.value)}
            required
          />
        </div>
        <div>
          <label>B_i:</label>
          <input
            type="text"
            value={B_i}
            onChange={(e) => setB_i(e.target.value)}
            required
          />
        </div>
        <div>
          <label>T:</label>
          <input
            type="text"
            value={T}
            onChange={(e) => setT(e.target.value)}
            required
          />
        </div>
        <button type="submit">Authenticate</button>
      </form>
      {authMessage && <p>{authMessage}</p>}
    </div>
  );
}

export default Authenticate;