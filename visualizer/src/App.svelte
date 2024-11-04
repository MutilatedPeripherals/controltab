<script lang="ts">
  import { onMount } from "svelte";

  let api: any = undefined;
  let newApi: any = undefined;
  let apiData: number[] = [];

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
      api = new window.alphaTab.AlphaTabApi(newTabContainer, {
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

      newApi = new window.alphaTab.AlphaTabApi(newTabContainerNew, {
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

      const getStringsAndFrets = (bar: any) => {
        const stringsAndFrets = [];
        for (const voice of bar.voices) {
          for (const beat of voice.beats) {
            for (const note of beat.notes) {
              stringsAndFrets.push({
                string: note.string,
                fret: note.fret,
                beatId: beat.id,
              });
            }
          }
        }
        return stringsAndFrets;
      };

      api.renderFinished.on(() => {
        console.log("Rendering finished for new.gp");
        const score = api.score;
        const track = score.tracks[0];
        const stave = track.staves[0];
        const bar = stave.bars[masterBar];
        console.log(getStringsAndFrets(bar));

        for (let voiceIndex = 0; voiceIndex < bar.voices.length; voiceIndex++) {
          const voice = bar.voices[voiceIndex];

          for (let beatIndex = 0; beatIndex < voice.beats.length; beatIndex++) {
            const beat = voice.beats[beatIndex];

            // Access the corresponding beat in newApi by using the same indices
            const otherTabBeat =
              newApi.score.tracks[0].staves[0].bars[bar.index].voices[
                voiceIndex
              ].beats[beatIndex];
            //console.log("tab 1", beat)
            //console.log("tab 2", otherTabBeat)
            // You can now work with both `beat` and `otherTabBeat`
            if (
              JSON.stringify(
                beat.notes.map((note) => ({
                  string: note.string,
                  fret: note.fret,
                }))
              ) ===
              JSON.stringify(
                otherTabBeat.notes.map((note) => ({
                  string: note.string,
                  fret: note.fret,
                }))
              )
            ) {
            } else {
              console.log(
                "The beats have different notes (string or fret mismatch).",
                beat.id
              );
              // paint the beat red
              // document.querySelectorAll(".b9188 text").forEach((element) => {
              //   element.style.fill = "red";
              //});
              document.querySelectorAll(`.b${beat.id}`).forEach((element) => {
                debugger;
                element.style.fill = "red";
              });
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
  });
</script>

<div class="flex">
  <div id="tabsContainer" class=""></div>
  <div id="tabsContainerNew"></div>
</div>
