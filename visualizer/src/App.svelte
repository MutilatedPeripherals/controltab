<script lang="ts">
  import Router from "svelte-spa-router";
  import routes from "./routes";
  import { QueryClient, QueryClientProvider } from "@tanstack/svelte-query";
  import { Toaster } from "svelte-french-toast";

  const queryClient = new QueryClient();
</script>

<div class="flex flex-col min-h-screen bg-base-200">
  <nav class="bg-primary text-primary-content shadow-lg p-4">
    <div class="container mx-auto flex justify-between items-center">
      <a href="#/" class="text-xl font-semibold hover:text-secondary">Home</a>
      <div class="space-x-4">
        <a
          href="#/visualizer"
          class="text-lg font-semibold hover:text-secondary"
        >
          Visualizer
        </a>
        <a
          href="#/dashboard"
          class="text-lg font-semibold hover:text-secondary"
        >
          Dashboard
        </a>
      </div>
    </div>
  </nav>

  <main>
    <QueryClientProvider client={queryClient}>
      <Toaster position="top-center" />

      <Router {routes} />
    </QueryClientProvider>
  </main>
</div>

<style global>
  @import "tailwindcss/tailwind.css";
</style>
