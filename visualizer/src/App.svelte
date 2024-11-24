<script lang="ts">
  import Router, { location, push } from "svelte-spa-router";
  import routes from "./routes";
  import { QueryClient, QueryClientProvider } from "@tanstack/svelte-query";
  import LeftSidebar from "./components/layout/LeftSidebar.svelte";
  import Topbar from "./components/layout/Topbar.svelte";
  import { Toaster } from "$lib/components/ui/sonner";

  const queryClient = new QueryClient();
</script>

<div class="flex flex-col min-h-screen bg-base-200">
  {#if $location !== "/login"}
    <Topbar />
  {/if}

  <div class="flex flex-1">
    {#if $location !== "/login"}
      <LeftSidebar
        currentPage={$location}
        onPageChange={(page) => push(page)}
      />
    {/if}

    <main class="flex-1 p-4">
      <QueryClientProvider client={queryClient}>
        <Router {routes} />
      </QueryClientProvider>
    </main>
  </div>
</div>

<Toaster />

<style global>
  @import "tailwindcss/tailwind.css";
</style>
