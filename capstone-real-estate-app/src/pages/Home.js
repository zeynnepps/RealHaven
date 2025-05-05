import { Link } from "react-router-dom";
import React, { useState } from "react";
import PropertyCard from "../components/PropertyCard";
import Chatbot from "../components/Chatbot";
import "../styles/Home.css";

const Home = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoginForm, setLoginForm] = useState(false);
  const [isSignupForm, setSignupForm] = useState(false);
  const [isOpenPopup, setIsOpenPopup] = useState(false);
  const [filteredProperties, setfilteredProperties] = useState([]);
  const [selectedValue, setSelectedValue] = useState('0');

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
      <Chatbot />
    </div>
  );
};

export default Home;
