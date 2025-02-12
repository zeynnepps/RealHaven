import React from "react";
import { Link } from "react-router-dom";

const PropertyCard = ({ property }) => {
  return (
    <div className="property-card">
      <img src={property.image} alt={property.title} />
      <h2>{property.title}</h2>
      <p>{property.price}</p>
      <p>{property.location}</p>
      <Link to={`/property/${property.id}`}>View Details</Link>
    </div>
  );
};

export default PropertyCard;
