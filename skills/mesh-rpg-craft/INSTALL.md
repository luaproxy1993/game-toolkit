# Mesh RPG Craft — 安装

**v1.0.1** · Doki 魔改网状 RPG 的锁序与踩坑。分享用。和 `/rpg-campaign-maker` 的接法见 `references/HANDOFF.md`。

## 装

```bash
./install.sh
```

装到 `~/.grok/skills/mesh-rpg-craft/`。也可：

```bash
./install.sh --dir ~/.cursor/skills/mesh-rpg-craft
./install.sh --dir ./.grok/skills/mesh-rpg-craft --force
```

Grok 里应出现 `/mesh-rpg-craft`。

## 还需要哪些现成技能

本包**不替代**生成器。请同时装（若尚未）：

| 用途 | 技能 |
|------|------|
| 静帧默认 | `game-asset-core`（Grok bundled） |
| 同一张脸 | `game-character-consistency` |
| 视频再抽帧 | `game-animation-frames` |
| 世界书 | `world-bible` / `/core-rule-book` |
| 一切口树 | `rpg-campaign-maker` |
| 卡带封装 | `doki-game-maker` |
| 数字人 seed | `pixverse-r1` |

## 打分享包

```bash
./scripts/package.sh
```

得到 `dist/mesh-rpg-craft-v1.0.0.tar.gz`。对方：

```bash
tar -xzf mesh-rpg-craft-v1.0.0.tar.gz && cd mesh-rpg-craft-v1.0.0 && ./install.sh
```

## 卸

```bash
rm -rf ~/.grok/skills/mesh-rpg-craft
```
