<script lang="ts">
  import { onMount } from "svelte";

  let api: any = undefined;
  let apiData: number[] = [];

  // Function to call the API
  async function callApi() {
    try {
      const response = await fetch("http://127.0.0.1:8000/");
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      console.log("API Response:", data);
      apiData = data;
    } catch (error) {
      console.error("Error calling API:", error);
    }
  }

  async function renderTabs() {
    if (!window.alphaTab) {
      console.error("AlphaTab not loaded");
      return;
    }

    const container = document.querySelector("#tabsContainer");
    if (!container) {
      console.error("Tabs container not found");
      return;
    }

    const containerNew = document.querySelector("#tabsContainerNew");
    if (!containerNew) {
      console.error("Tabs container not found");
      return;
    }

    for (const bar of apiData) {
      // Create a new container for each bar
      const newTabContainer = document.createElement("div");
      newTabContainer.className = "w-[800px] h-[450px] bg-gray-100 border border-gray-300 rounded-lg shadow-md overflow-hidden mb-4";
      container.appendChild(newTabContainer);

      const newTabContainerNew = document.createElement("div");
      newTabContainerNew.className = "w-[800px] h-[450px] bg-gray-100 border border-gray-300 rounded-lg shadow-md overflow-hidden mb-4";
      containerNew.appendChild(newTabContainerNew);

      // Rendering each bar
      api = new window.alphaTab.AlphaTabApi(newTabContainer, {
        file: "Empty.gp",
        displayBarRange: true,
        startBar: bar,
        barCount: 1,
        notation: {
          elements: {
            ScoreTitle: false,
            ScoreSubTitle: false,
            ScoreArtist: false,
            GuitarTuning: false,
            TrackNames: false,
            EffectMarker: false,
          },
        },
      });

      new window.alphaTab.AlphaTabApi(newTabContainerNew, {
        file: "Empty2.gp",
        displayBarRange: true,
        startBar: bar,
        barCount: 1,
        notation: {
          elements: {
            ScoreTitle: false,
            ScoreSubTitle: false,
            ScoreArtist: false,
            GuitarTuning: false,
            TrackNames: false,
            EffectMarker: false,
          },
        },
      });
      await new Promise(resolve => setTimeout(resolve, 500)); // delay for rendering
    }
  }

  onMount(async () => {
    // Call the API
    await callApi();
    // Render tabs using the response data
    await renderTabs();
  });
</script>

<div class="flex">
  <div
  id="tabsContainer"
  class=""
></div>
<div id="tabsContainerNew"></div>
</div>
