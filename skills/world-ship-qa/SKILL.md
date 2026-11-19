---
name: world-ship-qa
description: >-
  包装发布与质检：在玩通 sitting 之后做独立世界包校验、加载门、资源全量抽查、游客冷启动路径、参考壳对等门和版本发布清单。
  For doki-mesh-world, a pack that only passes paths/loading/assets but is a
  thinner shell than the shipped Strahd AVG on DokiDemo is not a pass — including
  0.1.0-internal style previews. Use when the user runs /world-ship-qa, says 发布质检,
  出包检查, 游客路径, 加载幕就绪, 资源抽查, world pack QA, or is about to upload or version a
  narrative world/pack. Not for writing the pack or App SDK itself (those are
  /doki-game-maker and /dokiimport), and not a substitute for the campaign
  playtest gate.
---
# 包装发布与质检

内容能玩，还不等于能发。本 skill 是发布门：校验包的自立与路径、加载幕是否等到静帧就绪、资源是否全在、游客能否走完主链、是否与参考壳对等、版本号是否一致。它不发明第二种打包格式。

```text
试玩门已过（坐通这一局）
  → 包校验（清单、相对路径、自包含）
  → 加载门（板先盖住，静帧/入场片解码后再交手）
  → 资源全量抽查（无断链、无失败片、无密钥、无源书原文）
  → 游客冷启动实测
  → 参考壳对等（doki-mesh-world，含内部预览）
  → 版本与发布清单
  → STOP  ship: accept
```

打包与 SDK 的主人还在原处：

| 层 | 主人 |
|----|------|
| 卡带形状、导出静态树、合入分层、无密钥 handoff | `/doki-game-maker` D5/D6，`references/SHIP_CHECKLIST.md` |
| App SDK：`manifest.json`、相对路径、`dist/` 自包含、校验与上传手续 | `/dokiimport` `check` / `export` / `handoff`，`references/CHECKLIST.md` |
| 静态战役 `dist/` 树 | `/rpg-campaign-maker` C6 |
| 未玩通不得出包 | `/rpg-campaign-maker` C5；mesh 网状坐法同等试玩门 |

本 skill 在这些命令之后跑，或指出它们还没跑。不要把质检条目塞进 `dokiimport`，也不要在这里重写 manifest 字段表。

## 1. 命令

```
/world-ship-qa
/world-ship-qa preflight | pack | loading | audit | guest | release | accept
```

无参数：按清单做下一未过关项，然后 **STOP**。  
目标：用户指定的 pack / world / `dist/`；不要把资源写进平台仓根目录来「顺便发布」。

## 2. 步骤

### Q0 · 预检

**完成：** 下面全部为真，否则停手，不准做发布动作。

- 这一局已经玩通，C5 或等价试玩门已 accept。未玩通 sitting 不开打包，更不开上传。  
- `docs/LOCK.md`（或 INTENT 里已继承的切口）仍被遵守。  
- IP：`unofficial-remix` 若要**公开发布**（外链、商店页、预告、众筹），换皮门必须先过；内部预览包须标明非公开。源书 PDF、框文、官方美术不得在包内。这是设计门，不是法律意见。
- **换皮名单未点名时：** Q 门最多收到「内部预览」；不要把内部预览的 Q5 写成公开 `ship: accept`。公开候选须另列：换皮点名、配音非占位、质检目录=即将上传的那一份。  
- **占位配音：** `edge-tts` 等占位 VO 可以跟内部预览一起过（须在 CREDITS/SHIP 标明）。占位配音**不能**成为公开 `ship: accept`。  
- 导演/对话密钥只在本机环境或宿主代理，不在说明文档或 zip 里「随便传」。

本地试玩必须走 HTTP，不要 `file://`。预览壳 ≠ 已上传的正式包；不要在预览会话里动官方 zip。

**STOP** 若试玩门或 IP 门未过。

### Q1 · 包校验

**完成：** 按产品形态跑对应主人的检查，再补上下面的**独立世界包路径**门。

先跑：

- 世界 / App：`/dokiimport check`（id 与目录一致、version 三处一致、entry/cover/运行资源皆为包内相对路径、无 selection 的 World 规则、sandbox 约束、`dist/` 无 secret / `.env` / 本机绝对路径）  
- 卡带：`/doki-game-maker` 的导出与 `SHIP_CHECKLIST.md`（根 `index.html`、server 与密钥已剔除、handoff 标明非已上线成品）  
- 静态 sitting：C6 的 `dist/` 树（无 `node_modules`、无 `_raw`、无密钥）

