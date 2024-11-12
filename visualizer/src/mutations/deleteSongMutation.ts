import { createMutation, useQueryClient } from "@tanstack/svelte-query";
import axiosInstance from "../axiosInstance";

export function useDeleteSong() {
  const queryClient = useQueryClient();

  return createMutation<void, Error, number>({
    mutationFn: async (songId: number) => {
      await axiosInstance.delete(`/songs/${songId}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["songs"] });
    },
  });
}
