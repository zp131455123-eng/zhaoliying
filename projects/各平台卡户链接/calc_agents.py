# -*- coding: utf-8 -*-
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 进行中客户（含新加3人）
active = [
    {"name": "范宇轩",            "agent": "张鹏",  "amount": 2000},
    {"name": "苏亮",              "agent": "张鹏",  "amount": 2000},
    {"name": "雷熊",              "agent": "张鹏",  "amount": 2000},
    {"name": "王欢",              "agent": "曾涛",  "amount": 2000},
    {"name": "林锦豪",            "agent": "张鹏",  "amount": 4000},
    {"name": "王泽远",            "agent": "张鹏",  "amount": 2000},
    {"name": "梁杰煌",            "agent": "张鹏",  "amount": 2000},
    {"name": "焦伟林",            "agent": "张鹏",  "amount": 10000},
    {"name": "谢远然",            "agent": "张鹏",  "amount": 2000},
    {"name": "雷蒙",              "agent": "公司",  "amount": 4000},
    {"name": "聂平华",            "agent": "张鹏",  "amount": 6000},
    {"name": "华哥(xiong yong)",  "agent": "公司",  "amount": 10000},
    {"name": "孙成(chenyingying)","agent": "刘涛",  "amount": 2000},
    {"name": "陈泽林",            "agent": "张鹏",  "amount": 2000},
    {"name": "张金虎",            "agent": "张鹏",  "amount": 2000},
    {"name": "杨静",              "agent": "刘涛",  "amount": 2000},
    {"name": "杨浩",              "agent": "张鹏",  "amount": 2000},
    {"name": "李维",              "agent": "刘佳轩","amount": 2000},
    {"name": "刘学习",            "agent": "刘佳轩","amount": 10000},
    {"name": "刘学习推荐",        "agent": "刘佳轩","amount": 4000},
]

# 停止客户
stopped = [
    {"name": "雷伟平",    "agent": "刘涛",  "amount": 2000},
    {"name": "朱睿",      "agent": "刘涛",  "amount": 2000},
    {"name": "徐敏",      "agent": "曾涛",  "amount": 2000},
    {"name": "孙明",      "agent": "张鹏",  "amount": 2000},
    {"name": "李超杰",    "agent": "张鹏",  "amount": 2000},
    {"name": "小叶",      "agent": "公司",  "amount": 8000},
    {"name": "万诺",      "agent": "张鹏",  "amount": 2000},
    {"name": "曾经，拥有","agent": "张鹏",  "amount": 2000},
    {"name": "张凯嘉",    "agent": "张鹏",  "amount": 2000},
    {"name": "MN医疗",    "agent": "张鹏",  "amount": 2000},
    {"name": "bibiubiu",  "agent": "张鹏",  "amount": 2000},
    {"name": "罗琴",      "agent": "刘涛",  "amount": 2000},
    {"name": "徐宝龙",    "agent": "张鹏",  "amount": 2000},
]

# 统计
from collections import defaultdict
stats = defaultdict(lambda: {"active_count":0,"active_amt":0,"stopped_count":0,"stopped_amt":0})

for c in active:
    stats[c['agent']]['active_count'] += 1
    stats[c['agent']]['active_amt'] += c['amount']
for c in stopped:
    stats[c['agent']]['stopped_count'] += 1
    stats[c['agent']]['stopped_amt'] += c['amount']

print("代理人统计：")
print(f"{'代理人':<10} {'客户数':>6} {'进行中客户':>8} {'进行中资金':>12} {'停止客户':>8} {'停止资金':>10} {'合计资金':>10}")
print("-"*70)
total_ac=total_aa=total_sc=total_sa=0
for agent, s in sorted(stats.items()):
    tc = s['active_count']+s['stopped_count']
    ta = s['active_amt']+s['stopped_amt']
    total_ac+=s['active_count']; total_aa+=s['active_amt']
    total_sc+=s['stopped_count']; total_sa+=s['stopped_amt']
    print(f"{agent:<10} {tc:>6} {s['active_count']:>8} {s['active_amt']:>12,} {s['stopped_count']:>8} {s['stopped_amt']:>10,} {ta:>10,}")
print("-"*70)
print(f"{'合计':<10} {total_ac+total_sc:>6} {total_ac:>8} {total_aa:>12,} {total_sc:>8} {total_sa:>10,} {total_aa+total_sa:>10,}")
