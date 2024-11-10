// src/mutations/deleteSongMutation.ts
import { createMutation, useQueryClient } from "@tanstack/svelte-query";

export function useDeleteSong() {
  const queryClient = useQueryClient();

  return createMutation<void, Error, number>({
    mutationFn: async (songId: number) => {
      const response = await fetch(`http://127.0.0.1:8000/songs/${songId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("Failed to delete song");
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["songs"] });
    },
  });
}
