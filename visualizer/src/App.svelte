<script lang="ts">
  import { onMount, afterUpdate } from "svelte";
  import TabBarPair from "./TabBarPair.svelte";

  let apiData: number[] = [];

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

  onMount(async () => {
    await callApi();
  });


</script>

<div class="flex flex-col">
  {#each apiData as masterBar}
    <TabBarPair {masterBar}/>
  {/each}
</div>