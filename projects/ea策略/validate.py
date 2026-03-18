# -*- coding: utf-8 -*-
"""
数据验证脚本 - 每次修改数据后运行
规则：只报告问题，不自动补全，不猜测
"""
import json

DATA_FILE = 'ea_clients.json'

def validate():
    with open(DATA_FILE, encoding='utf-8') as f:
        d = json.load(f)

    clients = d['clients']
    errors = []
    warnings = []

    for c in clients:
        name = c['name']

        # 错误：必填字段为空
        if not c.get('name'):
            errors.append(f'客户ID {c["id"]} 缺少姓名')
        if not c.get('status'):
            errors.append(f'[{name}] 缺少状态')
        if not c.get('manager'):
            errors.append(f'[{name}] 缺少负责人')
        if c.get('amount', 0) <= 0:
            errors.append(f'[{name}] 入金金额异常: {c.get("amount")}')

        # 警告：建议填写但允许为空
        if not c.get('platform'):
            warnings.append(f'[{name}] platform 为空（原始数据未记录）')
        if not c.get('account'):
            warnings.append(f'[{name}] account 为空（原始数据未记录）')
        if c.get('current_balance') is None:
            warnings.append(f'[{name}] current_balance 为空')

    # 汇总金额验证
    active_sum = sum(c['amount'] for c in clients if c['status'] == '进行中')
    stopped_sum = sum(c['amount'] for c in clients if c['status'] == '停止')
    meta_active = d['meta']['total_active']
    meta_stopped = d['meta']['total_stopped']

    if active_sum != meta_active:
        errors.append(f'进行中金额不一致：实际 {active_sum} vs meta {meta_active}')
    if stopped_sum != meta_stopped:
        errors.append(f'停止金额不一致：实际 {stopped_sum} vs meta {meta_stopped}')

    # 输出结果
    print('=== 数据验证报告 ===')
    if errors:
        print(f'\n[ERROR] 错误 ({len(errors)} 条) - 必须修复:')
        for e in errors:
            print(f'  {e}')
    else:
        print('\n[OK] 无错误')

    if warnings:
        print(f'\n[WARN] 警告 ({len(warnings)} 条) - 原始数据缺失，等待补充:')
        for w in warnings:
            print(f'  {w}')
    else:
        print('[OK] 无警告')

    print(f'\n=== 汇总 ===')
    print(f'  进行中: {active_sum} U ({len([c for c in clients if c["status"] == "进行中"])} 条)')
    print(f'  停止:   {stopped_sum} U ({len([c for c in clients if c["status"] == "停止"])} 条)')
    print(f'  总计:   {active_sum + stopped_sum} U')

if __name__ == '__main__':
    validate()
