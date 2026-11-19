# DokiImport 验收清单（App SDK / dokiworld.app/2）

对照 `APP_SDK_APP_DEVELOPMENT.zh-CN.md` §12 与官方示例 `game-match3` / `storyteller`。

## 身份与版本

- [ ] `id` 与目录名、`createAppClient({ appId })` 完全一致
- [ ] `id` 仅小写字母、数字、连字符
- [ ] `package.json.version` === 源码 `manifest.json.version` === `dist/manifest.json.version`
- [ ] `dist/manifest.json` 由 build 生成，不手工改 dist
- [ ] `entry`、`cover` 与全部运行资源在包内相对路径

## Game manifest

- [ ] `schemaVersion: 2`、`kind: "game"`
- [ ] `status` 为 `active` | `deprecated` | `disabled`
- [ ] `capability` 稳定、语言无关
- [ ] `selection.promptHint.en` 与 `selection.promptHint.zh-cn` 必填
- [ ] `activationPolicy` 为 `explicit` 或 `explicit-or-contextual`
- [ ] `runtime.protocol` = `dokiworld.app`，`protocolVersion` = `2`
- [ ] `runtime.input` + `runtime.outputs`（通常含 `doki.game.result` v1）
- [ ] `minPlayers` = 总参与方数（非 AI 座位数）

## World manifest

- [ ] `kind: "world"`（catalog 现用 `schemaVersion: 1`，runtime 仍 v2）
- [ ] **无** `selection`
- [ ] **无** 内嵌角色资料 / launchCharacter
- [ ] scopes 使用 `contextScopes.required` / `optional`
- [ ] 角色与 persona 仅来自 Host init 的 granted context

## SDK / 协议

- [ ] 使用 `@dokiworld/app-sdk`（建议 `^2.1.0`），SDK 打进 browser bundle
- [ ] **不**手写 v1 `dokiworld-game-*` wire（新项目）
- [ ] `runtime.extensions` ⊆ 实际 `createAppClient({ extensions })` ⊆ 真实调用
- [ ] `complete()` 等待 ack；中途退出用 `onPrepareExit` + `exited`（Game）
- [ ] 关闭 iframe 不伪装成功完成
- [ ] listener / timer / 嵌套 Host 在结束时释放

## 权限与 i18n

- [ ] required / optional scope 区分正确；optional 缺失可降级
- [ ] `locales.en` 与 `locales.zh-cn` 名称、描述（及 Game aliases / selection 文案）成对

## 安全与产物

- [ ] 可在 `sandbox="allow-scripts"`、无 `allow-same-origin` 下运行
- [ ] 不读父 DOM / Cookie / 未授权 API；不走私有 DokiWorld 模块
- [ ] `dist/` 无 secret、`.env`、token、绝对本机路径
- [ ] summary / error / output 不当 HTML、不当模型系统指令

## 联调 / 发布

- [ ] `npm test` + `npm run build` 通过
- [ ] 本地：`DOKIWORLD_EXT_ROOT=... npm run sync:local-apps` 或管理端上传完整 dist
- [ ] 真实 Host：启动 → 完成或中途退出 → 无 protocol/contract/scope 控制台错误
