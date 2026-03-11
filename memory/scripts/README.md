# 脚本使用说明

## 健康检查脚本

**文件**: `health-check.ps1`

**用途**: 检查记忆系统的 11 项健康指标

**执行方式**:
```powershell
# 方式1: 直接运行（如果允许执行脚本）
.\health-check.ps1

# 方式2: 绕过执行策略
powershell -ExecutionPolicy Bypass -File .\health-check.ps1

# 方式3: 在 OpenClaw 中执行
# 使用 exec 工具
```

**检查项目**:
1. 今日日志是否存在
2. MEMORY.md 行数（≤150）
3. 核心文件完整性
4. memory/ 目录结构
5. memory/ 核心文件
6. .env 文件
7. .gitignore
8. 最近日志数量
9. 向量库文件
10. Git 仓库状态
11. OpenClaw Gateway 状态

**返回值**:
- `0` - 全部通过
- `1` - 有错误
- `2` - 有警告

---

## 项目同步脚本

**文件**: `project-sync.ps1`

**用途**: 将外部项目的文档同步到 `memory/*-sync/` 目录

**配置方式**:

编辑 `project-sync.ps1`，在 `$Projects` 数组中添加项目配置：

```powershell
$Projects = @(
    @{
        Name = "my-project"              # 项目名称
        Path = "D:\workspace\my-project" # 项目路径
        Docs = "docs"                    # 文档子目录（或多个，逗号分隔）
    },
    @{
        Name = "another-project"
        Path = "C:\Projects\another"
        Docs = "README.md,docs,wiki"     # 支持多个路径
    }
)
```

**执行方式**:
```powershell
# 手动执行
powershell -ExecutionPolicy Bypass -File .\project-sync.ps1

# 自动执行（通过 Cron / 任务计划程序）
# 每天同步一次
```

**同步结果**:
- 文件会被同步到: `memory\<项目名>-sync\`
- 同步时间戳记录在: `.last-sync-ts`

**注意事项**:
- 只同步 `.md` 文件（Markdown 文档）
- 会递归复制子目录
- 已存在的文件会被覆盖

---

## 添加到 Cron（定期自动执行）

### Windows 任务计划程序

**健康检查（每天早上 9:00）**:
```powershell
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File C:\Users\Administrator\Desktop\智能体\memory\scripts\health-check.ps1"
$Trigger = New-ScheduledTaskTrigger -Daily -At 9am
Register-ScheduledTask -TaskName "OpenClaw-HealthCheck" -Action $Action -Trigger $Trigger
```

**项目同步（每天晚上 23:00）**:
```powershell
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File C:\Users\Administrator\Desktop\智能体\memory\scripts\project-sync.ps1"
$Trigger = New-ScheduledTaskTrigger -Daily -At 11pm
Register-ScheduledTask -TaskName "OpenClaw-ProjectSync" -Action $Action -Trigger $Trigger
```

### OpenClaw Cron（推荐）

在 OpenClaw 配置中添加：

```json
{
  "cron": {
    "health-check": {
      "schedule": "0 9 * * *",
      "command": "powershell -ExecutionPolicy Bypass -File memory/scripts/health-check.ps1",
      "workingDirectory": "C:\\Users\\Administrator\\Desktop\\智能体"
    },
    "project-sync": {
      "schedule": "0 23 * * *",
      "command": "powershell -ExecutionPolicy Bypass -File memory/scripts/project-sync.ps1",
      "workingDirectory": "C:\\Users\\Administrator\\Desktop\\智能体"
    }
  }
}
```

---

## 故障排查

### 执行策略错误

**错误信息**:
```
无法加载文件 xxx.ps1，因为在此系统上禁止运行脚本。
```

**解决方案**:
```powershell
# 临时允许（仅当前会话）
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 永久允许（当前用户）
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### 路径问题

**问题**: 脚本找不到文件

**解决方案**:
- 确保脚本中的路径是绝对路径
- 或在正确的工作目录下执行

### 权限问题

**问题**: 无法写入文件

**解决方案**:
- 以管理员身份运行 PowerShell
- 检查目标目录的写权限

---

## 日志输出

脚本输出可以重定向到日志文件：

```powershell
.\health-check.ps1 > "memory\logs\health-check-$(Get-Date -Format 'yyyy-MM-dd').log" 2>&1
```

---

*最后更新: 2026-03-10 22:26 UTC+8*
