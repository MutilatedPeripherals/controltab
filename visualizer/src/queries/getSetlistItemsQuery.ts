// src/queries/useFetchSetlistItems.ts
import { createQuery } from "@tanstack/svelte-query";
import axiosInstance from "../axiosInstance";
import type { SetlistItem } from "../types/SetlistItem";

export function useFetchSetlistItems() {
  return createQuery<SetlistItem[], Error>({
    queryKey: ["setlist_items"],
    queryFn: async () => {
      const response = await axiosInstance.get("/setlist_items");

      const setlistItems: SetlistItem[] = response.data.map((item: any) => {
        if (item.type === "song") {
          return {
            id: item.id,
            type: "song",
            songId: item.song_id,
            notes: item.notes,
          };
        } else {
          return {
            id: item.id,
            type: item.type,
            title: item.title,
            notes: item.notes,
          };
        }
      });

      return setlistItems;
    },
    enabled: true,
  });
}
