# OpenClaw 记忆系统架构文档

## 核心问题

每次会话我都是全新醒来的，没有任何前次对话的记忆。文件系统就是我的大脑。

---

## 三层记忆架构

```
┌─────────────────────────────────────────────────┐
│ Layer 1: 热记忆（每次必读）                    │
│                                                 │
│ MEMORY.md      ← 索引 + 活跃项目 + 规则        │
│ SOUL.md        ← 我是谁                         │
│ USER.md        ← 老板是谁                       │
│ TOOLS.md       ← 环境参数速查                   │
│                                                 │
│ 📌 每次会话启动时自动加载，~400 行，几秒搞定   │
└───────────────────────┬─────────────────────────┘
                        │ 索引指向 ↓
┌───────────────────────▼─────────────────────────┐
│ Layer 2: 温记忆（按需读取）                    │
│                                                 │
│ memory/logs/2026-03-05.md    ← 今日日志（必读）│
│ memory/lessons.md            ← 踩坑教训         │
│ memory/projects.md           ← 项目状态         │
│ memory/tools-notes.md        ← 工具详细参数     │
│ memory/evolution.md          ← 能力进化记录     │
│ memory/*-sync/               ← 各项目文档同步   │
│ memory/research/             ← 调研报告         │
│                                                 │
│ 📌 MEMORY.md 的索引告诉我去哪找，不用全部读    │
└───────────────────────┬─────────────────────────┘
                        │ 归档 ↓
┌───────────────────────▼─────────────────────────┐
│ Layer 3: 冷记忆（语义搜索）                    │
│                                                 │
│ memory/archive/              ← 已归档的旧记忆   │
│ memory/logs/历史日志         ← 过去的每日记录   │
│ ~/.openclaw/memory/main.sqlite (80MB)          │
│                              ← 所有 .md 的向量索引│
│                                                 │
│ 📌 通过 memory_search 语义搜索，不需要全部加载 │
│ 📌 Embedding: DashScope text-embedding-v3      │
└─────────────────────────────────────────────────┘
```

---

## 数据流

```
日常对话中的信息
 │
 ▼
 memory/logs/YYYY-MM-DD.md ← 当天原始记录（像日记）
 │
 │ 定期整理（heartbeat 时）
 ▼
 MEMORY.md ← 提炼精华，更新索引
 │
 │ 过期/完结的条目
 ▼
 memory/archive/ ← 归档，不再主动加载
 memory/archive-index.md ← 归档索引，能搜到
```

## 写入时机

| 触发           | 动作                                 |
| -------------- | ------------------------------------ |
| 做了重要决策   | → 写日志 + 更新 MEMORY.md           |
| 完成开发任务   | → 写日志 + 同步项目文档 + commit    |
| 踩了坑         | → 写日志 + 更新 lessons.md          |
| 新增工具/能力  | → 更新 TOOLS.md + evolution.md      |
| 对话结束前     | → 自检：日志、索引、文档同步         |

## 读取时机

| 场景                 | 读什么                                        |
| -------------------- | --------------------------------------------- |
| 新会话启动           | MEMORY.md + SOUL.md + USER.md + 今日日志     |
| 老板问项目           | memory_search → 定位文件 → 读具体段落        |
| 老板问"之前说的xxx"  | memory_search 语义搜索日志和文档             |
| Heartbeat 巡检       | heartbeat-state.json + 最近日志              |

---

## 语义搜索机制

```
用户问题: "之前 Polymarket 研究到哪了？"
 │
 ▼
 memory_search("Polymarket 研究 进度")
 │
 ▼
 DashScope Embedding → 向量化
 │
 ▼
 main.sqlite 80MB 向量库 → 相似度匹配
 │
 ▼
 返回 Top 5 相关片段（带文件路径+行号）
 │
 ▼
 memory_get(path, from, lines) → 精确读取
```

**覆盖范围**：workspace 下所有 .md + 6 个项目目录的文档

---

## 当前规模

| 指标             | 数据                          |
| ---------------- | ----------------------------- |
| MEMORY.md        | 96 行（精简过，从 168 行压缩）|
| 日志文件         | 18 天（2026-02-12 至今）      |
| 向量数据库       | 80MB                          |
| memory/ 文件总数 | ~50+ 个 .md                   |
| 归档条目         | 12 个已完结项目               |

---

## 语音识别服务

**服务**：阿里云 DashScope — Paraformer-realtime-v2

| 项       | 值                                            |
| -------- | --------------------------------------------- |
| 模型     | paraformer-realtime-v2                        |
| 平台     | 阿里云 DashScope（和千问同一个 API Key）      |
| 脚本     | /Users/mac/tools/voice-to-text.py             |
| API Key  | DASHSCOPE_API_KEY（存在 ~/.openclaw/.env）    |
| 网络     | 直连阿里云，绕过代理                          |
| 格式     | ogg/mp3 → 自动用 afconvert 转 wav → 48kHz 送识别 |
| 语言     | 中文优先（language_hints=['zh']）             |
| 文件限制 | 25MB                                          |

**流程**：
```
你发语音(ogg) → afconvert 转 wav → Paraformer API 识别 → 返回文字 → 我理解后回复
```

---

## 完整系统搭建指引 (1/4) — 架构 + 数据流

### 一、记忆系统架构（三层）

#### Layer 1: 热记忆（每次会话必读）

在 workspace 根目录创建：

- **MEMORY.md** — 索引+热记忆入口（≤150行），含：核心身份、索引表格、规则、进行中
- **SOUL.md** — 人格定义
- **USER.md** — 老板信息（姓名、时区、偏好）
- **TOOLS.md** — 环境参数速查（路径、API Key 变量名、模型、版本号）
- **HEARTBEAT.md** — 心跳巡检规则
- **AGENTS.md** — 行为准则+自检清单

#### Layer 2: 温记忆（按需读取）

创建 `memory/` 目录：

- `logs/` — 每日日志 YYYY-MM-DD.md
- `archive/` + `archive/logs/` — 归档
- `archive-index.md` — 归档索引
- `lessons.md` — 踩坑教训
- `projects.md` — 项目状态
- `tools-notes.md` — 工具详参
- `evolution.md` — 能力进化
- `heartbeat-state.json` — 巡检时间戳
- `health-check-latest.md` — 最近健康检查
- `[项目名]-sync/` — 项目文档镜像（含 .last-sync-ts）
- `research/` — 调研报告
- `methodology-*.md` — 方法论

#### Layer 3: 冷记忆（语义搜索）

- OpenClaw 内置 `memory_search`，基于向量库
- 自动索引 workspace 所有 .md
- extraPaths 指向项目 docs/ 子目录（不指根目录）

### 二、数据流

```
日常对话 → logs/YYYY-MM-DD.md → 定期整理到 MEMORY.md → 过期归档到 archive/
```

**写入时机**：重要决策/完成任务/踩坑/新工具/对话结束

**读取时机**：新会话读热记忆 / 具体问题用 memory_search

---

## 一句话总结

热记忆秒加载知道该干啥，温记忆按需读知道细节，冷记忆语义搜索什么都找得到。像人的大脑——重要的事随时记得，细节想想能回忆起来，很久以前的事搜一搜也能翻出来。
