export type SetlistItem =
  | {
      id?: string;
      type: "song";
      songId: number | null;
      notes?: string;
      order: number;
    }
  | {
      id?: string;
      type: "sample" | "break" | "speech";
      title: string;
      notes?: string;
      order: number;
    };
