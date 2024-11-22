import { wrap } from "svelte-spa-router/wrap";
import type { SvelteComponent } from "svelte";

import Home from "./routes/Home.svelte";
import Login from "./routes/login/Login.svelte";
import Songs from "./routes/songs/Songs.svelte";
import TabDetail from "./routes/TabDetail.svelte";
import CompareTabs from "./routes/comparer/CompareTabs.svelte";
import Visualizer from "./routes/Visualizer.svelte";
import VisualizerLegacy from "./routes/VisualizerLegacy.svelte";
import SetlistMode from "./routes/setlist-editor/SetlistMode.svelte";

import { isAuthenticated } from "./stores/auth";

function authGuard(): Promise<boolean> {
  return new Promise((resolve) => {
    isAuthenticated.subscribe((value) => {
      resolve(value);
    })();
  });
}

type SvelteComponentType = new (...args: any[]) => SvelteComponent;
// man the backwards compatibility between svelte-spa-router and svelte 5 is ASS
// unkown casting for everyone to enjoy
const routes: Record<string, SvelteComponentType | ReturnType<typeof wrap>> = {
  "/": Home as unknown as SvelteComponentType,
  "/login": Login as unknown as SvelteComponentType,
  "/songs": wrap({
    component: Songs as unknown as SvelteComponentType,
    conditions: [authGuard],
  }),
  "/songs/:id": wrap({
    component: TabDetail as unknown as SvelteComponentType,
    conditions: [authGuard],
  }),
  "/songs/:id/compare": wrap({
    component: CompareTabs as unknown as SvelteComponentType,
    conditions: [authGuard],
  }),
  "/visualizer": wrap({
    component: Visualizer as unknown as SvelteComponentType,
    conditions: [authGuard],
  }),
  "/visualizer-legacy": wrap({
    component: VisualizerLegacy as unknown as SvelteComponentType,
    conditions: [authGuard],
  }),
  "/setlists": wrap({
    component: SetlistMode as unknown as SvelteComponentType,
    conditions: [authGuard],
  }),
};

export default routes;
