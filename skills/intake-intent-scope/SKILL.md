---
name: intake-intent-scope
description: >-
  立项门：把一句话判成品类、作者真正要保留的体验，以及相近制作级该切多大、投入多少。Use when a project starts from a
  one-sentence pitch, "make a production-level game like this," or any brief
  that is about to enter world-bible / campaign / art production, and you need
  to lock author intent, product form, and a slice budget first. Not for writing
  the core rule book, the sitting lock, or generating assets.
---
# 立项门：作者意图与投入量

一句话还不能开世界书，更不能出图。本 skill 只做**立项门**：记下作者原话，判清品类，写出要保留的体验，估出这一刀的切片与投入，然后停在作者门。

下游的切口锁、世界箱、外观锁各有主人。本 brief 是它们的输入，不是第二份 `docs/LOCK.md`，也不是 `docs/LOOK.md`。

```text
一句话 / 参考作品
  → 品类（产品形态，不是题材标签）
  → 意图（保留什么体验，明确排除什么）
  → 切片预算（在场角色 / 房间 / 视频 / 语音 / 作者门）
  → STOP  intent: accept
        ↓
  /core-rule-book    需要共享设定箱时
  /rpg-campaign-maker C0   切一局 sitting（正式切口锁）
```

## 0. 管什么，不管什么

| 本 skill 写 | 不写，转交 |
|-------------|------------|
| `docs/INTENT.md`：原话、品类、保留体验、切片预算、IP/语言旗标、下一步技能 | 世界箱正文 → `/core-rule-book` |
| 品类判定（玩起来是哪一种产品） | 正式切口、系统名单、3 分钟验收句定稿 → `/rpg-campaign-maker` C0 |
| 投入量：资产大致数量 + 作者门次数 + 接线时间是否单列 | 外观锁与出图锁序 → `/mesh-rpg-craft` M0 起 |
| | 截图 mock / 作者挑图 → `/reverse-game-maker`（可选） |
| | 立绘堆量、视频规范、配音、出包质检 → 对应技能，立项通过后再开 |

禁止：未过 `intent: accept` 就写规则书、生成立绘/视频、搭壳、打包。

## 0.1 已有工程（补立项）

项目根已经有战役文件夹、`pipeline_state.json`、`docs/LOOK.md`、`docs/LOCK.md` 或窗/切片稿时，本 skill 是**补立项**，不是开新局。先读这些文件，再写 `docs/INTENT.md`。

- 只补意图与预算，不覆盖已有切口正文、`docs/LOOK.md`、`docs/LOCK.md`，也不重绘已 accept 的外观锚。
- 写 `pipeline_state.json` 必须**合并**：保留已有 `accepted`、锚、step 历史和其它字段，只追加本 skill 的状态（如 `intent`、I0–I4）。禁止用一份只含立项门的新文件替换整份状态。
- 外观或切口已经 accept 的，作者门序列里标成已过。不要因为缺少 `docs/INTENT.md`，就把「未过 intent 不准出图」理解成要推倒 M0。
- 已有稿的语言若作者已经写完一窗（例如中文切片稿），I2 的语言项以这份稿为提案，仍须在 I4 勾认；不要把「书是英文就不要先译」理解成必须作废已有译稿。
- 目录里若还有建角、别的规则系统壳、或未进切口的实验，默认写入 `explicit_out`，除非作者本轮点名要带进这一刀。

## 1. 命令

```
/intake-intent-scope
/intake-intent-scope intake | form | intent | scope | accept
```

无参数：读项目根 `pipeline_state.json`，做当前步，然后 **STOP**。  
项目根：用户给的路径 → 当前仓已有战役/世界文件夹 → 问一次。

## 2. 步骤

### I0 · 收原话

**完成：** `docs/INTENT.md` 开头有 `author_raw_input`，作者原文一字不漏；若给了参考作品或包，只记名称与作者点名的体验，不在这里拆书。

来源可以是一句话、一篇短简报、一个「像某某那样做成制作级」的指示。不要把笼统词直接当成策划案。

**STOP** 仅当原话都读不清（缺语言、缺参考、互相打架）。否则进入 I1，不必单独停门。

### I1 · 判品类

