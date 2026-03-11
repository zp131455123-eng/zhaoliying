# -*- coding: utf-8 -*-
import json
from datetime import datetime

DATA_FILE = 'ea_clients.json'

with open(DATA_FILE, encoding='utf-8') as f:
    d = json.load(f)

new_id = max(c['id'] for c in d['clients']) + 1
new_client = {
    "id": new_id,
    "name": "李四",
    "manager": "张三",
    "platform": None,
    "account": None,
    "amount": 50000,
    "status": "停止",
    "current_balance": None,
    "transferred": None,
    "notes": ""
}
d['clients'].append(new_client)

# 重新计算合计
active = sum(c['amount'] for c in d['clients'] if c['status'] == '进行中')
stopped = sum(c['amount'] for c in d['clients'] if c['status'] == '停止')
d['meta']['total_active'] = active
d['meta']['total_stopped'] = stopped
d['meta']['total'] = active + stopped
d['meta']['updated'] = datetime.now().strftime('%Y-%m-%d')

with open(DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"OK: 已新增 [{new_client['name']}] ID={new_id}, 停止, 50000U, 负责人=张三")
print(f"停止总计: {stopped} U")
