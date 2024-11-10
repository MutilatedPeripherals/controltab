<script lang="ts">
  import { push } from "svelte-spa-router";
  import { useFetchSongs } from "../queries/getSongsQuery";
  import { useDeleteSong } from "../mutations/deleteSongMutation";
  import toast from "svelte-french-toast";
  import type { Song } from "../types/Song";
  import AddSongForm from "../components/AddSongForm.svelte";

  let data: Song[] | undefined;
  let isLoading = false;
  let isError = false;
  let error: Error | null = null;
  let showDeleteDialog = false;
  let selectedSongId: number | null = null;
  let selectedSongTitle = "";

  const songsQuery = useFetchSongs();
  $: ({ data, isLoading, isError, error } = $songsQuery);

  const deleteSongMutation = useDeleteSong();

  function viewTab(id: number) {
    push(`/tabs/${id}`);
  }

  function suggestChange(id: number) {
    console.log("Suggesting a change for tab with id:", id);
    push(`/tabs/${id}/compare`);
  }

  function handleSongAdded() {
    $songsQuery.refetch();
  }

  function confirmDeleteSong(id: number, title: string) {
    selectedSongId = id;
    selectedSongTitle = title;
    showDeleteDialog = true;
  }

  function removeSong() {
    if (selectedSongId !== null) {
      $deleteSongMutation.mutate(selectedSongId, {
        onSuccess: () => {
          toast.success(`"${selectedSongTitle}" deleted successfully.`);
          $songsQuery.refetch();
          closeDeleteDialog();
        },
        onError: () => {
          toast.error(
            `Failed to delete "${selectedSongTitle}". Please try again.`
          );
          closeDeleteDialog();
        },
      });
    }
  }

  function closeDeleteDialog() {
    showDeleteDialog = false;
    selectedSongId = null;
    selectedSongTitle = "";
  }
</script>

<div class="container mx-auto p-6 bg-base-200 min-h-screen rounded-lg">
  <h1 class="text-3xl font-semibold text-center mb-4 text-gray-800">
    Your songs
  </h1>

  <AddSongForm on:songAdded={handleSongAdded} />

  {#if isLoading}
    <p class="text-center text-gray-500">Loading songs...</p>
  {:else if isError}
    <p class="text-center text-red-500">
      Failed to load songs: {error?.message}
    </p>
  {:else if data}
    <div class="grid gap-6">
      {#each data as song (song.id)}
        <div class="card bg-base-100 shadow-lg p-4 rounded-lg">
          <div class="card-body">
            <h2 class="card-title text-lg font-medium text-gray-800">
              {song.title}
            </h2>
            <p class="text-sm text-gray-600">
              Tab filename: {song.tab.filename}
            </p>
            <p class="text-sm text-gray-600">
              Uploaded at: {new Date(song.tab.uploaded_at).toLocaleString()}
            </p>
            <div class="mt-4 flex justify-end space-x-4">
              <button
                class="btn btn-outline btn-primary btn-sm"
                on:click={() => viewTab(song.tab.id)}
              >
                View Tab
              </button>
              <button
                class="btn btn-outline btn-secondary btn-sm"
                on:click={() => suggestChange(song.tab.id)}
              >
                Suggest a Change
              </button>
              <button
                class="btn btn-outline btn-error btn-sm"
                on:click={() => confirmDeleteSong(song.id, song.title)}
              >
                Remove Song
              </button>
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}

  <!-- Delete Confirmation Modal -->
  {#if showDeleteDialog}
    <div class="modal modal-open">
      <div class="modal-box">
        <h3 class="font-bold text-lg">Confirm Deletion</h3>
        <p class="py-4">
          Are you sure you want to delete "{selectedSongTitle}"?
        </p>
        <div class="modal-action">
          <button class="btn btn-error" on:click={removeSong}>Delete</button>
          <button class="btn" on:click={closeDeleteDialog}>Cancel</button>
        </div>
      </div>
    </div>
  {/if}
</div>
