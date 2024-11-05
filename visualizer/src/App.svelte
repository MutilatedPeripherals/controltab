<script lang="ts">
  import { onMount, tick } from "svelte";

  let leftTabRenderer: any = undefined;
  let rightTabRenderer: any = undefined;
  let apiData: number[] = [];
  let redBeats: number[] = [];
  let greenBeats: number[] = [];

  const getStringsAndFrets = (bar: any) => {
    const stringsAndFrets = [];
    for (const voice of bar.voices) {
      for (const leftTabBeat of voice.beats) {
        for (const note of leftTabBeat.notes) {
          stringsAndFrets.push({
            string: note.string,
            fret: note.fret,
            beatId: leftTabBeat.id,
          });
        }
      }
    }
    return stringsAndFrets;
  };

  const areBeatsDifferent = (beat1: any, beat2: any) => {
    return JSON.stringify(
      beat1.notes.map((note) => ({
        string: note.string,
        fret: note.fret,
      }))
    ) !== JSON.stringify(
      beat2.notes.map((note) => ({ 
        string: note.string, 
        fret: note.fret }))
    );
  };

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

    for (const masterBar of apiData) {
      // Create a new container for each bar
      const newTabContainer = document.createElement("div");
      newTabContainer.className =
        "w-[800px] h-[450px] bg-gray-100 border border-gray-300 rounded-lg shadow-md overflow-hidden mb-4";
      container.appendChild(newTabContainer);

      const newTabContainerNew = document.createElement("div");
      newTabContainerNew.className =
        "w-[800px] h-[450px] bg-gray-100 border border-gray-300 rounded-lg shadow-md overflow-hidden mb-4";
      containerNew.appendChild(newTabContainerNew);

      // Rendering each bar
      leftTabRenderer = new window.alphaTab.AlphaTabApi(newTabContainer, {
        file: "old.gp",
        displayBarRange: true,
        startBar: masterBar + 1,
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

      rightTabRenderer = new window.alphaTab.AlphaTabApi(newTabContainerNew, {
        file: "new.gp",
        displayBarRange: true,
        startBar: masterBar + 1,
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

      leftTabRenderer.postRenderFinished.on(() => {
        console.log("Rendering finished for new.gp");
        const score = leftTabRenderer.score;
        const track = score.tracks[0];
        const stave = track.staves[0];
        const bar = stave.bars[masterBar];

        for (let voiceIndex = 0; voiceIndex < bar.voices.length; voiceIndex++) {
          const voice = bar.voices[voiceIndex];

          for (let beatIndex = 0; beatIndex < voice.beats.length; beatIndex++) {
            const leftTabBeat = voice.beats[beatIndex];

            // Access the corresponding leftTabBeat in rightTabRenderer by using the same indices
            const rightTabBeat =
              rightTabRenderer.score.tracks[0].staves[0].bars[bar.index].voices[
                voiceIndex
              ].beats[beatIndex];

              if (areBeatsDifferent(leftTabBeat, rightTabBeat)) {
              console.log(
                "The beats have different notes (string or fret mismatch).",
                leftTabBeat.id,
                rightTabBeat.id
              );
              redBeats.push(leftTabBeat.id);
              greenBeats.push(rightTabBeat.id);
              
              const leftElements = document.querySelectorAll(`.b${leftTabBeat.id}`);
              const rightElements = document.querySelectorAll(`.b${rightTabBeat.id}`);

              if (leftElements.length === 0) {
                console.warn(`No elements found with class .b${leftTabBeat.id} in leftTabRenderer.postRenderFinished`);
              }else{
                leftElements.forEach((element) => {
                  element.setAttribute("style", "fill: red");
                });
              }
              if (rightElements.length === 0) {
                console.warn(`No elements found with class .b${rightTabBeat.id} in rightTabRenderer.postRenderFinished`);
              }else{
                rightElements.forEach((element) => {
                  element.setAttribute("style", "fill: #09ad09");
                });
              }
            }
          }
        }
      });

      await new Promise((resolve) => setTimeout(resolve, 500)); // delay for rendering
    }
  }

  onMount(async () => {
    // Call the API
    await callApi();
    // Render tabs using the response data
    await renderTabs();

    // After component is mounted and rendered, paint beats
    await tick();

    for (const leftTabBeat of redBeats) {
      document.querySelectorAll(`.b${leftTabBeat}`).forEach((element) => {
        element.setAttribute("style", "fill: red");
      });
    }

    for (const leftTabBeat of greenBeats) {
      document.querySelectorAll(`.b${leftTabBeat}`).forEach((element) => {
        element.setAttribute("style", "fill: #09ad09");
      });
    }
  });

  
</script>

<div class="flex">
  <div id="tabsContainer" class=""></div>
  <div id="tabsContainerNew"></div>
</div>

<style>
  .note-fill-red {
    fill: red;
  }
</style>
