import type { RouteDefinition } from "svelte-spa-router";
import type { SvelteComponent } from "svelte";
import Home from "./routes/Home.svelte";
import { wrap } from "svelte-spa-router/wrap";
import Dashboard from "./routes/Dashboard.svelte";
import TabDetail from "./routes/TabDetail.svelte";
import CompareTabs from "./routes/CompareTabs.svelte";
import Login from "./routes/Login.svelte";
import Visualizer from "./routes/Visualizer.svelte";
import { token } from "./mutations/loginMutation";
import VisualizerLegacy from "./routes/VisualizerLegacy.svelte";

const routes: RouteDefinition = {
  "/": Home as typeof SvelteComponent,
  "/dashboard": wrap({
    component: Dashboard as typeof SvelteComponent,
    conditions: [
      () => !!token, // Only allow if token is present
    ],
  }),
  "/tabs/:id": wrap({
    component: TabDetail as typeof SvelteComponent,
    conditions: [() => !!token],
  }),
  "/tabs/:id/compare": wrap({
    component: CompareTabs as typeof SvelteComponent,
    conditions: [() => !!token],
  }),
  "/login": Login as typeof SvelteComponent,
  "/visualizer": wrap({
    component: Visualizer as typeof SvelteComponent,
    conditions: [() => !!token],
  }),
  "/visualizer-legacy": wrap({
    component: VisualizerLegacy as typeof SvelteComponent,
    conditions: [() => !!token],
  }),
};

export default routes;
