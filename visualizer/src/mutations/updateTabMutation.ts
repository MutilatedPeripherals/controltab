import { createMutation, useQueryClient } from "@tanstack/svelte-query";
import axiosInstance from "../axiosInstance";

export function useConfirmTabChange() {
  const queryClient = useQueryClient();

  return createMutation({
    mutationFn: async ({
      songId,
      uploadedFileUrl,
    }: {
      songId: number;
      uploadedFileUrl: string;
    }) => {
      const response = await axiosInstance.put(
        `/songs/${songId}/confirm-changes`,
        {
          uploaded_file_url: uploadedFileUrl,
        }
      );

      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["songs"] });
    },
  });
}
