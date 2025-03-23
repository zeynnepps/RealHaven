import React, { useState } from "react";
import axios from "axios";

const Chatbot = () => {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/api/chatbot/", {
        query: query,
      });
      console.log("Backend Response:", res.data); // Log the response
      setResponse(res.data);
      setQuery("");
    } catch (error) {
      console.error("Error:", error);
      setResponse({ error: "An error occurred. Please try again." });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={styles.chatbotContainer}>
      <button onClick={() => setIsOpen(!isOpen)} style={styles.toggleButton}>
        {isOpen ? "Close Chat" : "Open Chat"}
      </button>

      {isOpen && (
        <div style={styles.chatbotWindow}>
          <h3>RealHeaven AI Assistant</h3>
          <form onSubmit={handleSubmit} style={styles.form}>
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter your query (e.g., Show me houses with 3 bedrooms in San Jose under $2,000,000.)"
              style={styles.textarea}
              disabled={isLoading}
            />
            <button type="submit" style={styles.button} disabled={isLoading}>
              {isLoading ? "Loading..." : "Submit"}
            </button>
          </form>

          {response && (
            <div style={styles.response}>
              {response.error ? (
                <p style={{ color: "red" }}>{response.error}</p>
              ) : response.message ? (
                <p>{response.message}</p>
              ) : Array.isArray(response.properties) ? (
                <div>
                  <h4>Matching Properties:</h4>
                  {response.properties.map((property, index) => (
                    <div key={index} style={styles.propertyCard}>
                      <h5>{property["Street Address"]}</h5>
                      <p>City: {property.City}</p>
                      <p>Price: ${property.Price.toLocaleString()}</p>
                      <p>Bedrooms: {property.Bedrooms}</p>
                      <p>Bathrooms: {property.Bathrooms}</p>
                      <p>Square Footage: {property["Square Footage"]} sqft</p>
                      <p>Type: {property["Property Type"]}</p>
                      <img
                        src={property.Image_Path}
                        alt={property["Street Address"]}
                        style={styles.propertyImage}
                      />
                    </div>
                  ))}
                </div>
              ) : (
                <p>No properties found.</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

const styles = {
  chatbotContainer: {
    position: "fixed",
    bottom: "20px",
    right: "20px",
    zIndex: 1000,
  },
  toggleButton: {
    padding: "10px 20px",
    fontSize: "16px",
    backgroundColor: "#007bff",
    color: "#fff",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
  chatbotWindow: {
    width: "300px",
    padding: "20px",
    backgroundColor: "#fff",
    border: "1px solid #ccc",
    borderRadius: "10px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
    marginTop: "10px",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  textarea: {
    padding: "10px",
    fontSize: "14px",
    borderRadius: "5px",
    border: "1px solid #ccc",
    minHeight: "80px",
  },
  button: {
    padding: "10px",
    fontSize: "14px",
    backgroundColor: "#007bff",
    color: "#fff",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
  response: {
    marginTop: "10px",
    padding: "10px",
    backgroundColor: "#f9f9f9",
    border: "1px solid #ddd",
    borderRadius: "5px",
    fontSize: "14px",
  },
  propertyCard: {
    marginBottom: "10px",
    padding: "10px",
    border: "1px solid #ddd",
    borderRadius: "5px",
  },
  propertyImage: {
    width: "100%",
    borderRadius: "5px",
    marginTop: "10px",
  },
};

export default Chatbot;