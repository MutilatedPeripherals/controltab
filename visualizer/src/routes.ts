// src/routes.ts
import type { RouteDefinition } from "svelte-spa-router";
import type { SvelteComponent } from "svelte";
import Home from "./routes/Home.svelte";
import { wrap } from "svelte-spa-router/wrap";
import Dashboard from "./routes/Dashboard.svelte";
import TabDetail from "./routes/TabDetail.svelte";
import CompareTabs from "./routes/CompareTabs.svelte";

const routes: RouteDefinition = {
  "/": Home as typeof SvelteComponent,
  "/dashboard": Dashboard as typeof SvelteComponent,
  "/tabs/:id": TabDetail as typeof SvelteComponent,
  "/tabs/:id/compare": CompareTabs as typeof SvelteComponent,
  "/visualizer": wrap({
    asyncComponent: () =>
      import("./routes/Visualizer.svelte") as Promise<{
        default: typeof SvelteComponent;
      }>,
  }),
};

export default routes;
