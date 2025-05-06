import React from "react";
import { Link } from "react-router-dom";

//const Navbar = () => {
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
//};

const Navbar = () => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) setUser(JSON.parse(storedUser));
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("user");
    setUser(null);
    navigate("/");
  };

  return (
    <nav style={styles.nav}>
      <Link to="/" style={styles.link}>Home</Link>
      <Link to="/chatbot" style={styles.link}>Chatbot</Link>
      <Link to="/visualizations" style={styles.link}>Visualizations</Link>

      {user ? (
        <>
          <span style={styles.link}>Welcome, {user.username}</span>
          <button onClick={handleLogout} style={styles.button}>Logout</button>
        </>
      ) : (
        <>
          <Link to="/login" style={styles.link}>Login</Link>
          <Link to="/signup" style={styles.link}>Sign Up</Link>
        </>
      )}
    </nav>
  );
};

// const styles = {
//   nav: {
//     display: "flex",
//     justifyContent: "space-around",
//     padding: "10px",
//     backgroundColor: "#007bff",
//   },
//   link: {
//     color: "#fff",
//     textDecoration: "none",
//     fontSize: "18px",
//   },
// };

const styles = {
  nav: {
    display: "flex",
    justifyContent: "space-around",
    alignItems: "center",
    padding: "10px",
    backgroundColor: "#007bff",
    flexWrap: "wrap",
  },
  link: {
    color: "#fff",
    textDecoration: "none",
    fontSize: "18px",
  },
  button: {
    backgroundColor: "#fff",
    color: "#007bff",
    border: "none",
    padding: "6px 12px",
    fontSize: "16px",
    cursor: "pointer",
    borderRadius: "4px",
  }
};


export default Navbar;