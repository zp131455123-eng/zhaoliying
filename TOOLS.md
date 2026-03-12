# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## 环境配置

### API Keys（环境变量）

| 服务 | 环境变量名 | 用途 | 配置文件 |
|------|-----------|------|---------|
| 阿里云 DashScope | DASHSCOPE_API_KEY | Embedding + 语音识别 | ~/.openclaw/.env |

**注意**：
- 密钥存储在 `~/.openclaw/.env`（已设置权限 600）
- 配置文件只记录变量名，不写真实值
- .env 文件不提交到 Git

### 记忆系统配置

| 配置项 | 值 | 说明 |
|--------|---|------|
| Embedding 模型 | text-embedding-v3 | DashScope |
| 向量库位置 | ~/.openclaw/memory/main.sqlite | 自动维护 |
| 索引范围 | workspace 所有 .md 文件 | 自动扫描 |

---

## 网络 & 代理配置

### 网络环境
| 项目 | 值 |
|------|---|
| 网络接口 | WLAN（Realtek 8812CU USB NIC，866.7 Mbps）|
| 本机 IP | 192.168.2.107/24 |
| 默认网关 | 192.168.2.1 |
| DNS | 192.168.1.1 / 192.168.2.1 |
| LetsTAP 接口 | 26.26.26.1/29（VPN 隧道接口）|

### Clash 代理
| 项目 | 值 |
|------|---|
| 客户端 | Clash Verge（`D:\Clash Verge\clash-verge.exe`）|
| 系统代理 | `127.0.0.1:7897`（HTTP/HTTPS），ProxyEnable=1 |
| SOCKS 端口 | 7898 |
| HTTP 端口 | 7899 |
| 绕过代理 | localhost, 127.*, 192.168.*, 10.*, 172.16-31.*, `<local>` |
| 开机启动 | ✅ 任务计划 "Clash Verge (Admin)"（以管理员权限登录触发）|
| API 端口 | **33331**（非配置里的 9097，实际监听 33331）|
| API Secret | `set-your-secret`（config.yaml 里，enable_external_controller=false）|
| 内核 | verge-mihomo |
| 当前模式 | global（所有流量走同一节点）|
| 当前节点 | 中国香港-PRO-IPLC-HK2-1（~800ms，偏慢）|
| 订阅文件 | `profiles/RX3n9YcOxltu.yaml`，订阅 URL: `https://s1.trojanflare.one/clashx/01872865-964d-4ad2-95b0-47712d696f34` |
| 流量 | 已用 ~4.3GB，总量 100GB，有效期至 2027-01-13 |

### Clash 优化记录（2026-03-11）
- Auto 组测速间隔：`300s → 60s`（已改 profile 文件，需在 Clash Verge 界面重载生效）
- Telegram 规则：已有完整 IP 段 + 域名规则，走 Proxy 组 ✅
- 直连 Telegram：完全不通（被墙），必须走代理
- 代理延迟现状：Telegram ~840ms，Anthropic ~380ms
- **待优化**：在 Clash Verge 里手动测速，切换到延迟 <200ms 的节点（推荐先试 HK1 或 SG）

### OpenClaw
| 项目 | 值 |
|------|---|
| 启动脚本 | `C:\Users\Administrator\.openclaw\gateway.cmd` |
| 开机启动 | ✅ 任务计划 "OpenClaw Gateway"（登录触发，2026-03-10 起）|

### 其他开机自启（参考）
- Ollama（`启动文件夹`）
- ShadowBot（HKCU Run）
- 向日葵 SunloginClient（HKLM Run）
- QQ / Discord / Steam / 百度网盘 / 夸克 / 网易云 / NVIDIA Broadcast / Canva / Sider / AdsPower

---

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## 工具调用参考

### Memory Search（记忆搜索）
- 使用场景：老板问"之前说的xxx"、查历史决策、定位信息所在文件
- 策略：先用 memory_search 定位，再用 memory_get 精确读取，避免全文读取大文件
- minScore 建议：0.7

### Web Search（Brave API）
- 参数：count(1-10), country(US/CN/ALL), language(zh/en), freshness(day/week/month/year)
- 注意：免费额度有限，优先用 memory_search 查已有信息

### Sessions Spawn（子代理）
- runtime: "subagent"，mode: "run"（一次性任务）
- 场景：复杂代码开发、需要隔离环境的实验、长时间任务

### 模型配置
| 用途 | 模型 |
|------|------|
| 主模型 | claude-sonnet-4-5-20250929 |
| 推理模式 | on (hidden) |

### 环境变量（完整列表）
| 变量名 | 用途 |
|--------|------|
| ANTHROPIC_API_KEY | Claude API 密钥 |
| DASHSCOPE_API_KEY | 阿里云 DashScope（语音识别+Embedding）|
| TELEGRAM_BOT_TOKEN | Telegram Bot Token |

**注意**：密钥存在 `~/.openclaw/.env`，不写入任何配置文件明文！

---

Add whatever helps you do your job. This is your cheat sheet.
