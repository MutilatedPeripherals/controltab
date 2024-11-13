import { createMutation } from "@tanstack/svelte-query";
import { writable } from "svelte/store";

// Store to hold the JWT token globally
const storedToken = localStorage.getItem("token");
export const token = writable<string | null>(storedToken);

// Subscribe to token changes to save to localStorage
token.subscribe((value) => {
  if (value) {
    localStorage.setItem("token", value); // Save token to localStorage
  } else {
    localStorage.removeItem("token"); // Remove token if null
  }
});

// Define the login mutation function
export function useLogin() {
  return createMutation<string, Error, string>({
    mutationFn: async (accessCode: string) => {
      // Prepare the form data with the access code
      const formData = new URLSearchParams();
      formData.append("access_code", accessCode);

      const response = await fetch("http://127.0.0.1:8000/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData.toString(),
      });

      if (!response.ok) {
        throw new Error("Invalid access code. Please try again.");
      }

      const data = await response.json();
      return data.access_token;
    },
    onSuccess: (data) => {
      token.set(data);
    },
    onError: (error) => {
      console.error("Login failed:", error);
    },
  });
}
