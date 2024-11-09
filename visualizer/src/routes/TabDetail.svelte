<script lang="ts">
  import { onMount, tick } from "svelte";
  import { push } from "svelte-spa-router";
  import "@coderline/alphatab"; // Import AlphaTab for rendering

  let tabData;
  let container: HTMLDivElement;
  export let params;
  const tabId = params.id; // Get the tab ID from the route parameters

  async function fetchTabData() {
    try {
      const response = await fetch(`http://127.0.0.1:8000/files/${tabId}`);
      if (!response.ok)
        throw new Error("Failed to fetch tab data from FastAPI");
      tabData = await response.json();
      await tick(); // Ensure the DOM is updated before rendering the tab
      renderSelectedTab();
    } catch (error) {
      console.error("Error fetching tab data:", error);
    }
  }

  function renderSelectedTab() {
    if (!window.alphaTab) {
      console.error("AlphaTab not loaded");
      return;
    }

    const settings = {
      file: tabData.content_url, // URL to the .gp file provided by the API
      core: {
        engine: "svg",
      },
      display: {
        layoutMode: 0, // Set layout to page mode for vertical scrolling
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

    // Initialize AlphaTabApi in the container with the selected file
    const tabRenderer = new window.alphaTab.AlphaTabApi(container, settings);

    tabRenderer.postRenderFinished.on(() => {
      console.log(`Tab ${tabData.filename} rendered successfully.`);
    });
  }

  function suggestChange() {
    console.log("Suggest a change clicked");
    push(`/tabs/${tabId}/compare`); // Navigate to the compare route with tabId
  }

  onMount(fetchTabData); // Fetch tab data and render on component mount
</script>

<div class="container mx-auto p-6 bg-base-200 min-h-screen rounded-lg">
  {#if tabData}
    <h2 class="text-3xl font-semibold text-center mb-4 text-gray-800">
      {tabData.filename}
    </h2>

    <!-- Container where AlphaTab will render the tab -->
    <div
      bind:this={container}
      class="w-full h-[500px] bg-white border border-gray-300 rounded-lg shadow-md overflow-y-auto overflow-x-hidden"
    ></div>

    <!-- Suggest a change button -->
    <div class="flex justify-center mt-6">
      <button on:click={suggestChange} class="btn btn-primary">
        Suggest a Change
      </button>
    </div>
  {:else}
    <p class="text-center text-gray-500">Loading tab data...</p>
  {/if}
</div>
