# Evaluation run outputs

`run_eval.py` stores generated run directories here. Raw outputs may contain prompts, local paths, configuration values, tool traces, source excerpts, or other sensitive content. Except for this README, they are ignored by Git by default.

Before committing evaluation results, review and redact them while retaining:

- `manifest.json`;
- `scores.json`, completed from `score-template.json`;
- the baseline and Skill `prompt.txt` files and final outputs;
- tool events in `events.jsonl`;
- per-check scores following `evals/rubric.md`;
- an explanation of failures and the execution environment.

Workspace-relative fixture instructions reduce unnecessary paths in prompts. They do not make raw run records safe to publish without review.
