import React from "react";
import { useParams, Link } from "react-router-dom";
import properties from "../data/properties";
import "../styles/PropertyDetails.css";
import { useLocation } from "react-router-dom";

const PropertyDetails = () => {
  const location = useLocation();
  const property = location.state?.property; // Access passed property data

  if (!property) return <h2>Property not found!</h2>;

  return (
    <div className="details-container">
      <div className="details-card">
        <img src={property.image_path} alt={property.city} />
        <h1>{property.street_address}</h1>
        <p className="price">Price: {property.price}</p>
        <p className="location">Number of bedrooms: {property.bedrooms}</p>
        <p className="description">Number of bathrooms: {property.bathrooms}</p>
        <p className="description">Area: {property.square_footage} square feet</p>
        <p className="description">Property Type: {property.property_type}</p>
        <p className="description">Area zipcode: {property.zip_code}</p>
        <Link to="/" className="back-button">← Back to Home</Link>
      </div>
    </div>
  );
};

export default PropertyDetails;
