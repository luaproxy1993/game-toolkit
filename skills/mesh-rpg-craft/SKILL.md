---
name: mesh-rpg-craft
description: >
  Doki 魔改网状 RPG 的锁序与踩坑：立绘/alpha intro/粒子、场景静帧与 idle loop、
  NPC 拍门控认知、导演只消费已闸内容、世界书与硬节点、GUI 数值绑定。
  GitHub 技能能省时间，Doki 接线不能省。改一层再推下一层；未锁主外观时禁止并行开特效。
  LOOK 接受后按已锁锚 + 空间清单出图；失败/未对齐板不得当下一稿参考；
  须装回正在跑的 DokiDemo 战役包，并在同一趟退役被取代的旧锚。
  Use when the user runs /mesh-rpg-craft, says 网状任务, NPC认知, 立绘alpha,
  idle loop, 导演agent, 吸血鬼战役踩坑, doki campaign, 主线支线硬节点,
  or is stuck regenerating one-off art/NPC lines that fight each other.
argument-hint: "[campaign_path] [lock|look|portrait|intro|fx|scene|loop|bible|nodes|npc|director|numbers|audit]"
user-invocable: true
metadata:
  short-description: Doki 网状 RPG 锁序 / 立绘场景 / NPC 导演踩坑
  version: "1.0.1"
  feeds: "doki-game-maker, rpg-campaign-maker, world-bible, game-asset-core"
---

# Mesh RPG Craft

一场能玩的 Doki 网状战役，观感来自**同一套画面元素**，推进来自**同一套拍门控**。  
心血来潮的单点特效会把前后层打穿。本 skill 管**锁序、停手标准、转交哪个生成器**，不重写 Imagine / PixVerse / 世界书的字段表。

```text
主外观锁（一张图 + 一句话）
        │
        ├─ 立绘静帧 RGBA ──► alpha intro ──► 人设粒子（叠，不烤进图）
        └─ 场景静帧     ──► idle loop
世界书 + 硬节点 ──► NPC 拍门控卡 ──► 导演只读当前拍 ──► GUI 数值绑 flag
```

立绘轨与场景轨在主外观锁之后**可以并行**。  
intro 不能先于静帧；loop 不能先于场景静帧；NPC 台词不能先于硬节点；导演不能先于拍门控。

## 0. 每次会话先对齐

1. 读战役根 `pipeline_state.json`（无则建，step=`M0`）。  
2. 没有已接受的**主外观**，只做 `lock` / `look`。  
3. 作者说「再调一下」时，先对照当前步的完成标准，而不是再开一轮生成。  
4. 改画面不重写 NPC 卡；改认知不重渲 CG。一层未过，下一层不开。

战役根：用户给的路径 → 当前仓 `campaigns/<slug>` → 问。  
若已有 `docs/LOCK.md`（rpg-campaign-maker），**不要另写一份切片锁**。外观锁写 `docs/LOOK.md`。接法：`references/HANDOFF.md`。

```
SKILL_ROOT=~/.grok/skills/mesh-rpg-craft
```

按层 load：

| 层 | 先读本 skill | 再转交（已有则用现成，禁止另起一套） |
|----|----------------|----------------------------------------|
| 主外观 / 静帧 | `references/LOCK-ORDER.md` | `game-asset-core`；角色一致性 `game-character-consistency` |
| 立绘 intro / loop | `references/PORTRAIT.md` `references/SCENE.md` | `game-animation-frames`；数字人 seed 用 `pixverse-r1` `SEED_VIDEO.md` |
| 世界书 | `references/BASE.md` | `/core-rule-book` |
| 一切口战役（切口/树/原声） | `references/HANDOFF.md` | `/rpg-campaign-maker`（C0–C3 主人；C4 走本 skill 锁序） |
| 卡带封装 | — | `/doki-game-maker` |
| 踩坑 | `references/PITFALLS.md` | — |
| NPC / 导演 | `references/DIRECTOR-NPC.md` | 本战役 `dialogue` + `conditions` + `buildContextPack` |

GitHub 上的通用技能能省生成轮次。**Doki 接线、拍门控、alpha、本地 HTML 包**仍要本仓改，这笔时间预算进立项，不要当「调一下就好」。

## 1. 命令

```
/mesh-rpg-craft
/mesh-rpg-craft lock|look
/mesh-rpg-craft portrait|intro|fx
/mesh-rpg-craft scene|loop
/mesh-rpg-craft bible|nodes
/mesh-rpg-craft npc|director|numbers
/mesh-rpg-craft audit
```

无参数：按 `pipeline_state.step` 做当前步，然后 **STOP** `step M#: accept`。

## 2. 步骤（作者门）

### M0 · 主外观锁

**完成：** `docs/LOOK.md`（或 pack ART）里有：一句气质、参考静帧路径、画幅、键色/透明规则、禁止的 IP/风格。一张**已接受**的锚图（人+景各一张更好）。新锚已 **remount** 进正在跑的 DokiDemo 战役包；被取代的旧锚已从 live pack **退役**。

未锁之前禁止：intro 视频、粒子、idle loop、多角色分风格。

已接受之后，所有出图从**这批已锁锚**出发，并带上空间清单（画面里有什么、谁在哪、空板不进人、镶嵌/顺序约束等）。契约：`SCENE.md`。不要拿落选稿当下一轮参考。

