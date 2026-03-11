# Tools Notes - 工具详细参考

## OpenClaw 核心工具

### 可用工具列表

| 工具 | 用途 | 状态 |
|------|------|------|
| read | 读取文件内容 | ✅ |
| write | 创建或覆盖文件 | ✅ |
| edit | 精确编辑文件（替换文本）| ✅ |
| exec | 执行 Shell 命令 | ✅ |
| process | 管理后台进程 | ✅ |
| web_search | Brave 搜索 | ✅ |
| web_fetch | 提取网页内容（markdown）| ✅ |
| browser | 浏览器控制 | ✅ |
| memory_search | 语义搜索记忆文件 | ✅ |
| memory_get | 精确读取记忆片段 | ✅ |
| message | Telegram 消息操作 | ✅ |
| sessions_spawn | 启动子代理 | ✅ |

---

## Memory Search（记忆搜索）

### 调用策略

**何时使用**：
- 老板问"之前说的xxx"
- 需要查找历史决策/讨论
- 查找项目相关上下文
- 不确定某个信息在哪个文件

**调用示例**：
```javascript
memory_search({
  query: "Polymarket 研究进度",
  maxResults: 5,
  minScore: 0.7
})
```

**返回结果**：
- 相关片段（带文件路径 + 行号）
- 相似度分数
- 片段上下文

**最佳实践**：
1. 先用 memory_search 定位文件
2. 再用 memory_get 精确读取需要的行
3. 避免全文读取大文件

---

## Web Search（网络搜索）

### Brave Search API

**参数**：
```javascript
web_search({
  query: "搜索关键词",
  count: 5,           // 返回结果数（1-10）
  country: "US",      // 地区代码（US/CN/ALL）
  language: "zh",     // 语言（zh/en）
  freshness: "day"    // 时效性（day/week/month/year）
})
```

**使用场景**：
- 实时新闻查询
- 技术文档搜索
- 市场数据查找

**注意事项**：
- 免费额度有限，避免频繁调用
- 优先用 memory_search 查找已有信息
- 搜索结果要验证可靠性

---

## Exec Tool（命令执行）

### 常用命令

**文件操作**：
```powershell
# 查看文件列表
Get-ChildItem -Path "路径" -Filter "*.md"

# 创建目录
New-Item -ItemType Directory -Force -Path "路径"

# 复制文件
Copy-Item -Path "源" -Destination "目标"
```

**Git 操作**：
```bash
git status                    # 查看状态
git add .                     # 添加所有修改
git commit -m "消息"          # 提交
git push                      # 推送
```

**注意事项**：
- Windows 默认用 PowerShell
- 路径用反斜杠 `\` 或正斜杠 `/`
- 中文路径可能显示乱码（不影响实际操作）

---

## Message Tool（Telegram）

### 发送消息

```javascript
message({
  action: "send",
  target: "telegram:5770799709",  // 老板的 Telegram ID
  message: "消息内容"
})
```

### 回复消息

```javascript
// 在回复前加上 [[reply_to_current]]
"[[reply_to_current]] 回复内容"
```

### 静默回复

当 Heartbeat 检查无需通知时：
```
HEARTBEAT_OK
```

---

## Sessions Spawn（子代理）

### 启动子代理

```javascript
sessions_spawn({
  runtime: "subagent",
  mode: "run",              // 一次性任务
  task: "任务描述",
  timeoutSeconds: 300
})
```

**使用场景**：
- 复杂的代码开发任务
- 需要隔离环境的实验
- 长时间运行的任务

---

## 浏览器控制（Browser Tool）

### 基本操作

```javascript
browser({
  action: "open",
  url: "https://example.com",
  profile: "openclaw"
})

browser({
  action: "snapshot",
  refs: "aria"
})

browser({
  action: "act",
  kind: "click",
  ref: "e12"
})
```

**使用场景**：
- 网页内容提取
- 表单填写
- 自动化操作

---

## 配置参数

### 模型配置

| 用途 | 模型 |
|------|------|
| 主模型 | claude-sonnet-4-5-20250929 |
| 默认模型 | claude-sonnet-4-5-20250929 |
| 推理模式 | on (hidden) |

### 环境变量

| 变量名 | 用途 |
|--------|------|
| ANTHROPIC_API_KEY | Claude API 密钥 |
| DASHSCOPE_API_KEY | 阿里云 DashScope（语音识别+Embedding）|
| TELEGRAM_BOT_TOKEN | Telegram Bot Token |

**注意**：密钥存在 `~/.openclaw/.env`，不写入任何配置文件明文！

---

## 快捷脚本（待创建）

### 项目同步脚本
- 路径：`memory/scripts/project-sync.sh`
- 用途：同步项目文档到 memory/*-sync/
- 状态：待创建

### 健康检查脚本
- 路径：`memory/scripts/health-check.sh`
- 用途：11项系统健康检查
- 状态：待创建

---

*最后更新: 2026-03-10 22:14*
