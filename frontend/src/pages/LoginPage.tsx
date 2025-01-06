import React, { useState } from "react";
import { useNavigate } from "react-router";

const LoginPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div>
      <h1>Login Page</h1>
      <button onClick={() => navigate("/home")}>To Home</button>
    </div>
  );
};

export default LoginPage;
