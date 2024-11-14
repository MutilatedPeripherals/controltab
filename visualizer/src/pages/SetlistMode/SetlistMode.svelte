<script lang="ts">
  import { writable } from "svelte/store";
  import { Button } from "$lib/components/ui/button";
  import { PlusCircle, Save } from "lucide-svelte";
  import type { SetlistItem } from "../../types/SetlistItem";
  import SongItem from "../../components/setlist-item/SongItem.svelte";
  import GenericItem from "../../components/setlist-item/GenericItem.svelte";

  const setlist = writable<SetlistItem[]>([]);

  const addItem = (type: SetlistItem["type"]) => {
    setlist.update((items) => [
      ...items,
      type === "song"
        ? {
            id: Date.now().toString(),
            type: "song",
            songId: "",
          }
        : {
            id: Date.now().toString(),
            type,
            title: `New ${type.charAt(0).toUpperCase() + type.slice(1)}`,
          },
    ]);
  };

  const updateItem = (id: string, updates: Partial<SetlistItem>) => {
    setlist.update((items) =>
      items.map((item) => {
        if (item.id !== id) return item;

        if (item.type === "song") {
          return {
            ...item,
            songId: "songId" in updates ? updates.songId! : item.songId,
            notes: "notes" in updates ? updates.notes : item.notes,
          };
        } else {
          return {
            ...item,
            title: "title" in updates ? updates.title! : item.title,
            notes: "notes" in updates ? updates.notes : item.notes,
          };
        }
      })
    );
  };
  const removeItem = (id: string) => {
    setlist.update((items) => items.filter((item) => item.id !== id));
  };

  const handleSave = () => {
    console.log("Saving setlist...");
    console.log($setlist);
  };
</script>

<div class="container mx-auto p-4">
  <h1 class="text-2xl font-bold mb-4">Setlist Mode</h1>

  <div class="flex space-x-2 mb-4 justify-between">
    <div class="flex space-x-2">
      <Button on:click={() => addItem("song")}
        ><PlusCircle class="mr-2 h-4 w-4" /> Add Song</Button
      >
      <Button on:click={() => addItem("sample")}
        ><PlusCircle class="mr-2 h-4 w-4" /> Add Sample</Button
      >
      <Button on:click={() => addItem("break")}
        ><PlusCircle class="mr-2 h-4 w-4" /> Add Break</Button
      >
      <Button on:click={() => addItem("speech")}
        ><PlusCircle class="mr-2 h-4 w-4" /> Add Speech</Button
      >
    </div>
    <Button
      on:click={() => handleSave()}
      class="ml-auto"
      disabled={$setlist.length === 0}
      ><Save class="mr-2 h-4 w-4" /> Save</Button
    >
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
    {#each $setlist as setlistItem}
      {#if setlistItem.type === "song"}
        <SongItem {setlistItem} onUpdate={updateItem} onRemove={removeItem} />
      {:else}
        <GenericItem
          {setlistItem}
          onUpdate={updateItem}
          onRemove={removeItem}
        />
      {/if}
    {/each}
  </div>
</div>
