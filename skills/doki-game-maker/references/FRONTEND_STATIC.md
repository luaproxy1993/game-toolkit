# Frontend-static 实战铁律

来自 heartbeat-70 / 爱花包迭代；v2.1 补充 stream-client 降级约定。

## 入口

- **主入口：`packs/<slug>/index.html`（pack 根）**
- `play/index.html` 仅兼容重定向到 `../index.html`
- 挂载：`/game-packs/<slug>/index.html?host=bridge|static|auto`

## 路径

```js
// 页在根 → PACK_BASE = .
// 页在 play/ → PACK_BASE = ..
assets/…  mechanics/data/…  相对 pack 根
```

## 对话

1. `host=bridge` / iframe → `dokiworld-pack-chat`  
2. 本地 `npm start` → `/api/manaka/chat`（可选）  
3. 无后端 → 脚本降级；**日程必须仍可玩**

## UI

- **禁止**再画 Dokiworld 顶栏（Logo / Download / Library / 假大厅）
- 游戏 HUD 可放在内容区小工具条
- 小机制（电台等）浮动控件，配置进 `mechanics/data/*.json`

## 生产 vs 本地

| | 生产 | 本地 |
|--|------|------|
| 静态 assets+play | ✅ | ✅ |
| server/ Node 代理 | ❌ | ✅ 预览 LLM / R1 HTTP |
| config.local.json / .env | ❌ 进仓 | ✅ gitignore |
| PIXVERSE_API_KEY | 仅宿主 BFF | 仅 env / 本地 server |

## 导出

```bash
# pack 内
./scripts/export-frontend-static.sh
# → dist/frontend-static/<slug>/
# rsync → frontend/public/game-packs/<slug>/
# 必须排除：server/、.env*、pixverse_r1_session.json、*token*
```

验收：`python3 -m http.server` 在 pack 根打开 `index.html?host=static`，资源 200。

## stream-client（R1）补充

- **入口规则不变**：仍是根 `index.html`  
- `host=static`：允许只出壳 + 「需 bridge / 代理才能进实时世界」  
- `host=bridge`：stream-open → 宿主下发 Agora → pack 出画  
- 播放器与导播 UI 可放 `play/r1-stream.js`；配置 `mechanics/data/r1_world.json`  
- **不要**为了 R1 把主入口改成独立 React 工程路径而不挂卡带 id  
- 完整契约：`PIXVERSE_R1_RUNTIME.md`；API 细节：`~/.grok/skills/pixverse-r1/`
