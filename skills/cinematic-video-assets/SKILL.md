---
name: cinematic-video-assets
description: >-
  动态视频资产制作规范：静帧锁定后再做 intro、场景 idle loop
  与过场拍，含镜头语言、按人设的立绘微动作、真透明循环交付、一致性与循环接缝。Use when the user runs
  /cinematic-video-assets, says 动态视频, idle loop, intro 视频, 过场片, 循环夜景平板, loading
  loop, or needs a production spec for narrative video plates — not PixVerse R1
  API/session (that is /pixverse-r1) and not sprite-sheet strips (that is
  /animate-sprites).
---
# 动态视频资产制作规范

本 skill 是**制作规范**，不是生成器，也不是实时会话工具。它规定：先有已接受的静帧，再拍哪一类片子，镜头怎么锁，怎样验循环，怎样交付进壳。

不重复这些主人：

| 层 | 主人 |
|----|------|
| 主外观、立绘静帧、场景静帧的锁序 | `/mesh-rpg-craft` M0 / M1 / M4；契约在 `PORTRAIT.md` / `SCENE.md` |
| 数字人 locked-portrait seed（近景中景、~40s 词库、still plate 背景、R1 接入） | `/pixverse-r1` `SEED_VIDEO.md` |
| R1 订棚 / Agora / 导播 | `/pixverse-r1` |
| 横条精灵、脚对齐走跑循环 | `/animate-sprites` |
| 夜景叙事 UI 气质（慢循环平板是其语汇） | `/cotny-style-narrative-ui` |
| 节点上的过场是作者期 clip-library | `/rpg-campaign-maker` `MEDIA-LAYERS.md` |

```text
已接受静帧
  → 分类（intro / alpha idle / 场景 loop / 加载或封面 loop / 节拍过场）
  → 按规范拍（机位锁、主体清单、一致画幅）
  → 完整备选，作者点名（失败片不拼接）
  → 交付：成片 + 海报静帧 + 清单
```

未锁静帧，不准开拍。intro 不能先于立绘静帧；场景 loop 不能先于场景静帧。

## 1. 命令

```
/cinematic-video-assets
/cinematic-video-assets classify | still | shoot | loop | deliver | accept
```

无参数：读当前战役的视频清单，只做未过关的一类，然后 **STOP**。

## 2. 类型（先分类再拍）

写 `docs/VIDEO.md` 或 `assets/video/manifest.json`。每一条只属于下一类之一，禁止把 R1 seed、游戏内 alpha idle、场景底板 loop 糊成同一条文件。

| `kind` | 用途 | 输入 | 透明 | 建议默认（可按槽改，须写进清单） |
|--------|------|------|------|--------------------------------|
| `portrait-intro` | 对话立绘出场一次 | 已接受 M1 静帧 | 默认要真透明。若也要叠房间，交付格式与 `portrait-alpha-idle` 相同；禁止亮度去底。**已锁白纸底 / LOOK 不抠透明时：保留纸白 MP4，不强制绿幕** | 与静帧同一画幅与人物比例 |
| `portrait-alpha-idle` | 出场后循环；叠在**房间场景**上 | 已接受的 chroma 静帧，同一姿态 | 要真透明。不能烤 still plate 背景。游戏内交付带 alpha 的循环图（默认 animated WebP，用 `<img>` 播），不要把 VP9 WebM 当浏览器里的播放文件 | 机位锁；口闭合；手不离躯干、也不从画外长出新肢体；**每人一条人设动作**（查装备、微表情等），禁止全员同一套深呼吸当主动作；清单里写清该人的可读动作 |
| `scene-idle` | 房间活底 | 已接受 M4 场景静帧 | 通常不透明 | 机位锁；景物微动；首尾可接；**同一张静帧作 first=last** 即可锁接缝，不必另拍尾帧；主体清单验收 |
| `cover-loop` | 标题 / 加载共用背景 | 已接受封面或场景静帧作海报 | 通常不透明 | 慢循环；减动效时停在海报，不把板藏掉 |
| `beat-cinematic` | 开场、葬礼、结尾等作者点名的拍 | 已接受静帧或同外观锚图 | 按合成需要 | 按拍出片，挂在节点上；不是一部到运行时才生成的长片 |
| `r1-seed` | 实时数字人种子 | — | **不要在本 skill 制作** | 转交 `/pixverse-r1 seed` |

叙事夜景的动画语汇是**稀疏慢循环**（雾、烛、旗、雨、窗帘、灯），不是忙视差，也不是跟拍动作片。这套语汇只给场景/封面 loop，不要套到立绘 idle 上当全员共享呼吸。

