<script lang="ts">
  import { onMount, tick } from "svelte";

  export let masterBar: number;
  
  let leftTabRenderer: any = undefined;
  let rightTabRenderer: any = undefined;
  let redBeats: number[] = [];
  let greenBeats: number[] = [];

  const areBeatsDifferent = (beat1: any, beat2: any) => {
    return JSON.stringify(
      beat1.notes.map((note) => ({
        string: note.string,
        fret: note.fret,
      }))
    ) !== JSON.stringify(
      beat2.notes.map((note) => ({ 
        string: note.string, 
        fret: note.fret 
      }))
    );
  };

  async function renderBarPair() {
    if (!window.alphaTab) {
      console.error("AlphaTab not loaded");
      return;
    }

    const commonSettings = {
      displayBarRange: true,
      tracks: [0, 1],
      startBar: masterBar + 1,
      barCount: 1,
      core: {
        engine: "svg"
      },
      rendering: {
        useWorkers: false,
        virtualization: "off"
      },
      notation: {
        elements: {
          ScoreTitle: false,
          ScoreSubTitle: false,
          ScoreArtist: false,
          GuitarTuning: false,
          TrackNames: false,
          EffectMarker: false
        },
      },
    };

    leftTabRenderer = new window.alphaTab.AlphaTabApi(leftContainer, {
      ...commonSettings,
      file: "old.gp"
    });

    rightTabRenderer = new window.alphaTab.AlphaTabApi(rightContainer, {
      ...commonSettings,
      file: "new.gp"
    });

    let hasProcessedBeats = false;

    rightTabRenderer.postRenderFinished.on(async () => {
      if (hasProcessedBeats) return;
      hasProcessedBeats = true;

      const score = leftTabRenderer.score;
      const track = score.tracks[0];
      const stave = track.staves[0];
      const bar = stave.bars[masterBar];

      for (let voiceIndex = 0; voiceIndex < bar.voices.length; voiceIndex++) {
        const voice = bar.voices[voiceIndex];

        for (let beatIndex = 0; beatIndex < voice.beats.length; beatIndex++) {
          const leftTabBeat = voice.beats[beatIndex];
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
          }
        }
      }
      await new Promise(resolve => setTimeout(resolve, 500));
      paintBeats();
    });
  }

  function paintBeats() {
    for (const beatId of redBeats) {
        const elements = document.querySelectorAll(`.b${beatId}`);
        if (elements.length === 0) {
            console.warn(`No elements found for red beat ID: ${beatId}`);
            continue;
        }
        elements.forEach((element) => {
            element.setAttribute("style", "fill: red");
        });
    }

    for (const beatId of greenBeats) {
        const elements = document.querySelectorAll(`.b${beatId}`);
        if (elements.length === 0) {
            console.warn(`No elements found for green beat ID: ${beatId}`);
            continue;
        }
        elements.forEach((element) => {
            element.setAttribute("style", "fill: #09ad09");
        });
    }
  }

  let leftContainer: HTMLDivElement;
  let rightContainer: HTMLDivElement;

  onMount(async () => {
    await renderBarPair();
  });
</script>

<div class="flex flex-row items-center justify-center gap-2">
  <div 
    bind:this={leftContainer}
    class="w-[600px] h-[420px] bg-gray-100 border border-gray-300 rounded-lg shadow-md overflow-hidden"
  ></div>
  <div 
    bind:this={rightContainer}
    class="w-[600px] h-[420px] bg-gray-100 border border-gray-300 rounded-lg shadow-md overflow-hidden"
  ></div>
</div> 