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
        <Card class="overflow-hidden">
          <CardContent class="p-0">
            <div
              class="flex items-center justify-between p-4 bg-primary text-primary-foreground"
            >
              <div class="flex items-center">
                <Music class="w-5 h-5 mr-2" />
                <h2 class="text-lg font-semibold">{song.title}</h2>
              </div>
              <DropdownMenu.Root>
                <DropdownMenu.Trigger asChild let:builder>
                  <Button
                    variant="ghost"
                    builders={[builder]}
                    class="h-8 w-8 p-0"
                  >
                    <span class="sr-only">Open menu</span>
                    <MoreHorizontal class="h-4 w-4" />
                  </Button>
                </DropdownMenu.Trigger>
                <DropdownMenu.Content align="end">
                  <DropdownMenu.Label>Actions</DropdownMenu.Label>
                  <DropdownMenu.Item
                    on:click={() => handleAction("open", song)}
                  >
                    <FileText class="mr-2 h-4 w-4" />
                    Open Tab
                  </DropdownMenu.Item>
                  <DropdownMenu.Item
                    on:click={() => handleAction("suggest", song)}
                  >
                    <MessageSquare class="mr-2 h-4 w-4" />

                    Suggest Changes
                  </DropdownMenu.Item>
                  <DropdownMenu.Item
                    on:click={() => handleAction("export", song)}
                  >
                    Export as PDF
                  </DropdownMenu.Item>

                  <DropdownMenu.Separator />
                  <DropdownMenu.Item
                    on:click={() => confirmDelete(song)}
                    class="text-red-600"
                  >
                    Delete Song
                  </DropdownMenu.Item>
                </DropdownMenu.Content>
              </DropdownMenu.Root>
            </div>
            <div class="p-4 flex items-center text-muted-foreground">
              <Calendar class="w-4 h-4 mr-2" />
              <span>Last modified: {formatDate(song.tab.uploaded_at)}</span>
            </div>
          </CardContent>
        </Card>
      {/each}
    </div>
  {/if}
</div>

<DeleteSongDialog
  bind:open={deleteDialogOpen}
  songId={$selectedSongId}
  songTitle={$selectedSongTitle}
/>
