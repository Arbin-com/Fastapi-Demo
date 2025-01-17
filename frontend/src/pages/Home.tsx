import React, { useState, useEffect, useCallback } from "react";
import Dropdown from "../components/Dropdown";
import Button from "../components/Button";
import InputField from "../components/InputField";
import {
  fetchFiles,
  fetchChannels,
  logout,
  startChannel,
  assignSchedule,
  stopChannel,
  fetchData,
} from "../api";
import {
  AssignScheduleRequest,
  StartChannelRequest,
  StopChannelRequest,
} from "../api/types";
import { useNavigate } from "react-router";
import DynamicLineChart from "../components/LineChart";

const Home: React.FC = () => {
  const [files, setFiles] = useState<{ value: string }[]>([]);
  const [selectedFile, setSelectedFile] = useState<string>("");
  const [channels, setChannels] = useState<{ value: string; status: number }[]>(
    []
  );
  const [selectedChannel, setSelectedChannel] = useState<string>("");
  const [testName, setTestName] = useState<string>("test_demo");
  const [isLoading, setIsLoading] = useState<boolean>();
  const [canStart, setCanStart] = useState<boolean>(true);
  const [isFetchingData, setIsFetchingData] = useState<boolean>(false);

  const [dataPoints, setDataPoints] = useState<
    {
      channel_index: number;
      test_time: number;
      step_time: number;
      voltage: number;
      current: number;
      temp: any;
    }[]
  >([]);

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
          ({ value, status }: { value: string; status: number }) => {
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

  const fetchDataPoints = useCallback(async () => {
    console.log(
      "Fetching data for channel",
      selectedChannel,
      " at ",
      new Date().toISOString()
    );
    try {
      console.log(
        `Now the channle is ${selectedChannel}, number version is ${Number(
          selectedChannel
        )}`
      );
      const response = await fetchData(Number(selectedChannel));
      console.log(`The selected channel is ${selectedChannel}`);
      if (response.success) {
        const newPoints = response.feedback
          .filter((item: any) => item.channel_index === Number(selectedChannel))
          .map((item: any) => ({
            channel_index: item.channel_index,
            test_time: item.test_time,
            step_time: item.step_time,
            voltage: item.voltage,
            current: item.current,
            temp: item.temp,
          }));

        console.log("In this round, new Points is ", newPoints);
        setDataPoints((prev) => {
          const updated = [...prev, ...newPoints];
          // console.log("This is updated result", updated);
          return updated.length > 10
            ? updated.slice(updated.length - 10)
            : updated;
        });
      } else {
        console.error("Load data failed", response.error);
        alert(`Load data error: ${response.message}`);
      }
    } catch (err) {
      console.error("Failed to fetch data points:", err);
    }
  }, [selectedChannel]);

  useEffect(() => {
    let interval: ReturnType<typeof setInterval> | null = null;

    if (isFetchingData) {
      interval = setInterval(fetchDataPoints, 1000); //get data points every second
    }

    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [isFetchingData]);

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
      console.error(
        "An unexpected error occurred during assign schedules: ",
        err
      );
    } finally {
      setIsLoading(false);
    }
  };

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
        setIsFetchingData(true);
      } else {
        console.error("Start channel failed", response.error);
        alert(`Start channel error: ${response.message}`);
      }
    } catch (err) {
      console.error("An unexpected error occurred", err);
    }
  };

  const handleStop = async () => {
    const requestData: StopChannelRequest = {
      channel_index: Number(selectedChannel),
      is_stop_all: false,
    };

    try {
      const response = await stopChannel(requestData);
      if (response.success) {
        console.log("Stop channel successfully.");
        setCanStart(true);
        setIsFetchingData(false);
      } else {
        console.error("Failed to stop channel", response.error);
        alert(`Failed to stop channel, ${response.message}`);
      }
    } catch (err) {
      console.error("An unexpected error occurred", err);
    }
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
      alert("An unexpected error occurred. Please try again later.");
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
          <label>Choose Channel:</label>
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

        <div className="mb-4 w-full max-w-lg">
          <label>Input test name</label>
          <InputField
            value={testName}
            placeholder="Input test name"
            onChange={setTestName}
          />
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

        <div className="w-full flex justify-between gap-4">
          <div className="flex-1 border-2 border-dashed border-gray-300 p-4">
            <DynamicLineChart
              title="Voltage"
              data={dataPoints.map((point) => ({
                test_time: point.test_time,
                value: point.voltage,
              }))}
              color="rgba(75, 192, 192, 1)"
            />
          </div>
          <div className="flex-1 border-2 border-dashed border-gray-300 p-4">
            <DynamicLineChart
              title="Current"
              data={dataPoints.map((point) => ({
                test_time: point.test_time,
                value: point.current,
              }))}
              color="rgba(192, 75, 192, 1)"
            />
          </div>
          <div className="flex-1 border-2 border-dashed border-gray-300 p-4">
            <DynamicLineChart
              title="Temperature"
              data={dataPoints.map((point) => ({
                test_time: point.test_time,
                value: point.temp,
              }))}
              color="rgba(192, 192, 75, 1)"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
