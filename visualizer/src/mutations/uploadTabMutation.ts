// src/mutations/uploadTabMutation.ts
import { createMutation } from "@tanstack/svelte-query";
import axiosInstance from "../axiosInstance";

export interface CompareResponse {
  comparison_result: number[];
  original_file_url: string;
  uploaded_file_url: string;
}

export function useUploadTab(tabId: number) {
  return createMutation<CompareResponse, Error, FormData>({
    mutationFn: async (formData: FormData) => {
      const response = await axiosInstance.post(`/compare/${tabId}`, formData, {
        transformRequest: [(data) => data],
      });

      return response.data;
    },
  });
}
