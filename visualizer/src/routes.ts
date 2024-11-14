import { isAuthenticated } from "./stores/auth";
import { get } from "svelte/store";
import type { RouteDefinition } from "svelte-spa-router";
import type { SvelteComponent } from "svelte";
import Home from "./routes/Home.svelte";
import TabDetail from "./routes/TabDetail.svelte";
import CompareTabs from "./routes/CompareTabs.svelte";
import Login from "./routes/Login.svelte";
import Visualizer from "./routes/Visualizer.svelte";
import VisualizerLegacy from "./routes/VisualizerLegacy.svelte";
import SetlistMode from "./pages/SetlistMode/SetlistMode.svelte";
import Songs from "./pages/Songs.svelte";
import { wrap } from "svelte-spa-router/wrap";

function authGuard() {
  return get(isAuthenticated);
}

export const ROUTES = {
  HOME: "/",
  LOGIN: "/login",
  SONGS: "/songs",
  SONG_DETAIL: "/songs/:id",
  SONG_COMPARE: "/songs/:id/compare",
  VISUALIZER: "/visualizer",
  VISUALIZER_LEGACY: "/visualizer-legacy",
  SETLISTS: "/setlists",
};

const routes: RouteDefinition = {
  [ROUTES.HOME]: Home as typeof SvelteComponent,
  [ROUTES.LOGIN]: Login as typeof SvelteComponent,
  [ROUTES.SONGS]: wrap({
    component: Songs as typeof SvelteComponent,
    conditions: [authGuard],
  }),
  [`${ROUTES.SONGS}/:id`]: wrap({
    component: TabDetail as typeof SvelteComponent,
    conditions: [authGuard],
  }),
  [`${ROUTES.SONGS}/:id/compare`]: wrap({
    component: CompareTabs as typeof SvelteComponent,
    conditions: [authGuard],
  }),
  [ROUTES.VISUALIZER]: wrap({
    component: Visualizer as typeof SvelteComponent,
    conditions: [authGuard],
  }),
  [ROUTES.VISUALIZER_LEGACY]: wrap({
    component: VisualizerLegacy as typeof SvelteComponent,
    conditions: [authGuard],
  }),
  [ROUTES.SETLISTS]: wrap({
    component: SetlistMode as typeof SvelteComponent,
    conditions: [authGuard],
  }),
};

export default routes;
