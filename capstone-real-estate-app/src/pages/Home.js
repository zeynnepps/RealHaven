import React, { useState } from "react";
import properties from "../data/properties";
import PropertyCard from "../components/PropertyCard";
import "../styles/Home.css";

const Home = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoginForm, setLoginForm] = useState(false);
  const [isSignupForm, setSignupForm] = useState(false);
  const [isOpenPopup, setIsOpenPopup] = useState(false);
  

  const filteredProperties = properties.filter(
    (property) =>
      property.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      property.location.toLowerCase().includes(searchTerm.toLowerCase())
  );

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

  return (
    <div className="home-container">
      {/* ADDED Buy and Rent Buttons */}
      <div className="top-buttons">
        <button className="buy-button">Buy</button>
        <button className="rent-button">Rent</button>
        <button className="sell-button">Sell</button>
      </div>

      <h1 className="home-title">Welcome to the Real Haven</h1>
      <button className="login-button" onClick={openLoginForm}>
        Login
      </button>

      <input
        type="text"
        placeholder="Enter an address, neighborhood, city, or ZIP code"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        style={{ width: "600px", height: "40px", fontSize: "16px" }} // Adjusted inline styles
        className="search-input"
      />

      <div className="property-list">
        {filteredProperties.map((property) => (
          <PropertyCard key={property.id} property={property} />
        ))}
      </div>

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
            
           {(isLoginForm && !isSignupForm)&& (
            <form>
              <input
                type="email"
                id="email"
                name="email"
                placeholder="Enter email"
              />
              <input
                type="password"
                id="password"
                name="password"
                placeholder="Enter password"
              />
              <button type="submit" className="submit-button">
                Sign in
              </button>
              <a href="#" className="forgot-password">
              Forgot your password?
            </a>
            </form> )}

            {isSignupForm && (
            <form name = "registration" >
              <input
                type="text"
                id="name"
                name="name"
                placeholder="Enter your name"
              />
              <input
                type="email"
                id="email"
                name="email"
                placeholder="Enter your email"
              />
                <input
                type="text"
                id="phone"
                name="phone"
                placeholder="Enter your phone number"
              />
              <button type="submit" className="submit-button">
                Submit
              </button>
            </form>)}

            
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
