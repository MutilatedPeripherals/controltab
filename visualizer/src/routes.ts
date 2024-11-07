// src/routes.ts
import type { RouteDefinition } from "svelte-spa-router";
import type { SvelteComponent } from "svelte";
import Home from "./routes/Home.svelte";
import { wrap } from "svelte-spa-router/wrap";

const routes: RouteDefinition = {
  "/": Home as typeof SvelteComponent,
  "/visualizer": wrap({
    asyncComponent: () =>
      import("./routes/Visualizer.svelte") as Promise<{
        default: typeof SvelteComponent;
      }>,
  }),
};

export default routes;
