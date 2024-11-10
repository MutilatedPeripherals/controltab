<script lang="ts">
  import { useCreateSong } from "../mutations/createSongMutation";
  import toast, { Toaster } from "svelte-french-toast";

  let newSongTitle = "";
  let selectedFile: File | null = null;
  let errorMessage = "";

  const createSongMutation = useCreateSong();

  function handleFileChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const file = target.files ? target.files[0] : null;
    if (file && file.name.endsWith(".gp")) {
      selectedFile = file;
      errorMessage = "";
    } else {
      selectedFile = null;
      errorMessage = "Please upload a valid .gp file.";
    }
  }

  function addSong() {
    if (!newSongTitle || !selectedFile) {
      errorMessage = "Please provide a title and select a valid .gp file.";
      return;
    }

    $createSongMutation.mutate(
      { title: newSongTitle, tabFile: selectedFile },
      {
        onSuccess: () => {
          newSongTitle = "";
          selectedFile = null;
          errorMessage = "";

          toast.success("Song added successfully!");
        },
        onError: (error) => {
          console.error("Error adding song:", error);

          toast.error("Failed to add song. Please try again.");
        },
      }
    );
  }
</script>

<div class="flex flex-col items-center mb-6">
  <input
    type="text"
    placeholder="Song title"
    bind:value={newSongTitle}
    class="input input-bordered w-full max-w-xs mb-2"
  />
  <input
    type="file"
    accept=".gp"
    on:change={handleFileChange}
    class="file-input file-input-bordered w-full max-w-xs mb-2"
  />
  {#if errorMessage}
    <p class="text-red-500 text-sm mb-2">{errorMessage}</p>
  {/if}
  <button
    class="btn btn-primary"
    on:click={addSong}
    disabled={$createSongMutation.isPending}
  >
    {#if $createSongMutation.isPending}Adding...{:else}Add Song{/if}
  </button>
</div>
