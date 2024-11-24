import { createQuery } from "@tanstack/svelte-query";
import axiosInstance from "../axiosInstance";
import type { Band } from "../types/Band";

export const useFetchBandData = () => {
  return createQuery<Band>({
    queryKey: ["band"],
    queryFn: async () => {
      const response = await axiosInstance.get(`/bands/me`);
      return response.data;
    },
  });
};
