import React, { useState, useEffect } from "react";
import Dropdown from "../components/Dropdown";
import Button from "../components/Button";
import InputField from "../components/InputField";
import { fetchFiles, fetchChannels, logout } from "../api";
import { useNavigate } from "react-router";

const Home: React.FC = () => {
  const [files, setFiles] = useState<{ value: string }[]>([]);
  const [selectedFile, setSelectedFile] = useState<string>("");
  const [channels, setChannels] = useState<{ value: string; status: string }[]>(
    []
  );
  const [selectedChannel, setSelectedChannel] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>();
  const [result, setResult] = useState<string>("");

  const navigate = useNavigate();
  const loadFiles = async () => {
    try {
      const response = await fetchFiles();
      console.log("The response for load files is ", response);
      if (response.success) {
        const file_list: { value: string }[] = [];
        for (const file of response.files) {
          console.log("The file is", file);
          file_list.push({ value: file });
          console.log("The file list is", file_list);
        }
        setFiles(file_list);
      } else {
        console.error("Load Files failed.", response.error);
        alert(`Load File Error: ${response.message}`);
      }
    } catch (err) {
      console.error("An unexpected error occurred", err);
      alert("Failed to fetch schedule files, please try again later.");
    }
  };

  const loadChannels = async () => {
    try {
      const response = await fetchChannels();
      console.log("The response for fetching files is: ", response);
      if (response.success) {
        const channel_list = response.feedback.map(
          ({ value, status }: { value: string; status: string }) => {
            return { value, status };
          }
        );
        console.log("The schedule result is", channel_list);
        setChannels(channel_list);
      } else {
        console.error("Load channel failed", response.error);
        alert(`Load channel error: ${response.message}`);
      }
    } catch (err) {
      console.error("An unexpected error occurred", err);
    }
  };

  useEffect(() => {
    const initializeApp = async () => {
      try {
        setIsLoading(true);
        await Promise.all([loadFiles(), loadChannels()]);
      } catch (err) {
        console.log("An error occurred during initialization", err);
        alert("Initialization failed, please try again.");
      } finally {
        setIsLoading(false);
      }
    };

    initializeApp();
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
      setIsLoading(true);
      const response = await logout();
      if (response.success) {
        console.log(response.message);
        navigate("/login");
      } else {
        alert(response.message);
      }
    } catch (error) {
      console.error("Logout failed:", error);
      alert("An unexpected error occured. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative">
      {isLoading && (
        <div className="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center z-50">
          <div className="text-white text-lg">Processing...</div>
        </div>
      )}
      <div className="absolute top-0 right-0">
        <button
          onClick={handleLogout}
          disabled={isLoading}
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
            disabled={isLoading}
          />
        </div>
        <div className="mb-4 w-full max-w-lg">
          <label className="">Choose Channel</label>
          <Dropdown
            options={channels}
            selected={selectedChannel}
            onChange={setSelectedChannel}
            disabled={isLoading}
          />
        </div>
        <div className="mb-6">
          <Button onClick={handleStart} label={"start"} disabled={isLoading} />
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
