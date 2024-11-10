<script lang="ts">
  import { push } from "svelte-spa-router";
  import { useFetchTabs } from "../queries/getTabsQuery";
  import type { Tab } from "../types/TabTypes";

  let data: Tab[] | undefined;
  let isLoading = false;
  let isError = false;
  let error: Error | null = null;

  const tabsQuery = useFetchTabs();
  $: ({ data, isLoading, isError, error } = $tabsQuery);

  function viewTab(id: number) {
    push(`/tabs/${id}`);
  }

  function exportToPDF(id: number) {
    console.log("Exporting tab to PDF with id:", id);
  }

  function suggestChange(id: number) {
    console.log("Suggesting a change for tab with id:", id);
    push(`/tabs/${id}/compare`);
  }
</script>

<div class="container mx-auto p-6 bg-base-200 min-h-screen rounded-lg">
  <h1 class="text-3xl font-semibold text-center mb-8 text-gray-800">
    Guitar Tabs
  </h1>

  {#if isLoading}
    <p class="text-center text-gray-500">Loading tabs...</p>
  {:else if isError}
    <p class="text-center text-red-500">
      Failed to load tabs: {error?.message}
    </p>
  {:else if data}
    <div class="grid gap-6">
      {#each data as tab (tab.id)}
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
  {/if}
</div>
