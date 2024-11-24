<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Label } from "$lib/components/ui/label";
  import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
    DialogTrigger,
  } from "$lib/components/ui/dialog";
  import { Plus } from "lucide-svelte";
  import { useCreateSong } from "../mutations/createSongMutation"; // Adjust path as needed
  import { writable } from "svelte/store";

  // Mutation for creating a new song
  const createSongMutation = useCreateSong();

  // State variables
  let newSongName = writable("");
  let newSongFile: File | null = null;
  let isDragging = false;
  let showAddSongDialog = writable(false);

  // File upload handling
  function handleDragOver(event: DragEvent) {
    event.preventDefault();
    isDragging = true;
  }

  function handleDragLeave() {
    isDragging = false;
  }

  function handleDrop(event: DragEvent) {
    event.preventDefault();
    isDragging = false;
    if (event.dataTransfer?.files.length) {
      newSongFile = event.dataTransfer.files[0];
    }
  }

  function handleFileInput(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
      newSongFile = target.files[0];
    }
  }

  function handleAddSong() {
    if ($newSongName && newSongFile) {
      $createSongMutation.mutate({
        title: $newSongName,
        tabFile: newSongFile,
      });

      // Clear inputs after submitting
      newSongName.set("");
      newSongFile = null;
      showAddSongDialog.set(false);
    }
  }
</script>

<Dialog bind:open={$showAddSongDialog}>
  <DialogTrigger asChild>
    <Button
      on:click={() => showAddSongDialog.set(true)}
      class="flex items-center gap-2 ml-auto"
    >
      <Plus class="w-4 h-4" />
      Add Song
    </Button>
  </DialogTrigger>

  <DialogContent>
    <DialogHeader>
      <DialogTitle>Add New Song</DialogTitle>
    </DialogHeader>

    <div class="grid gap-4 py-4">
      <!-- Song Name Input -->
      <div class="grid grid-cols-4 items-center gap-4">
        <Label for="song-name" class="text-right">Song Name</Label>
        <Input
          id="song-name"
          bind:value={$newSongName}
          class="col-span-3"
          placeholder="Enter song name"
        />
      </div>

      <!-- File Upload with Drag-and-Drop -->
      <div class="grid grid-cols-4 items-center gap-4">
        <Label for="song-file" class="text-right">GP File</Label>
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <div
          class="col-span-3 border-2 border-dashed rounded-md p-4 text-center"
          class:border-primary={isDragging}
          class:border-gray-300={!isDragging}
          on:dragover={handleDragOver}
          on:dragleave={handleDragLeave}
          on:drop={handleDrop}
        >
          <Input
            id="song-file"
            type="file"
            accept=".gp,.gpx"
            on:change={handleFileInput}
            class="hidden"
          />
          <Label for="song-file" class="cursor-pointer">
            {#if newSongFile}
              {newSongFile.name}
            {:else}
              Drag & drop or click to upload .gp or .gpx file
            {/if}
          </Label>
        </div>
      </div>
    </div>

    <DialogFooter>
      <Button on:click={handleAddSong} disabled={!$newSongName || !newSongFile}>
        Add Song
      </Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
