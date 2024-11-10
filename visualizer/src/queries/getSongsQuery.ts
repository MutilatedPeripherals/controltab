import { createQuery } from "@tanstack/svelte-query";
import type { Tab } from "../types/TabTypes";

export function useFetchSongs() {
  return createQuery<Tab[], Error>({
    queryKey: ["songs"],
    queryFn: async () => {
      const response = await fetch("http://127.0.0.1:8000/songs");
      if (!response.ok) {
        throw new Error("Failed to fetch songs");
      }
      return response.json();
    },
  });
}
