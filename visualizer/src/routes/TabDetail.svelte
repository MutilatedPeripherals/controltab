<script lang="ts">
  import { tick } from "svelte";
  import { push } from "svelte-spa-router";
  import "@coderline/alphatab";
  import { useFetchSongData } from "../queries/getSongQuery";
  import type { Song } from "../types/Song";

  export let params: { id: number };
  const tabId = params.id;

  const songDataQuery = useFetchSongData(tabId);
  let container: HTMLDivElement;

  $: if ($songDataQuery.isSuccess) {
    tick().then(() => {
      renderSelectedTab($songDataQuery.data);
    });
  }

  function renderSelectedTab(data: Song) {
    console.log(data);
    if (!window.alphaTab) {
      console.error("AlphaTab not loaded");
      return;
    }

    const settings = {
      file: data.tab.filepath,
      core: {
        engine: "svg",
      },
      display: {
        layoutMode: 0,
      },
      rendering: {
        useWorkers: false,
        virtualization: "off",
      },
      notation: {
        elements: {
          ScoreTitle: false,
        },
      },
    };

    const tabRenderer = new window.alphaTab.AlphaTabApi(container, settings);
    tabRenderer.postRenderFinished.on(() => {
      console.log(`Tab ${data.tab.filename} rendered successfully.`);
    });
  }

  function suggestChange() {
    console.log("Suggest a change clicked");
    push(`/tabs/${tabId}/compare`);
  }
</script>

<div class="container mx-auto p-6 bg-base-200 min-h-screen rounded-lg">
  {#if $songDataQuery.isLoading}
    <p class="text-center text-gray-500">Loading tab data...</p>
  {:else if $songDataQuery.isError}
    <p class="text-center text-red-500">Failed to load tab data.</p>
  {:else if $songDataQuery.isSuccess}
    <h2 class="text-3xl font-semibold text-center mb-4 text-gray-800">
      {$songDataQuery.data.title}
    </h2>

    <div
      bind:this={container}
      class="w-full h-[500px] bg-white border border-gray-300 rounded-lg shadow-md overflow-y-auto overflow-x-hidden"
    ></div>

    <div class="flex justify-center mt-6">
      <button on:click={suggestChange} class="btn btn-primary">
        Suggest a Change
      </button>
    </div>
  {/if}
</div>
