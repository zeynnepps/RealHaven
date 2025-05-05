import React from "react";
import { Link } from "react-router-dom";
import DataVisualizations from "../components/DataVisualizations";

const Visualizations = () => {
  return (
    <div className="visualizations-page">
      <Link to="/" className="back-button">
        ← Back to Home
      </Link>
      <h2 className="viz-title">📊 RealHaven Property Data Visualizations</h2>
      <DataVisualizations />
    </div>
  );
};

export default Visualizations;