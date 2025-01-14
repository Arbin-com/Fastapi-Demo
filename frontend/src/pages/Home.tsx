import React, { useState, useEffect } from "react";
import Dropdown from "../components/Dropdown";
import Button from "../components/Button";
import InputField from "../components/InputField";
import {
  fetchFiles,
  fetchChannels,
  logout,
  startChannel,
  assignSchedule,
} from "../api";
import { AssignScheduleRequest, StartChannelRequest } from "../api/types";
import { useNavigate } from "react-router";

const Home: React.FC = () => {
  const [files, setFiles] = useState<{ value: string }[]>([]);
  const [selectedFile, setSelectedFile] = useState<string>("");
  const [channels, setChannels] = useState<{ value: string; status: string }[]>(
    []
  );
  const [selectedChannel, setSelectedChannel] = useState<string>("");
  const [testName, setTestName] = useState<string>("TestTest");
  const [isLoading, setIsLoading] = useState<boolean>();
  const [canStart, setCanStart] = useState<boolean>(true);
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

  const handleStart = async () => {
    const requestData: StartChannelRequest = {
      test_name: testName,
      channels: [Number(selectedChannel)],
    };

    try {
      const response = await startChannel(requestData);
      if (response.success) {
        console.log("start the channel successfully.");
        setCanStart(false);
      } else {
        console.error("Start channel failed", response.error);
        alert(`Start channel error: ${response.message}`);
      }
    } catch (err) {
      console.error("An unexpected error occurred", err);
    }
  };

  const handleAssign = async () => {
    if (!selectedFile) {
      alert("Please select a schedule file first!");
      return;
    }
    if (!selectedChannel) {
      alert("Please select a channel to assign schedule!");
      return;
    }

    const requestData: AssignScheduleRequest = {
      schedule_name: selectedFile,
      channel_index: Number(selectedChannel),
    };

    setIsLoading(true);
    try {
      const response = await assignSchedule(requestData);
      if (response.success) {
        setIsLoading(false);
        console.log("Assign File successfully.");
      } else {
        console.error("Failed to assign schedule.", response.error);
        alert(`Failed to assign schedule: ${response.message}`);
      }
    } catch (err) {
      console.error("An unexpected error occurred", err);
    }
  };

  const handleStop = () => {};

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
          <label>Input test name</label>
          <InputField
            value={testName}
            placeholder="Input test name"
            onChange={setTestName}
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

        <div className="mb-4 w-full max-w-lg">
          <label>Choose schedule file:</label>
          <div className="flex items-center gap-4">
            <Dropdown
              options={files}
              selected={selectedFile}
              onChange={setSelectedFile}
              disabled={isLoading}
            />
            <Button
              onClick={handleAssign}
              label={"assign"}
              disabled={isLoading || !selectedFile}
            />
          </div>
        </div>

        <div className="mb-6 flex gap-10">
          <Button
            onClick={handleStart}
            label={"start"}
            disabled={isLoading || !canStart}
          />
          <Button
            onClick={handleStop}
            label={"stop"}
            disabled={isLoading || canStart}
          />
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
