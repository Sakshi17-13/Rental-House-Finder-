import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale);

const API = "http://127.0.0.1:5000";

const Analytics = () => {
  const [data, setData] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(`${API}/analytics`);
        const result = await res.json();
        setData(result);
      } catch (err) {
        console.error("Error loading analytics:", err);
      }
    };

    fetchData();
  }, []);

  const chartData = {
    labels: Object.keys(data),
    datasets: [
      {
        label: "Average Rent",
        data: Object.values(data),
      },
    ],
  };

  return (
    <>
      <Navbar />
      <div className="container">
        <h2>📊 Analytics</h2>

        {/* Prevent empty render crash */}
        {Object.keys(data).length > 0 ? (
          <Bar data={chartData} />
        ) : (
          <p>Loading...</p>
        )}
      </div>
    </>
  );
};

export default Analytics;