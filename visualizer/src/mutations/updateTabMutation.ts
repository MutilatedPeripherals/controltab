import { createMutation, useQueryClient } from "@tanstack/svelte-query";

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
      const response = await fetch(
        `http://127.0.0.1:8000/songs/${songId}/confirm-changes`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ uploaded_file_url: uploadedFileUrl }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to confirm tab changes");
      }

      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["songs"] });
    },
  });
}
