# -*- coding: utf-8 -*-
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open('../ea策略/ea_clients.json', encoding='utf-8') as f:
    data = json.load(f)
stopped = [c for c in data['clients'] if c['status'] == '停止']
print(f"停止客户共{len(stopped)}人：")
for c in stopped:
    print(f"  {c['name']}  平台:{c['platform']}  资金:{c['amount']}U")