**完成：** brief 里有且仅有一个 `product_form`。题材（吸血鬼、公路、宫廷）不是品类。品类是**玩家坐下来实际玩到的产品形态**。

| 品类 | 玩家碰到的东西 | 正式制作走 |
|------|----------------|------------|
| `doki-mesh-world` | 自由探索、立绘、场景 idle loop、导演、任务链、配音 | C0–C1 后 `/mesh-rpg-craft`，壳用已有 Doki 自由探索，收包 `/doki-game-maker` |
| `static-campaign-sitting` | 嵌套选择树、检定、物品、原声壳、静态 `dist/` | `/rpg-campaign-maker` 默认坐法 A |
| `digital-human-r1` | 实时数字人 / locked-portrait seed / 导播 | `/pixverse-r1` + `/doki-game-maker` stream-r1；坐席战役不要从 R1 开场 |
| `screenshot-first-idle` | 截图反推、Design Bible、白盒、`.rpc` | `game-maker-pipeline` / `/reverse-game-maker`（另一条总控，不要默认为叙事世界总控） |
| `engine-crpg-graybox` | 等轴/网格/战斗回合等引擎灰盒 | 引擎技能另接；**不要**用叙事世界的立绘/loop 管线冒充 |

实战提醒（短例，不是唯一路径）：同一句「做 Curse of Strahd 切片」可以先写成等轴回合 CRPG 设计稿，后来真正发布的却是 Doki 网状叙事世界。两份 brief 不要混用。作者若口头对标已有世界，以**已发布形态**为准，除非作者显式改品类。

品类说不清 → 列出候选，**STOP** `form: pick {id}`，禁止猜一个架构往下做。

### I2 · 作者意图

**完成：** brief 能让作者勾认下面五条，且互相不打脸。

1. **要保留的体验** — 玩家坐下来必须碰到的感觉与节拍（不是剧情摘要，不是系统清单）。  
2. **明确排除** — 本刀不做的地点、人物上台、系统、媒体线（例如城堡内部、完整预言链、直播数字人、战斗 HUD 当卖点）。  
3. **3 分钟体验句（草稿）** — 冷启动三分钟内玩家能感到「这不是聊天窗」。定稿在 C0，这里必须有可改的一句。  
4. **语言** — 对白与 UI 用源语言还是指定语言；要不要中英双轨。书/模组是英文就不要「帮忙」先译成别的语言（正式规则在 `/rpg-campaign-maker` C0/C1）。  
5. **IP 旗标** — `original` / `unofficial-remix` / `licensed`。同人/书徒：写明公开发布前要换皮；源书 PDF 与框文不进仓、不进包。这是旗标，不是法律意见。换皮名单的正式锁仍在 C0。

意图与品类冲突时（例如要「制作级巴洛维亚那种听感和 loop」，却把品类写成引擎灰盒），停在 I1/I2，让作者改一项，不要两边各做一半。

### I3 · 切片与投入量

**完成：** brief 里有一张**本刀预算表**，数字是估出来的上限，不是愿望清单。不满意时先审计当前层，默认不靠把切片扩成「全书」。

先画切口草图（正式锁仍是 C0）：

- 从哪开始、在哪结束  
- 本刀在场、闪回-only、明确出局  
- 哪些系统真的会开火（谈/检定/物品/时钟/战斗……）；不开火的不要列入制作量

再数资产与门（方法是建议默认，不是某次工程的实测清单；打开已有工程时应改用盘点数字）：

| 项 | 怎么数 | 计入 |
|----|--------|------|
| 在场说话脸 | 会上台开口的角色；闪回-only 只进文案，不建立绘/配音槽 | 每张：静帧 1；需要出场则 intro 1 |
| 可进房间 / 场景板 | 切口内的地点，不含地图冒充场景 | 每处：静帧 1；要活底则 idle loop 1 |
| 过场 / 节拍片 | 作者点名的短片（开场、葬礼、结尾），按拍数不是按「一部电影」 | 每拍一条 clip-library 文件 |
| 配音 | 将出口的台词：短句与长台词分开计；双语言则乘语言数 | 见 `/narrative-voice-production` |
| 作者门 | 至少列出后面必停的门 | 见下表 |
| 接线时间 | 网状世界的拍门控、导演、本地 HTML 包、通道 | **单列一行**。已有技能写明：GitHub 通用生成能省轮次，Doki 接线不能当成「调一下就好」 |

