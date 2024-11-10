import { createMutation, useQueryClient } from "@tanstack/svelte-query";
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

      const response = await fetch("http://127.0.0.1:8000/songs", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to create song");
      }

      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["songs"] });
    },
  });
}