## 3. 步骤

### Cine0 · 分类与镜头表

**完成：** 清单里每一条有 `id`（按地点/动作命名，不用 `clip3`）、`kind`、源静帧路径、画幅、主体清单、循环或单次、语言无关的用途一句。

每一条 `portrait-alpha-idle` 还要写**只属于该角色**的可读动作一句（查装备、扫一眼、冷笑、忍痛、寒颤等，从已锁静帧/人设来）。「全员呼吸循环」不是完整简报。

节拍过场按拍列（例如：起场、中拍、收束、结尾卡），一拍一条，不要先拍一条再事后切「电影感」。

**STOP** `step Cine0: accept`（清单很短且作者已点名类型时，可与 Cine1 同会话，但仍须先有表。）

### Cine1 · 静帧门

**完成：** 每条视频的源静帧已在 mesh 作者门接受。没有 `LOOK.md` 与锚图，退回 `/mesh-rpg-craft look`。

禁止为了「intro 更好看」另画一张不成套的立绘再去 i2v。后续一律从 master still `image_edit` / `image_to_video`。

主体清单写进 prompt，也写进验收（棺、门、祭坛、狼……）。拍完逐项还在。立绘半身要到腰，禁止用肩线/腰际 U 形淡出冒充透明底。

**STOP** 若有条目缺静帧。全齐则进入拍摄。

### Cine2 · 拍摄（镜头语言与一致性）

**完成：** 每个条目至少有一条（作者要「三个镜头」= 三个完整备选）符合下列规范。

镜头语言：

- **默认锁机位。** 循环类禁止 pan / tilt / orbit / handheld / 切镜。极轻的缓慢缩放仅在清单写明时允许。  
- **微动，不换景。** 主体不出画、不把清单物冲走。场景/封面：景物微动（闪烁、飘雾、旗、雨、窗帘、灯）。立绘 alpha idle 不要默认写成全员深呼吸。  
- **intro** 与静帧可叠：画幅、人物在画布中的比例一致；播一次后接 alpha idle 或静帧。减动效则静帧。  
- **alpha idle** 绿幕全程保持。每个角色的可读动作必须是清单里写明的人设业务（查装备、扫一眼、浅笑、忍痛、寒颤等），**第一秒就要看得出**。几乎静止的「一张静帧存成视频」是失败；全员同一套胸腔深呼吸是失败。残余的呼吸只允许当它**不是**主读点。手与静帧一致，不要从画外长出新肢体。抠像后可保留 VP9 `yuva420p` WebM 作源；游戏内叠场景的播放文件必须是目标浏览器真能合成透明的循环图（默认 animated WebP，`libwebp_anim` + `yuva420p` + loop 0，用 `<img>` 播）。**不要**用 `<video src="*.webm">` 播立绘：Safari 和不少解码器会丢掉 VP9 alpha，看起来像圈了一个人物尺寸的实心框（透明像素常解成黑底）。绿幕 H264 仅作 canvas 去底的备路。不要把这条当 R1 seed 上传。  
- **场景 / 封面 loop** 从静帧长出，光、色、介质与主外观一致。创建页背景轮播只用房间静帧交叉淡入，不拿角色展示构图冒充场景。场景 loop 可以保留不透明 H264 MP4，用 `<video>` 播。  
- **节拍过场** 仍服从主外观与主体清单；每拍内部默认锁机位。不要用失败段拼成「正片等作者挑」。

一致性失败即整条作废：脸漂、景换、画幅改、键边脏、与锚图两套世界。

失败片**不拼接进正片**，不进 live 目录。三选一等作者点名后再用通过的那一条。

**STOP** `step Cine2: accept` — 出示备选，等待 `video: pick {id} takeN`。

### Cine3 · 循环与接缝验收

对一切 `loop` 条目（含封面、场景、alpha idle）勾选。建议默认的检查方法：导出首帧、中帧、尾帧，再做首尾差图（实战里用过 first / mid / last / diff）。

