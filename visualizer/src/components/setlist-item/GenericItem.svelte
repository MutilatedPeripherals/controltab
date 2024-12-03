<script lang="ts">
  import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
  } from "$lib/components/ui/card";
  import { Textarea } from "$lib/components/ui/textarea";
  import { GripVertical, FileAudio, Coffee, Mic, Trash2 } from "lucide-svelte";
  import { Input } from "$lib/components/ui/input";
  import { Button } from "$lib/components/ui/button";
  import type { SetlistItem } from "../../types/SetlistItem";
  import { dragHandle } from "svelte-dnd-action";

  export let setlistItem: SetlistItem;
  export let onUpdate: (
    id: string | undefined,
    updates: Partial<SetlistItem>
  ) => void;
  export let onRemove: (identifier: string | undefined) => void;

  const identifier = setlistItem.id;
  if (import.meta.env.VITE_DEBUG) {
    console.log(identifier);
  }
  function getIconForType(type: SetlistItem["type"]) {
    switch (type) {
      case "sample":
        return FileAudio;
      case "break":
        return Coffee;
      case "speech":
        return Mic;
      default:
        return null;
    }
  }

  const IconComponent = getIconForType(setlistItem.type);
</script>

<div>
  <Card class="bg-card hover:shadow-md transition-shadow duration-200">
    <CardHeader
      class="flex flex-row items-center justify-between space-y-0 pb-2"
    >
      <CardTitle class="text-sm font-medium flex items-center">
        <div
          class="cursor-move p-2 flex items-center space-x-2"
          role="button"
          aria-label="Drag to reorder"
          use:dragHandle
        >
          <GripVertical class="h-4 w-4" />
          {#if IconComponent}
            <svelte:component this={IconComponent} class="h-4 w-4" />
          {/if}
        </div>
        {#if setlistItem.type !== "song"}
          <Input
            type="text"
            value={setlistItem.title}
            on:input={(e) =>
              onUpdate(identifier, {
                title: (e.target as HTMLInputElement)?.value,
              })}
            class="ml-2 h-8"
          />
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
</div>

<style>
</style>
