import { useState } from "react";
import Navbar from "../components/Navbar";

const API = "http://127.0.0.1:5000";

const Budget = () => {
  const [salary, setSalary] = useState("");
  const [result, setResult] = useState(null);

  const calculate = async () => {
    const res = await fetch(`${API}/budget`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ salary }),
    });

    const data = await res.json();
    setResult(data);
  };

  return (
    <>
      <Navbar />
      <div className="container">
        <h2>💰 Budget Planner</h2>

        <input
          type="number"
          placeholder="Enter Salary"
          onChange={(e) => setSalary(e.target.value)}
        />

        <button onClick={calculate}>Calculate</button>

        {result && (
          <div className="card">
            <p>Recommended Rent: ₹{result.recommended_rent}</p>
          </div>
        )}
      </div>
    </>
  );
};

export default Budget;