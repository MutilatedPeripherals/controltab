<script lang="ts">
  import { push } from "svelte-spa-router";
  import { useFetchSongs } from "../queries/getSongsQuery";
  import { writable, derived } from "svelte/store";

  // Import Shadcn components
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Card, CardContent } from "$lib/components/ui/card";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu";

  import {
    Calendar,
    FileText,
    MoreHorizontal,
    Music,
    Search,
    MessageSquare,
  } from "lucide-svelte";
  import type { Song } from "../types/Song";
  import AddSongDialog from "../components/AddSongDialog.svelte";
  import { formatDate } from "$lib/utils";
  import DeleteSongDialog from "../components/DeleteSongDialog.svelte";
  import { Switch } from "$lib/components/ui/switch";
  import SongCard from "../components/SongCard.svelte";

  const songsQuery = useFetchSongs();
  const searchTerm = writable("");

  const filteredSongs = derived(
    [songsQuery, searchTerm],
    ([$songsQuery, $searchTerm]) =>
      $songsQuery.data?.filter((song) =>
        song.title.toLowerCase().includes($searchTerm.toLowerCase())
      ) || []
  );

  let selectedSongId = writable<number | null>(null);
  let selectedSongTitle = writable<string>("");

  function confirmDelete(song: Song) {
    selectedSongId.set(song.id);
    selectedSongTitle.set(song.title);
    deleteDialogOpen.set(true);
  }

  let deleteDialogOpen = writable(false);

  function handleAction(action: string, song: Song) {
    switch (action) {
      case "open":
        push(`/tabs/${song.id}`);
        break;
      case "export":
        console.log(`Exporting ${song.title} as PDF`);
        break;
      case "suggest":
        push(`/tabs/${song.id}/compare`);
        break;
    }
  }
</script>

<div class="container mx-auto p-4">
  <h1 class="text-3xl font-bold mb-6 text-center">Dashboard</h1>

  <!-- Search input -->
  <div class="flex items-center mb-6">
    <Search class="w-5 h-5 mr-2 text-gray-500" />
    <Input
      type="text"
      placeholder="Search songs..."
      bind:value={$searchTerm}
      class="max-w-sm"
    />
    <div class="ml-auto flex items-center mr-4 gap-1">
      <Switch></Switch>
      <p>Setlist Mode</p>
    </div>

    <AddSongDialog />
  </div>

  <!-- Song Cards -->
  {#if $songsQuery.isLoading}
    <p class="text-center text-gray-500">Loading songs...</p>
  {:else if $songsQuery.isError}
    <p class="text-center text-red-500">
      Failed to load songs: {$songsQuery.error?.message}
    </p>
  {:else}
    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {#each $filteredSongs as song (song.id)}
        <SongCard {song} {handleAction} {confirmDelete} />
      {/each}
    </div>
  {/if}
</div>

<DeleteSongDialog
  bind:open={deleteDialogOpen}
  songId={$selectedSongId}
  songTitle={$selectedSongTitle}
/>
