import React, { useState } from "react";
import { useNavigate } from "react-router";
import { login } from "../api";
import InputField from "../components/InputField";
import Button from "../components/Button";

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [ipaddress, setIpaddress] = useState("127.0.0.1");
  const [isLoading, setIsLoading] = useState<boolean>();
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      setIsLoading(true);
      const response = await login(username, password);
      console.log("The login response is", response);
      if (response.success) {
        setIsLoading(false);
        navigate("/home");
      } else {
        console.error("Login failed", response.error);
        alert(`Error: ${response.error}`);
      }
    } catch (err) {
      console.error("An unexpected error occurred", err);
      alert("Failed to connect to server, please try again later.");
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
            value={ipaddress}
            onChange={setIpaddress}
            placeholder="ip address"
          />
        </div>

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
        <Button
          onClick={handleLogin}
          disabled={isLoading}
          label={isLoading ? "Logging you in" : "Sign in"}
        />
      </div>
    </div>
  );
};

export default LoginPage;
