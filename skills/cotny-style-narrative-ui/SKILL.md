---
name: CotNY-style narrative UI & art
description: >-
  use when designing or generating ORIGINAL narrative/VN UI, portraits, night
  backdrops, chrome, and FX that feel like Vampire: The Masquerade — Coteries of
  New York (dialogue-first painted noir; not combat HUD), including
  DokiDemo/Barovia shell restyles
---
# CotNY-style narrative UI & art（inspired only）

## When to use

- 做/改 **叙事向视觉小说壳**：对话主屏、地图枢纽、日志/关系、术语词典、标题/封面。
- 生成 **原创** 夜景底板、半身立绘、UI chrome、稀疏 FX 静帧/短循环，要求气质接近 CotNY。
- DokiDemo / Barovia 等项目要「CotNY 感」但保留本地叙事约束时。

**不要用** 在动作战斗 HUD、明亮高魔奇幻、二次元赛璐珞主视觉上硬套本 skill。

## Legal hard rule（硬规则）

- **只学构图、气氛、色板、动效节奏**；**禁止**把 CotNY / Shadows of New York / World of Darkness **官方美术、字体、Logo、UI 贴图、截图、rip 资源**放进任何 skill、`public/assets`、发布包或可分发目录。
- 产出必须是 **ORIGINAL** 绘画/立绘/矢量或 CSS chrome。
- 私有研究用的营销截图或临时采样只可留在本机研究目录，**分析完删除**；永不 commit。
- 文案与设定不要声称官方授权；Clan/Ankh 等商标符号勿原样复制进可发布 UI（可用抽象「左条/菱形标记」替代）。

## What “CotNY-like” means

几乎所有对白场景是 **三层叠**：

1. **满屏夜景底板**（painterly / 轻度 film grain / 重 vignette；可有极慢循环：雨、雾、窗帘、霓虹闪烁、车灯掠过）。
2. **半身立绘**（通常占右 1/3；腰上构图；表情克制；与场景 practical 光一致）。
3. **下三分之一对话板**（半透明近黑 slab + 猩红笔刷名牌 + 细锐红线框；2–4 条「像台词」的选项，不是系统动词）。

辅壳：

- **城市/活动地图枢纽**：一张区域插画 + 少量目的地点；点进场景。不是战斗小地图。
- **词典/术语**：遇词解锁；轻量 overlay；短条目。
- **日志/关系**：安静次级面板；政治与羁绊 > 战利品格。

气氛压过 chrome。不为阅读/选择服务的控件删掉。

## Visual tokens

| Token | Hex / 规格 | Notes |
| --- | --- | --- |
| Base / void | `#0a0a0c`–`#14181c` | 近黑；整屏偏低饱和 |
| Panel fill | `#12161c`–`#1e262e` @ 65–80% | 对话板半透明，透出底板 |
| Crimson UI | `#6b1018`–`#8b1a28`；线 `#9a2030`–`#c45a5a` | 名牌笔刷、细框、左强调条 |
| Gold rarity / chrome | `#78643c`–`#c5a059` | 顶栏图标、稀有强调；**绝不**大面积亮金 |
| Neon night（环境 only） | `#3a5f8a`–`#5d8aa8`；偶发品红 haze | 霓虹/屏幕光；**不要**做成彩虹 UI |
| Warm practical | `#967d59`–`#c5b358` | 烛光/台灯小面积 |
| Body text | `#f0f0f0`–`#ffffff` | 高对比 sans |
| Name text | 金/奶油色 on 猩红笔刷 | **衬线、全大写** |
| Choice idle | 暗半透明条 + 左细红条或简单圆点 | |
| Choice focus | 浅灰/羊皮纸斜切条 + 深色字 **或** 细红下划线 | 避免霓虹外发光轰炸 |
| Continue | 小块羊皮纸 `#c9b896` **或** 猩红 pill | 撕边/粗糙边可有，勿厚石板 |
| Grain | 全屏轻噪 4–12% | 统一立绘与底板 |
| Vignette | 边缘压暗 0.35–0.55 | 长软 mask，勿硬框 |

**Reject：** 明亮奇幻金洪流、厚重石雕按钮当主视觉、对话屏堆战斗条/小地图/背包格、赛璐珞二次元主风格、memes 贴纸、干净无拟物 flat SaaS UI、彩虹赛博 HUD。

## Screen recipes

### A. Conversation（主屏）

```
[ full-bleed night backdrop ]
[ portrait ≈ right third, waist-up ]
[ top-left: thin gold frame · 2 icons (log · glossary) ]
[ lower-third: translucent dark slab ]
   · crimson brush nameplate (serif caps)
   · body copy (clean sans, white)
   · 2–4 choice rows (spoken lines)  OR  CONTINUE chip
```

- 文本板 **不要挡住** 眼睛/嘴。
- 自由输入行（如「我想做的事情…」）视觉权重 = 普通选项，不是搜索框。
- **禁止** 本屏出现 HP/弹药/小地图。

