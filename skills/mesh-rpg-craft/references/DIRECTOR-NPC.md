# C · NPC 与导演

导演是**当前拍的消费者**，不是全知作者。全知发生在编写硬节点和拍门控卡的时候。

## 模块化 NPC 卡

每张说话卡一组：

| 字段 | 作用 |
|------|------|
| `conditions` | 这拍才注入 |
| `opening_line` | 开口就说（覆盖静态 `npc.dialogue`） |
| `presence_line` | 在场叙述 |
| `known_text` | 导演笔记：现在事实，不写「不要说旧事实」 |
| `forbidden_claims` | 硬禁（名字、西路、开棺） |

引擎：`buildContextPack` 只收 `evaluateConditions` 通过的行；`voiceLine` / `presence` 走拍呈现，不走未门控静帧。

行踪另写一行事实：人在哪、尸体在哪（侧厅 / 教堂 / 墓地 / 已入土）。

## 导演

- 合法动作与卡同一套 `conditions`。  
- 需要小游戏、战斗、CG：派发**已注册** action（`npc_conflict` / `story_cinematic`），不在台词里假装播了。  
- 关系网变化：只通过已声明的 relationship / knowledge / flag 效果；导演appraisal 不改节点。  
- 玩家跑题：先按当前拍人设正面答，再引回该 NPC 本拍目标；禁止提系统选项。

## 完成标准

在目标房间、目标 flag 下：开口、在场、候选动作、兜底问答，都不出现上一拍的世界状态。  
`audit` 时用正向匹配（「棺在这块地」）而不是负向「不得出现侧厅」——负向会误伤「不要说侧厅」这种笔记。
