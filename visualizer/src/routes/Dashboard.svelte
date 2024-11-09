<script>
  import { onMount } from "svelte";
  import { push } from "svelte-spa-router";

  let tabs = [];

  async function fetchTabs() {
    try {
      const response = await fetch("http://127.0.0.1:8000/tabs");
      if (!response.ok)
        throw new Error("Failed to fetch tabs from FastAPI service");
      tabs = await response.json();
    } catch (error) {
      console.error("Error fetching data from FastAPI:", error);
    }
  }

  onMount(fetchTabs);

  function viewTab(id) {
    push(`/tabs/${id}`);
  }

  function exportToPDF(id) {
    console.log("Exporting tab to PDF with id:", id);
  }

  function suggestChange(id) {
    console.log("Suggesting a change for tab with id:", id);
    push(`/tabs/${id}/compare`);
  }
</script>

<div class="container mx-auto p-6 bg-base-200 min-h-screen rounded-lg">
  <h1 class="text-3xl font-semibold text-center mb-8 text-gray-800">
    Guitar Tabs
  </h1>

  <div class="grid gap-6">
    {#each tabs as tab}
      <div class="card bg-base-100 shadow-lg p-4 rounded-lg">
        <div class="card-body">
          <h2 class="card-title text-lg font-medium text-gray-800">
            {tab.song_name}
          </h2>
          <p class="text-sm text-gray-600">Filename: {tab.filename}</p>
          <p class="text-sm text-gray-600">
            Uploaded at: {new Date(tab.uploaded_at).toLocaleString()}
          </p>
          <div class="mt-4 flex justify-end space-x-4">
            <button
              class="btn btn-outline btn-primary btn-sm"
              on:click={() => viewTab(tab.id)}
            >
              View Tab
            </button>
            <button
              class="btn btn-primary btn-sm"
              on:click={() => exportToPDF(tab.id)}
            >
              Export to PDF
            </button>
            <button
              class="btn btn-outline btn-secondary btn-sm"
              on:click={() => suggestChange(tab.id)}
            >
              Suggest a Change
            </button>
          </div>
        </div>
      </div>
    {/each}
  </div>
</div>