### B. Title / hub cover

- 一张情绪关键艺术或慢循环夜景满屏。
- 标题用 **字体排印**（CSS），非血渍浮雕 PNG Logo（除非项目明确批准）。
- Continue / New Game = 细长暗色控件 + 可选左猩红条。

### C. Map travel hub

- 一张城市/区域插画底板；**少量** pin / 缩略目的地。
- 锁定路线：雾、链、「今晚关闭」——不是 MMO 灰节点墙。
- 每夜行动次数有限的「日程感」可保留；勿做成开放世界雷达。

### D. Glossary / dictionary

- 首次遇到术语 → 小 toast → 面板。
- 过滤：新/全部/未读；条目短；不剧透未解锁内容。

### E. Journal / relationships

- 安静列表或卡片；强调人物与立场，不是装备栏。

## Portrait style

- **笔触：** 数字油画感，可见笔触；半写实；拒绝干净向量描边与赛璐珞平涂。
- **光：** 戏剧性 chiaroscuro；主光来自场景 practical（街灯、烛、显示器）；可有冷 rim。
- **构图：** 腰上 / 胸上；微侧向画面中心；多在 **右侧**。
- **表情：** 克制区间——阴郁、警惕、疲惫、冷笑、压低的怒；少大喊大叫。
- **肤色：** 偏低饱和、偏冷或病态白；虹膜可有极弱超自然光，勿动漫星星眼。
- **服装：** 当代都市 / 俱乐部 / 正装 / 街头——现代哥特，不是板甲法袍。
- **动画：** 立绘基本静止；换表情 sparingly；边缘可轻微融入雾/grain。

## Backdrop style

- 当代都市夜景、破旧室内、走廊、俱乐部、画廊、轿车后座、屋顶、小巷。
- 低饱和 + 局部高光（霓虹、烛、屏幕）。
- **Grain + vignette + 轻 chromatic fringe** 可统一观感。
- 动画语汇：**稀疏慢循环**（雨丝、雾、闪烁灯、窗帘、车流光）——不是 busy 视差 UI。
- 分辨率目标 **16:9**（1920×1080 基准）；UI 安全区：下 32% 与右 30% 给板/立绘。

## UI chrome

- 边缘：细锐红线、可微斜/微锯齿；名牌 = **猩红笔刷/血抹**，非圆角徽章。
- 顶栏图标：旧金/青铜、线框金矩形，2 个即可。
- 字体感：标题/名 **人文衬线**；正文/选项 **干净无衬线**。
- 透明度：对话板透出底板；不要实心黑板。
- 选项行：口语短句；hover = 左红条或浅底反色，勿霓虹 glow spam。

## FX language

| FX | 密度 | 时长感觉 |
| --- | --- | --- |
| 环境循环（雨/雾/灯） | 低 | 连续慢循环 |
| UI fade / crossfade | — | **≤300ms** |
| 场景切换 | 淡入黑/叠化 | 300–700ms |
| 血腥 | UI 笔刷符号为主；叙事高潮才可屏幕溅点 | 短、克制 |
| 屏幕闪（disciplines / shock） | 极偶发 | 1–3 帧白/红闪 + 短 fade |
| 粒子 | 光源旁少量尘埃 | 稀疏，非暴风雪 |
| 立绘 | 基本静 | 表情切 ≤200ms |

**Reject：** 弹跳 spring、夸张 screen shake 连打、全屏粒子狂欢、战斗连击数字。

## Motion timing（摘要）

- UI 显隐：150–300ms ease-out。
- 选项 focus：100–180ms。
- 对话接续：无弹跳；点按即换或短 fade。
- 环境：循环周期 4–12s，幅度小。

## Art generation prompt templates

> 生成时务必加负面词：`official asset, rip, screenshot UI clone, anime cel, bright fantasy gold, combat HUD, health bar, chibi`

### Backdrop / 底板

**EN：** `painterly digital oil night scene, contemporary urban gothic interior OR rainy city street, low saturation, heavy soft vignette, subtle film grain, dramatic practical lighting (neon OR candle OR streetlamp), shallow depth, empty of UI and characters, 16:9 environment concept, moody World-of-Darkness-inspired atmosphere — original art`

**ZH：** `数字油画风夜景环境概念，当代都市哥特室内或雨夜街道，低饱和，重软暗角，轻微胶片噪点，戏剧性实用光（霓虹/烛光/路灯），浅景深，无UI无人物，16:9，阴郁压抑，原创`

### Portrait / 立绘

**EN：** `waist-up character portrait, painterly brushwork, pale desaturated skin, chiaroscuro, rim light matching night neon or warm lamp, restrained expression, modern clothing, facing slightly toward frame center, transparent or simple dark ground, no UI chrome, original character`

**ZH：** `腰上立绘，可见笔触油画感，低饱和苍白肤色，明暗法，边缘光与夜景霓虹或暖灯一致，克制表情，现代服饰，微侧向画面中心，透明或简单暗底，无UI，原创角色`

