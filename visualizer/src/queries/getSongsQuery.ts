// src/queries/useFetchSongs.ts
import { createQuery } from "@tanstack/svelte-query";
import type { Tab } from "../types/Tab";
import axiosInstance from "../axiosInstance";

export function useFetchSongs() {
  return createQuery<Tab[], Error>({
    queryKey: ["songs"],
    queryFn: async () => {
      const response = await axiosInstance.get("/songs");
      return response.data;
    },
    enabled: true, // Only run the query if needed (token is added automatically by interceptor)
  });
}
