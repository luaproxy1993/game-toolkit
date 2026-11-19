---
name: narrative-voice-production
description: >-
  叙事游戏配音与演绎制作：先锁可朗读的听感，再出台词表、占位音、音色设计、短句与长台词分轨、多语言与重录替换。Use when the user runs
  /narrative-voice-production, says 配音, 音色, 台词表, VO, 旁白演绎, 葬礼长句, or needs spoken
  audio and in-world performance tone for a narrative sitting — not Godot audio
  buses, and not a rewrite of NPC beat-gate or director skills.
---
# 叙事游戏配音 / 演绎制作

玩家听到的，等于**文风**和**声音**两层。只改角色卡或只换一条提示词，进不了已发布的包。本 skill 管听感锁、台词表、占位与成片、分轨替换和听感验收。

不接管这些已有主人的层：

| 层 | 主人 |
|----|------|
| 对白语言、原声文案、框文不进包 | `/rpg-campaign-maker` C0/C1（original-voice） |
| NPC 当前拍开口、过期拍关掉 | `/mesh-rpg-craft` M7 |
| 导演只读已闸 context pack | `/mesh-rpg-craft` M8 |
| 引擎总线、空间混音、SFX 池 | `audio-system`（引擎技能，不要和本 skill 合并） |
| 节点上的媒体是 clip-library，禁止运行时现生成 | `/rpg-campaign-maker` `MEDIA-LAYERS.md` |

```text
听感锁（可朗读的文风）
  → 台词表（角色 / 语言 / 短句或长句 / 触发拍）
  → 系统占位音（槽位先通）
  → 音色设计 + 多条 take
  → 作者点名
  → 分轨成片替换占位
  → 进包听验收
```

未锁听感、未列台词表，不准批量出声。失败 take 不进 live 槽。

## 1. 命令

```
/narrative-voice-production
/narrative-voice-production tone | lines | placeholder | cast | record | replace | accept
```

无参数：按 `pipeline_state` 做当前步，然后 **STOP**。  
战役根与 `/mesh-rpg-craft` 相同：用户路径 → 已有战役文件夹 → 问一次。

## 2. 步骤

### V0 · 听感锁

**完成：** `docs/VOICE.md`（或 pack 的 tone 文件）写明：对谁说话、第几人称、句子完整还是允许界面短句、禁止的空词与电报体、语言列表。

建议默认的叙事听感（来自已发布世界的文风补丁；换气质时整段改写，不要只改项目名）：

- 说书人 / 在场角色把话**说完**，用完整、连着的句子。一个短段落正好。  
- 可以短，不能碎。停顿是喘气，不是把场面切成镜头清单。  
- 气氛写在动词和物件里，不要单开一句「你感到 / 命运 / 不祥 / 仿佛」。  
- 角色此刻要有想要的和不肯做的；口气对上这个人。  
- 界面状态短句可以留短，但仍应是一句完整话（「短剑已经在你手里。」），不要电报标签。

**必须一起改的三处**（只换其中一处，玩家听到的不会变）：

1. 包或导演使用的 `tone`（有几份语言改几份）  
2. 运行时拼进人格/导演的风格句（删掉与听感打架的「一句一个事实」「再短」）  
3. 写死的短句（位置答语、行动反馈、罐头提示）

城主卡或外部扮演卡可以按同一口吻改，但**不能**自动替代包内 `tone`。

文案尚未过 C1 / 节点表尚未过 M6 时，本步只锁规则，不编新剧情。开口仍须服从当前拍（M7）。

**STOP** `step V0: accept`

### V1 · 台词表

**完成：** `docs/VO-LINES.md`（或 `assets/audio/vo/lines.json`）每一条可出口台词都有：

| 字段 | 要求 |
|------|------|
| `id` | 稳定槽名，按地点/动作/角色，不用 `line3` |
| `speaker` | 在场说话的人；闪回-only 默认不出声，除非作者点名 |
| `lang` | 与 C0 语言一致；双轨则每条语言一行，不要运行时现译 |
| `text` | 将被朗读的原文；须能读出口，已过听感锁 |
| `kind` | `short`（应答、反馈、UI）或 `long`（葬礼、开场、过场旁白） |
| `cue` | 房间 / flag / 节点；没有拍门的「开口就说」不准进表 |
| `slot` | 将替换的占位文件路径 |

长台词与短句必须分轨，不要把葬礼段落和门边短句录在同一条循环里。  
目录建议：`assets/audio/vo/{lang}/{speaker}/{id}.mp3`（或项目既有槽，不另起一套路径）。

**STOP** `step V1: accept`

### V2 · 占位音

