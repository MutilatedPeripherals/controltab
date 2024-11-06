<script lang="ts">
  import { onMount, afterUpdate } from "svelte";
  import TabBarPair from "./TabBarPair.svelte";

  let apiData: number[] = [];
  let currentPage = 0;
  let paginatedData: number[] = [];
  const itemsPerPage = 2;

  async function callApi() {
    // TODO: replace with new endpoint that returns :\
    /*
      {
            "download_paths":  [
              [
                "old",
                "someurl.com"
              ],
              [
                "new",
                "someurl.com"
              ]
            ],
            "masterbar_diffs": [1,3,4,56,7]
        }
     */
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

  onMount(async () => {
    await callApi();
  });

  $: {
    paginatedData = apiData.slice(
      currentPage * itemsPerPage,
      (currentPage + 1) * itemsPerPage
    );
  }

  $: totalPages = Math.ceil(apiData.length / itemsPerPage);

  function nextPage() {
    if (currentPage < totalPages - 1) {
      currentPage += 1;
    }
  }

  function previousPage() {
    if (currentPage > 0) {
      currentPage -= 1;
    }
  }
</script>

<div class="flex flex-col gap-2 p-4">
  <div class="flex flex-col gap-2">
    {#each paginatedData as masterBar (masterBar)}
      <TabBarPair {masterBar}/>
    {/each}
  </div>

  <div class="flex justify-center gap-4 py-2 mt-2">
    <button 
      class="px-4 py-1 bg-blue-500 text-white rounded disabled:bg-gray-300" 
      on:click={previousPage} 
      disabled={currentPage === 0}
    >
      Previous
    </button>
    <span class="py-1">Page {currentPage + 1} of {totalPages}</span>
    <button 
      class="px-4 py-1 bg-blue-500 text-white rounded disabled:bg-gray-300" 
      on:click={nextPage} 
      disabled={currentPage === totalPages - 1}
    >
      Next
    </button>
  </div>
</div>