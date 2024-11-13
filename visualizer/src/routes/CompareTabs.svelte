<script lang="ts">
  import { push } from "svelte-spa-router";
  import { modifiedBars } from "../stores/modifiedBars";
  import {
    useUploadTab,
    type CompareResponse,
  } from "../mutations/uploadTabMutation";
  import { writable } from "svelte/store";
  import { Button } from "$lib/components/ui/button";
  import { Card, CardContent } from "$lib/components/ui/card";
  import { Alert, AlertDescription } from "$lib/components/ui/alert";
  import { FilePlus } from "lucide-svelte";

  export let params: { id: number };

  let selectedFile: File | null = null;
  let isDragging = writable(false);
  let errorMessage: string = "";
  let songId: number = params.id;
  let fileInput: HTMLInputElement;

  const uploadMutation = useUploadTab(songId);

  function handleFileChange(event: Event): void {
    const target = event.target as HTMLInputElement;
    const file = target.files ? target.files[0] : null;
    validateAndSetFile(file);
  }

  function validateAndSetFile(file: File | null): void {
    if (file && file.name.endsWith(".gp")) {
      selectedFile = file;
      errorMessage = "";
    } else {
      selectedFile = null;
      errorMessage = "Please upload a valid .gp file.";
    }
  }

  function handleUpload() {
    if (!selectedFile) {
      errorMessage = "No file selected.";
      return;
    }

    const formData = new FormData();
    formData.append("user_tab", selectedFile);

    $uploadMutation.mutate(formData, {
      onSuccess: (data: CompareResponse) => {
        modifiedBars.set({
          comparison_result: data.comparison_result,
          originalTabUrl: data.original_file_url,
          uploadedTabUrl: data.uploaded_file_url,
          songId: songId,
        });
        selectedFile = null;
        push("/visualizer-legacy");
      },
      onError: (error) => {
        console.error("Error uploading file:", error);
        errorMessage = "File upload failed. Please try again.";
      },
    });
  }
</script>

<div class="container mx-auto p-6 bg-base-200 min-h-screen rounded-lg">
  <h2 class="text-3xl font-semibold text-center mb-8 text-gray-800">
    Upload a .gp File
  </h2>

  <Card class="p-6 mb-6">
    <CardContent class="flex flex-col items-center space-y-4">
      <p class="text-gray-500 text-center">
        Drag and drop a .gp file here or click to select
      </p>

      <input
        type="file"
        accept=".gp"
        on:change={handleFileChange}
        class="hidden"
        bind:this={fileInput}
      />

      <Button
        variant="outline"
        on:click={() => fileInput.click()}
        class="flex items-center gap-2"
      >
        <FilePlus class="w-5 h-5" />
        Choose File
      </Button>

      {#if selectedFile}
        <p class="text-gray-700 mt-2">Selected file: {selectedFile.name}</p>
      {/if}

      {#if errorMessage}
        <Alert variant="destructive">
          <AlertDescription>{errorMessage}</AlertDescription>
        </Alert>
      {/if}
    </CardContent>
  </Card>

  <!-- Upload Button -->
  <div class="flex justify-center mt-6">
    <Button
      on:click={handleUpload}
      disabled={!selectedFile || $uploadMutation.isPending}
    >
      {#if $uploadMutation.isPending}Uploading...{:else}Upload File{/if}
    </Button>
  </div>
</div>
