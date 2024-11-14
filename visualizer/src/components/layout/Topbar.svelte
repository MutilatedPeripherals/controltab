<script lang="ts">
  import { Music2 } from "lucide-svelte";
</script>

<nav class="bg-primary text-primary-foreground shadow-md">
  <div class="container mx-auto px-4">
    <div class="flex items-center justify-between h-16">
      <div class="flex items-center">
        <a href="#/songs" class="flex items-center">
          <Music2 class="h-8 w-8 mr-2" />
          <span class="font-bold text-xl">ControlTab</span>
        </a>
      </div>

      <div class="hidden md:block">
        <div class="ml-10 flex items-baseline space-x-4"></div>
      </div>
    </div>
  </div>
</nav>
