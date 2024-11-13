<script lang="ts">
  import { onMount } from "svelte";
  import { modifiedBars } from "../stores/modifiedBars";
  import "@coderline/alphatab";
  import { useConfirmTabChange } from "../mutations/updateTabMutation";
  import { push } from "svelte-spa-router";
  import { Button } from "$lib/components/ui/button";
  import { Alert, AlertDescription } from "$lib/components/ui/alert";
  import { Card, CardHeader, CardContent } from "$lib/components/ui/card";
  import { AlertTriangle } from "lucide-svelte";

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
          push(`/tabs/${songId}`);
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
  <!-- Alert for Legacy Notice -->
  <Alert
    class="flex items-center bg-yellow-100 border border-yellow-300 text-yellow-800 p-4 rounded-lg mb-6"
  >
    <AlertTriangle class="w-5 h-5 mr-2" />
    <AlertDescription class="text-center font-semibold">
      Welcome to the legacy version of the tab visualizer! 🚀 Exciting updates
      are on the horizon: soon, you’ll be able to manage tab versions, review
      changes, leave comments, and collaborate just like a pro. Stay tuned—your
      ultimate tab management experience is coming soon!
    </AlertDescription>
  </Alert>

  <h2 class="text-3xl font-semibold text-center mb-8 text-gray-800">
    Visualize Original and Uploaded Tabs
  </h2>

  <!-- Tab Visualization Cards -->
  <div class="flex flex-col md:flex-row justify-center gap-6">
    <!-- Original Tab Card -->
    <Card class="w-full max-w-lg shadow-lg">
      <CardHeader>
        <h3 class="text-xl font-medium text-center text-gray-700">
          Original Tab
        </h3>
      </CardHeader>
      <CardContent>
        <div
          bind:this={originalContainer}
          class="w-full h-[500px] border border-gray-300 rounded-md overflow-y-auto"
        ></div>
      </CardContent>
    </Card>

    <!-- Uploaded Tab Card -->
    <Card class="w-full max-w-lg shadow-lg">
      <CardHeader>
        <h3 class="text-xl font-medium text-center text-gray-700">
          Uploaded Tab
        </h3>
      </CardHeader>
      <CardContent>
        <div
          bind:this={uploadedContainer}
          class="w-full h-[500px] border border-gray-300 rounded-md overflow-y-auto"
        ></div>
      </CardContent>
    </Card>
  </div>

  <!-- Confirm Changes Button -->
  <div class="flex justify-center mt-8">
    <Button on:click={confirmChanges} class="px-6 py-2 font-semibold">
      Confirm Changes
    </Button>
  </div>
</div>