**完成：** 每个槽先有一条系统/占位音色，时长和语言对得上，游戏里能点到、能播完。槽不通不准进入音色精做。

占位音也要能听出「这是一句完整话」，用来验收文案，而不是哔一声。

**STOP** `step V2: accept`（若作者允许占位与音色设计同会话进行，可在槽位清单已挂上后合并到 V3，但仍须先有可替换的路径。）

作者预收闸（如「通过all」）时，可以把 V0–V2/V5 记为本坐 accepted，用占位验槽与文案；**占位 TTS 不能当成公开发布成片**。CAST/CREDITS 必须写明公开或换皮前重做 V3–V4。

### V3 · 音色设计与试听

**完成：** 每个说话角色有一份音色说明（性别/年龄感、气口、距离、禁止的腔），以及**不少于三条完整 take**（同一段词，不是把失败片段拼成一条）。

结算记录里的一条完整实践是：系统占位 → 外部音色设计（实战用过 ElevenLabs，不绑死唯一供应商）→ 短句 / 长台词分轨 → 中英分录 → 重录替换。供应商可换，步骤不要删。

试听规则：

- 同一角色所有语言尽量共用同一音色设定，只换语言与用气，不换人。  
- take 必须是完整备选，供作者点名；失败条不 concat 进正片。  
- 长台词按段落换气，不要为了「省一条」把葬礼整场压成短句语速。

**STOP** `step V3: accept` — 出示试听表，等待点名。

### V4 · 作者点名

**完成：** 每个 `speaker`（或每个 `id`，若作者要求按句选）有一条被点名的 take。未点名的角色不准进 live。

`voice: pick {speaker} takeN` 或 `voice: revise — {note}`。  
revise 只重录被点名的层，不回头改节点表或立绘。

**STOP** 等到点名写进 `docs/VO-CAST.md`。

### V5 · 成片替换

**完成：** 点名 take 已写入 live 槽，占位被替换而不是并排残留；`?v=` 或等价缓存已 bump；双语包两种语言都能听到对的文件。

- 同一 `id` 覆盖原路径，不要让旧占位仍被清单引用。  
- 需要重录时改文件并保留 `id`，更新 take 记录。  
- 有配音就必须有 `assets/audio/CREDITS.md`（供应商、许可、是否原创）。官方原声带默认不进包。  
- 密钥、账号、供应商工程文件不进发布树。

**STOP** `step V5: accept`

### V6 · 听验收

**完成：** 冷启动走一条主链，对照清单全部勾上。

- [ ] 听感：完整句子，不碎、不空；写死短句已按 V0 改过  
- [ ] 当前拍开口与配音一致；坟边不念上一拍的侧厅稿（认知仍由 M7/M8 负责，本步复听）  
- [ ] 短句轨与长台词轨没有串槽  
- [ ] 每种发布语言都抽听至少一条 short、一条 long  
- [ ] 减动效 / 关音频时游戏仍可玩（有字幕或原文）  
- [ ] 无占位音残留在 live 清单，无密钥

**STOP** `step V6: accept`

## 3. 失败与停手

- 只改外部卡或只改 `tone`，导演拼句与罐头短句仍是电报体  
- 未列台词表就批量出声  
- 用失败 take 拼接充数  
- 把未门控的 `npc.dialogue` 拿去配音  
- 运行时调用生成器出声（那是另一产品，不是 sitting 的 clip-library）  
- 用引擎 `audio-system` 的总线设置代替本 skill 的听感与台词表

「再录三条」而没有完成标准时：对照 V0 与 V6，已过关的角色禁止回头群录。

## 4. 转交

| 缺口 | 先去 |
|------|------|
| 还没有切口、源语言、原声文案 | `/rpg-campaign-maker` C0/C1 |
| 还没有硬节点 / 拍门控 | `/mesh-rpg-craft` nodes 然后 npc |
| 场景或立绘视频要做 | `/cinematic-video-assets`（声画不同 skill） |
| 要收包 | 先过本 skill V6 与试玩门，再 `/world-ship-qa` |

## 5. Session bootstrap

```
load:
  - 本 SKILL.md
  - {CAMPAIGN}/docs/VOICE.md、VO-LINES.md、VO-CAST.md（若有）
  - {CAMPAIGN}/docs/LOCK.md（语言、IP）
  - /mesh-rpg-craft 的拍门控契约，当台词带 cue 时
  - /rpg-campaign-maker references/ASSETS.md 与 MEDIA-LAYERS.md，当媒体挂在节点上时
preflight:
  - 不改节点表、不重渲 CG 来「配合配音」
  - 不把供应商 key 写入包
  - 一次只推进当前 V 步
```
