import React, { useState, useEffect } from "react";
import Dropdown from "../components/Dropdown";
import Button from "../components/Button";
import InputField from "../components/InputField";
import { fetchFiles, startProcess, logout } from "../api";
import { useNavigate } from "react-router";

const Home: React.FC = () => {
  const [files, setFiles] = useState<string[]>([]);
  const [selectedFile, setSelectedFile] = useState<string>("");
  const [channelId, setChannelId] = useState<string>("");
  const [result, setResult] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const navigate = useNavigate();

  useEffect(() => {
    fetchFiles()
      .then((data) => setFiles(data))
      .catch((error) => console.error("Fetch scheduel file error", error));
  }, []);

  const handleStart = () => {
    if (!selectedFile || !channelId) {
      alert("Please choose schedule file and input channel id");
    }

    startProcess(selectedFile, channelId)
      .then((data) => setResult(data.message))
      .catch((error) => console.error("Error start channel:", error));
  };

  const handleLogout = async () => {
    try {
      //await logout();
      navigate("/login");
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <div className="relative">
      <div className="absolute top-0 right-0">
        <button
          onClick={handleLogout}
          className="bg-gray-100 text-gray-700 px-4 py-2 mr-5 rounded-tl-lg border-b-2 border-gray-300 hover:bg-gray-200"
        >
          Sign out
        </button>
      </div>

      <div className="mt-5 flex flex-col items-center p-6">
        <h1 className="text-2xl font-bold mb-4 mt-5">CTI Demo</h1>
        <div className="mb-4 w-full max-w-lg">
          <label>Choose schedule file:</label>
          <Dropdown
            options={files}
            selected={selectedFile}
            onChange={setSelectedFile}
          />
        </div>
        <div className="mb-4 w-full max-w-lg">
          <label className="">Input Channel Id:</label>
          <InputField
            value={channelId}
            placeholder={"Please input channel id"}
            onChange={setChannelId}
          />
        </div>
        <div className="mb-6">
          <Button onClick={handleStart} label={"start"} disabled={loading} />
        </div>

        <div
          className="w-full max-w-lg h-64 border-2 border-dashed border-gray-300 flex items-center justify-center"
          style={{ backgroundColor: "#f9f9f9" }}
        >
          <span className="text-gray-500">Placeholder for future drawing</span>
        </div>
      </div>
    </div>
  );
};

export default Home;
