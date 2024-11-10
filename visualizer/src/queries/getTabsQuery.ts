import { createQuery } from "@tanstack/svelte-query";
import type { Tab } from "../types/TabTypes";

export function useFetchTabs() {
  return createQuery<Tab[], Error>({
    queryKey: ["tabs"],
    queryFn: async () => {
      const response = await fetch("http://127.0.0.1:8000/tabs");
      if (!response.ok) {
        throw new Error("Failed to fetch tabs");
      }
      return response.json();
    },
  });
}
