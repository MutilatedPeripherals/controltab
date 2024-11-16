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
  import { useFetchSongs } from "../../queries/getSongsQuery";
  import type { SetlistItem } from "../../types/SetlistItem";
  import type { Selected } from "bits-ui";
  import { Button } from "$lib/components/ui/button";

  export let setlistItem: SetlistItem;
  export let onUpdate: (
    identifier: string | undefined,
    updates: Partial<SetlistItem>
  ) => void;
  export let onRemove: (identifier: string | undefined) => void;

  const songsQuery = useFetchSongs();

  function handleSongChange(selected: Selected<unknown> | undefined) {
    const identifier = setlistItem.id || setlistItem.tempId;
    if (identifier) {
      onUpdate(identifier, { songId: selected?.value as number | null });
    }
  }

  function getSongName(id: number) {
    const song = $songsQuery.data?.find((song) => song.id === id);
    return song?.title || "";
  }

  $: selectedElement =
    !$songsQuery.isLoading &&
    !$songsQuery.isError &&
    setlistItem.type === "song" &&
    setlistItem.songId
      ? { value: setlistItem.songId, label: getSongName(setlistItem.songId) }
      : undefined;

  const identifier = setlistItem.id || setlistItem.tempId;
</script>

<Card class="bg-card">
  <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
    <CardTitle class="text-sm font-medium flex items-center">
      <div class="cursor-move p-2 items-center flex">
        <GripVertical class="h-4 w-4" />
        <Music class="h-4 w-4 ml-2" />
      </div>

      {#if setlistItem.type === "song"}
        {#if $songsQuery.isSuccess}
          <Select.Root
            onSelectedChange={(e) => handleSongChange(e)}
            selected={selectedElement}
          >
            <Select.Trigger class="ml-2 h-8 w-full">
              <Select.Value placeholder="Select a song" />
            </Select.Trigger>
            <Select.Content>
              {#each $songsQuery.data || [] as song}
                <Select.Item value={song.id}>{song.title}</Select.Item>
              {/each}
            </Select.Content>
          </Select.Root>
        {/if}
      {:else}
        <span class="ml-2">{setlistItem.title}</span>
      {/if}
    </CardTitle>

    <Button
      on:click={() => onRemove(identifier)}
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
        onUpdate(identifier, {
          notes: (e.target as HTMLTextAreaElement)?.value,
        })}
      class="mt-2"
    />
  </CardContent>
</Card>
