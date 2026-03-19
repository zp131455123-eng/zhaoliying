import json
from datetime import datetime

with open('ea_clients.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

clients = data['clients']
active_clients = [c for c in clients if c['status'] == '进行中']
stopped_clients = [c for c in clients if c['status'] == '停止']
total_active = sum(c['amount'] for c in active_clients)
total_stopped = sum(c['amount'] for c in stopped_clients)
total_all = total_active + total_stopped

platform_map = {'星迈': '星迈', 'ebc': 'EBC', 'tmgm': 'TMGM'}
platform_amounts = {}
for c in clients:
    p = c['platform']
    platform_amounts[p] = platform_amounts.get(p, 0) + c['amount']

manager_data = {}
for c in clients:
    m = c['manager']
    if m not in manager_data:
        manager_data[m] = {'total': 0, 'active': 0, 'stopped': 0, 'active_amt': 0, 'stopped_amt': 0}
    manager_data[m]['total'] += c['amount']
    if c['status'] == '进行中':
        manager_data[m]['active'] += 1
        manager_data[m]['active_amt'] += c['amount']
    else:
        manager_data[m]['stopped'] += 1
        manager_data[m]['stopped_amt'] += c['amount']

date_str = datetime.now().strftime('%Y-%m-%d')

# Build active rows
active_rows = ""
for i, c in enumerate(active_clients, 1):
    p = c['platform']
    tag_class = {'星迈': 'xingmai', 'ebc': 'ebc', 'tmgm': 'tmgm'}.get(p, '')
    pname = platform_map.get(p, p)
    active_rows += f'<tr data-platform="{p}"><td class="center">{i}</td><td class="name">{c["name"]}</td><td class="center">{c["manager"]}</td><td class="center"><span class="tag tag-{tag_class}">{pname}</span></td><td class="right">{c["amount"]:,}</td></tr>\n        '

# Build stopped rows
stopped_rows = ""
for i, c in enumerate(stopped_clients, 1):
    stopped_rows += f'<tr><td class="center">{i}</td><td class="name">{c["name"]}</td><td class="center">{c["manager"]}</td><td class="right">{c["amount"]:,}</td></tr>\n        '

# Build manager rows
manager_rows = ""
for m, d in sorted(manager_data.items(), key=lambda x: -x[1]['total']):
    manager_rows += f'<tr><td class="name center">{m}</td><td class="center">{d["active"]+d["stopped"]}</td><td class="center">{d["active"]}</td><td class="right">{d["active_amt"]:,}</td><td class="center">{d["stopped"]}</td><td class="right">{d["stopped_amt"]:,}</td><td class="right"><b>{d["total"]:,}</b></td></tr>\n        '

# Build platform summary cards
platform_cards = ""
for p, amt in sorted(platform_amounts.items(), key=lambda x: -x[1]):
    pname = platform_map.get(p, p.upper())
    color = {'星迈': '#1a5276', 'ebc': '#a04000', 'tmgm': '#1e8449'}.get(p, '#1a3a5c')
    platform_cards += f'''<div class="sum-card">
    <div class="label">{pname}</div>
    <div class="value" style="color:{color}">{amt:,} U</div>
  </div>
'''

html = f'''<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>各平台客户资金总览</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; background: #f0f4f9; color: #222; }}
  .header {{
    background: linear-gradient(135deg, #1a3a5c, #2e6da4);
    color: #fff; padding: 28px 40px;
    display: flex; justify-content: space-between; align-items: center;
  }}
  .header h1 {{ font-size: 24px; letter-spacing: 2px; }}
  .header .date {{ font-size: 13px; opacity: 0.8; }}
  .summary-bar {{
    display: flex; gap: 20px; padding: 20px 40px;
    background: #fff; border-bottom: 1px solid #dde4ee; flex-wrap: wrap;
  }}
  .sum-card {{
    background: #f0f4f9; border-left: 4px solid #2e6da4;
    padding: 10px 20px; border-radius: 4px; min-width: 150px;
  }}
  .sum-card.green {{ border-color: #27ae60; }}
  .sum-card.red   {{ border-color: #e74c3c; }}
  .sum-card.gold  {{ border-color: #f39c12; }}
  .sum-card .label {{ font-size: 12px; color: #666; margin-bottom: 4px; }}
  .sum-card .value {{ font-size: 22px; font-weight: bold; color: #1a3a5c; }}
  .sum-card.green .value {{ color: #27ae60; }}
  .sum-card.red   .value {{ color: #e74c3c; }}
  .sum-card.gold  .value {{ color: #f39c12; }}
  .container {{ padding: 30px 40px; }}
  .section {{ margin-bottom: 36px; }}
  .section-title {{
    font-size: 16px; font-weight: bold; color: #1a3a5c;
    padding: 10px 16px; background: #dde8f5;
    border-left: 5px solid #2e6da4; border-radius: 0 4px 4px 0;
    margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;
  }}
  .section-title span {{ font-size: 13px; color: #555; font-weight: normal; }}
  .section-title.stopped {{ background: #fde8e8; border-color: #e74c3c; color: #c0392b; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
  thead tr {{ background: #2e6da4; color: #fff; }}
  thead tr.red-head {{ background: #c0392b; }}
  thead th {{ padding: 10px 14px; text-align: center; font-weight: bold; letter-spacing: 1px; }}
  tbody tr:nth-child(odd)  {{ background: #f7faff; }}
  tbody tr:nth-child(even) {{ background: #ffffff; }}
  tbody tr:hover {{ background: #e3edf8; }}
  td {{ padding: 9px 14px; border-bottom: 1px solid #e8edf5; }}
  td.center {{ text-align: center; }}
  td.right  {{ text-align: right; font-weight: 500; }}
  td.name   {{ font-weight: 500; }}
  .tag {{
    display: inline-block; padding: 2px 10px;
    border-radius: 4px; font-size: 12px; font-weight: bold;
  }}
  .tag-xingmai {{ background: #d6eaf8; color: #1a5276; }}
  .tag-tmgm    {{ background: #d5f5e3; color: #1e8449; }}
  .tag-ebc     {{ background: #fde8d8; color: #a04000; }}
  tfoot tr {{ background: #1a3a5c; color: #fff; }}
  tfoot tr.red-foot {{ background: #922b21; }}
  tfoot td {{ padding: 10px 14px; font-weight: bold; font-size: 14px; }}
  .filter-bar {{
    margin-bottom: 16px; display: flex; gap: 10px;
    flex-wrap: wrap; align-items: center;
  }}
  .filter-bar label {{ font-size: 13px; color: #555; }}
  .filter-bar button {{
    padding: 5px 16px; border: 1px solid #2e6da4; border-radius: 20px;
    background: #fff; color: #2e6da4; cursor: pointer; font-size: 13px; transition: all 0.15s;
  }}
  .filter-bar button:hover, .filter-bar button.active {{ background: #2e6da4; color: #fff; }}
  @media print {{ .filter-bar {{ display: none; }} body {{ background: #fff; }} }}
</style>
</head>
<body>

<div class="header">
  <h1>📊 各平台客户资金总览</h1>
  <div class="date">更新日期：{date_str}</div>
</div>

<div class="summary-bar">
  <div class="sum-card gold">
    <div class="label">总资金量</div>
    <div class="value">{total_all:,} U</div>
  </div>
  <div class="sum-card green">
    <div class="label">进行中</div>
    <div class="value">{total_active:,} U</div>
  </div>
  <div class="sum-card red">
    <div class="label">已停止</div>
    <div class="value">{total_stopped:,} U</div>
  </div>
  {platform_cards}
</div>

<div class="container">
  <div class="filter-bar">
    <label>筛选：</label>
    <button class="active" onclick="filterAll(this)">全部</button>
    <button onclick="filterGroup('active', this)">🟢 进行中</button>
    <button onclick="filterGroup('stopped', this)">🔴 已停止</button>
    <button onclick="filterPlatform('星迈', this)">星迈</button>
    <button onclick="filterPlatform('ebc', this)">EBC</button>
    <button onclick="filterPlatform('tmgm', this)">TMGM</button>
  </div>

  <div class="section" data-group="active">
    <div class="section-title">
      🟢 进行中客户
      <span>共{len(active_clients)}人 · {total_active:,} U</span>
    </div>
    <table>
      <thead><tr><th>序号</th><th>姓名</th><th>代理人</th><th>平台</th><th>资金 (U)</th></tr></thead>
      <tbody>
        {active_rows}      </tbody>
      <tfoot><tr><td colspan="4" class="center">合计</td><td class="right">{total_active:,}</td></tr></tfoot>
    </table>
  </div>

  <div class="section" data-group="stopped">
    <div class="section-title stopped">
      🔴 已停止客户
      <span style="color:#888">共{len(stopped_clients)}人 · {total_stopped:,} U</span>
    </div>
    <table>
      <thead><tr class="red-head"><th>序号</th><th>姓名</th><th>代理人</th><th>资金 (U)</th></tr></thead>
      <tbody>
        {stopped_rows}      </tbody>
      <tfoot><tr class="red-foot"><td colspan="3" class="center">合计</td><td class="right">{total_stopped:,}</td></tr></tfoot>
    </table>
  </div>

  <div class="section">
    <div class="section-title" style="background:#e8f5e9; border-color:#27ae60; color:#1e8449;">
      👤 代理人统计
      <span style="color:#555">进行中 + 已停止</span>
    </div>
    <table>
      <thead><tr style="background:#27ae60">
        <th>代理人</th><th>总客户数</th><th>进行中客户</th><th>进行中资金 (U)</th><th>已停止客户</th><th>停止资金 (U)</th><th>合计资金 (U)</th>
      </tr></thead>
      <tbody>
        {manager_rows}      </tbody>
      <tfoot><tr style="background:#1e8449; color:#fff">
        <td class="center">合计</td><td class="center">{len(clients)}</td><td class="center">{len(active_clients)}</td><td class="right">{total_active:,}</td><td class="center">{len(stopped_clients)}</td><td class="right">{total_stopped:,}</td><td class="right"><b>{total_all:,}</b></td>
      </tr></tfoot>
    </table>
  </div>
</div>

<script>
function filterAll(btn) {{
  document.querySelectorAll('.section').forEach(s => s.style.display = '');
  document.querySelectorAll('tbody tr').forEach(r => r.style.display = '');
  setActive(btn);
}}
function filterGroup(group, btn) {{
  document.querySelectorAll('.section').forEach(s => {{
    s.style.display = s.dataset.group === group ? '' : 'none';
  }});
  document.querySelectorAll('tbody tr').forEach(r => r.style.display = '');
  setActive(btn);
}}
function filterPlatform(platform, btn) {{
  document.querySelectorAll('.section').forEach(s => s.style.display = '');
  document.querySelectorAll('tbody tr').forEach(r => {{
    r.style.display = r.dataset.platform === platform ? '' : 'none';
  }});
  setActive(btn);
}}
function setActive(btn) {{
  document.querySelectorAll('.filter-bar button').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}}
</script>
</body>
</html>'''

with open('EA客户总览.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! Generated EA客户总览.html")
