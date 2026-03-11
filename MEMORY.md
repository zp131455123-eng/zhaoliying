# MEMORY.md - 索引 + 热记忆

## 核心身份
- **我**: 赵丽颖 🌸（AI 助手）
- **老板**: GainLab 白熊 (Telegram @asher2025BTC)
- **工作空间**: C:\Users\Administrator\Desktop\智能体
- **时区**: Asia/Shanghai (UTC+8)
- **启动时间**: 2026-03-10

---

## 索引（活跃项目 & 重要文档）

| 主题 | 一句话描述 | 详情位置 |
|------|-----------|---------|
| 记忆系统架构 | 三层记忆架构设计 | [[OpenClaw记忆系统架构.md]] |
| 开发流程规范 | TASK 规范 + 血泪教训 | [[RULES-TASK开发流程规范.md]] |
| 踩坑教训 | 历史错误汇总 | [[memory/lessons.md]] |
| 项目状态 | 当前所有项目概览 | [[memory/projects.md]] |
| EA策略客户管理 | 30个客户，90000U入金，JSON+Excel系统 | [[ea策略/README.md]] |
| 工具详参 | 搜索/API/MCP 详细用法 | [[memory/tools-notes.md]] |
| 网络配置 | 代理/Clash/开机启动详情 | [[TOOLS.md#网络--代理配置]] |
| 能力进化 | 每次新增能力记录 | [[memory/evolution.md]] |

---

## 规则（必须遵守的红线）

### 🔴 绝对规则
- **私有数据不外泄** — 任何涉及密钥、个人信息的内容都不能发到外部
- **破坏性操作先问** — 删除、覆盖、发送消息等不可逆操作必须先确认
- **密钥不写明文** — TOOLS.md / config 只记录环境变量名，不记录真实值
- **时区必须标注** — Cron / 日志 / 时间戳必须明确 UTC / Asia/Shanghai
- **文档同步优先** — 改了架构/API 必须同步项目文档，commit 前自检
- **🌐 网络配置必须确认** — 任何涉及 Clash / 代理 / 系统网络的修改，必须先说明改什么、为什么，等老板确认后才能动

### ⚠️ 注意事项
- **trash > rm** — 能用回收站就不用 rm -rf
- **记忆归档** — MEMORY.md 超过 150 行必须归档到 memory/archive/
- **日志必写** — 每次对话结束前更新 memory/logs/YYYY-MM-DD.md
- **Heartbeat 静默时段** — 深夜 (23:00-08:00) 非紧急事件不打扰

---

## 进行中（当前活跃任务）

### 记忆系统优化
- **状态**: 完成 ✅
- GitHub 自动同步已配置（每天凌晨2点，任务计划 "ZhaoLiying GitSync"）
- 仓库：git@github.com:zp131455123-eng/zhaoliying.git

### EA策略客户管理系统
- **状态**: 完成 ✅
- 30个客户，90000U总入金
- 文件：`ea策略/ea_clients.json` + `ea_manager.py`
- 操作：直接跟我说，我更新JSON并导出Excel

### AI视频制作
- **状态**: 待规划 🔲
- 老板想用AI做视频（AI生成视频，非AI内容视频）
- 具体工具和工作流待讨论确认
- **下一步**: 了解他想做哪种类型（数字人/文转视频/全流程自动化）

---

## 最近学习/发现

### 2026-03-11
- 🔍 检查网络配置：Clash + OpenClaw 开机启动均正常
- ⚡ 定位延迟根因：当前 HK 节点 ~800ms，直连 Telegram 被墙
- 🔧 优化：Auto 组测速间隔 300s→60s（待重载生效）
- 📌 Clash API 实际端口 33331（非配置里的 9097）
- 💡 学到：Clash Verge enable_external_controller=false 时 API 端口会随机变

### 2026-03-10
- ✅ 完成记忆系统三层架构搭建（热/温/冷记忆）
- ✅ 创建健康检查脚本（11项指标）+ 项目同步脚本
- ✅ 配置 DashScope 语义搜索（text-embedding-v3）
- ✅ C 盘空间清理两次（总释放 168 GB）
  - 第一次：126 GB（剪映缓存为主）
  - 第二次：42 GB（会议录制+游戏+缓存）
- 💡 学到：PowerShell 中文编码问题（用 UTF-8 BOM 或纯英文）
- 💡 学到：DashScope 兼容 OpenAI API 格式
- 💡 学到：向量搜索需要时间构建索引，不是即时生效
- 💡 学到：剪映缓存可以占用 122 GB，定期清理很有必要

---

## 待办事项

- [x] 完成记忆系统基础文件创建
- [x] 创建健康检查脚本
- [x] 创建项目同步脚本
- [x] 配置 .gitignore
- [x] 配置语义搜索
- [x] C 盘空间清理
- [ ] 测试 memory_search 语义搜索功能（等待索引构建）
- [ ] 配置 Heartbeat 自动巡检（可选）

---

## 归档提示

当 MEMORY.md 超过 150 行时：
1. 将"完成"的项目移至 memory/archive-index.md
2. 将"最近学习/发现"超过 7 天的内容移至对应日志文件
3. 保持 MEMORY.md 精简、高频访问

---

*最后更新: 2026-03-10 23:57*
