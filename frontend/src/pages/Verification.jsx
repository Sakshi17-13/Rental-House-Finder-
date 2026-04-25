import { useState } from "react";
import Navbar from "../components/Navbar";

const API = "http://127.0.0.1:5000";

const Verification = () => {
  const [idProof, setIdProof] = useState(null);
  const [propertyProof, setPropertyProof] = useState(null);

  const upload = async () => {
    const formData = new FormData();
    formData.append("id_proof", idProof);
    formData.append("property_proof", propertyProof);

    await fetch(`${API}/upload-documents`, {
      method: "POST",
      body: formData,
    });

    alert("Uploaded! Verification Pending");
  };

  return (
    <>
      <Navbar />
      <div className="container">
        <h2>🪪 Verification</h2>

        <input type="file" onChange={(e) => setIdProof(e.target.files[0])} />
        <input type="file" onChange={(e) => setPropertyProof(e.target.files[0])} />

        <button onClick={upload}>Upload Documents</button>
      </div>
    </>
  );
};

export default Verification;