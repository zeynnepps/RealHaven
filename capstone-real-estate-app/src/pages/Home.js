import { Link } from "react-router-dom";
import React, { useState } from "react";
import PropertyCard from "../components/PropertyCard";
import Chatbot from "../components/Chatbot";
import "../styles/Home.css";
import { signup } from "../components/api";
import { login } from "../components/api";

const Home = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoginForm, setLoginForm] = useState(false);
  const [isSignupForm, setSignupForm] = useState(false);
  const [isOpenPopup, setIsOpenPopup] = useState(false);
  const [filteredProperties, setfilteredProperties] = useState([]);
  const [selectedValue, setSelectedValue] = useState('0');
  const [signupName, setSignupName] = useState('');
  const [signupEmail, setSignupEmail] = useState('');
  const [signupPassword, setSignupPassword] = useState('');
  const [signupSuccess, setSignupSuccess] = useState(false);
  const [signupError, setSignupError] = useState('');
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [loginError, setLoginError] = useState('');
  const [loginSuccess, setLoginSuccess] = useState(false);

  const openLoginForm = () => {
    setLoginForm(true);
    setIsOpenPopup(true);
    setSignupForm(false);
  };

  const closeLoginForm = () => {
    setLoginForm(false);
    setSignupForm(false);
    setIsOpenPopup(false);
  };

  const openSignupForm = () => {
    setSignupForm(true);
    setLoginForm(false)
  };


  // Handle change in dropdown selection
  const handleChange = (event) => {
   
    setSelectedValue(event.target.value);
    if(searchTerm && searchTerm != ""){
      setSearchTerm("");
    }
  };

  const handleSignupSubmit = async (e) => {
    e.preventDefault();
    try {
      await signup({ name: signupName, email: signupEmail, password: signupPassword });
      setSignupSuccess(true);
      setSignupError('');
      setSignupName('');
      setSignupEmail('');
      setSignupPassword('');

      setTimeout(() => {
        setSignupSuccess(false);  // clear success message if desired
        openLoginForm();          // switch to login form
      }, 1500);
      
    } catch (err) {
      setSignupError("Signup failed. Try a different email.");
      setSignupSuccess(false);
    }
  };
  
  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await login(loginEmail, loginPassword);
      console.log("✅ Login success response:", response.data);
      setLoginSuccess(true);
      setLoginError('');
      setLoginEmail('');
      setLoginPassword('');
      closeLoginForm();
    } catch (err) {
      console.error("❌ Login error:", err.response?.data || err.message);
      setLoginError("Invalid email or password");
      setLoginSuccess(false);
    }
  };

  const fetchPropertyDetails = async () =>{
    try{
       const response = await fetch('http://127.0.0.1:8000/api/properties/search/?'+selectedValue+'='+searchTerm);
       console.log("response...", response);
       const data = await response.json();
       setfilteredProperties(data);
     //  console.log("Data....", data);
    }catch(e){
      console.log("error..", e)
    }
  }

  return (
    // <div className="home-container">
    <div
    className="home-container"
    style={{
      minHeight: "100vh",
      backgroundImage: `url(${process.env.PUBLIC_URL}/images/la.jpg)`,
      backgroundSize: "cover",
      backgroundPosition: "center",
      backgroundRepeat: "no-repeat",
    }}
  >
      {/* ADDED Buy and Rent Buttons */}
      <div className="top-buttons">
        <button className="buy-button">Buy</button>
        <button className="rent-button">Rent</button>
        <Link to="/visualizations">
          <button className="visualizations-button">Visualizations</button>
        </Link>
      </div>
      
      <h1 className="home-title">Welcome to the Real Haven
     </h1>

      {filteredProperties.length > 0 && (
      <div className="home-return-button">
        <button onClick={() => {
        setfilteredProperties([]);
        setSearchTerm("");
        setSelectedValue("0");
      }}>
        🏠 Back to Home
      </button>

      </div>
    )}
      
     <img src="images/logo.jpeg" className="logo-style"></img>
      <button className="login-button" onClick={openLoginForm}>
        Login
      </button>
      
      <div className="input-search">
      <div>
      <select className="search-type" value={selectedValue} onChange={handleChange}>
        <option value='0'>Search By</option>
        <option value='zip_code'>Zipcode</option>
        <option value='address'>Address</option>
        <option value='property_type'>Property Type</option>
      </select>
      </div>
      <input
        type="text"
        placeholder="Enter an address, neighborhood, city, or ZIP code"
        value={searchTerm} disabled={selectedValue === '0'}
        onChange={(e) => setSearchTerm(e.target.value)}
        style={{ width: "600px", height: "40px", fontSize: "16px" }} // Adjusted inline styles
        className="search-input"
      />
      <button className="search-button" onClick={fetchPropertyDetails}>Search</button>
      </div>
      {filteredProperties.length > 0 && <div className="property-list" >
        {filteredProperties.map((property) => (
           <PropertyCard key={property.id} property={property}/>
        ))}
      </div>}

      {isOpenPopup && (
        <div className="login-modal-overlay">
          <div className="login-modal">
            <button className="close-button" onClick={closeLoginForm}>
              X
            </button>
            <h2 className="modal-title">Real Haven</h2>
            <div className="tab-buttons">
              <button className={isLoginForm ? "tab-button active" : "tab-button"} onClick = {openLoginForm}>Sign in</button>
              <button className={isSignupForm ? "tab-button active" : "tab-button"} onClick = {openSignupForm}
              >New account</button>
            </div>
            
           {(isLoginForm && !isSignupForm) && (
              <form onSubmit={handleLoginSubmit}>
                <input
                  type="email"
                  id="email"
                  name="email"
                  placeholder="Enter email"
                  value={loginEmail}
                  onChange={(e) => setLoginEmail(e.target.value)}
                  required
                />
                <input
                  type="password"
                  id="password"
                  name="password"
                  placeholder="Enter password"
                  value={loginPassword}
                  onChange={(e) => setLoginPassword(e.target.value)}
                  required
                />
                <button type="submit" className="submit-button">
                  Sign in
                </button>

                {loginError && <p style={{ color: 'red' }}>{loginError}</p>}
                {loginSuccess && <p style={{ color: 'green' }}>✅ Logged in successfully</p>}

                <a href="#" className="forgot-password">
                  Forgot your password?
                </a>
              </form>
            )}

            {isSignupForm && (
              <form name="registration" onSubmit={handleSignupSubmit}>
                <input
                  type="text"
                  id="name"
                  name="name"
                  placeholder="Enter your name"
                  value={signupName}
                  onChange={(e) => setSignupName(e.target.value)}
                  required
                />
                <input
                  type="email"
                  id="email"
                  name="email"
                  placeholder="Enter your email"
                  value={signupEmail}
                  onChange={(e) => setSignupEmail(e.target.value)}
                  required
                />
                <input
                  type="password"
                  id="password"
                  name="password"
                  placeholder="Enter your password"
                  value={signupPassword}
                  onChange={(e) => setSignupPassword(e.target.value)}
                  required
                />
                <button type="submit" className="submit-button">
                  Submit
                </button>

                {signupSuccess && <p style={{ color: "green" }}>✅ Signup successful!</p>}
                {signupError && <p style={{ color: "red" }}>{signupError}</p>}
              </form>
            )}

          </div>
        </div>
      )}
      <Chatbot />
    </div>
  );
};

export default Home;
