import { createMutation, useQueryClient } from "@tanstack/svelte-query";
import axiosInstance from "../axiosInstance"; // Import the axios instance
import type { Song } from "../types/Song";

interface CreateSongResponse extends Song {}
interface CreateSongVariables {
  title: string;
  tabFile: File;
}

export function useCreateSong() {
  const queryClient = useQueryClient();

  return createMutation<CreateSongResponse, Error, CreateSongVariables>({
    mutationFn: async ({ title, tabFile }) => {
      const formData = new FormData();
      formData.append("title", title);
      formData.append("tab_file", tabFile);

      const response = await axiosInstance.post("/songs/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        transformRequest: [(data) => data],
      });

      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["songs"] });
    },
  });
}
