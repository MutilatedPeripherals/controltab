export type SetlistItem =
  | {
      id?: string;
      type: "song";
      songId: number | null;
      notes?: string;
    }
  | {
      id?: string;
      type: "sample" | "break" | "speech";
      title: string;
      notes?: string;
    };
