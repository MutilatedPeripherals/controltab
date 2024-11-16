<script lang="ts">
  import { get, writable } from "svelte/store";
  import { Button } from "$lib/components/ui/button";
  import { PlusCircle, Save } from "lucide-svelte";
  import type { SetlistItem } from "../../types/SetlistItem";
  import SongItem from "../../components/setlist-item/SongItem.svelte";
  import GenericItem from "../../components/setlist-item/GenericItem.svelte";
  import { useFetchSetlistItems } from "../../queries/getSetlistItemsQuery";
  import { useUpdateSetlist } from "../../mutations/updateSetlistMutation";
  import { dragHandleZone, type DndEvent } from "svelte-dnd-action";

  const setlist = writable<SetlistItem[]>([]);

  const setlistItemsQuery = useFetchSetlistItems();
  const updateSetlistResult = useUpdateSetlist();

  // Load existing items from the server
  $: if ($setlistItemsQuery.isSuccess) {
    setlist.set($setlistItemsQuery.data ?? []);
  }

  // Add a new item with a temporary ID
  const addItem = (type: SetlistItem["type"]) => {
    setlist.update((items) => [
      ...items,
      type === "song"
        ? {
            tempId: crypto.randomUUID(),
            type: "song",
            songId: null,
            notes: "",
          }
        : {
            tempId: crypto.randomUUID(),
            type,
            title: `New ${type.charAt(0).toUpperCase() + type.slice(1)}`,
            notes: "",
          },
    ]);
  };

  // method looks ass because of the nature of SetlistItem. Apparently unions are quite complicated to handle in Typescript
  const updateItem = (
    id: string | undefined,
    updates: Partial<SetlistItem>
  ) => {
    if (!id) return;

    setlist.update((items) =>
      items.map((item) => {
        if (item.id === id || item.tempId === id) {
          if (item.type === "song") {
            return {
              ...item,
              songId:
                "songId" in updates
                  ? (updates.songId ?? item.songId)
                  : item.songId,
              notes:
                "notes" in updates ? (updates.notes ?? item.notes) : item.notes,
            };
          } else if (
            item.type === "sample" ||
            item.type === "break" ||
            item.type === "speech"
          ) {
            return {
              ...item,
              title:
                "title" in updates ? (updates.title ?? item.title) : item.title,
              notes:
                "notes" in updates ? (updates.notes ?? item.notes) : item.notes,
            };
          }
        }
        return item;
      })
    );
  };

  const removeItem = (id: string | undefined) => {
    console.log("hello", id);
    if (!id) return;
    setlist.update((items) =>
      items.filter((item) => item.id !== id && item.tempId !== id)
    );
  };

  const handleSave = () => {
    const currentSetlist = get(setlist);
    $updateSetlistResult.mutate({ setlist: currentSetlist });
  };

  function handleSort(e: CustomEvent<DndEvent<SetlistItem>>): void {
    console.log(e.detail.items);
    setlist.set(e.detail.items);
  }
</script>

<div class="container mx-auto p-4">
  <h1 class="text-2xl font-bold mb-4">Setlist Mode</h1>

  <div class="flex space-x-2 mb-4 justify-between">
    <div class="flex space-x-2">
      <Button on:click={() => addItem("song")}>
        <PlusCircle class="mr-2 h-4 w-4" /> Add Song
      </Button>
      <Button on:click={() => addItem("sample")}>
        <PlusCircle class="mr-2 h-4 w-4" /> Add Sample
      </Button>
      <Button on:click={() => addItem("break")}>
        <PlusCircle class="mr-2 h-4 w-4" /> Add Break
      </Button>
      <Button on:click={() => addItem("speech")}>
        <PlusCircle class="mr-2 h-4 w-4" /> Add Speech
      </Button>
    </div>
    <Button
      on:click={() => handleSave()}
      class="ml-auto"
      disabled={$setlist.length === 0}
    >
      <Save class="mr-2 h-4 w-4" /> Save
    </Button>
  </div>

  <div class="space-y-2">
    {#if $setlist.length === 0}
      <div
        class="text-center text-gray-500 p-4 border border-dashed border-gray-300 rounded"
      >
        <p class="mb-2">Your setlist is currently empty.</p>
        <p>
          Click <strong>Add Song</strong> or another option above to start building
          your setlist.
        </p>
      </div>
    {/if}
    <div
      use:dragHandleZone={{ items: $setlist }}
      on:consider={handleSort}
      on:finalize={handleSort}
      class="space-y-2"
    >
      {#each $setlist as setlistItem}
        <div>
          {#if setlistItem.type === "song"}
            <SongItem
              {setlistItem}
              onUpdate={updateItem}
              onRemove={removeItem}
            />
          {:else}
            <GenericItem
              {setlistItem}
              onUpdate={updateItem}
              onRemove={removeItem}
            />
          {/if}
        </div>
      {/each}
    </div>
  </div>
</div>
