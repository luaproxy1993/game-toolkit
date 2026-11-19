# PixVerse 数字人 · Locked-Portrait Seed

> 单一事实源。R1 HTTP / Agora 仍以 `VERIFIED_API.md` / `AGORA_PROTOCOL.md` 为准。  
> 说话层见 doki-game-maker `R2_DIALOGUE_PROMPT.md`。导播见 DataStream `prompt_message`。  
> **本文件只管种子视频：** 动作幅度小、稳定性高的数字人，先把 seed 做成 locked-portrait loop。

## 0. 产品位置

R1 是自回归实时流：每一帧吃前面的帧，也吃 seed 的运动词库。  
说话时语态、lipsync、微动作稳不稳，**先看 seed，再看导播**。

```text
世界 r1_world.json          场景长什么样（静）
seed  assets/r1/seed.mp4    人物怎么闲着（本标准）
说话  r2_realtime_dialogue  怎么答、怎么念
导播  prompt_message        此刻画面发生什么
```

四层禁止糊成一条。`world_setting` 不写动效；导播不补镜头和背景戏；说话信封不写构图。

本模式默认 `style: Ambient`。POV / Dramatic 会抢镜头和剧情，不用于「小幅度高稳定」数字人。

## 1. Locked-portrait 铁律

优秀 seed 同时满足下面全部。缺一条，运行时口型/动作就会漂。

| # | 铁律 | 完成标准 |
|---|------|----------|
| 1 | **人物绝对中心** | 主体在画面几何中心；头+肩（近景）或头到腰（中景）；不偏、不裁半张脸 |
| 2 | **近景或中景，面部清晰** | 双眼、嘴、下颌在画幅里可读；口型像素够用。远景 / 全身站立不合格 |
| 3 | **Fixed camera** | 锁死机位。允许极轻的缓慢缩放。禁止 pan / tilt / orbit / handheld / 切镜 |
| 4 | **Loop seam** | 首帧与尾帧姿态、构图、光、背景可无缝接。循环播放时没有跳一下 |
| 5 | **~40s 词库 loop** | 成片约 35–45s。短于 ~20s 词库不够，模型会塌成同一下抽动 |
| 6 | **Idle vocabulary** | 多段不同的小动作，不是一条 2s 呼吸循环拉长。看 40s 不觉得在重播同一拍 |
| 7 | **Still plate 背景** | 背景等于一张不动的底图。零粒子、零闪灯、零天气、零行人、零布料自运动。背景**不参与**人物动效 |

**幅度小 × 词库多。** 幅度指单次位移；词库指 40s 里有多少种不同的闲着。

## 2. Idle vocabulary（seed 里只放这些）

Seed 是**静息态**，不是预录说话、不是表演秀。口型留给运行时。

词库（上半身微动，始终面向镜头）：

- 眨眼、轻呼吸、肩胸起伏
- 重心在两肩之间微调
- 头微侧再回正、目光略偏再看回镜头
- 手指/手腕休息位微调
- 发丝或衣领的被动微颤（贴着身体，不独立成景）

幅度上限：手不离开躯干轮廓；头转不超过约 1/8 圈；脚/髋不走出原站位；身体不出画。

## 3. Still plate（背景）

背景在 seed 全长里是同一张静帧。人物在它前面动，它自己不动。

制作时先定一张背景静帧（或把角色抠在静景上），再只动人物。验收时把任意两帧背景差一下：只应看到人物区域在变。

`world_setting` 只描写这张静景（空间、光线、陈设），不写「风吹、霓虹跳、蒸汽涌」。

## 4. 制作步骤

Imagine 单段只有 6s / 10s。40s seed = **同一张 master still 上的多段 idle 拼接**，不是一条长文生视频。

1. **Master still**  
   人物绝对中心，近景或中景，面部清晰，背景已是 still plate。构图从此锁定。后续一律 `image_edit` / `image_to_video` 从这张长，禁止重新 `image_gen`。

2. **Idle 段**  
   从 master still 出 4–6 条 6–10s：每条**一种**微动 + `camera locked`。首帧就是 still。不同条换词库，不换机位、不换景、不换衣服。

3. **拼到 ~40s**  
   `ffmpeg` concat（同分辨率同帧率，`-c copy`）。段与段之间姿态要接得上；做不到就在段间回到 master still 再接下一条。

4. **Loop seam**  
   尾帧回到 master still（或与首帧可叠化）。整条循环播 2 圈，接缝处无跳、无闪、无背景位移。

5. **接入 R1**  
   - 静帧：`world/create` 的 `image_url`（`style: Ambient`）  
   - 成片：`init_message.preset_video_uri`（见 `AGORA_PROTOCOL.md`）  
   - pack：`assets/r1/seed.mp4` + `assets/r1/seed_still.png`；`r1_world.json` 只指路径，不把运动写进 `world_setting`

## 5. 导播怎么吃这条 seed

Seed 已经锁了镜头和背景。运行时 `prompt_message` **只改人物**：

```text
面向镜头，近景，口型跟着这句话，轻微点头。镜头与背景保持原样。
```

进程感知句同样：半身、面向镜头、微表情；不写运镜、不写场景 FX。

## 6. 验收（可勾）

- [ ] 人物在画面正中，近景或中景，双眼和嘴清晰  
- [ ] 全程 fixed camera；若有缩放，幅度仅能感觉到「轻轻靠近」  
- [ ] 循环 2 圈，首尾无跳帧  
- [ ] 时长 35–45s  
- [ ] 40s 内至少 4 种可分辨的 idle（眨眼/呼吸/重心/侧目…），不像一条循环拉长  
- [ ] 任意两帧对比，背景像素基本不动  
- [ ] 人物无行走、无大幅度挥手、无转体出画、无对物体交互  
- [ ] 嘴在静息闭合或微张休息，没有在念词  
- [ ] `r1_world.style = Ambient`；seed 路径已写，运动未写进 `world_setting`

## 7. 反模式

| 反模式 | 正确 |
|--------|------|
| 全身远景 / 人物偏一侧 | 绝对中心，近景或中景，脸可读 |
| 运镜、手持、环绕、推拉很大 | fixed camera，最多极轻缩放 |
| 背景粒子、闪灯、天气、路人 | still plate |
| 走路、坐下、拿东西、大挥手 | idle vocabulary，手不离躯干 |
| 8s 单一呼吸循环当 seed | ~40s，多种微动 |
| 首尾姿态不同，硬切循环 | loop seam |
| seed 里已经在说话/唱歌 | 静息态；说话留给运行时 |
| 每段 idle 重新文生，脸和景都漂 | 从同一张 master still 长出来 |
| 把「镜头锁定、背景别动」写进说话信封 | 构图在 seed；说话只负责怎么答 |

## 8. Agent 协议（`/pixverse-r1 seed`）

1. 定构图：近景或中景、绝对中心、Ambient、still plate。  
2. 出 master still；后续全部从它派生。  
3. 规划 idle 词库 ≥4 种，写每段一条动作。  
4. 生成 4–6 段 6–10s → concat ~40s → 验 loop seam 与背景差。  
5. 落到 `assets/r1/seed.mp4` + `seed_still.png`；`r1_world.json` 指路径、`style: Ambient`。  
6. 对照 §6 逐条勾。不合格先改 seed，不靠导播补镜头。

已有成片审计：只对照 §1 / §6，列失败项，不重写人设。
