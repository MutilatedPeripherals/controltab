<script lang="ts">
  import Router from "svelte-spa-router";
  import routes from "./routes";
</script>

<div class="flex flex-col bg-gray-100">
  <nav class="bg-blue-600 text-white p-4">
    <div class="container mx-auto flex justify-between">
      <a href="#/" class="text-lg font-bold">Home</a>
      <a href="#/visualizer" class="text-lg font-bold">Visualizer</a>
    </div>
  </nav>

  <main class="flex-grow container mx-auto p-4">
    <Router {routes} />
  </main>
</div>

<style global>
  @import "tailwindcss/tailwind.css";
</style>
