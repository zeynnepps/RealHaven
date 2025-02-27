import React, { useState } from "react";
import properties from "../data/properties";
import PropertyCard from "../components/PropertyCard";
import "../styles/Home.css";

const Home = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);

  const filteredProperties = properties.filter(
    (property) =>
      property.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      property.location.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const openLoginModal = () => {
    setIsLoginModalOpen(true);
  };

  const closeLoginModal = () => {
    setIsLoginModalOpen(false);
  };

  return (
    <div className="home-container">
      {/* ADDED Buy and Rent Buttons */}
      <div className="top-buttons">
        <button className="buy-button">Buy</button>
        <button className="rent-button">Rent</button>
      </div>

      <h1 className="home-title">Welcome to the Real Haven</h1>
      <button className="login-button" onClick={openLoginModal}>
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

      {isLoginModalOpen && (
        <div className="login-modal-overlay">
          <div className="login-modal">
            <button className="close-button" onClick={closeLoginModal}>
              X
            </button>
            <h2 className="modal-title">Real Haven</h2>
            <div className="tab-buttons">
              <button className="tab-button active">Sign in</button>
              <button className="tab-button">New account</button>
            </div>
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
            </form>
            <a href="#" className="forgot-password">
              Forgot your password?
            </a>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
