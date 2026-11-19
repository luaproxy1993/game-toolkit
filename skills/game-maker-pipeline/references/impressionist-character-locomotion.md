# 写意角色表意（Impressionist Character Locomotion）

> **v1.8.1** · 规则 **RE-28** · 默认角色 locomotion 模型  
> 类比：中国山水画用笔意与动势表意，不靠透视写实。

## 何时启用（默认 ON）

以下类型 **默认** `animation_model: impressionist_single_sprite`，无需作者特别声明：

- top-down / 侧视 survivor、horde、arena
- 小品 RPG、氛围探索、陪伴 slice
- mockup 中可见「一个小人/剪影」但无 walk 帧合同
- AI 美术产能不足以支撑 sprite sheet 时

**禁自动启用**（须 gdd 显式 `animation_model: sprite_sheet` + 作者 `locomotion: accept sprite_sheet`）：

- 平台跳跃（精确落点）
- 格斗（帧对齐 hitbox）
- 作者明确要求多帧 walk/attack

## 核心合同

| 项 | 规则 |
|----|------|
| 资产数 | **1 PNG/角色**（+ 可选 1 张 `*_hit_flash` 同图 tint，仍算 1 registry 条） |
| 方向 | 仅 **left / right**；`scaleX` 翻转，**不生成** reverse 图 |
| 垂直轴 | **无** up/down facing；俯视或侧视锁死 |
| 走路 | 程序 **bob_y + tilt**（sin 波），不换帧 |
| idle | 轻微 **breath_bob** |
| 攻击/蓄力 | **squash** 压扁再弹回（≤150ms） |
| 受击 | **shake** 随机偏移 2–4 帧 |
| 死亡 | fade + squash（可选） |
| 远景单位 | 同图 **scale ↓ + alpha ↓**（泼墨远近） |

**RE-28：** 写意 locomotion 的动画在 **runtime 代码** 实现；**不**受 RE-10「动画默认 phase-2」约束（该条仅针对 **资产批次** walk 帧/粒子贴图）。

## Registry 登记（RE-19 兼容）

```json
{
  "asset_id": "HERO_PIXEL",
  "category": "character_single_sprite",
  "phase": 1,
  "output_path": "assets/v01/characters/hero.png",
  "aspect_ratio": "1:1",
  "references": ["ANCHOR-ID-v1"],
  "animation_model": "impressionist_single_sprite",
  "locomotion_contract": {
    "directions": ["left", "right"],
    "flip_axis": "x",
    "no_vertical_facing": true,
    "procedural_effects": {
      "walk": ["bob_y", "tilt"],
      "idle": ["breath_bob"],
      "attack": ["squash"],
      "hit": ["shake"],
      "death": ["fade", "squash"]
    },
    "sprite_sheet_forbidden": true
  },
  "prompt_delta": "ONE isolated pixel character sprite, orthographic side or top-down readable silhouette, transparent ground-aligned base, 32-48px readable at 4:3 viewport. Single pose neutral stand.",
  "verification": {
    "transparent_bg": true,
    "ground_line_px": 0,
    "anchor_px": { "left": 0, "bottom": 0, "width": 48, "height": 48 }
  }
}
```

## asset-decomposition.json 字段

```json
{
  "id": "HERO_PIXEL",
  "type": "character_single_sprite",
  "animation_model": "procedural_impressionist",
  "registry_ref": "HERO_PIXEL",
  "runtime_module": "game/impressionist-sprite.js"
}
```

## 白盒实现要点（re_07）

1. 独立模块 `game/impressionist-sprite.js`（或内联 `app.js` 同函数集）
2. 绘制顺序：`translate(x, y+bobY)` → `scale(facing * (1+squash), 1 - squash*0.3)` → `rotate(tilt)` → `drawImage`
3. **禁止**为多方向 walk 预留空槽或 CSS sprite sheet 占位
4. 敌人可复用同一 `ImpressionistSprite` 类 + 不同 `output_path`

### 参考实现（伪代码）

```javascript
function updateImpressionistSprite(s, dt, vx) {
  if (vx !== 0) {
    s.facing = vx > 0 ? 1 : -1;
    s.walkPhase += dt * 8;
    s.bobY = Math.sin(s.walkPhase) * 2;
    s.tilt = Math.sin(s.walkPhase) * 0.08;
  } else {
    s.bobY = Math.sin(performance.now() * 0.003) * 1;
    s.tilt = 0;
  }
}

function drawImpressionistSprite(ctx, s, img) {
  const w = img.width, h = img.height;
  ctx.save();
  ctx.translate(s.x, s.y + (s.bobY || 0));
  const sq = s.squash || 0;
  ctx.scale(s.facing * (1 + sq), 1 - sq * 0.3);
  ctx.rotate(s.tilt || 0);
  if (s.shake) ctx.translate((Math.random() - 0.5) * s.shake, 0);
  ctx.drawImage(img, -w / 2, -h);
  ctx.restore();
}
```

## 与背景层协调

写意角色 **不要求** 背景拆成血月+多层云独立 PNG。推荐：

| 层 | 策略 |
|----|------|
| 天空/血月/远云 | **scene_plate 整板** 或 **Canvas/CSS 程序化**（gradient + noise） |
| 可动云 | 最多 **1–2 层** parallax PNG，`scroll_factor` 登记在 `asset-decomposition.json` |
| 角色 | 单图 + 程序动效，z-order 在场景 UI 之下、前景特效之上 |

**禁止：** 为「山水画意境」强行 AI 拆解 5+ 背景零件且指望像素对齐。

## 策划案 / GDD 必填句

`idea-brief.json` → `策划案.systems_phase_1` 或 `gdd/input-map.json`：

```json
{
  "character_locomotion": {
    "model": "impressionist_single_sprite",
    "rule_id": "RE-28",
    "rationale": "单图+程序动效；省 AI 帧一致性成本；侧视/俯视仅左右"
  }
}
```

## 验收清单

- [ ] registry 仅 1 条 character（每角色 1 PNG）
- [ ] `locomotion_contract.sprite_sheet_forbidden === true`
- [ ] game/ 无 `walk_*.png` / `attack_*.png` 多帧硬编码路径
- [ ] 换向仅靠 `facing` 翻转，无反向图资产
- [ ] idle 有 breath；移动有 bob/tilt
- [ ] `art_verify` / `match_and_correct` 仍对 **该单图** 跑 RE-25/27

## 违反 → TERMINATE

| 码 | 条件 |
|----|------|
| T-LOC-01 | 未登记 sprite_sheet 合同却生成 walk 多帧资产 |
| T-LOC-02 | 写意合同下用 CSS sprite sheet 或 object-fit 多帧硬贴冒充动画 |
| T-LOC-03 | mockup 仅 1 小人却 scope 膨胀为多方向动作表 |

## 作者门（仅当偏离默认时）

```
locomotion: accept impressionist   # 确认单图写意（默认可省略）
locomotion: accept sprite_sheet  # 显式要多帧表；须补 delivery 工时
```