当 LOOK 被修订并再次接受：在**同一趟**把新锚装进正在跑的 DokiDemo 战役包，并从 live pack 退役被取代的旧锚（例如 painterly 锁过之后，包里不得再留上一闸的水彩锚）。装包是必做步，不是事后补。未 remount、未退役，M0 不算完成。

**STOP** `step M0: accept`

### M1 · 立绘静帧

转交 `game-asset-core` + `game-character-consistency`。契约：`references/PORTRAIT.md`。  
产物：干净 RGBA，白底或纯键色，**不烤场景、不烤光晕、不烤粒子**。同一角色只从 master still `image_edit`。通过后 remount 进正在跑的 DokiDemo 战役包。

**STOP** `step M1: accept`

### M2 · alpha intro

从 **M1 同一张静帧** `image_to_video`。画幅、人物比例与静帧一致。透明通道：仅当 LOOK/M0 要求抠键时走 chroma/WebM；**已锁白纸底则保留纸白、不抠透明**。失败片**不拼接进正片**；三选一等作者点名。契约：`PORTRAIT.md` §intro。

**STOP** `step M2: accept`

### M3 · 立绘特效

粒子/闪光是**叠层**，匹配人设，不写进 PNG。人设变了只换 FX 配方，不重绘脸。

**STOP** `step M3: accept`

### M4 · 场景静帧

同一主外观。原生画幅（场景板不是地图、不是 1:1 挂进去）。契约：`SCENE.md`。

生成前写空间清单（画面里有什么、谁在哪、空板不进人、镶嵌/顺序约束、门洞与相邻房间）。验收不过：整张作废，从**上一张已接受的锁/锚**重切，禁止把未对齐/失败板当作下一稿参考（教训：走廊天/山/河/火镶嵌、实验室书架、舱口站位一类错构图，用失败稿再生成会把错误锁死）。

通过后必须 **remount** 进正在跑的 DokiDemo 战役包；live 壳里不得留下已退役的 LOOK 锚。未 remount 不算 M4 完成。

**STOP** `step M4: accept`

### M5 · 场景 idle loop

从 **M4 静帧**做 loop：机位锁、景物微动、首尾可接。优先用**同一张静帧**作 i2v 的 first 与 last 锁循环接缝，不必另拍尾帧。数字人背景用 still plate（`SEED_VIDEO.md`）。失败 clip 不 concat。

**STOP** `step M5: accept`

### M6 · 世界书 + 硬节点

硬节点：写在战役 `docs/NODES.md`（或 pack 的 quest/event 表）。契约：`BASE.md`。没有节点表，不准写「开口就说」。  
切片切口仍以 rpg-campaign-maker 的 `docs/LOCK.md` 为准。

- 若本战役已有 `docs/LOCK.md` 且 `docs/BIBLE.md` / `docs/NODES.md` 已齐：M6 **只核表并 accept**，不要另开 `/core-rule-book`，除非作者点名。  
- 若还没有世界书、且作者点名要一本：才转交 `/core-rule-book`（本步不画图）。

立绘 / 进场的透明与底色以已锁 LOOK 为准；白纸底战役不要照抄 `PORTRAIT.md` 的 chroma 默认。

**STOP** `step M6: accept`

### M7 · NPC 拍门控卡

每张卡：`conditions` + 当前拍 `opening_line` / `known_text`。过期拍关掉。行踪按**尸体/人现在在哪**写，不写「不要说旧拍」当人格。契约：`DIRECTOR-NPC.md`。

**STOP** `step M7: accept`

### M8 · 导演

导演只读当前拍的 context pack。合法动作、开口、在场、guardrail 必须已闸。导演**不**发明节点、不重开西路、不把静帧台词当永远。需要小游戏/CG 时发已注册 action，不现场编片。

**STOP** `step M8: accept`

### M9 · GUI 数值

条、键、资源只绑 `flags` / `player` / 冲突状态。UI 文案跟拍走。改数值不重做立绘。

**STOP** `step M9: accept`

### `audit`

对照 `PITFALLS.md` + 当前 step 完成标准列失败项。只修当前层。

## 3. 停手

「改到什么程度都不满意」时，用完成标准，不用感觉：

- 静帧：键干净、比例对、与锚图同一套气质  
- 视频：画幅/alpha/loop 过关，作者点名的那一条，不是三败片叠在一起  
- NPC：当前房间+flag 下开口不出现上一拍事实  
- 导演：候选动作与开口同拍  

未过关 → 只重做这一层。已过关 → 记入 `accepted`，禁止为下一层回头「再生成三张」。

## 4. Session bootstrap

```
load:
  - {SKILL_ROOT}/SKILL.md
  - {CAMPAIGN}/pipeline_state.json
  - {SKILL_ROOT}/references/LOCK-ORDER.md
  - {SKILL_ROOT}/references/HANDOFF.md           当战役已有 / 将跑 rpg-campaign-maker
  - {SKILL_ROOT}/references/PITFALLS.md          当作者说不满意 / 来回改
  - PORTRAIT.md / SCENE.md / DIRECTOR-NPC.md / BASE.md  按当前 step
  - 转交技能的 SKILL.md 仅在进入该层时
preflight:
  - 有主外观锁，或本步就是 M0
  - 不把失败视频 concat 进正片
  - 不把失败/未对齐静帧当下一稿参考；从上一张已接受的锁重切
  - LOOK 修订后同一趟 remount 新锚并退役 live pack 里的旧锚
  - 不把未门控的 NPC.dialogue 当开口
  - 改认知不重渲 CG；改 CG 不重写世界书
```
