# RULES → TASK 开发流程规范

## 核心理念

**血泪教训**：没有 PRD 不知道做什么，没有 TASK 不知道怎么拆，没有 VERIFY 不知道做对没有。

来自 2026-02-17 的教训：Phase 1-2.5 整个项目没有一次走过完整流程——7 个工具 275 tests 全是"边做边补"。展示页反复改错的根因就是没有结构文档。

---

## 文档链（强制顺序）

```
RULES.md → status.md → PRD → TASK → 实现 → 验证 → 文档同步 → 提交
```

**永远不能跳过**：验证 → 文档同步 → 提交

---

## 每个文件的角色

| 文件            | 放哪里                           | 干什么                     | 什么时候更新   |
| --------------- | -------------------------------- | -------------------------- | -------------- |
| **RULES.md**    | 代码仓库根目录                   | 开发规范、禁区、图表规范   | 规范变更时     |
| **ARCHITECTURE.md** | 代码仓库根目录               | 目录结构 + 数据流 + 技术决策 | 架构改动后   |
| **PRD**         | `research/docs/plans/`           | 产品需求文档               | 需求确认时     |
| **TASK**        | `research/docs/plans/p{N}-tasks/` | 任务分解（每个任务独立文件） | 开工前       |
| **decisions.md** | `research/docs/`                | 重大决策记录（只追加）     | 做决策时       |
| **lessons.md**  | `research/docs/`                 | 踩坑教训（只追加）         | 踩坑时         |
| **status.md**   | `research/docs/`                 | 当前进度（覆盖更新）       | 每批完成后     |

---

## 详细说明

### 1. RULES.md（开发规范）

**位置**：代码仓库根目录

**内容**：
- 编码规范（命名、格式、注释风格）
- 禁止操作清单（禁区）
- 图表规范（Mermaid 格式）
- Git commit 规范
- 测试覆盖率要求

**更新时机**：规范变更时

**示例**：
```markdown
# RULES.md

## 命名规范
- 变量：snake_case
- 类：PascalCase
- 常量：UPPER_SNAKE_CASE

## 禁区
- 禁止直接修改 production 数据库
- 禁止在代码中硬编码密钥

## 图表规范
- 使用 Mermaid 语法
- 架构图必须标注数据流方向
```

---

### 2. ARCHITECTURE.md（架构文档）

**位置**：代码仓库根目录

**内容**：
- 目录结构说明
- 数据流图
- 技术栈选型及理由
- 关键模块交互

**更新时机**：架构改动后

**示例**：
```markdown
# ARCHITECTURE.md

## 目录结构
\`\`\`
src/
├── api/       # API 路由
├── models/    # 数据模型
├── services/  # 业务逻辑
└── utils/     # 工具函数
\`\`\`

## 数据流
\`\`\`mermaid
graph LR
A[Client] --> B[API]
B --> C[Service]
C --> D[Database]
\`\`\`
```

---

### 3. PRD（产品需求文档）

**位置**：`research/docs/plans/`

**内容**：
- 功能描述
- 用户故事
- 验收标准
- UI/UX 原型（如有）

**更新时机**：需求确认时

**命名**：`p{N}-{feature-name}.md`（例如 `p1-user-auth.md`）

**示例**：
```markdown
# PRD: 用户认证系统

## 功能描述
实现用户注册、登录、登出功能

## 用户故事
- 作为用户，我希望能够注册账号
- 作为用户，我希望能够登录系统

## 验收标准
- [ ] 用户可以成功注册
- [ ] 用户可以成功登录
- [ ] 密码加密存储
```

---

### 4. TASK（任务分解）

**位置**：`research/docs/plans/p{N}-tasks/`

**内容**：
- 具体技术实现步骤
- 每个任务的输入输出
- 依赖关系

**更新时机**：开工前

**命名**：`task-{N}-{description}.md`

**示例**：
```markdown
# Task 1: 创建用户模型

## 输入
- 数据库 schema 设计

## 输出
- `models/user.py`
- 数据库迁移文件

## 步骤
1. 定义 User 类
2. 添加字段：username, email, password_hash
3. 生成迁移文件
4. 运行测试

## 验证
\`\`\`bash
pytest tests/test_user_model.py
\`\`\`
```

---

### 5. decisions.md（决策记录）

**位置**：`research/docs/`

**内容**：
- 重大技术决策
- 选型理由
- 权衡考量

**更新时机**：做决策时

**格式**：只追加，不修改历史

