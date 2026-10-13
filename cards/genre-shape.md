# Genre shape

Source: https://github.com/gamedev-skills/awesome-gamedev-agent-skills — Apache-2.0. `skills/genres/rpg` and `skills/genres/visual-novel`, pushed 2026-10-09.

Rule. A genre skill composes. It names the primary loop and points at the skills that implement each primitive. It does not re-teach stats, dialogue, or saving.

One paradigm is primary. The others hang off it. A visual novel is mostly reading a branch. Dialogue inside a larger game is the RPG skill consuming the dialogue skill, not a second game.

Leave. Do not copy the 74 skills into this repo. Load upstream when the engine is Godot, Unity, Phaser, or another stack that repo already covers. This account's campaigns stay on their own runner unless a card says otherwise.
