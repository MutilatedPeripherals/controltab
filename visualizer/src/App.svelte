<script lang="ts">
  import Router, { location } from "svelte-spa-router";
  import routes from "./routes";
  import { QueryClient, QueryClientProvider } from "@tanstack/svelte-query";
  import { isAuthenticated } from "./stores/auth"; // Use the isAuthenticated derived store
  import { Music2 } from "lucide-svelte";

  const queryClient = new QueryClient();
</script>

<div class="flex flex-col min-h-screen bg-base-200">
  <!-- Conditionally show the navbar if not on the login page -->
  {#if $location !== "/login"}
    <nav class="bg-primary text-primary-foreground shadow-md">
      <div class="container mx-auto px-4">
        <div class="flex items-center justify-between h-16">
          <!-- Logo and Home Link -->
          <div class="flex items-center">
            <a href="#/dashboard" class="flex items-center">
              <Music2 class="h-8 w-8 mr-2" />
              <span class="font-bold text-xl">ControlTab</span>
            </a>
          </div>

          <!-- Links Section, hidden on smaller screens -->
          <div class="hidden md:block">
            <div class="ml-10 flex items-baseline space-x-4">
              <!-- Conditionally render navbar links based on authentication status -->
              {#if $isAuthenticated}
                <a
                  href="#/dashboard"
                  class="px-3 py-2 rounded-md text-sm font-medium hover:bg-primary-foreground hover:text-primary transition-colors"
                >
                  Dashboard
                </a>
                <a
                  href="#/visualizer"
                  class="px-3 py-2 rounded-md text-sm font-medium hover:bg-primary-foreground hover:text-primary transition-colors"
                >
                  Visualizer
                </a>
                <a
                  href="https://www.youtube.com/watch?v=26X2TBp3T_U"
                  class="px-3 py-2 rounded-md text-sm font-medium hover:bg-primary-foreground hover:text-primary transition-colors"
                >
                  Necrophagist - Extreme Unction [Live At Party.San 2005] 4K
                </a>
              {/if}

              <!-- Show Login link if not authenticated -->
              {#if !$isAuthenticated}
                <a
                  href="#/login"
                  class="px-3 py-2 rounded-md text-sm font-medium hover:bg-primary-foreground hover:text-primary transition-colors"
                >
                  Login
                </a>
              {/if}
            </div>
          </div>
        </div>
      </div>
    </nav>
  {/if}

  <main>
    <QueryClientProvider client={queryClient}>
      <Router {routes} />
    </QueryClientProvider>
  </main>
</div>

<style global>
  @import "tailwindcss/tailwind.css";
</style>
