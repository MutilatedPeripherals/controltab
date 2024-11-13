<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
    DialogTrigger,
  } from "$lib/components/ui/dialog";
  import { useDeleteSong } from "../mutations/deleteSongMutation"; // Adjust the path as needed
  import { writable } from "svelte/store";

  // Props to receive from the parent component
  export let songId: number | null = null;
  export let songTitle: string = "";
  export let open = writable(false);

  const deleteSongMutation = useDeleteSong();

  function handleDelete() {
    if (songId !== null) {
      $deleteSongMutation.mutate(songId);
      open.set(false);
    }
  }
</script>

<Dialog bind:open={$open}>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Confirm Deletion</DialogTitle>
    </DialogHeader>
    <p>Are you sure you want to delete "{songTitle}"?</p>
    <DialogFooter class="mt-4 flex justify-end">
      <Button variant="destructive" on:click={handleDelete}>Delete</Button>
      <Button on:click={() => open.set(false)}>Cancel</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
