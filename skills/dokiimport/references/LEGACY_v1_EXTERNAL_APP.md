# Legacy：旧版 external App 接入（dokiworld.game/1）

> **新项目不要使用本文。** 现行规范见 `APP_SDK_APP_DEVELOPMENT.zh-CN.md` 与 skill 主文档。
> 仅当维护无法升级的旧 pack 时查阅。

## 与现行规范的差异摘要

| 项 | Legacy v1 | 现行 App SDK |
|----|-----------|--------------|
| 清单文件 | `game.json` | `dist/manifest.json` |
| 协议 | `dokiworld.game/1` | `dokiworld.app/2` |
| 通信 | 手写 `postMessage` | `@dokiworld/app-sdk` `createAppClient` |
| Game status/selection | 常在 `external-apps.json` | **写在 Game manifest** |
| 交付 | `frontend/public/games/<id>/` 静态树 | 独立 npm 包 build → `dist/` |

## 旧消息名（仅对照）

```text
dokiworld-game-ready → init → initialized → result / close
可选：dokiworld-pack-chat / pack-chat-result
```

## 迁移建议

1. 增加 `package.json` + `@dokiworld/app-sdk@^2.1.0`
2. 将 `game.json` 改为符合 Game schema v2 或 World schema 的 `manifest.json`（含 `status`/`selection` 规则）
3. 用 `createAppClient` 替换手写桥；Game 结算改 `createGameResult` + `complete`
4. `npm run build` 产出自包含 `dist/`，走 game-admin 或 `sync:local-apps`

历史 skill 中的长文 `EXTERNAL_APP_INTEGRATION.zh-CN.md` 已移除。**生成新包时禁止复制 v1 交付规则**；一律走 App SDK 文档。
