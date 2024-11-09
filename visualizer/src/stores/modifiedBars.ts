import { writable } from "svelte/store";

export const modifiedBars = writable({
  comparison_result: [],
  originalTabUrl: "",
  uploadedTabUrl: "",
});
