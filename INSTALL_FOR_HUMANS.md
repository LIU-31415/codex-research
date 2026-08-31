# 安装说明（给人看）

`codex-research` 是一个 Codex Skill。推荐让 Codex 自己完成复制和检查，人只需要确认源目录与安装范围。

## 推荐方式：指挥 Codex 安装

在包含本项目的 Codex 对话中，把下面这段发给 Codex，并把路径替换成你的实际路径：

```text
请读取 <项目目录>\INSTALL_FOR_CODEX.md，并按其中步骤把本仓库的 codex-research 安装为当前用户的 Codex Skill。
安装前先核对源目录确实包含 SKILL.md 和 references/；如果目标目录已有内容，不要直接覆盖，先告诉我差异并等待确认。
这次只安装 Skill，不安装或配置 paper-search-mcp，不修改其他 Codex 配置。
```

例如本机目录是 `C:\Users\LIU\Desktop\codex-research` 时，可以写成：

```text
请读取 C:\Users\LIU\Desktop\codex-research\INSTALL_FOR_CODEX.md，并按其中步骤安装这个 Skill。安装前先检查目标是否已有同名 Skill；有差异就先报告，不要覆盖。
```

Codex 会把可运行的文件放到用户级目录 `~/.agents/skills/codex-research/`。它只应复制 `SKILL.md` 和 `references/` 等运行所需内容，不需要把整个 Git 仓库塞进 Skill 目录。

## 安装后验证

开一个新的 Codex 对话，显式调用：

```text
$codex-research 请先帮我把“某技术为什么在不同条件下表现不同”拆成几个可检索的研究问题，不要马上生成论文清单。
```

如果没有配置 `paper-search-mcp`，Skill 仍可以做问题界定和 Web 勘察；论文检索能力会受当前 Codex 工具配置限制。Skill 不会替用户安装或维护这个连接器。

## 安装范围

- **用户级安装（推荐）**：所有项目都能使用，目录为 `~/.agents/skills/codex-research/`。
- **仓库级安装**：只在指定仓库内使用，目录为 `<仓库>/.agents/skills/codex-research/`。

若安装后没有被识别，先开启新的 Codex 对话；仍未出现时再重启 Codex。

## 手动备用方式

只有在 Codex 无法执行安装时再手动复制。

### Windows PowerShell

在项目根目录执行：

```powershell
$dest = Join-Path $HOME ".agents\skills\codex-research"
New-Item -ItemType Directory -Force $dest | Out-Null
Copy-Item .\SKILL.md $dest -Force
Copy-Item .\references $dest -Recurse -Force
```

### macOS / Linux

在项目根目录执行：

```bash
mkdir -p "$HOME/.agents/skills/codex-research"
cp SKILL.md "$HOME/.agents/skills/codex-research/"
cp -R references "$HOME/.agents/skills/codex-research/"
```

发布包或压缩包如果不能直接被当前 Codex 识别，应先解包成一个包含 `SKILL.md` 的目录，再按照上面的方式交给 Codex 处理。