- [ ] 循环播两圈，接缝无跳、无闪、无机位挪动  
- [ ] 首尾姿态、构图、光、背景可接；做不到就在段间回到 master still 再接下一段  
- [ ] 主体清单逐项还在（例如狼冲过道不得把棺材冲没）  
- [ ] 关视频或 `prefers-reduced-motion` 时，落到的静帧仍是源海报，不是黑场或另一张图  
- [ ] 封面/加载 loop 若被复用：只加载一次、循环播放；减动效暂停视频并留下板
- [ ] **立绘 alpha idle：** 四角与剪影周围画布为真透明（alpha 0），人物不被困在硬矩形里。不透明像素只出现在身体/衣装上；禁止用腰际 U 形淡出冒充透明底。必须在**棋盘格**和**场景静帧**上合成查看，不能只探查文件头  
- [ ] **立绘 alpha 验收：** 用能保留 alpha 平面的解码器。VP9 源须 `ffmpeg -c:v libvpx-vp9`（应为 `yuva420p`，剪影 fill 不是 1.0）。默认 ffmpeg / ffprobe 常把带 `ALPHA_MODE=1` 的文件报成 `yuv420p`、fill=1.0，那不算过关  
- [ ] **立绘动作：** 每个角色的主读点对得上清单里写的人设动作，且不是和其他角色同一套深呼吸；第一秒已经有明显运动

时长与帧率跟槽走，不在本规范写死唯一数字。已有实战参考（不是普适强制）：某世界封面 loop 用 VP9、1280×720、24fps、约 12s 的轻量循环；叙事底板常以 16:9（1920×1080 基准）为目标。数字人 seed 的 35–45s 词库循环不套在场景底板上。

**STOP** 未过接缝的条目只重做该条。

### Cine4 · 交付

**完成：** live 路径上每条都是成片 + 海报静帧 + 清单字段齐全。

交付契约：

- 原生画幅：场景板是场景板，地图是地图，禁止把 1:1 塞进 16:9 槽。  
- 命名按地点/动作；清单写 `src`、`poster`、`kind`、时长、是否循环。`portrait-alpha-idle` 还要写该角色的可读动作。  
- **立绘 alpha idle 的游戏内文件**是带 alpha 的循环图（默认 animated WebP），由 `<img>` 播（与静帧同一布局：`object-fit: contain`，背景透明）。可保留抠好的 VP9 WebM 作源，但 `play/` 不得把立绘 `<video>` 指向它。场景 idle 仍用不透明 H264 MP4 + `<video>`。  
- 过场挂在节点上（`media: { type: "video", src, poster }`），`play/` 不调用生成器，包内无密钥。  
- 替换后 bump `?v=` 或等价缓存。  
- 加载幕（若有）：在窗口前先盖住，直到立绘/场景静帧（以及将播放的 intro）解码完成，再用短交叉淡入把板交给画面。已有实战：某世界用约 720ms 交手；循环视频与装饰盾层**不要**一直占着加载板。具体毫秒可按壳调整，但「等到静帧就绪再交手」是门，不是装饰。  
- 只学构图与节奏。禁止把他作官方视频、字体、Logo、UI 贴图拷进可分发目录。

**STOP** `step Cine4: accept`

## 4. 失败与停手

- 未锁静帧就 i2v  
- 把三版失败片 concat 成正片  
- 场景 loop 丢掉主体或改机位  
- 游戏内 alpha idle 烤了不透明背景，或浏览器里播成人物尺寸的实心框（VP9 alpha 被丢掉）  
- 用腰际 U 形淡出冒充透明底  
- 全员同一套深呼吸，或几乎静止的「静帧改视频」当 idle  
- 在本 skill 重写 PixVerse 字段或精灵表流程  
- 运行时现生成过场  
- 把 alpha idle 当 R1 seed 上传

已过关的条目禁止为下一层回头「再生成三张」。作者不满意时审计当前 `kind`，不把切片扩成新地点再补拍。

## 5. 转交

| 情况 | 去 |
|------|----|
| 没有主外观 / 静帧 | `/mesh-rpg-craft look` 或 `portrait` / `scene` |
| 要做数字人 seed | `/pixverse-r1 seed` |
| 要横条精灵 | `/animate-sprites` |
| 要夜景 UI 气质，而不是片子本身 | `/cotny-style-narrative-ui` |
| 批量静帧立绘/地点板 | `/world-bible-pack`（出图后若要动起来，回到本规范） |
| 片子要进发布包 | `/world-ship-qa`（加载门与资源抽查） |

## 6. Session bootstrap

```
load:
  - 本 SKILL.md
  - {CAMPAIGN}/docs/LOOK.md、docs/VIDEO.md（若有）
  - /mesh-rpg-craft/references/PORTRAIT.md、SCENE.md、LOCK-ORDER.md
  - /pixverse-r1/references/SEED_VIDEO.md   仅当条目 kind 是 r1-seed（然后停手转交）
  - /cotny-style-narrative-ui 当作者点名慢循环夜景平板气质
preflight:
  - 源静帧已接受，或本步就是退回静帧门
  - 不把失败视频写入 live
  - 立绘 alpha idle 必须有逐人动作简报，且交付路径能在目标浏览器里真透明叠场景
  - 不在本会话改 NPC 卡或世界书
```
