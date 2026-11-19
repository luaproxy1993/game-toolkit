---
name: dokiimport
description: >
  DokiWorld 外部 App / World 接入与交付（App SDK 规范）：用 @dokiworld/app-sdk
  生成/校验 manifest.json、npm 工程、esbuild dist/、createAppClient 生命周期、
  Game selection 自包含 manifest、World 无 selection、本地 sync 与 game-admin 上传。
  Use when the user runs /dokiimport, says "doki import", "接入 DokiWorld",
  "external app", "manifest.json 交付", "app-sdk", "dokiworld.app/2",
  "打包 game/world", "createAppClient", or wants to package a project like
  game-match3 / storyteller for DokiWorld host.
argument-hint: "[pack_path] [check|scaffold|manifest|build|export|handoff]"
user-invocable: true
metadata:
  short-description: DokiWorld App SDK 接入 / 交付
  version: "2.0.0"
  source_spec: "app-sdk-app-development.zh-CN.md + dokiworld-apps examples"
  examples:
    - "https://github.com/raptoravis/dokiworld-apps (game-match3 / storyteller / banquet-contract)"
    - "https://github.com/raptoravis/dokiworld-apps/blob/master/app-sdk-app-development.zh-CN.md"
---

# DokiImport — DokiWorld App SDK 接入 Skill

把本地 Game / World 收成 **DokiWorld 可加载的 App 交付物**（自包含 `dist/` + `manifest.json`）。

**完整规范（全文）：** `{SKILL_ROOT}/references/APP_SDK_APP_DEVELOPMENT.zh-CN.md`

**官方示例（优先对照）：**

