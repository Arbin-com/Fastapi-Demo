import React, { useState, useEffect } from "react";
import Dropdown from "../components/Dropdown";
import Button from "../components/Button";
import InputField from "../components/InputField";
import { fetchFiles, startProcess, logout } from "../api";
import { useNavigate } from "react-router";

const Home: React.FC = () => {
  const [files, setFiles] = useState<{ value: string }[]>([]);
  const [selectedFile, setSelectedFile] = useState<string>("");
  const [channels, setChannels] = useState<{ value: string; status: string }[]>(
    []
  );
  const [selectedChannel, setSelectedChannel] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<string>("");

  const navigate = useNavigate();

  useEffect(() => {
    fetchFiles()
      .then((data: string[]) => {
        setFiles(data.map((file) => ({ value: file, label: file })));
      })
      .catch((error) => console.error("Fetch files error", error));
  }, []);

  const handleStart = () => {
    // if (!selectedFile || !selectedChannel) {
    //   alert("Please choose schedule file and input channel id");
    // }
    // startProcess(selectedFile, selectedChannel)
    //   .then((data) => setResult(data.message))
    //   .catch((error) => console.error("Error start channel:", error));
  };

  const handleLogout = async () => {
    try {
      setLoading(true);
      logout();
      navigate("/login");
    } catch (error) {
      console.error("Logout failed:", error);
    } finally {
      setLoading(false);
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
          <label className="">Choose Channel</label>
          <Dropdown
            options={channels}
            selected={selectedChannel}
            onChange={setSelectedChannel}
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
