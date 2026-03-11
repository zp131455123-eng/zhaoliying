# -*- coding: utf-8 -*-
import json, sys
from datetime import datetime

DATA_FILE = 'ea_clients.json'
name = sys.argv[1]

with open(DATA_FILE, encoding='utf-8') as f:
    d = json.load(f)

before = len(d['clients'])
d['clients'] = [c for c in d['clients'] if c['name'] != name]
after = len(d['clients'])

if before == after:
    print(f'未找到客户: {name}')
    sys.exit(1)

active = sum(c['amount'] for c in d['clients'] if c['status'] == '进行中')
stopped = sum(c['amount'] for c in d['clients'] if c['status'] == '停止')
d['meta']['total_active'] = active
d['meta']['total_stopped'] = stopped
d['meta']['total'] = active + stopped
d['meta']['updated'] = datetime.now().strftime('%Y-%m-%d')

with open(DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f'OK: 已删除 [{name}]，剩余 {after} 条')
print(f'停止总计: {stopped} U，总计: {active+stopped} U')
