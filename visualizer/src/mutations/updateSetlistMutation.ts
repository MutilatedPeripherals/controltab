import { createMutation, useQueryClient } from "@tanstack/svelte-query";
import axiosInstance from "../axiosInstance";
import type { SetlistItem } from "../types/SetlistItem";

type UpdateSetlistResponse = SetlistItem[];
interface UpdateSetlistVariables {
  setlist: SetlistItem[];
}

// Function to map client-side attributes to server-side attributes
function mapSetlistForServer(setlist: SetlistItem[]) {
  return setlist.map((item) => {
    const { tempId, songId, ...rest } = item;
    return {
      ...rest,
      song_id: songId,
    };
  });
}

export function useUpdateSetlist() {
  const queryClient = useQueryClient();

  return createMutation<UpdateSetlistResponse, Error, UpdateSetlistVariables>({
    mutationFn: async ({ setlist }) => {
      const mappedSetlist = mapSetlistForServer(setlist);

      const response = await axiosInstance.put(
        "/setlist_items/setlist",
        mappedSetlist,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["setlist"] });
    },
  });
}
