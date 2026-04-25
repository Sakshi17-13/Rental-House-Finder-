import { Link, useNavigate } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("user");
    navigate("/");
  };

  return (
    <div className="navbar">
      <h2>🏠 Rental Finder</h2>

      <div>
        <Link to="/home">Home</Link>
        <Link to="/favorites">Favorites</Link>
        <Link to="/analytics">Analytics</Link>
        <Link to="/budget">Budget</Link>
        <Link to="/verify">Verify</Link>
        <button onClick={logout}>Logout</button>
      </div>
    </div>
  );
};

export default Navbar;