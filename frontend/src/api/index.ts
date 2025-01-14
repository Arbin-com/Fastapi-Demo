import axios from "axios";
import { StartChannelRequest } from "./types";

const BASE_URL = "http://127.0.0.1:8000"; //the fastapi url

export const login = async (
  username: string,
  password: string,
  ipaddress?: string
) => {
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

export const startChannel = async (data: StartChannelRequest) => {
  try {
    const response = await axios.post(`${BASE_URL}/channels/start`, data);
    return response.data;
  } catch (err) {
    console.log("Failed to start channel", err);
    throw err;
  }
};

export const stopChannel = async () => {};

export const assignSchedule = async () => {};
