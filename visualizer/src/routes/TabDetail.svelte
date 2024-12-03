<script lang="ts">
  import { tick } from "svelte";
  import { push } from "svelte-spa-router";
  import "@coderline/alphatab";
  import { useFetchSongData } from "../queries/getSongQuery";
  import type { Song } from "../types/Song";
  import { MessageSquare } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";
  import { Checkbox } from "$lib/components/ui/checkbox";

  export let params: { id: number };
  const songId = params.id;

  const songDataQuery = useFetchSongData(songId);
  let container: HTMLDivElement;
  let tabPlayer: AlphaTabApi;
  let currentScore: Score;
  let trackStates: boolean[] = [];
  let tracks: Track[] = [];

  $: if ($songDataQuery.isSuccess) {
    tick().then(() => {
      renderAlphaTabPlayer($songDataQuery.data);
    });
  }

  function renderAlphaTabPlayer(data: Song) {
    if (import.meta.env.VITE_DEBUG) {
      console.log("Rendering AlphaTab player for:", data);
    }
    if (!window.alphaTab) {
      console.error("AlphaTab not loaded");
      return;
    }

    container.innerHTML = "";

    const settings: AlphaTabSettings = {
      file: data.tab.filepath,
      core: {
        engine: "svg",
      },
      display: {
        layoutMode: 0,
      },
    };

    tabPlayer = new window.alphaTab.AlphaTabApi(container, settings);

    tabPlayer.scoreLoaded.on((score) => {
      if (import.meta.env.VITE_DEBUG) {
        console.log("Full Score Loaded:", score);
        console.log("Total Tracks:", score.tracks.length);
      }

      currentScore = score;
      tracks = score.tracks;
      trackStates = new Array(score.tracks.length).fill(true);

      tabPlayer.renderTracks(score.tracks);
    });
  }

  function toggleTrack(index: number) {
    trackStates[index] = !trackStates[index];
    const visibleTracks = tracks.filter((_, i) => trackStates[i]);
    tabPlayer.renderTracks(visibleTracks);
  }

  function suggestChange() {
    push(`/songs/${songId}/compare`);
  }

  function printTab() {
    if (!tabPlayer) {
      console.error("AlphaTab player is not initialized.");
      return;
    }
    tabPlayer.print(undefined, { display: { barsPerRow: 4 } });
    if (import.meta.env.VITE_DEBUG) {
      console.log("Printing the tab...");
    }
  }
</script>

<div class="container mx-auto p-6 bg-base-200 rounded-lg">
  {#if $songDataQuery.isLoading}
    <p class="text-center text-gray-500">Loading tab data...</p>
  {:else if $songDataQuery.isError}
    <p class="text-center text-red-500">Failed to load tab data.</p>
  {:else if $songDataQuery.isSuccess}
    <div class="flex flex-wrap justify-center items-center mb-4 space-x-4">
      {#each tracks as track, index}
        <div class="flex items-center space-x-2">
          <Checkbox
            bind:checked={trackStates[index]}
            onCheckedChange={() => toggleTrack(index)}
            id={`track-${index}`}
          />
          <label
            for={`track-${index}`}
            class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          >
            {track.name || track.shortName || `Track ${index + 1}`}
          </label>
        </div>
      {/each}
    </div>

    <div
      bind:this={container}
      class="flex-1 w-full bg-white border border-gray-300 rounded-lg shadow-md overflow-y-auto h-[42rem] overflow-x-hidden"
    ></div>

    <div class="flex justify-center mt-6 space-x-4">
      <Button on:click={suggestChange} class="flex items-center gap-2">
        <MessageSquare className="w-4 h-4" />
        Suggest a Change
      </Button>
      <Button on:click={printTab} class="flex items-center gap-2">
        Print Tab
      </Button>
    </div>
  {/if}
</div>
