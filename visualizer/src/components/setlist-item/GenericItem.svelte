<script lang="ts">
  import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
  } from "$lib/components/ui/card";
  import { Textarea } from "$lib/components/ui/textarea";
  import { GripVertical, FileAudio, Coffee, Mic, Trash2 } from "lucide-svelte";
  import { draggable } from "@thisux/sveltednd";
  import type { SetlistItem } from "../../types/SetlistItem";
  import { Input } from "$lib/components/ui/input";
  import { Button } from "$lib/components/ui/button";

  export let setlistItem: SetlistItem;
  export let onUpdate: (id: string, updates: Partial<SetlistItem>) => void;
  export let onRemove: (id: string) => void;

  // Function to get the appropriate icon component
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

<Card class="bg-card">
  <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
    <CardTitle class="text-sm font-medium flex items-center">
      <div
        use:draggable={{ container: "setlist", dragData: setlistItem }}
        class="cursor-move p-2 flex items-center space-x-2"
      >
        <GripVertical class="h-4 w-4" />
        {#if IconComponent}
          <svelte:component this={IconComponent} class="h-4 w-4" />
        {/if}
      </div>

      <Input
        type="text"
        value={setlistItem.title}
        on:input={(e) =>
          onUpdate(setlistItem.id, { title: e.target?.value || "" })}
        class="ml-2 h-8"
      />
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
      on:input={(e) => onUpdate(setlistItem.id, { notes: e.target?.value })}
      class="mt-2"
    />
  </CardContent>
</Card>
