import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { signup } from '../components/api';

const Signup = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    console.log("Signup form submitted");
    try {
      const response = await signup({ name: username, email, password });
      console.log('Signup successful:', response.data);
      setSuccess(true);
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err) {
        console.error("❌ Signup failed:", err);
        setError("Signup failed. Please try again.");
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: 'auto', padding: '2rem' }}>
      <h2>Sign Up</h2>
        {/* ✅ Success Message */}
        {success && <p style={{ color: 'green' }}>✅ Signup successful! Redirecting to login...</p>}

        {/* ❌ Error Message */}
        {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSignup}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <br /><br />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <br /><br />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <br /><br />
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
};

export default Signup;
