import { writable } from "svelte/store";

interface ModifiedBars {
  songId: number;
  comparison_result: number[];
  originalTabUrl: string;
  uploadedTabUrl: string;
}

export const modifiedBars = writable<ModifiedBars>({
  songId: 0,
  comparison_result: [],
  originalTabUrl: "",
  uploadedTabUrl: "",
});
