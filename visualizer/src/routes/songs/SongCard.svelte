<script lang="ts">
  import { Card, CardContent } from "$lib/components/ui/card";
  import { Button } from "$lib/components/ui/button";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
  import {
    Music,
    FileText,
    MessageSquare,
    MoreHorizontal,
    Calendar,
  } from "lucide-svelte";
  import { formatDate } from "$lib/utils";
  import type { Song } from "../types/Song";

  export let song: Song;
  export let handleAction: (action: string, song: Song) => void;
  export let confirmDelete: (song: Song) => void;
</script>

<Card class="overflow-hidden">
  <CardContent class="p-0">
    <div
      class="flex items-center justify-between p-4 bg-primary text-primary-foreground"
    >
      <div class="flex items-center">
        <Music class="w-5 h-5 mr-2" />
        <h2 class="text-lg font-semibold">{song.title}</h2>
      </div>
      <DropdownMenu.Root>
        <DropdownMenu.Trigger asChild let:builder>
          <Button variant="ghost" builders={[builder]} class="h-8 w-8 p-0">
            <span class="sr-only">Open menu</span>
            <MoreHorizontal class="h-4 w-4" />
          </Button>
        </DropdownMenu.Trigger>
        <DropdownMenu.Content align="end">
          <DropdownMenu.Label>Actions</DropdownMenu.Label>
          <DropdownMenu.Item on:click={() => handleAction("open", song)}>
            <FileText class="mr-2 h-4 w-4" /> Open Tab
          </DropdownMenu.Item>
          <DropdownMenu.Item on:click={() => handleAction("suggest", song)}>
            <MessageSquare class="mr-2 h-4 w-4" /> Suggest Changes
          </DropdownMenu.Item>
          <DropdownMenu.Item on:click={() => handleAction("export", song)} disabled>
            Export as PDF
          </DropdownMenu.Item>
          <DropdownMenu.Separator />
          <DropdownMenu.Item
            on:click={() => confirmDelete(song)}
            class="text-red-600"
          >
            Delete Song
          </DropdownMenu.Item>
        </DropdownMenu.Content>
      </DropdownMenu.Root>
    </div>
    <div class="p-4 flex items-center text-muted-foreground">
      <Calendar class="w-4 h-4 mr-2" />
      <span>Last modified: {formatDate(song.tab.uploaded_at)}</span>
    </div>
  </CardContent>
</Card>
