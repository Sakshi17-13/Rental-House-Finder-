import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";

const API = "http://127.0.0.1:5000";

const Favorites = () => {
  const [data, setData] = useState([]);
  const user = localStorage.getItem("user");

  useEffect(() => {
    const loadFavorites = async () => {
      try {
        const res = await fetch(`${API}/get-favorites/${user}`);
        const result = await res.json();
        setData(result);
      } catch (err) {
        console.error("Error fetching favorites:", err);
      }
    };

    loadFavorites();
  }, [user]); // ✅ dependency added

  return (
    <>
      <Navbar />
      <div className="container">
        <h2>❤️ Favorites</h2>

        <div className="grid">
          {data.map((p, i) => (
            <div key={i} className="card">
              <h3>{p.title}</h3>
              <p>{p.location}</p>
              <p>₹{p.price}</p>
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

export default Favorites;