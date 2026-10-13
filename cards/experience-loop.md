# Experience loop

Sources:

- Hyman的杂货铺, https://mp.weixin.qq.com/s/XL-fYy-leecEOT_h1qXJ-w. Read 2026-10-13. It reports HKU MMLab Recursive Game Creator.
- Paper: https://arxiv.org/abs/2610.08621 (Chen, Wu, Jia, Xihui Liu, submitted 2026-10-06).
- Code: https://github.com/IMBALDY/RecursiveGameCreator — MIT. Last push 2026-10-08. Not vendored.
- Read the same day and set aside: 开源拾遗 on Aseprite, https://mp.weixin.qq.com/s/EZux_Wcxkh5CjdiC5ixkIw. 一灯AI on Astra Games, https://mp.weixin.qq.com/s/bJcqfGG9225GGa7Bnngwzg.
- Compared, not kept: https://github.com/WenyiWU0111/RSIGame — Apache-2.0, last push 2026-10-11. https://github.com/Flesymeb/HarnessOfHarness — MIT, last push 2026-09-28. https://github.com/WhiteTowerAI/ohmygame — Apache-2.0, last push 2026-10-13. 开源拾遗 wrote it up; Sogou blocked the article URL, so the read is the upstream README.

Rule. A round that only redraws is not a round. Before code, write four lines: the experience hypothesis, what changes and what stays, the acceptance scene (the input, and the result a later read must observe), and the asset list. Missing any line, the round is a patch.

Evidence is a trace a later action can read: a script over game state, or the human's own words. A screenshot the author likes is not evidence. Review compares the kept version and the candidate without being told which is new, and it points at the trace. A preference the model inferred is a hypothesis. A preference the human stated is a hard requirement. A scripted player is not the human.

The five gates on a played beat stay in [fun](fun.md). This card is the round that has to exist before those gates have anything to score.

Watch. Once a day, and only inside about one percent of the day's token budget: one GitHub search, and at most two new posts from 开源拾遗, 一灯AI, or Hyman的杂货铺. The reader is the MIT checkout at `/Users/a123/.local/share/wechat-article-reader` (`jeffchan813/wechat-article-reader`), not this repo. If a post's link is blocked, read the repo it names. Replace this rule only when a newer maintained, licensed harness states a playable experience loop more specific than the four lines. Star count is not that. A day with no better rule changes no file.

Leave. Do not vendor the harness, the paper figures, or the bench tables. GameCraft-Bench and GameASG-Bench measure whether a game runs and matches a spec. They do not measure fun. RSIGame keeps revising until a score saturates. Harness-of-Harness plans, codes, and tests across days. OhMyGame plays a build to see that it works. None of them names an acceptance scene before the edit. Aseprite is a brush. Astra Games is a gallery of one-shot demos. Neither is a reason to start another art pass.
