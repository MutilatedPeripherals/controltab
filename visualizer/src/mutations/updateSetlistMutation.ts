import { createMutation, useQueryClient } from "@tanstack/svelte-query";
import axiosInstance from "../axiosInstance";
import type { SetlistItem } from "../types/SetlistItem";

type UpdateSetlistResponse = SetlistItem[];
interface UpdateSetlistVariables {
  setlist: SetlistItem[];
}

function mapSetlistForServer(setlist: SetlistItem[]) {
  console.log("enter", setlist);
  return setlist.map((item) => {
    if (item.type === "song") {
      const { songId, ...rest } = item;
      return {
        ...rest,
        song_id: songId,
      };
    }

    return item;
  });
}

export function useUpdateSetlist() {
  const queryClient = useQueryClient();

  return createMutation<UpdateSetlistResponse, Error, UpdateSetlistVariables>({
    mutationFn: async ({ setlist }) => {
      const mappedSetlist = mapSetlistForServer(setlist);
      console.log(mappedSetlist);
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
