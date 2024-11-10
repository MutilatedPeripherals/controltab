import { createMutation } from "@tanstack/svelte-query";

export interface CompareResponse {
  comparison_result: number[];
  original_file_url: string;
  uploaded_file_url: string;
}

export function useUploadTab(tabId: number) {
  return createMutation<CompareResponse, Error, FormData>({
    mutationFn: async (formData: FormData) => {
      const response = await fetch(`http://127.0.0.1:8000/compare/${tabId}`, {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        throw new Error("File upload failed");
      }
      return response.json();
    },
  });
}
