import { useState } from "react";

const API = "http://127.0.0.1:5000";

const Home = () => {
  const [location, setLocation] = useState("");
  const [type, setType] = useState("");
  const [results, setResults] = useState([]);

  const search = async () => {
    const res = await fetch(
      `${API}/search?location=${location}&type=${type}`
    );
    const data = await res.json();
    setResults(data);
  };

  return (
    <div className="container">
      <h1>🏠 Rental House Finder</h1>

      <input
        placeholder="Location"
        onChange={(e) => setLocation(e.target.value)}
      />

      <input
        placeholder="Type"
        onChange={(e) => setType(e.target.value)}
      />

      <button onClick={search}>Search</button>

      <div className="grid">
        {results.map((p, i) => (
          <div key={i} className="card">
            <h3>{p.title}</h3>
            <p>{p.location}</p>
            <p>₹{p.price}</p>
            
             <button onClick={() => saveFavorite(p.id)}>❤️ Save</button>
            {p.is_verified && <p className="verified">✅ Verified</p>}
            {p.fraud_flag && <p className="fraud">⚠ Fake</p>}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;
const user = localStorage.getItem("user");

const saveFavorite = async (id) => {
  await fetch(`${API}/add-favorite`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: user,
      property_id: id,
    }),
  });

  alert("Saved to favorites!");
};