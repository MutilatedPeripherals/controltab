// types/alphatab.d.ts
declare interface Window {
  alphaTab: {
    AlphaTabApi: new (
      container: HTMLElement,
      settings: AlphaTabSettings
    ) => AlphaTabApi;
  };
}

interface AlphaTabSettings {
  file?: string;
  core?: {
    engine?: string;
  };
  display?: {
    layoutMode?: number;
    barsPerRow?: number;
  };
}

interface AlphaTabApi {
  scoreLoaded: {
    on: (callback: (score: Score) => void) => void;
  };
  postRenderFinished: {
    on: (callback: () => void) => void;
  };
  renderTracks: (tracks: Track[]) => void;
  print: (
    element?: undefined,
    settings?: { display: { barsPerRow: number } }
  ) => void;
}

interface Score {
  tracks: Track[];
}

interface Track {
  name?: string;
  shortName?: string;
}
