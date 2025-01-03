import React, { useState, useEffect } from "react";
import Dropdown from "../components/Dropdown";
import Button from "../components/Button";
import InputField from "../components/InputField";
import { fetchFiles, startProcess } from "../api";

const Home: React.FC = () => {
  const [files, setFiles] = useState<string[]>([]);
  const [selectedFile, setSelectedFile] = useState<string>("");
  const [channelId, setChannelId] = useState<string>("");
  const [result, setResult] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

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

  return (
    <div className="flex flex-col items-center p-6">
      <h1 className="text-2xl font-bold mb-4">CTI Demo</h1>
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
  );
};

export default Home;
