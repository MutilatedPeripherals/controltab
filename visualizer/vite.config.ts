import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import { alphaTab } from "@coderline/alphatab/vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [svelte()],
});
