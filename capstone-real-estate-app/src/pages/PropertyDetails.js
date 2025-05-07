import React from "react";
import { useParams, Link } from "react-router-dom";
import properties from "../data/properties";
import "../styles/PropertyDetails.css";
import { useLocation, useNavigate } from "react-router-dom";

const PropertyDetails = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const property = location.state?.property; // Access passed property data
  const from = location.state?.from || "/";

  //const property = location.state?.property || properties.find(p => p.id === parseInt(id));

  if (!property) return <h2>Property not found!</h2>;
  
  return (
    <div className="details-container">
      <div className="details-card">
        <img src={property.image_url} alt={property.city} />
        <h1>{property.street_address}</h1>
        <p className="price">Price: {property.price}</p>
        <p className="location">Number of bedrooms: {property.bedrooms}</p>
        <p className="description">Number of bathrooms: {property.bathrooms}</p>
        <p className="description">Area: {property.square_footage} square feet</p>
        <p className="description">Property Type: {property.property_type}</p>
        <p className="description">Area zipcode: {property.zip_code}</p>
        <button onClick={() => navigate(from)} className="back-wrapper">
          <span className="circle-icon">←</span>
          <span className="back-label">Back</span>
        </button>
      </div>
    </div>
  );
};

export default PropertyDetails;