**示例**：
```markdown
# 决策记录

## 2026-03-10: 选择 PostgreSQL 而非 MySQL

**背景**：需要选择数据库

**决策**：PostgreSQL

**理由**：
- JSON 支持更好
- 全文搜索原生支持
- 社区活跃

**权衡**：
- 学习曲线稍陡
- 部署略复杂
```

---

### 6. lessons.md（踩坑教训）

**位置**：`research/docs/`

**内容**：
- 遇到的问题
- 解决方案
- 预防措施

**更新时机**：踩坑时

**格式**：只追加，不修改历史

**示例**：
```markdown
# 踩坑教训

## 2026-03-10: 忘记运行数据库迁移导致启动失败

**问题**：部署后服务无法启动，报数据库表不存在

**原因**：忘记在部署脚本中添加迁移步骤

**解决**：
\`\`\`bash
python manage.py migrate
\`\`\`

**预防**：
- 在 CI/CD 流程中添加迁移检查
- 部署前运行 dry-run
```

---

### 7. status.md（当前进度）

**位置**：`research/docs/`

**内容**：
- 已完成的任务
- 进行中的任务
- 下一步计划

**更新时机**：每批完成后

**格式**：覆盖更新（不是追加）

**示例**：
```markdown
# 项目进度

最后更新：2026-03-10

## 已完成
- [x] p1-task-1: 创建用户模型
- [x] p1-task-2: 实现注册接口

## 进行中
- [ ] p1-task-3: 实现登录接口（80%）

## 下一步
- p1-task-4: 添加 JWT 认证
- p1-task-5: 编写集成测试
```

---

## 什么时候可以跳步

### 允许跳过 PRD + TASK 的情况

- **小改**（单文件 bug fix）
- **紧急修复**（生产环境故障）

### 永远不能跳过

无论多小的改动，以下三步永远不能跳：

```
验证 → 文档同步 → 提交
```

**验证**：至少手动测试，理想是自动化测试

**文档同步**：
- 改了架构 → 更新 ARCHITECTURE.md
- 改了 API → 更新 API 文档
- 新增功能 → 更新 README.md

**提交**：
- commit 信息清晰
- 关联 issue/task 编号

---

## 完整工作流示例

### 场景：新增用户认证功能

#### 第 1 步：检查 RULES.md
```bash
cat RULES.md | grep -A 5 "认证"
```
了解认证相关规范

#### 第 2 步：更新 status.md
```markdown
## 进行中
- [ ] p1: 用户认证系统
```

#### 第 3 步：编写 PRD
创建 `research/docs/plans/p1-user-auth.md`

#### 第 4 步：拆分 TASK
创建：
- `research/docs/plans/p1-tasks/task-1-user-model.md`
- `research/docs/plans/p1-tasks/task-2-register-api.md`
- `research/docs/plans/p1-tasks/task-3-login-api.md`

#### 第 5 步：实现
按 TASK 顺序开发

#### 第 6 步：验证
```bash
pytest tests/test_auth.py
```

#### 第 7 步：文档同步
- 更新 ARCHITECTURE.md（新增认证模块）
- 更新 API 文档

#### 第 8 步：提交
```bash
git add .
git commit -m "feat(auth): 实现用户认证 [p1-task-1,2,3]"
git push
```

#### 第 9 步：更新 status.md
```markdown
## 已完成
- [x] p1: 用户认证系统
```

---

## 自检清单

每次提交前，问自己：

- [ ] 我读过 RULES.md 了吗？
- [ ] 有 PRD 吗？（小改可跳过）
- [ ] 有 TASK 吗？（小改可跳过）
- [ ] **我测试过了吗？**（必答）
- [ ] **我更新文档了吗？**（必答）
- [ ] **commit 信息清晰吗？**（必答）

**三个必答问题永远不能跳过。**

---

## 为什么这么做

### 真实案例：2026-02-17 惨案

**问题**：Phase 1-2.5 整个项目没有一次走过完整流程

**后果**：
- 7 个工具 275 tests 全是"边做边补"
- 展示页反复改错
- 架构腐化严重

**根因**：没有结构文档

**教训**：
> 没有 PRD 不知道做什么  
> 没有 TASK 不知道怎么拆  
> 没有 VERIFY 不知道做对没有

---

## 一句话总结

**RULES 告诉你规矩，PRD 告诉你目标，TASK 告诉你步骤，验证告诉你对错，文档让下次的你能接手。**
