import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  // return (
  //   // <nav style={styles.nav}>
  //   //   <Link to="/" style={styles.link}>
  //   //     Home
  //   //   </Link>
  //   //   <Link to="/chatbot" style={styles.link}>
  //   //     Chatbot
  //   //   </Link>
  //   // </nav>
  // );
};


const styles = {
  nav: {
    display: "flex",
    justifyContent: "space-around",
    padding: "10px",
    backgroundColor: "#007bff",
  },
  link: {
    color: "#fff",
    textDecoration: "none",
    fontSize: "18px",
  },
};


export default Navbar;