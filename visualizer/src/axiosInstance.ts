// src/axiosInstance.ts
import axios from "axios";
import { get } from "svelte/store";
import { token } from "./mutations/loginMutation";

// Create an Axios instance
const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// Add a request interceptor to include the token in the Authorization header
axiosInstance.interceptors.request.use((config) => {
  const accessToken = get(token); // Retrieve the token from the store
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
});

export default axiosInstance;
