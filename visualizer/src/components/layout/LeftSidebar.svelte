<script lang="ts">
  import * as Tooltip from "$lib/components/ui/tooltip/index.js";
  import { Music, List, Users, FileText } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";

  // Props
  export let currentPage: string;
  export let onPageChange: (page: string) => void;

  // Define menu items with full paths and add `disabled` property to specific items
  const menuItems = [
    { id: "/songs", label: "Songs", icon: Music, disabled: false },
    { id: "/setlists", label: "Setlists", icon: List, disabled: false },
    { id: "/myband", label: "My Band", icon: Users, disabled: true },
    { id: "/rider", label: "Rider Editor", icon: FileText, disabled: true },
  ];
</script>

<div class="flex w-16 flex-col bg-gray-100 p-2">
  <nav class="space-y-2">
    {#each menuItems as item}
      <Tooltip.Root>
        <Tooltip.Trigger asChild let:builder>
          <Button
            variant="ghost"
            class={`w-full p-2 transition-colors ${
              currentPage === item.id
                ? "bg-gray-200 hover:bg-gray-300" // Selected and hover effect
                : "hover:bg-gray-200" // Default hover effect
            }`}
            on:click={() => !item.disabled && onPageChange(item.id)}
            disabled={item.disabled}
            builders={[builder]}
          >
            <item.icon class="h-6 w-6" />
            <span class="sr-only">{item.label}</span>
          </Button>
        </Tooltip.Trigger>
        <Tooltip.Content side="right">
          <p>{item.label}</p>
        </Tooltip.Content>
      </Tooltip.Root>
    {/each}
  </nav>
</div>
