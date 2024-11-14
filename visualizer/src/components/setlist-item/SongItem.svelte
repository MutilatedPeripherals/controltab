<script lang="ts">
  import * as Select from "$lib/components/ui/select";
  import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
  } from "$lib/components/ui/card";
  import { Textarea } from "$lib/components/ui/textarea";
  import { GripVertical, Music, Trash2 } from "lucide-svelte";
  import { draggable } from "@thisux/sveltednd";
  import { useFetchSongs } from "../../queries/getSongsQuery";
  import type { SetlistItem } from "../../types/SetlistItem";
  import type { Selected } from "bits-ui";
  import { Button } from "$lib/components/ui/button";

  export let setlistItem: SetlistItem;
  export let onUpdate: (id: string, updates: Partial<SetlistItem>) => void;
  export let onRemove: (id: string) => void;
  const songsQuery = useFetchSongs();

  function handleSongChange(selected: Selected<unknown> | undefined) {
    onUpdate(setlistItem.id, { songId: selected?.value as string });
  }
</script>

<Card class="bg-card">
  <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
    <CardTitle class="text-sm font-medium flex items-center">
      <div
        use:draggable={{ container: "setlist", dragData: setlistItem }}
        class="cursor-move p-2 items-center flex"
      >
        <GripVertical class="h-4 w-4" />
        <Music class="h-4 w-4 ml-2" />
      </div>

      <Select.Root onSelectedChange={(e) => handleSongChange(e)}>
        <Select.Trigger class="ml-2 h-8 w-full">
          <Select.Value placeholder="Select a song" />
        </Select.Trigger>
        <Select.Content>
          {#each $songsQuery.data || [] as song}
            <Select.Item value={song.id}>{song.title}</Select.Item>
          {/each}
        </Select.Content>
      </Select.Root>
    </CardTitle>
    <Button
      on:click={() => onRemove(setlistItem.id)}
      class="text-red-600"
      variant="ghost"
    >
      <Trash2 class="h-5 w-5" />
    </Button>
  </CardHeader>

  <CardContent>
    <Textarea
      placeholder="Add notes..."
      value={setlistItem.notes || ""}
      on:input={(e) =>
        onUpdate(setlistItem.id, { notes: e.target?.value || "" })}
      class="mt-2"
    />
  </CardContent>
</Card>