独立世界包路径（发布实践里踩过的坑，写成门）：

- 资产与入口按**包根**解析（`PACK_BASE` 或等价），不要写死平台根目录、本机绝对路径、或把世界文件打进宿主仓库根。  
- 上传或同步时提交的是完整、自包含的 `dist/` / 世界包，而不是散落在宿主工程里的相对上级引用。  
- 预览目录与即将上传的目录分开；质检对即将上传的那份跑，不对「刚好能在本机打开的另一份」。

**STOP** `step Q1: accept`

### Q2 · 加载门

**完成：** 冷启动与缺图两种情况下，加载板都先盖住窗口，不把未解码的立绘/场景或半截包露出来。

对照（建议默认，毫秒可按壳调整）：

- [ ] 包开始跑之前，加载板已经盖住窗口  
- [ ] 立绘或场景静帧尚未解码时，板再次（或仍然）盖住  
- [ ] 将播放的 intro / 封面循环未就绪时，先用海报静帧，不闪黑、不把错误比例的图拉满  
- [ ] 交手是短交叉淡入；循环视频层和装饰盾层**不要**一直占着加载板（某世界实战交手约 720ms，可改，不可取消「等到就绪」）  
- [ ] `prefers-reduced-motion` 时停在静帧海报，板本身不消失  
- [ ] 标题/加载若复用封面 loop：视频加载一次并循环，海报是同一张静帧

加载幕美术方案本身用 mock 让作者挑，不在本步改设计。本步只验「发出版」是否遵守就绪门。未过则退回壳或 `/cinematic-video-assets` 补海报/loop，不靠上传后再补。

**STOP** `step Q2: accept`

### Q3 · 资源全量抽查

**完成：** 对照清单把将发布树里的引用走一遍，不是抽几张「看着好」。

- [ ] manifest / pack.json / 节点表 / 台词表 / 视频表引用的每个路径，在包内存在且相对包根有效  
- [ ] 没有失败 take、失败 i2v、研究用截图、官方 rip、源书扫描件进入发布树  
- [ ] 立绘透明通道与已锁 LOOK 一致（抠键则 RGBA/chroma；白纸底可不抠）；场景是原生画幅；视频有海报；公开发布时配音槽无占位残留（内部预览可保留占位并在 CREDITS/SHIP 标明）  
- [ ] 有音频则有 `CREDITS.md` 或等价署名  
- [ ] 无 API key、token、`.env`、本机会话文件  
- [ ] 缓存参数已 bump，硬刷新后看到的是新资产  
- [ ] 中英（或 LOCK 指定的语言）名称、描述、必要文案成对，没有一种语言漏槽

断链或脏文件：只修发布树里的引用与文件，不重开世界书。

**STOP** `step Q3: accept`

### Q4 · 游客 / 冷启动路径

**完成：** 未登录或等价游客身份，从标题冷启动走完切口声明的主链（或 3 分钟验收句 + 至少一条到结局/收束的主路径），并留下简报。

必测：

- [ ] 3 分钟验收句在冷启动上为真  
- [ ] 切口被遵守：出局地点/闪回人物不上台  
- [ ] 失败的检定会改变下一节点或资源；至少有一条可错过的枝  
- [ ] 问句、选择问（「还是」）、还没接受的意图，**不得**把玩家传送过已写好的节拍（实战：对 NPC 说话时提到「去见某人」，跳过了担保/抵达拍）。可执行的短指令仍应能走。  
- [ ] 作者写死的进门/进房对白不要被标成「AI 已生成」而让玩家误以为是临场编的  
- [ ] 待结算的检定不能在玩家继续说话后错序落地  
- [ ] 不要在官方任务旁边留下一条未完成的动态复制任务  
- [ ] 导演开口与当前房间/flag 一致（复测 M7/M8，不在本步改卡）  
- [ ] 游客提示真实：能走完主线的要写清；登录后才有的导演能力不要假装已经开启

本地预览简报里不写密钥。不在预览未 accept 时上传。

**STOP** `step Q4: accept`

### Q-parity · 参考壳对等

**完成：** 对 `doki-mesh-world`（以及跑在 DokiDemo 壳上的等价叙事世界包），正在跑的包已与**指定参考 AVG 壳**逐帧对等。内部预览（含 `0.1.0-internal` 这类）也必须过这一门。

对照：

