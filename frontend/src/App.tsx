import React from "react";
import Home from "./pages/Home";
import { Routes, Route, Navigate } from "react-router";
import LoginPage from "./pages/LoginPage";

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path="login" element={<LoginPage />} />
      <Route path="home" element={<Home />} />
    </Routes>
  );
};

export default App;
