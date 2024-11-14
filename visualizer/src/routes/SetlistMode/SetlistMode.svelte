<script lang="ts">
  import { writable } from "svelte/store";
  import { draggable, droppable, type DragDropState } from "@thisux/sveltednd";
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Textarea } from "$lib/components/ui/textarea";
  import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
  } from "$lib/components/ui/card";
  import { Switch } from "$lib/components/ui/switch";
  import { Label } from "$lib/components/ui/label";
  import {
    PlusCircle,
    Music,
    Mic,
    Coffee,
    FileAudio,
    GripVertical,
    X,
  } from "lucide-svelte";
  import SetlistItemCard from "../../components/SetlistItemCard.svelte";
  import type { SetlistItem } from "../../types/SetlistItem";

  // Setlist store to manage items
  const setlist = writable<SetlistItem[]>([]);

  const addItem = (type: SetlistItem["type"]) => {
    setlist.update((items) => [
      ...items,
      {
        id: Date.now().toString(),
        type,
        title:
          type === "song"
            ? "New Song"
            : `New ${type.charAt(0).toUpperCase() + type.slice(1)}`,
        showTuning: false,
        tuning: type === "song" ? "EADGBE" : undefined,
      },
    ]);
  };

  const updateItem = (id: string, updates: Partial<SetlistItem>) => {
    setlist.update((items) =>
      items.map((item) => (item.id === id ? { ...item, ...updates } : item))
    );
  };

  const removeItem = (id: string) => {
    setlist.update((items) => items.filter((item) => item.id !== id));
  };

  const handleDrop = (state: DragDropState<SetlistItem>) => {
    const { draggedItem, targetContainer } = state;
    if (!targetContainer) return;

    setlist.update((items) => {
      const itemIndex = items.findIndex((item) => item.id === draggedItem.id);
      items.splice(itemIndex, 1);
      const dropIndex = parseInt(targetContainer);
      items.splice(dropIndex, 0, draggedItem);
      return items;
    });
  };
</script>

<div class="container mx-auto p-4">
  <h1 class="text-2xl font-bold mb-4">Setlist Mode</h1>

  <!-- Add Item Buttons -->
  <div class="flex space-x-2 mb-4">
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

  <!-- Setlist Items (Drag and Drop Zone) -->
  <div
    use:droppable={{ container: "setlist", callbacks: { onDrop: handleDrop } }}
    class="grid gap-4 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3"
  >
    {#each $setlist as setlistItem (setlistItem.id)}
      <div
        use:draggable={{ container: "setlist", dragData: setlistItem }}
        class="cursor-move"
      >
        <SetlistItemCard
          {setlistItem}
          onUpdate={updateItem}
          onRemove={removeItem}
        />
      </div>
    {/each}
  </div>
</div>
