export type SetlistItem = {
  id: string;
  type: "song" | "sample" | "break" | "speech";
  title: string;
  notes?: string;
};
