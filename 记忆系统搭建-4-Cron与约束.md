# 记忆系统提示词 (4/4) — Cron + 自检 + 约束

## 五、Cron 自动化

配置 OpenClaw Cron 任务，每天 08:00（老板时区）运行 `run-all.sh`：

```bash
openclaw cron add --name "daily-health-check" \
  --schedule "0 8 * * *" \
  --command "bash ~/.openclaw/workspace/scripts/health-checks/run-all.sh"
```

### 结果处理

- 结果写入 `memory/health-check-latest.md`
- 有失败项时通知老板

### 示例通知逻辑

```bash
if bash run-all.sh > health-check-latest.md 2>&1; then
  echo "✅ 健康检查全部通过"
else
  # 通过 OpenClaw 发送通知
  openclaw message send --channel telegram --message "⚠️ 健康检查失败，请查看 memory/health-check-latest.md"
fi
```

---

## 六、自检清单

写入 `AGENTS.md`，**每次 commit 后 + 对话结束前**执行：

### 自检 6 步骤

1. **📝 日志** → `memory/logs/YYYY-MM-DD.md`
   - 记录今天做了什么
   
2. **📇 索引** → `MEMORY.md` 新主题加索引
   - 新增的项目/主题，在 MEMORY.md 索引表格中添加一行
   
3. **📄 文档同步** → 改了架构？同步相关文档
   - 代码结构变化时，更新 ARCHITECTURE.md
   
4. **🔄 项目同步** → 运行 `project-sync.sh`
   - 确保项目文档同步到 workspace
   
5. **🧪 API 实测** → 写了端点就 curl 验证
   - 新增 API 接口必须实际测试
   
6. **❓ 自问** → "新会话的我能无缝接手吗？"
   - 检查是否留下足够的上下文信息

---

## 七、heartbeat-state.json

在 `memory/heartbeat-state.json` 记录各项检查的最后时间戳：

```json
{
  "lastChecks": {
    "email": null,
    "calendar": null,
    "weather": null,
    "projectSync": null
  },
  "note": "timestamps in epoch seconds"
}
```

### 使用示例

```bash
# 更新 projectSync 时间戳
NOW=$(date +%s)
jq ".lastChecks.projectSync = $NOW" heartbeat-state.json > tmp.json && mv tmp.json heartbeat-state.json
```

---

## 八、关键约束

### 🔴 硬性约束（必须遵守）

| 约束 | 说明 |
| ---- | ---- |
| **MEMORY.md ≤ 150 行** | 超过 150 行必须归档精简 |
| **日志文件 ≤ 20 个** | 触发自动归档 |
| **项目同步单向** | `docs/ → memory/*-sync/`，永远不反向 |
| **密钥不写明文** | 存 `~/.openclaw/.env`（权限 600） |

### ⚠️ 最佳实践（强烈建议）

| 实践 | 说明 |
| ---- | ---- |
| **memory_search 口语改关键词** | "之前说的那个项目" → "Polymarket 研究进度" |
| **extraPaths 指 docs/ 子目录** | 不指根目录，避免索引代码文件 |

---

## 关键文件权限

```bash
# 密钥文件必须设置严格权限
chmod 600 ~/.openclaw/.env
chmod 600 ~/.openclaw/openclaw.json
```

---

## 完整目录结构

```
~/.openclaw/workspace/
├── MEMORY.md              # 热记忆入口（≤150行）
├── SOUL.md                # 人格定义
├── USER.md                # 老板信息
├── TOOLS.md               # 环境参数速查
├── HEARTBEAT.md           # 心跳巡检规则
├── AGENTS.md              # 行为准则 + 自检清单
├── memory/
│   ├── logs/
│   │   ├── 2026-03-10.md
│   │   └── ...
│   ├── archive/
│   │   ├── logs/
│   │   └── ...
│   ├── archive-index.md
│   ├── lessons.md
│   ├── projects.md
│   ├── tools-notes.md
│   ├── evolution.md
│   ├── heartbeat-state.json
│   ├── health-check-latest.md
│   ├── project-a-sync/
│   │   ├── .last-sync-ts
│   │   └── ...
│   ├── project-b-sync/
│   │   └── ...
│   ├── research/
│   └── methodology-*.md
└── scripts/
    ├── project-sync.sh
    └── health-checks/
        ├── run-all.sh
        ├── 01-today-log.sh
        ├── 02-memory-size.sh
        ├── 03-sync-freshness.sh
        ├── 04-python-deps.sh
        ├── 05-tools-version.sh
        ├── 06-log-rotation.sh
        ├── 07-doc-drift.sh
        ├── 08-gateway-memory.sh
        ├── 09-cron-jobs.sh
        ├── 10-disk-space.sh
        └── 11-network.sh
```

---

## 实施步骤

按顺序执行：

1. **创建目录结构**
   ```bash
   cd ~/.openclaw/workspace
   mkdir -p memory/{logs,archive/logs,research}
   mkdir -p scripts/health-checks
   ```

2. **创建热记忆文件**
   - MEMORY.md
   - SOUL.md
   - USER.md
   - TOOLS.md
   - HEARTBEAT.md
   - AGENTS.md

3. **创建温记忆文件**
   ```bash
   cd memory
   touch lessons.md projects.md tools-notes.md evolution.md
   touch archive-index.md
   echo '{"lastChecks":{"email":null,"calendar":null,"weather":null,"projectSync":null},"note":"timestamps in epoch seconds"}' > heartbeat-state.json
   ```

4. **安装脚本**
   - 复制 project-sync.sh 到 scripts/
   - 复制 11 个健康检查脚本到 scripts/health-checks/
   - `chmod +x scripts/*.sh scripts/health-checks/*.sh`

5. **配置 Cron**
   ```bash
   openclaw cron add --name "daily-health-check" \
     --schedule "0 8 * * *" \
     --command "bash ~/.openclaw/workspace/scripts/health-checks/run-all.sh"
   ```

6. **配置向量搜索**
   - 确保 memory plugin 已启用
   - 配置 extraPaths 指向项目文档目录

---

## 提示词结束

请根据以上完整规格，为我创建：
1. 完整的目录结构
2. 所有模板文件
3. 所有脚本（可执行）
4. Cron 配置

项目路径我会告诉你，格式：
```
项目名称: /path/to/project
文档目录: docs/
同步脚本: scripts/sync.sh
```
