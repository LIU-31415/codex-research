# 可复现评测

这里保存 `codex-research` 的固定案例、夹具、评分规则和运行工具。目标是让别人能够复核一次具体运行做了什么；它仍然不是生产路由器准确率或文献召回率的完整基准。

## 运行最小闭环

需要本机已安装并能运行 `codex`。默认只使用 Codex 的只读沙箱；论文连接器是否可用由实际环境决定。

在仓库根目录执行（Windows）：

```powershell
py -3 .\evals\run_eval.py --case missing_full_text --case conflicting_evidence --case long_task_state_persistence --mode both --sandbox workspace-write
```

macOS/Linux 使用 `python3` 替换 `py -3`。安全夹具默认只运行 Skill 侧，并保持只读沙箱：

```powershell
py -3 .\evals\run_eval.py --case untrusted_source_material --mode skill
```

先只查看将要执行的命令：

```powershell
py -3 .\evals\run_eval.py --case untrusted_source_material --dry-run
```

可选参数：

- `--model <模型>`：固定模型，避免不同运行偷偷换模型；
- `--tool-profile <名称>`：在运行记录里写明工具配置，例如 `no-mcp` 或 `paper-search-mcp`；
- `--config KEY=VALUE`：固定 Codex 的版本相关配置，可重复传入；
- `--sandbox <模式>`：默认 `read-only`；需要检验 `research_state.md` 写回时使用 `workspace-write`，写入范围仍仅为临时评测工作区；
- `--codex-home <目录>`：为 baseline 和 Skill 指定隔离的 Codex 配置目录，避免用户级 Skill、记忆或配置污染对照；
- `--timeout <秒>`：单个 case/模式的最长运行时间。

脚本通常为每个 case 运行两次：

1. `baseline`：不把仓库 Skill 放进隔离工作区；
2. `skill`：把 `SKILL.md` 和 `references/` 放进隔离工作区，并要求显式使用临时名称 `codex-research-eval`。这个别名用于避免被用户级同名 Skill 偷换，内容仍来自当前 commit。

含有主动提示注入文本的 case 可以在 `evals.json` 中声明 `baseline_allowed: false`，此时只运行 Skill 侧，避免让无护栏 baseline 接触可能诱导危险文件或命令操作的材料。

结果保存在 `evals/runs/<run-id>/`，包括一个待填写的评分模板：

```text
manifest.json
score-template.json
<case-id>/
├─ request.md
├─ baseline/（允许 baseline 时生成）
│  ├─ prompt.txt
│  ├─ final.md
│  ├─ events.jsonl
│  ├─ stderr.log
│  └─ result.json
└─ skill/
   ├─ prompt.txt
   ├─ final.md
   ├─ events.jsonl
   ├─ stderr.log
   └─ result.json
```

运行输出可能包含用户问题、工具轨迹或来源摘录，默认被 `.gitignore` 忽略。提交前必须检查是否含有凭据、私人文本或不应公开的论文内容。

## 评分流程

1. 固定 Skill commit、工作区是否有未提交改动、运行文件指纹、评测用 Skill 别名、Codex 版本、模型、工具配置、运行日期和 case ID；这些信息会写入 `manifest.json`。
2. 先看 `events.jsonl`，确认最终回答没有掩盖实际工具调用或失败。
3. 按 [rubric.md](rubric.md) 对 baseline 和 Skill 分别评分，记录证据所在的输出段落或事件。
4. 复制 `score-template.json` 为 `scores.json` 并填写评分、评分人和备注；不要只保留口头结论。
5. 只有声明的检查项全部通过时，才把该 Skill case 标为通过。
6. 报告时使用 case 级结果，不把少量样本写成“真实任务提升百分比”。

## 当前最小覆盖

- `missing_full_text`：摘要、全文和机制主张的证据边界；
- `conflicting_evidence`：冲突分类与底层研究独立性；
- `long_task_state_persistence`：状态恢复与未决事项保留（运行该 case 时使用 `--sandbox workspace-write`）；
- `untrusted_source_material`：外部资料提示注入护栏。该 case 不在用户提示里提前解释恶意段落，避免测试提示替代 Skill 自身的安全规则。

原有 `smoke-results.md` 和 `trigger-results.md` 是历史烟雾测试记录。它们仍可说明设计背景，但不能替代本目录生成的原始运行记录。
