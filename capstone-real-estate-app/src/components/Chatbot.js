import React, { useState } from "react";
import axios from "axios";

const Chatbot = () => {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const img_path_prefix = "http://127.0.0.1:8000/media/";

  const getEmojiForQuery = (text) => {
    const lower = text.toLowerCase();
    if (lower.includes("buy") || lower.includes("purchase")) return "🏠🛍️";
    if (lower.includes("rent") || lower.includes("lease")) return "🏡💸";
    if (lower.includes("bedroom") || lower.includes("bed")) return "🛏️";
    if (lower.includes("bathroom") || lower.includes("bath")) return "🛁";
    if (lower.includes("price") || lower.includes("budget") || lower.includes("$")) return "💰";
    if (lower.includes("san jose")) return "📍San Jose";
    return "🤖";
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    const currentQuery = query;

    // Add user message
    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: currentQuery,
        emoji: getEmojiForQuery(currentQuery),
      },
    ]);
    setQuery("");

    try {
      const res = await axios.post("http://127.0.0.1:8000/api/chatbot/", {
        query: currentQuery,
      });

      console.log("🧠 Backend Response:", res.data);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          message: res.data.message || null,
          recommendations: res.data.recommendations || [],
          filters: res.data.query_interpretation || {},
        },
      ]);
    } catch (error) {
      console.error("❌ Error in API call:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "❌ An error occurred. Please try again." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const renderPropertyCard = (property) => (
    <div key={property["Street Address"]} style={styles.propertyCard}>
      <h5>{property["Street Address"]}</h5>
      <p>City: {property.City}</p>
      <p>Price: ${property.Price.toLocaleString()}</p>
      <p>Bedrooms: {property.Bedrooms}</p>
      <p>Bathrooms: {property.Bathrooms}</p>
      <p>Square Footage: {property["Square Footage"]} sqft</p>
      <p>Type: {property["Property Type"]}</p>
      <img
        src={img_path_prefix + property.Image_Path}
        alt={property["Street Address"]}
        style={styles.propertyImage}
      />
    </div>
  );

  return (
    <div style={styles.chatbotContainer}>
      <button onClick={() => setIsOpen(!isOpen)} style={styles.toggleButton}>
        {isOpen ? "Close Chat" : "Open Chat"}
      </button>

      {isOpen && (
        <div style={styles.chatbotWindow}>
          <h3>RealHaven AI Assistant</h3>

          <div style={styles.chatArea}>
            {messages.length === 0 ? (
              <div style={styles.welcomeMessage}>
                👋 How can I help you with real estate today?
              </div>
            ) : (
              messages.map((msg, index) => (
                <div
                  key={index}
                  style={{
                    ...styles.message,
                    ...(msg.sender === "user"
                      ? styles.userMessage
                      : styles.botMessage),
                  }}
                >
                  {msg.sender === "bot" ? (
                    <div>
                      {msg.message && (
                        <div style={{ whiteSpace: "pre-line", marginBottom: "10px" }}>
                          💬 {msg.message}
                        </div>
                      )}
                      {msg.recommendations && msg.recommendations.length > 0 ? (
                        <div>
                          <h4>🏡 Matching Properties:</h4>
                          {msg.recommendations.map(renderPropertyCard)}
                        </div>
                      ) : null}
                    </div>
                  ) : (
                    <div style={{ whiteSpace: "pre-line" }}>
                      {msg.emoji && (
                        <span style={{ marginRight: "5px" }}>{msg.emoji}</span>
                      )}
                      {msg.text}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>

          <form onSubmit={handleSubmit} style={styles.form}>
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ex: Show me 3-bed homes in San Jose under $2M"
              style={styles.textarea}
              disabled={isLoading}
            />
            <button
              type="submit"
              style={styles.button}
              disabled={isLoading || !query.trim()}
            >
              {isLoading ? "Thinking..." : "Send"}
            </button>
          </form>
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
    width: "370px",
    height: "530px",
    display: "flex",
    flexDirection: "column",
    padding: "15px",
    backgroundColor: "#fff",
    border: "1px solid #ccc",
    borderRadius: "10px",
    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.2)",
  },
  chatArea: {
    flex: 1,
    overflowY: "auto",
    marginBottom: "15px",
    padding: "10px",
    backgroundColor: "#f9f9f9",
    borderRadius: "5px",
  },
  welcomeMessage: {
    textAlign: "center",
    color: "#666",
    padding: "20px",
  },
  message: {
    maxWidth: "85%",
    padding: "10px",
    marginBottom: "10px",
    borderRadius: "10px",
    wordWrap: "break-word",
  },
  userMessage: {
    backgroundColor: "#d1ecf1",
    marginLeft: "auto",
    borderTopRightRadius: "0",
  },
  botMessage: {
    backgroundColor: "#f8f9fa",
    marginRight: "auto",
    borderTopLeftRadius: "0",
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
    minHeight: "60px",
    resize: "none",
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
  propertyCard: {
    marginBottom: "15px",
    padding: "10px",
    backgroundColor: "#fff",
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