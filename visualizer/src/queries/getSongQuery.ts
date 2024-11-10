// queries/fetchTabQuery.ts
import { createQuery } from "@tanstack/svelte-query";
import type { Song } from "../types/Song";

export const useFetchSongData = (songId: number) => {
  return createQuery<Song>({
    queryKey: ["songId", songId],
    queryFn: async () => {
      const response = await fetch(`http://127.0.0.1:8000/songs/${songId}`);
      if (!response.ok) {
        throw new Error("Failed to fetch song data from FastAPI");
      }
      return response.json();
    },
  });
};
