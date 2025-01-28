import axios from "axios";
import {
  AssignFileRequest,
  AssignScheduleRequest,
  StartChannelRequest,
  StopChannelRequest,
} from "./types";

//ip address should correspond to the server where the FastAPI is currently running.
const DEFAULT_PORT = 8000;
let BASE_URL =
  sessionStorage.getItem("baseUrl") || `http://127.0.0.1:${DEFAULT_PORT}`;

export const setBaseUrl = (ipaddress: string) => {
  BASE_URL = `http://${ipaddress}:${DEFAULT_PORT}`;
  sessionStorage.setItem("baseUrl", BASE_URL);
};

//function to get base_url
export const getBaseUrl = () => BASE_URL;

// APIs
export const login = async (
  username: string,
  password: string,
  ipaddress?: string
) => {
  console.log("The url is", sessionStorage.getItem("baseUrl"));
  const response = await axios.post(`${BASE_URL}/login`, {
    username,
    password,
    ipaddress,
  });
  return response.data;
};

export const logout = async () => {
  try {
    const response = await axios.post(`${BASE_URL}/logout`);
    console.log("The url is", BASE_URL);
    return response.data;
  } catch (error) {
    console.error("Logout API error", error);
    throw error;
  }
};

export const fetchFiles = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/schedules`);
    console.log("Fetch files as below:");
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error("Failed to fetch schedule files: ", error);
    throw error;
  }
};

export const fetchChannels = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/channels/status`);
    return response.data;
  } catch (error) {
    console.log("Failed to fetch channels: ", error);
    throw error;
  }
};

export const fetchTestObjects = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/test_objects`);
    return response.data;
  } catch (error) {
    console.log("Failed to fetch test objects: ", error);
    throw error;
  }
};

export const assignTO = async (data: AssignFileRequest) => {
  try {
    const response = await axios.post(`${BASE_URL}/test_objects/assign`, data);
    return response.data;
  } catch (err) {
    console.log("Failed to assign file.", err);
    throw err;
  }
};

export const assignSchedule = async (data: AssignScheduleRequest) => {
  try {
    const response = await axios.post(`${BASE_URL}/schedules/assign`, data);
    return response.data;
  } catch (err) {
    console.log("Failed to assign schedules.", err);
    throw err;
  }
};

export const startChannel = async (data: StartChannelRequest) => {
  try {
    const response = await axios.post(`${BASE_URL}/channels/start`, data);
    return response.data;
  } catch (err) {
    console.log("Failed to start channel", err);
    throw err;
  }
};

export const stopChannel = async (data: StopChannelRequest) => {
  try {
    const response = await axios.post(`${BASE_URL}/channels/stop`, data);
    return response.data;
  } catch (err) {
    console.log("Failed to stop channel", err);
    throw err;
  }
};

export const fetchData = async (channel_index: number) => {
  try {
    const response = await axios.get(
      `${BASE_URL}/channels/data/${channel_index}`
    );
    console.log(`Send request to ${BASE_URL}/channels/data/${channel_index}`);
    return response.data;
  } catch (err) {
    console.log("Failed to fetch data", err);
    throw err;
  }
};
