import React from "react";
import { useParams, Link } from "react-router-dom";
import properties from "../data/properties";
import "../styles/PropertyDetails.css";
import { useLocation, useNavigate } from "react-router-dom";

const PropertyDetails = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const property = location.state?.property; // Access passed property data
  // const from = location.state?.from || "/";

  //const property = location.state?.property || properties.find(p => p.id === parseInt(id));

  if (!property) return <h2>Property not found!</h2>;
  
  const roomImages = Object.entries(property)
  .filter(([key, value]) =>
    value && // skip null
    ["bathroom", "bedroom", "kitchen", "dining", "living_room"].some(prefix => key.startsWith(prefix))
  );

  return (
    <div className="details-container">
      <div className="details-card">
        <img src={property.image_url} alt={property.city} />
        <h1>{property.street_address}</h1>
        <p className="price">Price: ${parseFloat(property.price).toLocaleString()}</p>
        <p>Bedrooms: {property.bedrooms}</p>
        <p>Bathrooms: {property.bathrooms}</p>
        <p>Area: {property.square_footage} sq ft</p>
        <p>Type: {property.property_type}</p>
        <p>Zipcode: {property.zip_code}</p>

        <h3>Detailed Images</h3>
        <div className="room-images-section">
      <h2>🏡 Room Images</h2>

      {/* Bathrooms */}
      <div className="room-group">
        <h3>🛁 Bathrooms</h3>
        {Object.entries(property)
          .filter(([key, value]) => key.startsWith("bathroom") && typeof value === "string" && value.trim() !== "")
          .map(([key, url]) => (
            <div key={key} className="room-item">
              <img src={url} alt={key} className="room-img" />
              <p>{key.replace("_", " ")}</p>
            </div>
          ))}
      </div>

      {/* Bedrooms */}
      <div className="room-group">
        <h3>🛏️ Bedrooms</h3>
        {Object.entries(property)
          .filter(([key, value]) => key.startsWith("bedroom") && typeof value === "string" && value.trim() !== "")
          .map(([key, url]) => (
            <div key={key} className="room-item">
              <img src={url} alt={key} className="room-img" />
              <p>{key.replace("_", " ")}</p>
            </div>
          ))}
      </div>

      {/* Other rooms */}
      {["kitchen", "dining", "living_room"].map((key) => {
        if (!property[key]) return null;

        const titles = {
          kitchen: "🍳 Kitchen",
          dining: "🍽 Dining Room",
          living_room: "🛋 Living Room",
        };

        return (
          <div key={key} className="room-item">
            <h3>{titles[key]}</h3>
            <img src={property[key]} alt={key} className="room-img" />
          </div>
        );
      })}

    </div>

        <button onClick={() => navigate(-1)} className="back-wrapper">
          <span className="circle-icon">←</span>
          <span className="back-label">Back</span>
        </button>
      </div>
    </div>
  );
};

export default PropertyDetails;
