import React from "react";
import { Link, useLocation } from "react-router-dom";

const PropertyCard = ({ property }) => {
  const location = useLocation();

  return (
    <div className="property-card">
      <img src={property.image_url} alt={property.city} />
      <h2>{property.street_address}</h2>
      <p>{property.zip_code}</p>
      <Link
        to={`/property/${property.id}`}
        state={{ property, from: location }}
      >
        View Details
      </Link>
    </div>
  );
};

export default PropertyCard;
