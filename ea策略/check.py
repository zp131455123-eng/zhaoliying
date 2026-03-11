# -*- coding: utf-8 -*-
import json
with open('ea_clients.json', encoding='utf-8') as f:
    d = json.load(f)

clients = d['clients']
active = [c for c in clients if c['status'] == '进行中']
stopped = [c for c in clients if c['status'] == '停止']

print('=== 数据完整性检查 ===')
print(f'总客户数: {len(clients)}')
print(f'进行中: {len(active)} 条，合计 {sum(c["amount"] for c in active)} U')
print(f'停止: {len(stopped)} 条，合计 {sum(c["amount"] for c in stopped)} U')
print(f'贵2: {len(d["gui2"])} 条，合计 {sum(g["amount"] for g in d["gui2"])} U')
print(f'总计(进行+停止): {d["meta"]["total"]} U')

print('\n=== 字段缺失检查 ===')
issues_found = False
for c in clients:
    issues = []
    if not c.get('platform'):
        issues.append('缺platform')
    if not c.get('account'):
        issues.append('缺account')
    if not c.get('manager'):
        issues.append('缺manager')
    if issues:
        print(f'  [{c["name"]}] {" / ".join(issues)}')
        issues_found = True
if not issues_found:
    print('  无缺失')
