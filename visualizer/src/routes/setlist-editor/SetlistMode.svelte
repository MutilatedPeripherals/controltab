<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { PlusCircle, Save, Eye, List } from "lucide-svelte";
  import type { SetlistItem } from "../../types/SetlistItem";
  import SongItem from "../../components/setlist-item/SongItem.svelte";
  import GenericItem from "../../components/setlist-item/GenericItem.svelte";
  import { useFetchSetlistItems } from "../../queries/getSetlistItemsQuery";
  import { useUpdateSetlist } from "../../mutations/updateSetlistMutation";
  import { dragHandleZone, type DndEvent } from "svelte-dnd-action";
  import { flip } from "svelte/animate";
  import { toast } from "svelte-sonner";
  import SetlistPreview from "./SetlistPreview.svelte";

  let setlist = $state<SetlistItem[]>([]);
  let previewMode = $state(false);

  const togglePreviewMode = () => {
    previewMode = !previewMode;
  };

  const setlistItemsQuery = useFetchSetlistItems();
  const updateSetlistResult = useUpdateSetlist();

  $effect(() => {
    if ($setlistItemsQuery.isSuccess) {
      setlist = $setlistItemsQuery.data ?? [];
    }
  });

  const canSave = $derived(() => setlist.length > 0);

  const addItem = (type: SetlistItem["type"]) => {
    setlist = [
      ...setlist,
      type === "song"
        ? {
            id: crypto.randomUUID(),
            type: "song",
            songId: null,
            notes: "",
            order: setlist.length,
          }
        : {
            id: crypto.randomUUID(),
            type,
            title: `New ${type.charAt(0).toUpperCase() + type.slice(1)}`,
            notes: "",
            order: setlist.length,
          },
    ];
  };

  const updateItem = (
    id: string | undefined,
    updates: Partial<SetlistItem>
  ) => {
    if (!id) return;

    setlist = setlist.map((item) => {
      if (item.id === id) {
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
    });
  };

  const removeItem = (id: string | undefined) => {
    if (!id) return;

    setlist = setlist
      .filter((item) => item.id !== id)
      .map((item, index) => ({ ...item, order: index }));
  };

  const handleSave = () => {
    const invalidItems = setlist.filter(
      (item) => item.type === "song" && item.songId === null
    );

    if (invalidItems.length > 0) {
      toast.error("Failed to save setlist.", {
        description: "All songs must have a song selected before saving.",
      });
      return;
    }

    $updateSetlistResult.mutate(
      { setlist },
      {
        onSuccess: () => {
          toast.success("Setlist saved successfully!", {
            description: "Your setlist changes have been saved.",
          });
        },
        onError: () => {
          toast.error("Failed to save setlist.", {
            description: "Please try again later.",
          });
        },
      }
    );
  };

  function handleSort(e: CustomEvent<DndEvent<SetlistItem>>): void {
    setlist = e.detail.items.map((item, index) => ({
      ...item,
      order: index,
    }));
  }

  const flipDurationMs = 300;
</script>

<div class="container mx-auto p-4">
  <div class="flex justify-between items-center mb-4">
    <h1 class="text-2xl font-bold">
      {previewMode ? "Preview Mode" : "Setlist Mode"}
    </h1>
    <div class="flex space-x-2">
      <Button on:click={togglePreviewMode} variant="outline">
        {#if previewMode}
          <List class="mr-2 h-4 w-4" /> Edit Mode
        {:else}
          <Eye class="mr-2 h-4 w-4" /> Preview Mode
        {/if}
      </Button>
      <Button on:click={handleSave} disabled={!canSave()}>
        <Save class="mr-2 h-4 w-4" /> Save
      </Button>
    </div>
  </div>

  {#if previewMode}
    <SetlistPreview {setlist} />
  {:else}
    <div class="flex space-x-2 mb-4">
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

    <div class="space-y-2">
      {#if setlist.length === 0}
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
        use:dragHandleZone={{ items: setlist, flipDurationMs }}
        onconsider={handleSort}
        onfinalize={handleSort}
        class="space-y-2"
      >
        {#each setlist as setlistItem (setlistItem.id)}
          <div animate:flip={{ duration: flipDurationMs }}>
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
  {/if}
</div>
