import React from "react";
import { Link } from "react-router-dom";

const PropertyCard = ({ property }) => {
  return (
    <div className="property-card">
      <img src={property.image_path} alt={property.city} />
      <h2>{property.street_address}</h2>
      <p>{property.zip_code}</p>
       <Link to={`/property/${property}`} state={{property}}>View Details</Link>
    </div>
  );
};

export default PropertyCard;
