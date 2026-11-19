# 和 `/rpg-campaign-maker` 怎么接

两套技能管同一场切片的**不同层**。战役 maker 写**坐下来玩什么**。本 skill 写**Doki 网状实现时层与层怎么锁**。不要两套 lock，不要两套世界书。

```text
/core-rule-book          可选：世界箱（文本）。不是这场切片。
        ↓ 切一局
/rpg-campaign-maker      这场 sitting：切口、树、检定、原声、3 分钟验收
        ↓ 要 Doki 网状 / 导演 / intro / idle / 拍门控时
/mesh-rpg-craft          锁序：外观 → 静帧 → 视频 → 节点表 → NPC 卡 → 导演
        ↓ 可选
/doki-game-maker         收成卡带。未玩通 sitting 时不要开。
```

同一战役文件夹。`docs/LOCK.md` 只有一份，由 rpg-campaign-maker C0 写。本 skill 的 `docs/LOOK.md` 是外观锁，不是第二份切片锁。

## 谁拥有哪份文件

| 文件 | 主人 | mesh 做什么 |
|------|------|-------------|
| `docs/LOCK.md` | rpg-campaign-maker C0 | 只读。切口、系统名单、3 分钟句、语音、IP、入口脸 |
| `docs/BIBLE.md` / `docs/TREE.md` | rpg-campaign-maker C1 | 只引用页码，不重写世界。框文如需摘录，只放私有 `_raw/source/`，不进发布树 |
| `play/story.js` 或选择树 | rpg-campaign-maker C2 | 静态 AVG 仍走树。Doki 网状另写节点表，**不删树** |
| `docs/NODES.md` 或 pack `quest`/`event` 表 | **mesh M6** | 房间 + flag + 谁在场 + 下一拍。挂在 C2 的系统名单上 |
| `docs/LOOK.md` + 锚图 | **mesh M0** | C4 开始前必须有。C4 的 chroma/FX 服从这把锁 |
| 立绘 / intro / 场景 / loop | mesh M1–M5 | 特化 rpg-campaign-maker C4，禁止 C4 心血来潮单点出图 |
| NPC 拍门控卡 / 导演 | mesh M7–M8 | 静态壳用树节点即可；Doki 自由探索必须有 |
| `play/sheet.js` 检定 | rpg-campaign-maker C2 | mesh M9 把同一套数绑到 HUD，不另发明属性 |

## 两种坐法

**A. 静态一切口（默认 rpg-campaign-maker）**  
C0→C3 照旧。到 C4 时 load 本 skill 的 `LOCK-ORDER.md`：先 M0 外观，再静帧，再 FX。没有导演、没有拍门控也算完成。C5–C6 仍交静态 `dist/`。

**B. Doki 网状（吸血鬼村这类，品类 `doki-mesh-world`）**  
C0–C1 仍是 rpg-campaign-maker（切口、原声、引文）。  
C2 的「树」= **硬节点表**（mesh M6），不是只有 `story.js`。检定和物品仍要能失败、能花掉。  
C3 壳 = 把内容包挂到**已有的 DokiDemo GameShell**。默认路径 `/Users/a123/grokmaker/campaigns/DokiDemo`，或该仓的 git worktree（例如 `DokiDemo-brew`）。品质门是与已发布、跑在同一壳上的 Strahd AVG 逐帧对等：满幅场景板、对话双人、intro、BGM、HUD。不要再搭一套 VN，也不要在战役根新写一个 walk / look / talk 的 `index.html`。盒子上没有 DokiDemo 就停手去取壳，不要用纸壳顶替。打开首个场景的本地 HTTP 不是完成。  
C4 = mesh M0–M5（出图从已锁锚 + 空间清单；失败板不得当下一稿参考；通过后 remount 进正在跑的包，LOOK 修订时同一趟退役旧锚）。  
然后 M7–M9，而不是急着 C6 静态包。本地试玩仍要 HTTP，但是挂在 DokiDemo 壳上，不是另写一页。

`pipeline_state.json` 可记两步：

```json
{
  "sitting": "rpg-campaign-maker",
  "step": "C2",
  "mesh": "mesh-rpg-craft",
  "mesh_step": "M0"
}
```

一次会话只推进其中一步。改立绘不重开 C0；改 NPC 认知不重开 C4。

## 转交口令

- 还没有切口、3 分钟句、入口脸 → `/rpg-campaign-maker lock`  
- 切口有了，图在互打、NPC 仍念上一拍 → `/mesh-rpg-craft audit`  
- 世界还没箱、这是整本设定不是一局 → `/core-rule-book`  
- sitting 能玩、要收成卡带 → `/doki-game-maker`（另一次会话）
