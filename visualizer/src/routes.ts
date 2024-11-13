import { isAuthenticated } from "./stores/auth";
import { get } from "svelte/store";
import type { RouteDefinition } from "svelte-spa-router";
import type { SvelteComponent } from "svelte";
import Home from "./routes/Home.svelte";
import { wrap } from "svelte-spa-router/wrap";
import Dashboard from "./routes/Dashboard.svelte";
import TabDetail from "./routes/TabDetail.svelte";
import CompareTabs from "./routes/CompareTabs.svelte";
import Login from "./routes/Login.svelte";
import Visualizer from "./routes/Visualizer.svelte";
import VisualizerLegacy from "./routes/VisualizerLegacy.svelte";

function authGuard() {
  return get(isAuthenticated);
}

const routes: RouteDefinition = {
  "/": Home as typeof SvelteComponent,
  "/dashboard": wrap({
    component: Dashboard as typeof SvelteComponent,
    conditions: [authGuard],
  }),
  "/tabs/:id": wrap({
    component: TabDetail as typeof SvelteComponent,
    conditions: [authGuard],
  }),
  "/tabs/:id/compare": wrap({
    component: CompareTabs as typeof SvelteComponent,
    conditions: [authGuard],
  }),
  "/login": Login as typeof SvelteComponent,
  "/visualizer": wrap({
    component: Visualizer as typeof SvelteComponent,
    conditions: [authGuard],
  }),
  "/visualizer-legacy": wrap({
    component: VisualizerLegacy as typeof SvelteComponent,
    conditions: [authGuard],
  }),
};

export default routes;
