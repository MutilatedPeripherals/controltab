<script lang="ts">
  import { push } from "svelte-spa-router";
  import { Input } from "$lib/components/ui/input";

  import { Search } from "lucide-svelte";
  import type { Song } from "../../types/Song";
  import AddSongDialog from "../../components/AddSongDialog.svelte";
  import SongCard from "./SongCard.svelte";
  import DeleteSongDialog from "../../components/DeleteSongDialog.svelte";
  import { useFetchSongs } from "../../queries/getSongsQuery";

  const songsQuery = useFetchSongs();

  let searchTerm = $state("");
  let selectedSongId = $state<number | null>(null);
  let selectedSongTitle = $state("");
  let deleteDialogOpen = $state(false);

  const filteredSongs = $derived(
    () =>
      $songsQuery.data?.filter((song) =>
        song.title.toLowerCase().includes(searchTerm.toLowerCase())
      ) || []
  );

  function confirmDelete(song: Song) {
    selectedSongId = song.id;
    selectedSongTitle = song.title;
    deleteDialogOpen = true;
  }

  function handleAction(action: string, song: Song) {
    switch (action) {
      case "open":
        push(`/songs/${song.id}`);
        break;
      case "export":
        if (import.meta.env.VITE_DEBUG) {
          console.log(`Exporting ${song.title} as PDF`);
        }
        break;
      case "suggest":
        push(`/songs/${song.id}/compare`);
        break;
    }
  }
</script>

<div class="container mx-auto p-4">
  <h1 class="text-3xl font-bold mb-6 text-center">Songs</h1>

  <div class="flex items-center mb-6">
    <Search class="w-5 h-5 mr-2 text-gray-500" />
    <Input
      type="text"
      placeholder="Search songs..."
      bind:value={searchTerm}
      class="max-w-sm"
    />

    <AddSongDialog />
  </div>

  {#if $songsQuery.isLoading}
    <p class="text-center text-gray-500">Loading songs...</p>
  {:else if $songsQuery.isError}
    <p class="text-center text-red-500">
      Failed to load songs: {$songsQuery.error?.message}
    </p>
  {:else}
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {#each filteredSongs() as song (song.id)}
        <SongCard {song} {handleAction} {confirmDelete} />
      {/each}
    </div>
  {/if}
</div>

<DeleteSongDialog
  bind:open={deleteDialogOpen}
  songId={selectedSongId}
  songTitle={selectedSongTitle}
/>
