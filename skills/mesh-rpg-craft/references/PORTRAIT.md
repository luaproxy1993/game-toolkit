# A · 立绘轨

生成器字段以 `game-asset-core`、`game-character-consistency`、`game-animation-frames` 为准。这里只写 Doki 网状战役多出来的契约。

## A1 静帧

- 主体隔离，平面键色或真透明，剪影干净。  
- 不烤地面、不烤房间、不烤光晕粒子。  
- 同一人：一张 master still，其余 `image_edit`。  
- 对话立绘、创建页缩略、卡片，同一身份，只换裁切。  
- 完成：键边无杂色；和 `LOOK.md` 锚图同一套气质。

## A2 alpha intro

- 输入必须是已接受的 A1。  
- 画幅、人物在画布中的比例，与静帧一致。  
- 透明：WebM+VP9 或绿幕 MP4 + 运行时 chroma；不要用亮度去底。
- **已锁白纸底 / LOOK 写明不抠透明时：** 不要照抄本默认。进场片保留纸白（或不透明底），MP4 可不抠；叠在面板旁，不叠进房间画面去底。已锁键/底规则优先于本文件的 chroma 默认。  
- 作者要「三个镜头 2」= **三个完整备选**，不是三段失败片接成一条。  
- 完成：循环或单次出场与静帧可叠；狼/门/棺等主体清单不丢。

## A2.5 游戏内 alpha idle loop（R2 数字人的第一步）

和 R1 seed 分开：游戏对话要叠在**房间场景**上，所以 idle 必须带透明，不能烤 still plate。

- 输入：已接受的 chroma 静帧（纯绿底，与立绘同一姿态）。  
- i2v：机位锁、口闭合、手不离躯干；绿幕全程保持。词库多段（呼吸/眨眼、侧头、重心），每段 6s。  
- 回文接缝（forward+reverse）再 chromakey → VP9 `yuva420p` WebM + 绿幕 H264 MP4（canvas 去底）。  
- 对话：intro 播一次，然后 loop idle。减动效则静帧。  
- R1/R2 实时棚的 seed 仍走 `pixverse-r1` `SEED_VIDEO.md`（不透明 still plate，~40s）。不要把 alpha idle 当 seed 上传。

## A3 特效生成器

- 配方绑人设（血、尘、烛、雾），密度写死，运行时 canvas/DOM 叠在立绘上。  
- 禁止把 FX 烘焙进 PNG 再给 intro 用。  
- 人设变了只换配方 id。  
- 完成：关 FX 立绘仍能单独成立。
