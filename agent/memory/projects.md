# Projects - 项目状态
*最后更新: 2026-03-15*

---

## ✅ 已完成

### 记忆系统搭建
- 三层架构（热/温/冷）✅
- 向量搜索（DashScope text-embedding-v3）✅
- GitHub 自动同步（每天凌晨2点）✅
- 健康检查脚本 / project-sync 脚本 ✅

### EA策略客户管理系统
- 文件：`projects/ea策略/ea_clients.json` + `ea_manager.py` + `validate.py`
- 30个客户，**进行中74,000U**（20人），**停止32,000U**（13人），**总计106,000U**
- **平台分布**：
  - 星迈：36,000 U（8×2000 + 4000 + 6000 + 10000）
  - ebc：14,000 U（5×2000 + 4000）
  - tmgm：24,000 U（10000 + 10000 + 4000）
- **负责人**：张鹏(54,000) / 公司(22,000) / 刘涛(10,000) / 曾涛(4,000) / 刘佳轩(16,000)
- 注意：杨浩、李维、刘学习、刘学习推荐 账户号原始数据缺失，勿乱填
- 验证：每次修改后跑 `validate.py`，只报缺失不猜测
- **重要**：平台名称用"星迈"、"ebc"、"tmgm"，不用 dlsm/DLSM

### GitHub 仓库配置
- 仓库：`git@github.com:zp131455123-eng/zhaoliying.git`（私有）
- 用户：zp131455123-eng / zp131455123@gmail.com
- SSH Key：ed25519，已添加到 GitHub
- 自动同步：任务计划 "ZhaoLiying GitSync"，凌晨2点

### 各平台卡户链接管理系统 ✅
- 文件位置：`各平台卡户链接/`
- links.json：数据存储
- links_manager.py：管理程序
- export_word.py：Word导出
- 各平台卡户链接.xlsx / .docx / 客户资金总览.html
- 平台：星迈(ECN/USC) / DLSM / LMAX / TMGM / EBC
- 进行中：58,000U，停止：32,000U，总计：90,000U

### 语音识别ASR ✅
- 文件位置：`memory/scripts/asr.py`
- 阿里云DashScope paraformer-realtime-v2
- 流程：Telegram ogg → ffmpeg转wav → paraformer识别 → 文本
- 已配置到 OpenClaw tools.media.audio ✅

---

## 🔄 进行中

### AI视频pipeline
- 文件位置：`ai视频/pipeline/`
- step1_hotspot.py：热点抓取
  - 抖音 ✅ HackerNews ✅ YouTube ✅
  - 微博/知乎/小红书 ❌（需cookie）
- step2_script.py：文案生成（Claude API，结构化JSON，3选题/次）
- run.py：主入口，串联两步
- 待做：补cookie、Reddit OAuth、确定数字人方案（Step3）
- 数字人方案：HeyGen/D-ID，TTS 用 DashScope CosyVoice
- 已推送GitHub ✅

---

## 环境
| 项目 | 值 |
|------|---|
| 工作空间 | `C:\Users\Administrator\Desktop\智能体` |
| 系统 | Windows 10 x64 |
| Python | 已安装（openpyxl 可用）|
| Node.js | v24.14.0 |
| Shell | PowerShell |
