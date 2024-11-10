<script lang="ts">
  import { push } from "svelte-spa-router";
  import { modifiedBars } from "../stores/modifiedBars";

  export let params: { id: number };

  let selectedFile: File | null = null;
  let isDragging: boolean = false;
  let errorMessage: string = "";
  let tabId: number = params.id;
  let fileInput: HTMLInputElement;

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

  async function handleUpload(): Promise<void> {
    if (!selectedFile) {
      errorMessage = "No file selected.";
      return;
    }

    const formData = new FormData();
    formData.append("user_tab", selectedFile);

    try {
      const response = await fetch(`http://127.0.0.1:8000/compare/${tabId}`, {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error("File upload failed");

      const data = await response.json();

      modifiedBars.set({
        comparison_result: data.comparison_result as number[],
        originalTabUrl: data.original_file_url as string,
        uploadedTabUrl: data.uploaded_file_url as string,
      });

      alert("File uploaded successfully!");
      selectedFile = null;

      push("/visualizer");
    } catch (error) {
      console.error("Error uploading file:", error);
      errorMessage = "File upload failed. Please try again.";
    }
  }

  function handleDragOver(event: DragEvent): void {
    event.preventDefault();
    isDragging = true;
  }

  function handleDragLeave(): void {
    isDragging = false;
  }

  function handleDrop(event: DragEvent): void {
    event.preventDefault();
    isDragging = false;
    const file = event.dataTransfer ? event.dataTransfer.files[0] : null;
    validateAndSetFile(file);
  }
</script>

<div class="container mx-auto p-6 bg-base-200 min-h-screen rounded-lg">
  <h2 class="text-3xl font-semibold text-center mb-8 text-gray-800">
    Upload a .gp File
  </h2>

  <div
    class="border-2 border-dashed border-gray-400 p-6 rounded-lg bg-white flex flex-col items-center justify-center space-y-4"
    on:dragover={handleDragOver}
    on:dragleave={handleDragLeave}
    on:drop={handleDrop}
    role="button"
    tabindex="0"
    class:isDragging
  >
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

    <button
      class="btn btn-outline btn-primary"
      on:click={() => fileInput.click()}
    >
      Choose File
    </button>

    {#if selectedFile}
      <p class="text-gray-700 mt-2">Selected file: {selectedFile.name}</p>
    {/if}

    {#if errorMessage}
      <p class="text-red-500 mt-2">{errorMessage}</p>
    {/if}
  </div>

  <div class="flex justify-center mt-6">
    <button
      class="btn btn-primary"
      on:click={handleUpload}
      disabled={!selectedFile}
    >
      Upload File
    </button>
  </div>
</div>

<style>
  .isDragging {
    background-color: #f0faff;
  }
</style>
