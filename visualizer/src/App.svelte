<script lang="ts">
  import { onMount } from "svelte";

  let leftTab, rightTab;
  let api: any = undefined;

  /*onMount(() => {
    const leftOptions = { file: "path/to/main-version.xml", cursor: true };
    const rightOptions = { file: "path/to/modified-version.xml", cursor: true };
    console.log(alphaTab);

    leftTab = new alphaTab.AlphaTabApi(
      document.querySelector("#leftTab"),
      leftOptions
    );
    rightTab = new alphaTab.AlphaTabApi(
      document.querySelector("#rightTab"),
      rightOptions
    );
  });*/

  onMount(async () => {
    if (!window.alphaTab) {
      console.error("AlphaTab not loaded");
      return;
    }
    let target = document.querySelector("#leftTab");
    api = new window.alphaTab.AlphaTabApi(target, {
      file: "test.gp",
      //file: "guitar_pro_export_test.xml",
    });
  });
</script>

<div
  class="flex flex-col lg:flex-row justify-center items-center h-screen p-4 space-y-4 lg:space-y-0 lg:space-x-4"
>
  <div
    id="leftTab"
    class="w-full lg:w-1/2 h-full bg-gray-100 border border-gray-300 rounded-lg shadow-md overflow-hidden"
  ></div>
  <div
    id="rightTab"
    class="w-full lg:w-1/2 h-full bg-gray-100 border border-gray-300 rounded-lg shadow-md overflow-hidden"
  ></div>
</div>
