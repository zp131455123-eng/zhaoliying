# 记忆系统提示词 (2/4) — project-sync.sh 模板

## 项目文档同步脚本

这是一个统一管理多个项目文档同步到 OpenClaw workspace 的 Bash 脚本。

### 脚本内容

```bash
#!/usr/bin/env bash
set -uo pipefail
# project-sync.sh — 统一项目同步入口
# 用法: bash project-sync.sh [--fix]

FIX="${1:-}"
ERRORS=0; WARNS=0

red() { printf "\033[31m ✘ %s\033[0m\n" "$1"; ERRORS=$((ERRORS+1)); }
yellow() { printf "\033[33m ⚠ %s\033[0m\n" "$1"; WARNS=$((WARNS+1)); }
green() { printf "\033[32m ✔ %s\033[0m\n" "$1"; }
section(){ echo ""; echo "━━━ $1 ━━━"; }

WORKSPACE="$HOME/.openclaw/workspace"

# === 改成你的项目 ===
# 格式: "项目路径|sync目录名|sync脚本路径"
PROJECTS=(
  "/path/to/project-a|project-a-sync|scripts/sync.sh"
  "/path/to/project-b|project-b-sync|scripts/sync.sh"
)

# 1. 文档同步
section "1/3 文档同步"
for PROJ_ENTRY in "${PROJECTS[@]}"; do
  IFS='|' read -r PROJ_PATH SYNC_NAME SYNC_SCRIPT <<< "$PROJ_ENTRY"
  SYNC_DST="$WORKSPACE/memory/$SYNC_NAME"
  mkdir -p "$SYNC_DST"
  if [ -f "$PROJ_PATH/$SYNC_SCRIPT" ]; then
    if bash "$PROJ_PATH/$SYNC_SCRIPT" >/dev/null 2>&1; then
      green "$SYNC_NAME 同步完成"
      date +%s > "$SYNC_DST/.last-sync-ts"
    else
      red "$SYNC_NAME 同步失败"
    fi
  else
    yellow "$SYNC_NAME 无同步脚本"
  fi
done

# 2. 未推送检查
section "2/3 未推送检查"
for PROJ_ENTRY in "${PROJECTS[@]}"; do
  IFS='|' read -r PROJ_PATH SYNC_NAME _ <<< "$PROJ_ENTRY"
  PROJ_NAME=$(basename "$PROJ_PATH")
  if [ -d "$PROJ_PATH/.git" ]; then
    cd "$PROJ_PATH"
    BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    UPSTREAM=$(git rev-parse --abbrev-ref "@{upstream}" 2>/dev/null || echo "")
    if [ -n "$UPSTREAM" ]; then
      AHEAD=$(git rev-list --count "$UPSTREAM..HEAD" 2>/dev/null || echo "0")
      if [ "$AHEAD" -gt 0 ]; then
        yellow "$PROJ_NAME: $AHEAD 个未推送"
        [ "$FIX" == "--fix" ] && git push origin "$BRANCH"
      else
        green "$PROJ_NAME 已同步"
      fi
    fi
    [ -n "$(git status --porcelain 2>/dev/null)" ] && yellow "$PROJ_NAME 有未提交变更"
  fi
done

# 3. 汇总
echo ""
if [ "$ERRORS" -gt 0 ]; then
  printf "\033[31m❌ %d 错误, %d 警告\033[0m\n" "$ERRORS" "$WARNS"; exit 1
elif [ "$WARNS" -gt 0 ]; then
  printf "\033[33m⚠ 0 错误, %d 警告\033[0m\n" "$WARNS"
else
  printf "\033[32m✅ 全绿\033[0m\n"
fi
```

## 功能说明

### 主要功能

1. **文档同步** — 遍历配置的项目，执行各自的 sync.sh，同步文档到 `workspace/memory/[项目名]-sync/`
2. **未推送检查** — 检查 Git 仓库是否有未推送的 commit 或未提交的变更
3. **自动修复** — 传入 `--fix` 参数可自动推送未推送的 commit

### 使用方法

```bash
# 检查同步状态
bash project-sync.sh

# 检查并自动修复
bash project-sync.sh --fix
```

### 配置说明

在 `PROJECTS` 数组中配置你的项目：

```bash
PROJECTS=(
  "/path/to/project-a|project-a-sync|scripts/sync.sh"
  "/path/to/project-b|project-b-sync|scripts/sync.sh"
)
```

格式：`项目路径|同步目录名|同步脚本相对路径`

- **项目路径**：项目在本地的完整路径
- **同步目录名**：在 `workspace/memory/` 下创建的子目录名
- **同步脚本相对路径**：项目内的同步脚本路径（相对项目根目录）

### 输出示例

```
━━━ 1/3 文档同步 ━━━
 ✔ project-a-sync 同步完成
 ✔ project-b-sync 同步完成

━━━ 2/3 未推送检查 ━━━
 ✔ project-a 已同步
 ⚠ project-b: 2 个未推送

⚠ 0 错误, 1 警告
```

## 适配到 Windows PowerShell

**注意**：这是 Bash 脚本，Windows 环境需要：
- WSL (Windows Subsystem for Linux)
- Git Bash
- 或改写成 PowerShell 版本

如果需要 PowerShell 版本，告诉我，我可以转写一个。
