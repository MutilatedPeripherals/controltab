import { createQuery } from "@tanstack/svelte-query";
import axiosInstance from "../axiosInstance";
import type { Song } from "../types/Song";

export function useFetchSongs() {
  return createQuery<Song[], Error>({
    queryKey: ["songs"],
    queryFn: async () => {
      const response = await axiosInstance.get("/songs");
      return response.data;
    },
    enabled: true,
  });
}
