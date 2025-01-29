import React, { useState } from "react";
import { useNavigate } from "react-router";
import { setBaseUrl, login } from "../api";
import InputField from "../components/InputField";
import Button from "../components/Button";
import { LoginRequest } from "../api/types";

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [ipaddress, setIpaddress] = useState("");
  const [isLoading, setIsLoading] = useState<boolean>();
  const navigate = useNavigate();

  const validateIpAddress = (value: string) => {
    setIpaddress(value);
    const ipRegex =
      /^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$/;
    console.log(ipRegex.test(value));
    return ipRegex.test(value);
  };

  const handleLogin = async () => {
    try {
      setIsLoading(true);
      if (!validateIpAddress(ipaddress)) {
        alert("Ip Address is not valid.");
      }
      if (username === "") {
        alert("Please input your username.");
      }
      setBaseUrl(ipaddress);
      const requestData: LoginRequest = {
        username: username,
        password: password,
        ipaddress: ipaddress,
      };
      const response = await login(requestData);
      console.log("The login response is", response);
      if (response.success) {
        setIsLoading(false);
        navigate("/home");
      } else {
        console.error("Login failed", response.error);
        alert(`Error: ${response.message}`);
      }
    } catch (err) {
      console.error("An unexpected error occurred", err);
      alert("Failed to connect to server, please try again later.");
    } finally {
      setIsLoading(false);
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