### UI chrome（参考板，勿抄官方）

**EN：** `dark translucent dialogue panel mockup, thin sharp crimson rules, rough crimson brushstroke nameplate with serif caps, clean white sans body text, small parchment continue chip, muted bronze icons in thin gold frame, high-contrast on near-black, minimal gothic narrative UI, flat layout sheet, no logos`

**ZH：** `半透明深色对话框示意，细锐猩红边线，粗糙猩红笔刷名牌配衬线大写名，白无衬线正文，小羊皮纸继续键，哑光青铜图标金细框，近黑高对比，极简哥特叙事UI示意，无商标`

### FX stills

**EN：** `sparse cinematic FX still: soft fog tendrils OR single dust motes in red bulb light OR one-frame crimson screen flash residue, dark empty frame, subtle grain, not busy particles`

**ZH：** `稀疏电影感FX静帧：薄雾 或 红灯泡下少量尘埃 或 单帧猩红闪屏余韵，暗色空镜，轻噪点，粒子不要密`

## Delivery checklist（交付）

- [ ] 比例：底板/合成屏 **16:9**（推荐 1920×1080）；立绘导出保留透明，高度足够覆盖下沿被对话板遮挡后仍见肩以上。
- [ ] 命名建议（项目内原创资源）：`bg_<loc>_night_v#`, `po_<id>_<emotion>`, `ui_panel_dialogue`, `ui_nameplate_brush`, `fx_fog_loop` —— **勿**使用官方角色/地点文件名。
- [ ] 导出：底板 JPG/WebP 质量优先；立绘 PNG/WebP 透明；UI 优先矢量/CSS，栅格仅纹理。
- [ ] 色检：平均画面暗；猩红只作强调；无大面积纯白 UI。
- [ ] 法律：无官方资产；私有参考未进仓库。
- [ ] 动效：UI ≤300ms；环境循环慢而稀。

## Do / Don’t

**Do：** 阅读舒适、稀疏猩红、口语选项、地图当章节选择、词典、原创绘画、grain+vignette、对话三角构图。  
**Don’t：** 复制 Draw Distance / Paradox 资产；声称 VTM 授权；对话屏上战斗 HUD；把章节做成纽约换皮而无本地叙事；GUI 框架级改动不经项目批准流程。

## Done check

- 陌生人一眼能分清：对白 / 地图 / 枢纽。
- 对白屏三角（底板+立绘+文本）完整。
- 无盗用资产。
- 若改 DokiDemo GUI 框架：已走视觉提案批准（见附录）。

---

## Appendix A — DokiDemo / Barovia（保留）

尊重项目门禁：

1. **内容 vs 壳：** YAML/剧情可直接做；**GUI 框架**改动（ConversationView 布局、CompanionHub、共享 chrome、主题系统重做）需 `VISUAL_APPROVAL.md`：实机截图基线 → 在截图上画 mock → `npm run visual:proposal` → 给用户看 → 明确「按照X做」→ `visual:approve` → `visual:check` → 再实现。
2. 优先在 `src/free-roam/ui/theme.ts` 加主题预设（如 `night_crimson`）+ pack `presentation.theme` 覆盖，再考虑改布局。
3. Barovia 已有猩红强调：CotNY 化 = 更深面板、更安静 chrome、对话优先、少青铜石钮。
4. **不要**把 CombatView 当章节卖点；西路保持封闭；封面标题若已批 CSS 则保持。
5. CSS/主题后：`npm run build:html`，硬刷新玩家包 `:8766`。
6. 动 HUD 血尘与 CharacterAura 时保持隔离。

### 建议改动顺序（批准后）

1. `theme.ts` — `night_crimson`
2. `free-roam.css` — 对话板、封面、选项行；长软暗角
3. `ConversationView.tsx` / `CompanionHub.tsx` / `GameShell.tsx` — 仅当层级变（需提案）
4. Pack 原创夜景/立绘
5. 测试：chrome class / 文案锚点；Barovia 语感测试不动

## Appendix B — Research notes（给维护者）

- 公开 Steam 营销图（app 1096410）足以锁定对话三角与色板；优先用其做构图研究。
- CotNY 评论普遍描述：静态立绘 + 环境微动画（雨/雾/叶/灯）；地图选夜程活动；词典随遭遇解锁。
- 本机 `VtmCony.app`（Draw Distance / Unity）：场景流 `MainMenu → PlayerCharacter → Gameplay → End/GameOver/Credits`；底板大量以 Addressables **1080p 60fps 慢循环视频平板** 形式存在（命名形如 `{ID}_{LOC}_OUTPUT_1080p_60fps_*.mp4`：街景、俱乐部、画廊、墓地、地铁、公寓、车后座等）；音频 FMOD；对话有 StreamingAssets CSV。生成时学「慢循环夜景平板」思路，**勿**把官方视频/贴图拷进项目。
- 安装目录若同时含 SoNY 对话库 / DLC 视频键，同样只作类型参考，禁止 rip。
