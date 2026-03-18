# TOOLS.md - 本地配置笔记

Skills 定义工具怎么用，这个文件记你特有的配置。

---

## 搜索能力

### 网络搜索（当前可用）
| 工具 | 状态 | 说明 |
|------|------|------|
| Tavily API | ✅ 已配置 | 替代 Brave Search，完整网页搜索 |
| Browser | ✅ openclaw profile | 浏览器直接访问网页 |

### Tavily API
- Key: `TAVILY_API_KEY`（存于 `~/.openclaw/.env`）
- 用法：`python memory/scripts/search.py "关键词"`
- 支持：`search_depth`, `max_results`, `domains` 过滤

### Browser 工具
| Profile | 状态 | 说明 |
|---------|------|------|
| openclaw | ✅ 可用 | 默认用这个 |
| user | ⚠️ 需配置 | 需要 Chrome 调试模式 |

---

## 浏览器配置

**user profile 连接方法**：
1. 关掉所有 Chrome
2. 快捷方式属性末尾加：`--remote-debugging-port=9222`

**常用命令**：
- `browser(action=open, url="...", profile="openclaw")`
- `browser(action=snapshot)` - 获取页面快照

---

## 环境变量

| 变量 | 用途 |
|------|------|
| DASHSCOPE_API_KEY | Embedding + 语音识别 |
| TAVILY_API_KEY | 网络搜索 |
| ANTHROPIC_API_KEY | Claude API |
| TELEGRAM_BOT_TOKEN | Telegram Bot |

---

## 模型配置
| 用途 | 模型 |
|------|------|
| 主模型 | minimax/MiniMax-M2.7 |

---

## 记忆系统
| 配置项 | 值 |
|--------|---|
| Embedding | text-embedding-v3 (DashScope) |
| 向量库 | ~/.openclaw/memory/main.sqlite |
