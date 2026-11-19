# One sentence to production

Source: first-party skills on this account, settled 2026-11-16 in the Curse of Strahd production-skills inventory. This is a Barovia-quality bar, not Barovia content.

Rule. To take one sentence to a production-level narrative world, follow these eight steps and the skills named for each. Do not invent a second path beside this one, and do not use `game-maker-pipeline` as the conductor.

1. Intent and scope — `intake-intent-scope`
2. World bible and slice lock — `core-rule-book` (repo: world-bible), `rpg-campaign-maker` C0
3. Script breakdown and quest chains — `rpg-campaign-maker` C1–C2, `mesh-rpg-craft` M6
4. Art direction and mock — `mesh-rpg-craft` M0, `cotny-style-narrative-ui`, `reverse-game-maker`
5. Asset production (portraits, bulk assets, video) — `mesh-rpg-craft` M1–M5, `world-bible-pack`, `cinematic-video-assets`; `pixverse-r1` is optional runtime
6. Performance and voice — `mesh-rpg-craft` M7–M8, `narrative-voice-production`
7. Playable shell and playtest — `rpg-campaign-maker` C3/C5, `mesh-rpg-craft` M9, `doki-game-maker`
8. Packaging, shipping, and QA — `doki-game-maker`, `dokiimport`, `world-ship-qa`

Twelve of the sixteen skills live in `skills/`. `world-bible`, `world-bible-pack`, and `rpg-campaign-maker` stay in their own repos and are not recopied here. `dokiworld-ui-taste` and `game-maker-pipeline` are support skills, not the conductor. `one-sentence-conductor` is not written yet; do not start it unasked.

Shell, QA, and LOOK gates now live in the named skills (do not invent a side path): for `doki-mesh-world`, C3 reuses the named DokiDemo GameShell and must not substitute a paper walk/look/talk page; C5 and `world-ship-qa` require frame-by-frame parity with the shipped Strahd AVG on that shell, including internal previews; `mesh-rpg-craft` generates from the locked LOOK plus a spatial checklist, must not use a failed plate as the next generate ref, and remounts accepted art into the live pack while retiring superseded anchors.

Leave. Do not vendor GodotPrompter engine modules into this path. A campaign lock stays in that campaign. Public release still has to pass the slice lock's IP / skin-change gate.
