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

  const createSongMutation = useCreateSong();

  let newSongName = $state("");
  let newSongFile: File | null = $state(null);
  let isDragging = $state(false);
  let showAddSongDialog = $state(false);

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
    if (newSongName && newSongFile) {
      $createSongMutation.mutate({
        title: newSongName,
        tabFile: newSongFile,
      });

      newSongName = "";
      newSongFile = null;
      showAddSongDialog = false;
    }
  }
</script>

<Dialog bind:open={showAddSongDialog}>
  <DialogTrigger asChild>
    <Button
      onclick={() => (showAddSongDialog = true)}
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
          bind:value={newSongName}
          class="col-span-3"
          placeholder="Enter song name"
        />
      </div>

      <div class="grid grid-cols-4 items-center gap-4">
        <Label for="song-file" class="text-right">GP File</Label>
        <div
          role="button"
          tabindex="0"
          class="col-span-3 border-2 border-dashed rounded-md p-4 text-center"
          class:border-primary={isDragging}
          class:border-gray-300={!isDragging}
          ondragover={handleDragOver}
          ondragleave={handleDragLeave}
          ondrop={handleDrop}
          aria-label="Drop GP file here"
        >
          <Input
            id="song-file"
            type="file"
            accept=".gp"
            onchange={handleFileInput}
            class="hidden"
          />
          <Label for="song-file" class="cursor-pointer">
            {#if newSongFile}
              {newSongFile.name}
            {:else}
              Drag & drop or click to upload .gp file
            {/if}
          </Label>
        </div>
      </div>
    </div>

    <DialogFooter>
      <Button onclick={handleAddSong} disabled={!newSongName || !newSongFile}>
        Add Song
      </Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
