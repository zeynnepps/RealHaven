import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import PropertyDetails from "./pages/PropertyDetails";
import Chatbot from "./components/Chatbot";  
import Visualizations from "./pages/Visualizations";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/property/:id" element={<PropertyDetails />} />
        <Route path="/chatbot" element={<Chatbot />} />
        <Route path="/visualizations" element={<Visualizations />} /> 
      </Routes>
    </Router>
  );
}

export default App;