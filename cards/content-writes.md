# Content writes

Source: https://github.com/nightquill/rpgmaker-agent-skills — MIT, pushed 2026-04-22. RPG Maker projects break when IDs shift. Their tools dry-run first and write a backup before a change.

Rule. A content write touches one pack. Show the dry effect, or compile that pack alone. Record the other pack's file timestamp before the write and require it unchanged after. Do not reorder rows so that later references point at a different entity.

Leave. Do not import RPG Maker's JSON layout. The lesson is the write discipline, not the engine.
