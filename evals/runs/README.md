# Evaluation run outputs

`run_eval.py` 生成的运行目录放在这里。原始输出可能包含提示、工具轨迹、来源摘录或其他敏感内容，因此除本说明外默认不纳入 Git。

提交评测结果前请先脱敏，并同时保留：

- `manifest.json`；
- `score-template.json` 填写后形成的 `scores.json`；
- baseline 与 Skill 的 `prompt.txt` 和最终输出；
- `events.jsonl` 工具事件；
- 按 `evals/rubric.md` 记录的逐项评分；
- 对失败和运行环境的说明。
