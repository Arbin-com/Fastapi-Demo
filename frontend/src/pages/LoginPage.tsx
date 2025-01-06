import React, { useState } from "react";
import { useNavigate } from "react-router";
import { login } from "../api";
import { logout } from "../api";
import InputField from "../components/InputField";
import Button from "../components/Button";

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      // const token = await login(username, password);
      // localStorage.setItem("token", token);
      navigate("/home");
    } catch (err) {
      setError("please check your username and password");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-6 rounded shadow-md w-96 flex flex-col items-center justify-center">
        <h1 className="text-2xl font-bold mb-4 text-center">
          Welcome to CTI demo
        </h1>

        <div className="mb-4 w-full">
          <InputField
            value={username}
            onChange={setUsername}
            placeholder="username"
          />
        </div>

        <div className="mb-4 w-full">
          <InputField
            type="password"
            value={password}
            onChange={setPassword}
            placeholder="password"
          />
        </div>
        <Button onClick={handleLogin} label="Sign In" />
      </div>
    </div>
  );
};

export default LoginPage;
