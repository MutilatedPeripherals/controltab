<script lang="ts">
  import { Switch } from "$lib/components/ui/switch";
  import { Input } from "$lib/components/ui/input";
  import { Textarea } from "$lib/components/ui/textarea";
  import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
  } from "$lib/components/ui/card";
  import { Label } from "$lib/components/ui/label";
  import {
    GripVertical,
    Music,
    Mic,
    Coffee,
    FileAudio,
    X,
  } from "lucide-svelte";
  import { draggable } from "@thisux/sveltednd";
  import type { SetlistItem } from "../types/SetlistItem";

  export let setlistItem: SetlistItem;
  export let onUpdate: (
    id: string,
    updates: Partial<typeof setlistItem>
  ) => void;
  export let onRemove: (id: string) => void;

  const typeIcons = {
    song: Music,
    sample: FileAudio,
    break: Coffee,
    speech: Mic,
  };

  const IconComponent = typeIcons[setlistItem.type] || Music;

  function handleTitleChange(event) {
    onUpdate(setlistItem.id, { title: event.target.value });
  }

  function handleNotesChange(event) {
    onUpdate(setlistItem.id, { notes: event.target.value });
  }
</script>

<div
  use:draggable={{ container: "setlist", dragData: setlistItem }}
  class="cursor-move"
>
  <Card class="bg-card">
    <CardHeader
      class="flex flex-row items-center justify-between space-y-0 pb-2"
    >
      <CardTitle class="text-sm font-medium flex items-center">
        <span class="mr-2"><GripVertical class="h-4 w-4" /></span>
        <IconComponent class="h-4 w-4" />
        <Input
          value={setlistItem.title}
          on:input={handleTitleChange}
          class="ml-2 h-8"
        />
      </CardTitle>
      <button on:click={() => onRemove(setlistItem.id)} class="text-red-600">
        <X class="h-4 w-4" />
      </button>
    </CardHeader>

    <CardContent>
      {#if setlistItem.type === "song"}
        <div class="space-y-2">
          <div class="flex items-center space-x-2">
            <Switch
              disabled
              id={`show-tuning-${setlistItem.id}`}
              checked={false}
            />
            <Label for={`show-tuning-${setlistItem.id}`}>Show Tuning</Label>
          </div>
        </div>
      {/if}

      <Textarea
        placeholder="Add notes..."
        value={setlistItem.notes || ""}
        on:input={handleNotesChange}
        class="mt-2"
      />
    </CardContent>
  </Card>
</div>
