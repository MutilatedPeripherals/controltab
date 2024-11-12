<script lang="ts">
  import { onMount } from "svelte";
  import { modifiedBars } from "../stores/modifiedBars";
  import "@coderline/alphatab";
  import { useConfirmTabChange } from "../mutations/updateTabMutation";
  import { push } from "svelte-spa-router";

  let originalTabUrl = "";
  let uploadedTabUrl = "";
  let originalContainer: HTMLDivElement;
  let uploadedContainer: HTMLDivElement;
  let songId: number | undefined;

  const confirmTabChangeMutation = useConfirmTabChange();

  modifiedBars.subscribe((bars) => {
    originalTabUrl = bars.originalTabUrl;
    uploadedTabUrl = bars.uploadedTabUrl;
    songId = bars.songId;
  });

  function renderTab(container: HTMLDivElement, fileUrl: string) {
    const settings = {
      file: fileUrl,
      core: { engine: "svg" },
      display: { layoutMode: 0 },
      rendering: { useWorkers: false, virtualization: "off" },
      notation: { elements: { ScoreTitle: false } },
    };
    new window.alphaTab.AlphaTabApi(container, settings);
  }

  function confirmChanges() {
    if (!uploadedTabUrl || !songId) {
      return;
    }

    $confirmTabChangeMutation.mutate(
      { songId: songId, uploadedFileUrl: uploadedTabUrl },
      {
        onSuccess: () => {
          modifiedBars.update((bars) => ({ ...bars, uploadedTabUrl: "" }));
          push(`/tabs/${songId}`); // Redirect to the song's tab page
        },
      }
    );
  }

  onMount(() => {
    if (originalTabUrl && uploadedTabUrl) {
      renderTab(originalContainer, originalTabUrl);
      renderTab(uploadedContainer, uploadedTabUrl);
    }
  });
</script>

<div class="container mx-auto p-6 bg-base-200 min-h-screen rounded-lg">
  <div
    class="p-4 mb-6 text-yellow-800 bg-yellow-100 border border-yellow-300 rounded-lg"
  >
    <p class="text-center font-semibold">
      ⚠️ Welcome to the legacy version of the tab visualizer! 🚀 Exciting
      updates are on the horizon: soon, you’ll be able to manage tab versions,
      review changes, leave comments, and collaborate just like a pro. Stay
      tuned—your ultimate tab management experience is coming soon!
    </p>
  </div>

  <h2 class="text-3xl font-semibold text-center mb-8 text-gray-800">
    Visualize Original and Uploaded Tabs
  </h2>

  <div class="flex flex-col md:flex-row justify-center gap-6">
    <div
      class="flex flex-col items-center w-full max-w-lg p-4 bg-white rounded-lg shadow-lg"
    >
      <h3 class="text-xl font-medium text-center text-gray-700 mb-4">
        Original Tab
      </h3>
      <div
        bind:this={originalContainer}
        class="w-full h-[500px] border border-gray-300 rounded-md overflow-y-auto"
      ></div>
    </div>

    <div
      class="flex flex-col items-center w-full max-w-lg p-4 bg-white rounded-lg shadow-lg"
    >
      <h3 class="text-xl font-medium text-center text-gray-700 mb-4">
        Uploaded Tab
      </h3>
      <div
        bind:this={uploadedContainer}
        class="w-full h-[500px] border border-gray-300 rounded-md overflow-y-auto"
      ></div>
    </div>
  </div>

  <div class="flex justify-center mt-8">
    <button
      class="btn btn-primary px-6 py-2 font-semibold rounded-lg"
      on:click={confirmChanges}
    >
      Confirm Changes
    </button>
  </div>
</div>
