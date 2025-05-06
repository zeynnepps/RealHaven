import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import PropertyDetails from "./pages/PropertyDetails";
import Chatbot from "./components/Chatbot";  
import Visualizations from "./pages/Visualizations";
import Login from "./pages/Login";         
import Signup from "./pages/Signup";       


function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/property/:id" element={<PropertyDetails />} />
        <Route path="/chatbot" element={<Chatbot />} />
        <Route path="/visualizations" element={<Visualizations />} /> 
        <Route path="/login" element={<Login />} />     
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </Router>
  );
}

export default App;