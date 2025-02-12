import React from "react";
import { useParams, Link } from "react-router-dom";
import properties from "../data/properties";
import "../styles/PropertyDetails.css";

const PropertyDetails = () => {
  const { id } = useParams();
  const property = properties.find((p) => p.id === parseInt(id));

  if (!property) return <h2>Property not found!</h2>;

  return (
    <div className="details-container">
      <div className="details-card">
        <img src={property.image} alt={property.title} />
        <h1>{property.title}</h1>
        <p className="price">{property.price}</p>
        <p className="location">{property.location}</p>
        <p className="description">{property.description}</p>
        <Link to="/" className="back-button">← Back to Home</Link>
      </div>
    </div>
  );
};

export default PropertyDetails;
