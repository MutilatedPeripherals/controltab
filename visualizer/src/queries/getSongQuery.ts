import { createQuery } from "@tanstack/svelte-query";
import axiosInstance from "../axiosInstance";
import type { Song } from "../types/Song";

export const useFetchSongData = (songId: number) => {
  return createQuery<Song>({
    queryKey: ["songId", songId],
    queryFn: async () => {
      const response = await axiosInstance.get(`/songs/${songId}`);

      return response.data;
    },
  });
};
