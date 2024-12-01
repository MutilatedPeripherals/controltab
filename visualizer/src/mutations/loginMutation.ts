import axios from "axios";
import { createMutation } from "@tanstack/svelte-query";
import { writable } from "svelte/store";
import axiosInstance from "../axiosInstance";

// Store to hold the JWT token globally
const storedToken = localStorage.getItem("token");
export const token = writable<string | null>(storedToken);

token.subscribe((value) => {
  if (value) {
    localStorage.setItem("token", value);
  } else {
    localStorage.removeItem("token");
  }
});

export function useLogin() {
  return createMutation<string, Error, string>({
    mutationFn: async (accessCode: string) => {
      try {
        const formData = new URLSearchParams();
        formData.append("access_code", accessCode);

        const response = await axiosInstance.post(
          "/token",
          formData,
          {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
          }
        );

        return response.data.access_token;
      } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
          throw new Error("Invalid access code. Please try again.");
        }
        throw new Error("An unexpected error occurred.");
      }
    },
    onSuccess: (data) => {
      token.set(data);
    },
    onError: (error) => {
      console.error("Login failed:", error);
    },
  });
}
