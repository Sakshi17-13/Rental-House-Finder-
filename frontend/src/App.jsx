import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Analytics from "./pages/Analytics";
import Budget from "./pages/Budget";
import Verification from "./pages/Verification";
import Favorites from "./pages/Favorites";
import ProtectedRoute from "./components/ProtectedRoute";
import Chat from "./pages/Chat";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />

      <Route
        path="/home"
        element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        }
      />

      <Route
        path="/favorites"
        element={
          <ProtectedRoute>
            <Favorites />
          </ProtectedRoute>
        }
      />

      <Route
        path="/analytics"
        element={
          <ProtectedRoute>
            <Analytics />
          </ProtectedRoute>
        }
      />

      <Route
        path="/budget"
        element={
          <ProtectedRoute>
            <Budget />
          </ProtectedRoute>
        }
      />

      <Route
        path="/verify"
        element={
          <ProtectedRoute>
            <Verification />
          </ProtectedRoute>
        }
      />

      <Route path="/chat" element={
        <ProtectedRoute>
          <Chat />
        </ProtectedRoute>
        } 
      />
    </Routes>
  );
}

export default App;