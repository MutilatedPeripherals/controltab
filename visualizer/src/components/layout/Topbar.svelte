<script lang="ts">
  import { Music2 } from "lucide-svelte";
</script>

<nav class="bg-primary text-primary-foreground shadow-md">
  <div class="container mx-auto px-4">
    <div class="flex items-center justify-between h-16">
      <!-- Logo and Title -->
      <div class="flex items-center">
        <a href="#/songs" class="flex items-center">
          <Music2 class="h-8 w-8 mr-2" />
          <span class="font-bold text-xl">ControlTab</span>
        </a>
        <!-- Early Access Badge -->
        <span
          class="ml-3 px-2 py-1 text-xs font-semibold text-white bg-yellow-500 rounded-full"
        >
          Early Access
        </span>
      </div>

      <div class="hidden md:block">
        <div class="ml-10 flex items-baseline space-x-4"></div>
      </div>
    </div>
  </div>
</nav>
