import axios from "axios";

const BASE_URL = "http://localhost:8000"; //the fastapi frontend

export const fetchFiles = async (): Promise<string[]> => {
  const response = await axios.get(`${BASE_URL}/files`);
  return response.data;
};

export const startProcess = async (
  file: string,
  channel: string
): Promise<{ message: string }> => {
  const response = await axios.post(`${BASE_URL}/start`, { file, channel });
  return response.data;
};

export const login = async (
  username: string,
  password: string
): Promise<string> => {
  const response = await axios.post(`${BASE_URL}/login`, {
    username,
    password,
  });
  return response.data;
};

export const logout = async () => {
  try {
    const response = await axios.post("/logout");
    return response.data;
  } catch (error) {
    console.error("Logout API error", error);
    throw error;
  }
};
