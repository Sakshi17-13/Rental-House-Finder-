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

        <button onClick={logout}>Logout</button>
      </div>
    </div>
  );
};

export default Navbar;