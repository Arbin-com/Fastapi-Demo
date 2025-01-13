import axios from "axios";

const BASE_URL = "http://127.0.0.1:8080"; //the fastapi url

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
    return response.data.files;
  } catch (error) {
    console.error("Failed to fetch schedule files:", error);
    throw error;
  }
};

export const startProcess = async () => {};