| 类型 | 仓库路径 | 用途 |
|------|----------|------|
| Game | [game-match3](https://github.com/raptoravis/dokiworld-apps/tree/master/game-match3) | `createAppClient` + `createGameResult` |
| World（通用 Episode） | [storyteller](https://github.com/raptoravis/dokiworld-apps/tree/master/storyteller) | Episode / Dialogue / media 等 capability |
| World（定制） | [banquet-contract](https://github.com/raptoravis/dokiworld-apps/tree/master/banquet-contract) | 嵌套 Game + Episode |

**本地 reference 模板：**

- `references/example-manifest-game.json` — Game schema v2
- `references/example-manifest-world.json` — World schema v1 + runtime v2
- `references/example-app-client.js` — `createAppClient` 最小片段
- `references/CHECKLIST.md` — 验收清单

默认 `SKILL_ROOT` = `~/.grok/skills/dokiimport`

---

## 0. 调用

```text
/dokiimport
/dokiimport /path/to/app
/dokiimport check [app]
/dokiimport scaffold <app-id> [game|world]
/dokiimport manifest [app]        # 生成/校验 manifest.json（version 来自 package.json）
/dokiimport build [app]           # npm run build → dist/
/dokiimport export [app]          # 确认 dist/ 自包含可上传
/dokiimport handoff [app]         # 交付清单 + game-admin 上传提示
```

**用户一句话指令模板（可直接贴给 agent）：**

```text
# game
参考 https://github.com/raptoravis/dokiworld-apps/tree/master/game-match3
和 https://github.com/raptoravis/dokiworld/blob/dev/docs/app-sdk-app-development.zh-CN.md，
把本项目打包生成相应的 manifest.json 与 dist/

# world
参考 https://github.com/raptoravis/dokiworld-apps/tree/master/storyteller
和 https://github.com/raptoravis/dokiworld/blob/dev/docs/app-sdk-app-development.zh-CN.md，
把本项目打包生成相应的 manifest.json 与 dist/
```

Session 启动：

1. 读本 SKILL.md + `references/APP_SDK_APP_DEVELOPMENT.zh-CN.md`（§1–6、§8–12）
2. 定位 App 根（有 `package.json` + 源码；目标产物为 `dist/manifest.json`）
3. 判定 kind：`game` | `world`（对照示例）
4. **默认协议：`dokiworld.app/2` + `@dokiworld/app-sdk@^3.1.1`，manifest `schemaVersion: 3`**  
   不要手写 v1 `dokiworld-game-*` postMessage；不要再发布 schema v1/v2。
5. `todo_write`：manifest → SDK 接入 → build → zip → check → handoff

---

## 1. 架构铁律（相对旧规范的关键变化）

| 主题 | **新规范（现行）** | 旧 skill（已废弃默认） |
|------|-------------------|------------------------|
| 交付清单 | **`dist/manifest.json`** | `game.json` |
| 协议 | **`dokiworld.app/2`** | `dokiworld.game/1` |
| 通信 | **`createAppClient()`**，不手写 wire 字符串 | 手写 `postMessage` |
| Game 启停/选择 | **写在 Game manifest 内**（`status` + `selection`） | 归 DokiWorld `external-apps.json` |
| World 选择 | **禁止 `selection`** | 部分旧示例有 promptHint |
| 版本事实源 | **`package.json.version`** → 生成器写入 manifest | 手改 manifest |
| 工程形态 | 独立 npm 包 + esbuild/Vite 打 SDK 进 bundle | 纯静态目录 |
| 注册文件 | Game **不需要** `external-apps.json` | 需要 registration |

**禁止：**

- App 导入 DokiWorld `frontend/src` 或 backend 内部模块
- 手工编辑 `dist/`
- 发布时使用 `file:../../dokiworld...` 本地 SDK 依赖（联调后必须恢复公共 semver）
- 在 World manifest 写 `selection` 或内嵌角色副本
- 只上传改过的 JS、保留旧 manifest 版本

---

## 2. 推荐工程结构

```text
my-app/
├─ package.json                 # version = 发布版本唯一事实源
├─ package-lock.json
├─ manifest.json                # 源码 manifest（或 scripts 生成）
├─ index.html / src/
├─ scripts/
│  ├─ generate-manifest.mjs     # 读 package.json.version，写 manifest
│  └─ build.mjs                 # 清 dist → 拷资源 → esbuild 打 SDK
├─ tests/
└─ dist/                        # 交付物（自包含）
   ├─ manifest.json
   ├─ index.html
   ├─ *.js / *.css
   └─ assets/
```

`package.json` 最低要求：

```json
{
  "type": "module",
  "scripts": {
    "generate:manifest": "node scripts/generate-manifest.mjs",
    "test": "node --test tests/*.test.mjs",
    "build": "node scripts/build.mjs"
  },
  "dependencies": {
    "@dokiworld/app-sdk": "^2.1.0"
  },
  "devDependencies": {
    "esbuild": "^0.25.0"
  }
}
```

```bash
npm install "@dokiworld/app-sdk@^2.1.0" --save
```

构建必须把 SDK **内联进浏览器 bundle**；部署环境不装 npm。

---

## 3. Manifest

### 3.1 Game（schemaVersion: 2）

必填要点：

- `schemaVersion: 2`、`version`（= package）、`id`、`kind: "game"`
- `status`: `active` | `deprecated` | `disabled`
- `capability`（稳定英文 ID，如 `game.puzzle.match-three`）
- `entry`、`locales.en` + `locales.zh-cn`
- `selection.promptHint` **双语必填**；`activationPolicy`: `explicit` | `explicit-or-contextual`
- `context.requiredScopes` / `optionalScopes`
- `runtime.protocol: "dokiworld.app"`、`protocolVersion: 2`
- `runtime.input` + `runtime.outputs[]`（contract 名+version，**不内嵌 JSON Schema**）
- `launchRequirements.minPlayers` = **总参与方数**（去重 AI + 1 人类），不是 AI 座位数

完整形状见 `references/example-manifest-game.json`（对齐 game-match3）。

### 3.2 World（catalog 现用 schemaVersion: 1，runtime 仍 v2）

- `kind: "world"`、`status`、`entry`、`protocolVersion: 2`
- `runtime` 同 v2 形状；`episodeRenderer: true`（若渲染 Episode）
- scopes 字段名：`contextScopes.required` / `optional`（不是 `context.*`）
- **不得**声明 `selection`
- **不得**内嵌角色资料；角色来自 Host init 的 granted context
- 同步目标：`frontend/public/worlds/<id>/`

完整形状见 `references/example-manifest-world.json`（对齐 storyteller）。

### 3.3 生成器规则

1. 读 `package.json.version` 写入 `manifest.version`
2. 校验 `id`：小写字母/数字/连字符，且 = 目录名 = `createAppClient({ appId })`
3. Game：有双语 `selection.promptHint`；World：无 `selection`
4. `runtime.extensions` **只列真实创建/调用的** SDK extension
5. build 把同一 manifest 复制到 `dist/manifest.json`

---

## 4. SDK 生命周期（默认实现路径）

```js
import { createAppClient } from "@dokiworld/app-sdk";
import { createGameResult } from "@dokiworld/app-sdk/game-result"; // Game only

const app = createAppClient({
  appId: "my-game", // = manifest.id
  extensions: ["progress", "checkpoint"], // ⊆ manifest.runtime.extensions
});

app.connect({
  onInit: async ({ locale, context, input }) => {
    await startApp({ locale, context, options: input?.data });
  },
  onPrepareExit: () => ({
    isDirty: false,
    canSuspend: false,
    // Game 中途退出：exited outcome + 当时分数
    output: createGameResult({
      normalizedScore: currentScore,
      outcome: "exited",
      metrics: {},
    }),
  }),
  onExitDecision: (decision) => handleExitDecision(decision),
});

// 正常结束
await app.complete(createGameResult({
  normalizedScore: 82, // 0..100 整数
  outcome: "win",      // win | loss | draw | completed
  metrics: { points: 300 },
}));
```

协议保证（SDK 负责，业务代码不要重造）：

- ready 带 `appId` + App 生成的 `instanceId`；Host init 建立 `runId`
- `complete()` 稳定 `resultId` 重试，**收到 complete-ack 后**才算权威结算
- 关闭 iframe ≠ 完成；退出走 prepare-exit / exit-decision
- 不读 DokiWorld token / Cookie / 内部 HTTP

### 4.1 类型化 capability（四处一致）

每项扩展必须同时：

1. manifest `runtime.extensions` 声明  
2. `createAppClient({ extensions })` 声明  
3. 创建对应 client extension 并真实调用  
4. Host 侧已注册（发布环境）  

| 模块 | 用途 |
|------|------|
| `@dokiworld/app-sdk/dialogue` | 对话 / 开场 / 建议 |
| `@dokiworld/app-sdk/media` | 图/视频任务 |
| `@dokiworld/app-sdk/speech` | TTS |
| `@dokiworld/app-sdk/storage` | 隔离 checkpoint |
| `@dokiworld/app-sdk/character` | 当前角色 |
| `@dokiworld/app-sdk/persona` | 玩家 persona |
| `@dokiworld/app-sdk/apps` | 嵌套启动 v2 App |
| `@dokiworld/app-sdk/episode` | Episode 事件与游戏结果路由 |
| `@dokiworld/app-sdk/game-result` | `doki.game.result/1` |

未声明消息被拒；Host 未实现 → `unsupported-operation`。结束时释放 listener / timer / 嵌套 Host。

---

## 5. 构建与打包

顺序：

1. `npm run generate:manifest`（校验 + 同步 version）  
2. 清理重建 `dist/`  
3. esbuild/Vite 把源码 + SDK 打成浏览器 bundle  
4. 复制 HTML/CSS/manifest/全部运行资源  
5. 校验 `dist/manifest.json.entry` 存在且路径不逃出 `dist/`  

```text
dist/
├─ manifest.json
├─ index.html
├─ app.js / index.js
├─ styles.css
└─ assets/
```

相对路径资源（Vite：`base: "./"`）。禁止把 `.env`、token、私有模块、源码测试垃圾打进 dist。

```bash
cd <app>
npm install
npm run generate:manifest
npm test
npm run build
```

---

## 6. 本地同步 / 发布

### 6.1 本地联调（有 DokiWorld 主仓时）

```bash
cd <dokiworld-main>
export DOKIWORLD_EXT_ROOT="<path-to-dokiworld-apps-or-your-apps-root>"
npm run sync:local-apps
# 清理：npm run sync:clean-apps
# 仅 catalog：npm run generate:catalogs --workspace dokiworld-chat-mvp
```

同步脚本会 build 各 App，按 `kind` 拷到 `frontend/public/games/<id>/` 或 `worlds/<id>/`，再生成 catalog。**不要手改** public catalog。

### 6.2 管理端上传

- 入口：`https://dev.aimeng.ai/game-admin` 或 `https://test.aimeng.ai/game-admin`
- 指引：DokiWorld 仓 `docs/game-admin-guide.md`（若可访问）
- 上传 **完整 `dist/`**（含 manifest），版本与 package 一致

### 6.3 发布一次变更

1.  bump `package.json.version`  
2. contract 不兼容时才升 contract version  
3. 锁定 SDK + 提交 lockfile  
4. generate + test + build  
5. 检查 package / 源码 manifest / `dist/manifest.json` 版本一致  
6. 上传完整 dist 或更新静态源  
7. 真实 Host：启动 → 完成/中途退出 → cleanup  

四个版本维度独立：App version、manifest schema、runtime protocol、业务 contract。

---

## 7. Agent 工作流

### `check [app]`

输出表格对照 `references/CHECKLIST.md`：

- [ ] id = 目录名 = `createAppClient` appId  
- [ ] package / manifest / dist 版本一致  
- [ ] Game：status + 双语 selection.promptHint + result contract  
- [ ] World：无 selection、无角色副本  
- [ ] extensions 三处一致且有真实调用  
- [ ] scopes 缺失有降级  
- [ ] complete / exited / cleanup 有路径  
- [ ] en + zh-cn  
- [ ] dist 自包含、无 secret  

### `scaffold <app-id> [game|world]`

从对应示例骨架创建：package.json、manifest、generate/build 脚本、最小 `createAppClient` 入口、tests 占位。

### `manifest [app]`

生成或升级 `manifest.json`（Game v2 / World v1+runtime2），version 从 package 写入。

### `build` / `export`

跑 `npm run build`；确认 `dist/` 可 zip 上传；路径写入 handoff。

### `handoff [app]`

交付：

1. 完整 `dist/`（或 zip）  
2. `manifest.json` 摘要（id / kind / version / capability / scopes）  
3. SDK 与 extensions 列表  
4. 中英名称  
5. 本地 preview：`npx serve dist`（桥测需 Host / game-admin）  
6. 上传目标：game-admin 或 sync:local-apps  

---

## 8. 与创作 skill 的分工

| Skill | 职责 |
|-------|------|
| **doki-game-maker** / **galgame-maker** | 内容与玩法创作 |
| **dokiimport** | **宿主对接**：App SDK、manifest、build、验收、上传 |

典型顺序：做出可玩前端 → `/dokiimport scaffold|manifest|build|check|handoff`。

---

## 9. Session 输出格式

完成后给用户：

1. **kind** + **协议**：`dokiworld.app/2`  
2. **产物路径**：`dist/`  
3. **manifest 摘要**：id、version、capability、scopes、extensions  
4. **SDK 状态**：createAppClient / complete / exit 已接  
5. **未完成项**（Host registration、capability 宿主侧等）  
6. **下一步**：game-admin 上传或 `sync:local-apps`  

---

## 10. 一句话

> **交付自包含 dist/（manifest.json + 内联 app-sdk 的静态包）；Game 的 status/selection 写在 manifest 里；World 不写 selection、角色只来自 Host init；用 createAppClient，不要手写 v1 postMessage。**

---

## 11. Legacy（仅维护旧包时）

若目标宿主仍是纯 `dokiworld.game/1` 且无法升级：

- 旧文档曾用 `game.json` + 手写 ready/init/result  
- **新项目禁止**以此为默认  
- 迁移：schema 可先 v2，runtime 改为 `dokiworld.app/2`，桥改为 `createAppClient`  

旧文件若仍存在于历史 pack，可只读参考，不要再复制为新交付模板。
