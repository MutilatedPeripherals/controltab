<script lang="ts">
  import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
  } from "$lib/components/ui/card";
  import { Music, Mic, Coffee, FileAudio } from "lucide-svelte";
  import { useFetchBandData } from "../../queries/getBandQuery";
  import { useFetchSongs } from "../../queries/getSongsQuery";
  import type { SetlistItem } from "../../types/SetlistItem";

  export let setlist: SetlistItem[] = [];

  const bandQuery = useFetchBandData();
  const songsQuery = useFetchSongs();

  const getSongName = (songId: number | null): string => {
    if (!songId) return "Unknown Song";
    const song = $songsQuery?.data?.find((song) => song.id === songId);
    return song?.title || "Unknown Song";
  };

  const getItemIcon = (type: SetlistItem["type"]) => {
    switch (type) {
      case "song":
        return Music;
      case "sample":
        return FileAudio;
      case "break":
        return Coffee;
      case "speech":
        return Mic;
      default:
        return null;
    }
  };
</script>

<div class="container mx-auto p-4 max-w-2xl print:p-0">
  <div class="text-center mb-8">
    <h1 class="text-3xl font-bold">{$bandQuery.data?.name}</h1>
  </div>

  <div class="space-y-4">
    {#each setlist as item, index}
      <Card class="bg-card print:break-inside-avoid">
        <CardHeader class="flex flex-row items-center space-y-0 pb-2">
          <CardTitle class="text-base font-medium flex items-center">
            <span
              class="w-8 h-8 flex items-center justify-center bg-primary text-primary-foreground rounded-full mr-3"
            >
              {index + 1}
            </span>
            {#if getItemIcon(item.type)}
              <svelte:component this={getItemIcon(item.type)} class="h-4 w-4" />
            {/if}
            <span class="ml-2">
              {item.type === "song"
                ? getSongName(item.songId)
                : item.title || "Untitled"}
            </span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {#if item.notes}
            <p class="text-sm italic">{item.notes}</p>
          {/if}
        </CardContent>
      </Card>
    {/each}
  </div>
</div>
