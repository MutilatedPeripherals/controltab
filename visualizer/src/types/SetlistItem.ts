export type SetlistItem =
  | {
      id?: string;
      tempId?: string;
      type: "song";
      songId: number | null;
      notes?: string;
    }
  | {
      id?: string;
      tempId?: string;
      type: "sample" | "break" | "speech";
      title: string;
      notes?: string;
    };
