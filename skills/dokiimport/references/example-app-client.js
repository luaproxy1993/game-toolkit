/**
 * Minimal DokiWorld App SDK client (dokiworld.app/2).
 * Aligns with game-match3: createAppClient + createGameResult.
 * Do NOT hand-write dokiworld-game-* v1 postMessage wires for new apps.
 */
import { createAppClient } from "@dokiworld/app-sdk";
import { createGameResult } from "@dokiworld/app-sdk/game-result";

const APP_ID = "game-match3"; // must equal manifest.id and directory name

const app = createAppClient({
  appId: APP_ID,
  // Must match manifest.runtime.extensions and real usage below
  extensions: ["resize", "progress", "checkpoint"],
});

let score = 0;
let metrics = { points: 0, moves: 0 };

function normalizedScore(points) {
  return Math.max(0, Math.min(100, Math.round(points)));
}

function currentResult(outcome) {
  return createGameResult({
    normalizedScore: normalizedScore(score),
    outcome, // win | loss | draw | completed | exited
    metrics: { ...metrics },
  });
}

async function startGame({ locale, options }) {
  // apply locale, options from input.data, render UI...
  void locale;
  void options;
  score = 0;
  metrics = { points: 0, moves: 0 };
}

async function finishWin() {
  await app.complete(
    createGameResult({
      normalizedScore: normalizedScore(score),
      outcome: "win",
      metrics: { ...metrics },
    }),
  );
}

app.connect({
  onInit: async ({ locale, context, input }) => {
    void context;
    await startGame({
      locale,
      options: input?.data?.options ?? input?.data,
    });
  },
  onPrepareExit: () => ({
    isDirty: false,
    canSuspend: false,
    // Mid-session quit: report score with exited, do not fake "win"
    output: currentResult("exited"),
  }),
  onExitDecision: (decision) => {
    // stay | discard | suspend
    if (decision === "discard") {
      // cleanup UI / timers
    }
  },
});

// Example: optional resize extension message (only if declared)
// app.send("dokiworld-app-resize", { height: 640 });

export { app, finishWin };