**建议默认的作者门序列**（叙事世界制作级；品类不同则删增，不要假装这些门不存在）：

1. 本 skill `intent: accept`  
2. 需要世界箱时：`/core-rule-book` 的锁与 W6  
3. `/rpg-campaign-maker` C0 切口锁  
4. 要网状实现时：`/mesh-rpg-craft` M0 主外观  
5. mock / 作者挑图（若走了 `/reverse-game-maker` 或加载幕等多方案 mock）  
6. 玩通 sitting：战役 C5 或等价试玩门  
7. `/world-ship-qa` 发布质检  

可选第二刀（例如序章）写在「A 通过后再做」，不要和第一刀的预算混成一笔。

低完成度也可以玩：切的是可坐完的一局（村子与一条主链），不是全模组。投入量不够就**缩小切口**，不要暗中加房间和脸。

### I4 · 作者门

把 `docs/INTENT.md` 交给作者。必须能看见：原话、品类、保留/排除、3 分钟草稿、语言、IP 旗标、预算表、下一步技能。

**STOP** `step I4: accept` — 等待 `intent: accept` 或 `intent: revise — {note}`。

- accept：**合并**写入 `pipeline_state.json`（保留已有 `accepted`、锚和其它字段；追加 `skill: intake-intent-scope`，并把 I4 加入 `accepted`），只打印下一步技能名，**不要在本会话自动开世界书或出图**，除非作者本轮点名。不要用新文件覆盖已 accept 的 S0/M0 等历史。  
- revise：留在对应步，把 note 并进 brief，再停一次门。

## 3. 产出

`docs/INTENT.md` 至少包含：

```markdown
# Intent brief
- author_raw_input:
- product_form:          # 上表之一
- keep_experiences:      # 要保留的体验（条目）
- explicit_out:
- three_minute_draft:
- language:
- ip: original | unofficial-remix | licensed
- slice_sketch: start / stop / in / out / systems
- budget: faces / places / loops / cinematics / vo_lines / author_gates / wiring
- next_skill:            # core-rule-book 或 rpg-campaign-maker lock
```

`pipeline_state.json` 记 `step` 与 `status`。不要在这里写 `docs/LOCK.md` 或 `docs/LOOK.md`。

## 4. 失败与停手

未过关（任一即停）：

- 没有作者原话，或把推断写成了原话  
- 品类未锁定，或两个产品形态各做了一半  
- 只有题材/世界观，没有「保留的体验」和「明确排除」  
- 预算没有数字（「若干立绘」「一些 loop」不合格）  
- 把 Doki 接线或导演当成零成本  
- 未 accept 就开始 `/core-rule-book` 以外的制作（作者本轮点名的除外）  
- 把本 brief 当成正式切口锁或外观锁

## 5. 转交

| 作者接下来要 | 开 |
|--------------|----|
| 共享设定箱，还不是一局 | `/core-rule-book` |
| 切这一局（切口、系统、3 分钟句定稿） | `/rpg-campaign-maker lock`；把本 brief 当作 C0 输入 |
| 已有 C0，要网状外观与出图锁序 | `/mesh-rpg-craft look` |
| 先出可点的界面/加载幕 mock 再定外观 | `/reverse-game-maker` 或既有 mock 流程；作者挑图后再锁 |
| 数字人运行时 | `/pixverse-r1`（资产规范仍按视频/配音技能，不在立项里拍） |

剧本拆解、任务链、立绘 PNG 属于已有技能；视频、配音、出包分别走 `/cinematic-video-assets`、`/narrative-voice-production`、`/world-ship-qa`，不在本门展开。

## 6. Session bootstrap

```
load:
  - 本 SKILL.md
  - {PROJECT}/docs/INTENT.md、pipeline_state.json（若有）
  - 作者本轮点名的参考包/一句话（只摘体验，不拆全书）
preflight:
  - 不写 docs/LOCK.md、docs/LOOK.md、不调用出图/出视频
  - 已有 LOCK.md、LOOK.md 或非空 pipeline_state.json 则只补意图/预算，不覆盖切口或外观，写状态时必须合并
  - 一次只推进 I0–I4 中一步需停门的部分
```
