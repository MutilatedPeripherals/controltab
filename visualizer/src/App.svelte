<script lang="ts">
  import Router from "svelte-spa-router";
  import routes from "./routes";
</script>

<div class="flex flex-col min-h-screen bg-base-200">
  <!-- Navbar -->
  <nav class="bg-primary text-primary-content shadow-lg p-4">
    <div class="container mx-auto flex justify-between items-center">
      <a href="#/" class="text-xl font-semibold hover:text-secondary">Home</a>
      <div class="space-x-4">
        <a
          href="#/visualizer"
          class="text-lg font-semibold hover:text-secondary">Visualizer</a
        >
        <a href="#/dashboard" class="text-lg font-semibold hover:text-secondary"
          >Dashboard</a
        >
      </div>
    </div>
  </nav>

  <!-- Main Content -->
  <main>
    <Router {routes} />
  </main>
</div>

<style global>
  @import "tailwindcss/tailwind.css";
</style>
