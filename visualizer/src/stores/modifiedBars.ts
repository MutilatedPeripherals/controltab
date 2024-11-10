import { writable } from "svelte/store";

interface ModifiedBars {
  comparison_result: number[];
  originalTabUrl: string;
  uploadedTabUrl: string;
}

export const modifiedBars = writable<ModifiedBars>({
  comparison_result: [],
  originalTabUrl: "",
  uploadedTabUrl: "",
});
