# EA策略客户管理系统

**创建时间**：2026-03-11  
**负责人**：GainLab 白熊  
**工作目录**：`C:\Users\Administrator\Desktop\智能体\ea策略\`

---

## 这是什么

管理 EA 策略客户入金、状态、平台的系统。  
数据存在 JSON（机器读），导出 Excel（人工看）。

---

## 文件结构

| 文件 | 用途 |
|------|------|
| `ea_clients.json` | 核心数据库，所有客户数据 |
| `ea_manager.py` | 管理脚本（查询/更新/导出）|
| `EA策略资金表.xlsx` | 自动生成的 Excel，发给人看 |
| `EA策略资金表.html` | 网页版表格 |

---

## 数据结构（ea_clients.json）

```json
{
  "meta": {
    "updated": "日期",
    "total_active": 进行中总金额,
    "total_stopped": 停止总金额,
    "total": 总入金
  },
  "clients": [
    {
      "id": 唯一编号,
      "name": "客户名",
      "manager": "负责人（张鹏/刘涛/曾涛/公司）",
      "platform": "交易平台（tmgm/dlsm/ebc）",
      "account": "账号ID",
      "amount": 入金金额（U）,
      "status": "进行中 / 停止",
      "current_balance": "当前资金",
      "transferred": true/false（是否已转平台）,
      "notes": "备注"
    }
  ],
  "gui2": [ 贵2客户列表 ],
  "platform_summary": { 平台汇总金额 }
}
```

---

## 常用操作（脚本命令）

```bash
# 查看所有客户
python ea_manager.py list

# 只看进行中
python ea_manager.py list 进行中

# 只看已停止
python ea_manager.py list 停止

# 查询某个客户详情
python ea_manager.py query 焦伟林

# 更新客户字段
python ea_manager.py update 焦伟林 status 停止
python ea_manager.py update 焦伟林 current_balance 15000u
python ea_manager.py update 焦伟林 notes "已出金"

# 新增客户（交互式）
python ea_manager.py add

# 汇总统计
python ea_manager.py summary

# 导出 Excel
python ea_manager.py export
```

---

## 可更新的字段

| 字段 | 说明 | 示例值 |
|------|------|--------|
| status | 状态 | 进行中 / 停止 |
| current_balance | 当前资金 | 12000u / 826rmb |
| notes | 备注 | 已出金 / 待转回 |
| platform | 平台 | tmgm / dlsm / ebc |
| account | 账号ID | 50201215 |
| amount | 入金金额 | 2000 |
| transferred | 是否已转 | true / false |
| manager | 负责人 | 张鹏 |

---

## 平台说明

| 简称 | 全称 |
|------|------|
| tmgm | TMGM |
| dlsm | 达陌 |
| ebc | EBC |

---

## 负责人

- **张鹏** — 管理客户最多
- **刘涛** — 部分客户
- **曾涛** — 部分客户
- **公司** — 公司自有资金客户

---

## 当前统计（2026-03-11）

| 项目 | 金额 |
|------|------|
| 进行中 | 58,000 U |
| 停止 | 32,000 U |
| **总计入金** | **90,000 U** |

**平台分布：**
- 达陌(dlsm)：36,000 U
- EBC：12,000 U  
- TMGM：10,000 U

**负责人分布：**
- 张鹏：54,000 U
- 公司：22,000 U
- 刘涛：10,000 U
- 曾涛：4,000 U

---

## 如何跟赵丽颖交互

直接说就行，不需要跑脚本：

> "查一下焦伟林"  
> "焦伟林已停止，备注出金完成"  
> "新增客户：张三，张鹏管，tmgm，账号12345，2000U，进行中"  
> "导出最新 Excel 发我"  
> "现在进行中总共多少钱"

---

## 历史记录

| 日期 | 操作 |
|------|------|
| 2026-03-11 | 系统初始化，从原始 Excel 导入 30 个客户，总入金 90,000U |
