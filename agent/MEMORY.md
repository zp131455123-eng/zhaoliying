# MEMORY.md - 索引（轻量版）
*最后更新: 2026-03-19 | 保持 ≤80行*

---

## 核心身份
- **我**: 赵丽颖 🌸（AI 助手）
- **老板**: GainLab 白熊 (Telegram @asher2025BTC, ID: 5770799709)
- **工作空间**: `C:\Users\Administrator\Desktop\智能体`
- **时区**: Asia/Shanghai (UTC+8)
- **GitHub**: git@github.com:zp131455123-eng/zhaoliying.git（私有）

---

## 文件夹结构

```
智能体/
├── agent/           # Agent 核心（我的）
│   ├── .openclaw/  # OpenClaw 配置
│   ├── memory/     # 记忆系统
│   └── *.md        # 身份文件
│
├── projects/        # 业务项目（老板的）
│   ├── ea策略/     # EA客户管理
│   ├── ai视频/     # AI视频流水线
│   ├── 各平台卡户链接/  # 账号管理
│   └── games/      # 游戏
│
└── archive/        # 残留文件归档
```

---

## 索引

| 主题 | 详情位置 |
|------|---------|
| 项目状态 | `agent/memory/projects.md` |
| 网络配置 / Clash | `agent/TOOLS.md` + `agent/memory/network-config.md` |
| 踩坑教训 | `agent/memory/lessons.md` |
| 能力进化 | `agent/memory/evolution.md` |
| 每日日志 | `agent/memory/logs/YYYY-MM-DD.md` |
| EA策略 | `projects/ea策略/` |
| 各平台卡户链接 | `projects/各平台卡户链接/links.json` |
| AI视频流水线 | `projects/ai视频/pipeline/` |
| 语音识别ASR | `agent/memory/scripts/asr.py` |
| 残留归档 | `archive/` |

---

## 🔴 红线规则
1. **私有数据不外泄** — 密钥、客户信息不能发到外部
2. **破坏性操作先问** — 删除/覆盖/发消息等不可逆操作必须确认
3. **密钥不写明文** — 只记环境变量名，不记真实值
4. **🌐 网络配置必须确认** — 任何 Clash/代理/系统网络修改，先说明后确认再动
5. **trash > rm** — 能用回收站就不用 rm
6. **数据验证** — 修改 EA 数据后必须跑 validate.py，不乱填缺失字段
7. **分类存放** — 项目放 projects/，Agent 内容放 agent/，残留放 archive/

---

## 当前活跃
- EA策略系统 ✅
- GitHub 自动同步 ✅ 每天凌晨2点
- AI视频流水线 🔄 step1/2完成，step3待定
- 各平台卡户链接 ✅
- 语音识别ASR ✅

---

*超过80行时：把"最近学习"移到当日日志，把完结项目移到 projects.md*
