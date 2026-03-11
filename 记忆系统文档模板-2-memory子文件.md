# 记忆系统各文档结构模板 (2/3) — memory/ 子文件

## memory/logs/YYYY-MM-DD.md（每日日志）

```markdown
# YYYY-MM-DD 工作日志

## 主题1
- 做了什么
- 决策/结论
- 踩坑/发现

## 主题2
- ...
```

**特点**：
- 原始记录，像日记
- 每个主题独立章节
- 不需要精炼，记全就行

---

## memory/lessons.md（踩坑教训）

```markdown
# Lessons Learned

## 索引（按类别+条数+关键词）

| 类别 | 条数 | 关键词 |
|------|------|--------|
| 安全/密钥 | 3 | .env, 600, 明文 |
| 时区/配置 | 2 | UTC, Asia/Shanghai |
| 工具操作 | 5 | Git, Docker, npm |
| 搜索规范 | 2 | 关键词, 术语 |
| 工作流程 | 4 | VERIFY, 文档同步 |
| 记忆管理 | 3 | MEMORY.md, 归档 |

---

## 类别1：安全/密钥

### 教训1: 密钥泄露到 Git 历史

**现象**：
.env 文件被 commit 到 Git

**原因**：
忘记添加 .gitignore

**修复**：
```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
```

**教训**：
- **密钥文件必须在 .gitignore 第一行**
- **初始化仓库时立即添加 .gitignore**
- **commit 前运行 git status 检查**

---

## 类别2：时区/配置

### 教训2: Cron 任务时区错误

**现象**：
设置 08:00 执行，实际 00:00 执行

**原因**：
Cron 使用 UTC 时区，没有转换

**修复**：
```bash
# 北京时间 08:00 = UTC 00:00
0 0 * * * /path/to/script.sh
```

**教训**：
- **Cron 时间必须转换为 UTC**
- **脚本内部使用 TZ 环境变量**
- **配置文档明确标注时区**

---

## 类别3：工具操作

### 教训3: npm install 覆盖了手动修改

**现象**：
手动修改 node_modules 后被 npm install 覆盖

**原因**：
npm install 会重新安装依赖

**修复**：
使用 patch-package 固化补丁

**教训**：
- **永远不要直接修改 node_modules**
- **使用 patch-package 管理补丁**
- **或提交 PR 到上游项目**

---

（继续添加其他教训...）
```

**格式**：现象→原因→修复→教训（结论加粗）

**特点**：
- 按类别分组
- 顶部有索引表
- 每条教训结构化

---

## memory/projects.md（项目状态）

```markdown
# Projects

## 项目A（主项目）

| 仓库 | 技术栈 | 说明 |
|------|--------|------|
| github.com/xxx/project-a | Node.js, TypeScript | 主要业务系统 |

### 当前状态

- **路径**: `/path/to/project-a`
- **技术栈**: Node.js 24.x, TypeScript 5.x, PostgreSQL 16
- **测试数**: 275 tests, 85% coverage
- **线上地址**: https://project-a.example.com

### 子项目状态

- `api/` — REST API (已完成)
- `web/` — 前端页面 (进行中)
- `worker/` — 后台任务 (待开始)

---

## 项目B

...

---

## GitHub 信息

- **用户名**: your-username
- **常用仓库**: project-a, project-b, project-c

---

## 环境配置

| 环境 | 描述 | 访问方式 |
|------|------|----------|
| 开发 | 本地 | localhost:3000 |
| 测试 | VPS | test.example.com |
| 生产 | 云服务器 | prod.example.com |
```

**特点**：
- 每个项目独立章节
- 包含仓库列表、技术栈、状态、开工脚本

---

## memory/tools-notes.md（工具详参）

```markdown
# Tools Notes

## 搜索体系

### 调用策略

| 场景 | 首选 | 备选 |
|------|------|------|
| 中文新闻/实时 | Perplexity | Google |
| 英文技术 | Google | Perplexity |
| 学术论文 | Google Scholar | - |
| 代码示例 | GitHub Search | Stack Overflow |

### 各引擎参数

| 引擎 | 脚本 | 额度 | 速度 | 特点 |
|------|------|------|------|------|
| Perplexity | perplexity_search | 免费 | 快 | 中文友好 |
| Google | google_search | 免费 | 快 | 覆盖广 |
| Brave | brave_search | 免费 | 快 | 隐私优先 |

### 引擎对比（实测结论）

- **Perplexity**: 中文新闻最佳，实时性强
- **Google**: 英文技术文档最全
- **Brave**: 去广告效果好，结果干净

---

## MCP Servers

| Server | 用途 | 状态 |
|--------|------|------|
| filesystem | 文件操作 | ✅ 已启用 |
| github | GitHub API | ✅ 已启用 |
| postgres | 数据库查询 | ⏸️ 待配置 |

---

## OpenClaw 进阶配置

### Hooks
...

### Sub-agents
...

### Memory Search
...

---

## 各 API 详细参数

### OpenAI API

```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### Anthropic API

...
```

**特点**：
- TOOLS.md 的扩展版
- 放详细用法、对比、调用策略

---

## memory/evolution.md（能力进化）

```markdown
# Evolution

## 方法论

**原则**：
- 免费优先
- 一号搞定（统一账号体系）
- 中文国产 / 英文国际

---

## Timeline

### 2026-03-10

**新增能力**：
- Telegram 消息接收/发送
- 代理配置（Clash Verge）

**配置工具**：
- openclaw gateway
- Telegram Bot API

---

### 2026-03-09

**新增能力**：
- 记忆系统三层架构
- 健康检查脚本

**配置工具**：
- memory_search
- Cron 定时任务

---

## 能力现状

| 能力 | 状态 | 说明 |
|------|------|------|
| 文件读写 | ✅ | Read/Write/Edit tool |
| 命令执行 | ✅ | Exec tool (pty 支持) |
| Web 搜索 | ✅ | Brave/Google/Perplexity |
| 浏览器控制 | ✅ | Browser tool |
| Telegram | ✅ | 收发消息 |
| 记忆系统 | ✅ | 三层架构 + 向量搜索 |
| 语音识别 | ⏸️ | 待配置 (Paraformer) |
| TTS | ⏸️ | 待配置 (ElevenLabs) |
```

**特点**：
- 按日期记录每次能力增长
- 底部有完整能力清单