- [ ] 包挂在已有的 DokiDemo GameShell 上。默认路径 `/Users/a123/grokmaker/campaigns/DokiDemo`，或该仓的 git worktree（例如 `DokiDemo-brew`）。不是战役根新写的 walk / look / talk `index.html`，也不是另一套更薄的页。  
- [ ] 与已发布、跑在同一壳上的 Strahd AVG 对照：满幅场景板、对话双人、intro reel、BGM、HUD。路径、加载、资源抽查都过，但看起来是另一套更薄的壳 → **不得**记为 world-ship-qa 通过，包括内部预览。  
- [ ] 打开首个场景的本地 HTTP 不是对等门的完成条件。  
- [ ] 占位 VO 可以留在内部预览；公开 `ship: accept` 仍要求非占位配音。

其他品类（`static-campaign-sitting`、idle/`.rpc`、Godot 2D）不走这条对等门，仍走各自的壳与质检。

找不到 DokiDemo 或参考 AVG 时停手去取，不要把「本机刚好能打开的纸壳」写成通过。

**STOP** `step Q-parity: accept` — `doki-mesh-world` 未过此门，不得把 Q5 或任何内部预览标成 world-ship-qa 通过。

### Q5 · 版本与发布清单

**完成：** 版本号在源码 manifest、构建产物、对外说明里一致；有简短变更说明；发布目标明确。

- 升版本再传，不要用同一版本号覆盖已发出的包却改了内容。  
- 写明本包是内部预览、dev、还是公开候选。  
- 上传手续走 `/dokiimport handoff` 或宿主既定管理端；本 skill 只确认清单勾完。  
- 外发系统包（`.app` / zip / 预览壳）须标注 ≠ 大厅正式卡带，密钥仅本机环境。

发布清单（全部勾上才能请求 `ship: accept`）：

- [ ] Q0–Q4 已 accept  
- [ ] Q-parity 已 accept（`doki-mesh-world` 必过，含内部预览；其他品类可记 N/A）  
- [ ] `/dokiimport` 或对应导出检查通过  
- [ ] 版本号一致，变更说明已写  
- [ ] 即将上传的目录 = 刚质检的那一份  
- [ ] 无密钥、无源书、无平台根目录污染  
- [ ] 公开 `ship: accept` 不含占位 VO（内部预览可保留并标明）

**STOP** `step Q5: accept` — 等待 `ship: accept`。accept 之后才允许执行作者本轮点名的上传。本 skill 不把「写了清单」当成已经发布。

## 3. 失败与停手

- 未玩通就出包或上传  
- 把文件打到宿主/平台根目录，或用本机绝对路径  
- 加载板在静帧未解码时撤掉  
- 只抽查封面，不跑引用清单  
- 用已登录作者号代替游客冷启动  
- 在质检未过时改官方已发布包  
- 把本 skill 写成第二份 App SDK 规范
- 只过路径/加载/资源、视觉上却是更薄的纸壳，却把内部预览写成 world-ship-qa 通过
- 把 `edge-tts` 等占位配音写成公开 `ship: accept`

## 4. 转交

| 缺口 | 去 |
|------|------|
| 坐席还不能玩、3 分钟句不成立 | `/rpg-campaign-maker playtest` 或补 mesh 当前层，不要发 |
| 壳是另写的 walk/look/talk 页，或与参考 AVG 不对等 | 停手去取 DokiDemo 壳并 remount，不要发；C3 规则在 `/rpg-campaign-maker` |
| manifest / dist 结构不对 | `/dokiimport check` 然后修，再回到 Q1 |
| 卡带导出、密钥剔除、合入分层 | `/doki-game-maker` D5/D6 |
| 加载 loop / 海报缺失 | `/cinematic-video-assets` |
| 配音槽仍是占位 | `/narrative-voice-production` |
| 还没有切口或 IP 旗标 | `/intake-intent-scope` 或 C0，不要靠发包来补锁 |

## 5. Session bootstrap

```
load:
  - 本 SKILL.md
  - 将发布目录的 manifest / pack.json / 资源清单
  - /dokiimport/references/CHECKLIST.md
  - /doki-game-maker/references/SHIP_CHECKLIST.md
  - 战役 docs/LOCK.md 与最近一次试玩简报（若有）
preflight:
  - 试玩门已过，或本步就是 Q0 停手
  - doki-mesh-world 须过 Q-parity（含内部预览），不要用纸壳顶替
  - 不把预览改动写进官方已发布树
  - 不打印完整密钥
```
