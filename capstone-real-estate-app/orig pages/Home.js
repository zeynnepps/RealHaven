import React, { useState } from "react";
import properties from "../data/properties";
import PropertyCard from "../components/PropertyCard";
import "../styles/Home.css";

const Home = () => {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredProperties = properties.filter((property) =>
    property.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    property.location.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="home-container">
      <div className="hero-section">
        <h1>Find Your Dream Home</h1>
        <input
          type="text"
          placeholder="Search by title or location..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-bar"
        />
      </div>

      <div className="property-list">
        {filteredProperties.length > 0 ? (
          filteredProperties.map((property) => (
            <PropertyCard key={property.id} property={property} />
          ))
        ) : (
          <h2>No properties found</h2>
        )}
      </div>
    </div>
  );
};

export default Home;