import { useState } from "react";
import Navbar from "../components/Navbar";

const API = "http://127.0.0.1:5000";

const Chat = () => {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const sendMessage = async () => {
    const res = await fetch(`${API}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    const data = await res.json();
    setChat([...chat, data]);
    setMessage("");
  };

  return (
    <>
      <Navbar />
      <div className="container">
        <h2>💬 Chat</h2>

        <div className="card">
          {chat.map((c, i) => (
            <p key={i}>{c.message}</p>
          ))}
        </div>

        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />

        <button onClick={sendMessage}>Send</button>
      </div>
    </>
  );
};

export default Chat;