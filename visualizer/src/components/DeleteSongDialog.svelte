<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
  } from "$lib/components/ui/dialog";
  import { useDeleteSong } from "../mutations/deleteSongMutation";

  let { songId = null, songTitle = "", open = $bindable(false) } = $props();

  const deleteSongMutation = useDeleteSong();

  function handleDelete() {
    if (songId !== null) {
      $deleteSongMutation.mutate(songId);
      open = false;
    }
  }
</script>

<Dialog bind:open>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Confirm Deletion</DialogTitle>
    </DialogHeader>
    <p>Are you sure you want to delete "{songTitle}"?</p>
    <DialogFooter class="mt-4 flex justify-end">
      <Button variant="destructive" onclick={handleDelete}>Delete</Button>
      <Button onclick={() => (open = false)}>Cancel</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
