import axios from "axios";
import { get } from "svelte/store";
import { token } from "./mutations/loginMutation";

// Determine the base URL based on the environment
const baseURL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
console.log("vite api bvase url", import.meta.env.VITE_API_BASE_URL)
// Create an Axios instance
const axiosInstance = axios.create({
  baseURL,
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