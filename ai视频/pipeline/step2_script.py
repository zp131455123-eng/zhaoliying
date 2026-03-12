# -*- coding: utf-8 -*-
"""
Step 2: 文案生成
- 读取 hotspots.json
- 调用 Claude API（已有key）生成结构化脚本
- 输出 scripts.json
"""
import sys, io, json, os, datetime, re
try:
    from json_repair import repair_json
    HAS_REPAIR = True
except ImportError:
    HAS_REPAIR = False
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests

# Claude relay配置
ANTHROPIC_BASE_URL = "https://relay-api.vibeshell.ai/api"
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL = "claude-sonnet-4-6"  # 用sonnet，速度/质量平衡

PROMPT_TEMPLATE_HOT = """你是爆款短视频编剧，擅长情感治愈/实用干货/轻剧情反转风格。

今天的热点列表：
{hotspots}

任务：从以上热点中，选出3个最适合制作8秒短视频的选题（优先选情感共鸣强、有反转、干货实用的）。"""

PROMPT_TEMPLATE_FINANCE = """你是专注加密货币/黄金/财经的短视频编剧，擅长把复杂金融信息转化为普通人看得懂、有共鸣的爆款短视频。

今天的金融/加密/黄金数据和新闻：
{hotspots}

任务：从以上内容中，选出3个最适合制作8秒短视频的选题。
优先选：价格大涨大跌、重大事件、普通人关心的投资信息、反直觉的财经知识。
风格：数字冲击 + 情绪共鸣 + 一句话点破真相。

⚠️ 必须严格输出JSON数组，不要任何其他文字、标题、markdown，直接输出纯JSON：
rank/source_topic/title/hook/script/scenes(数组)/style/hashtags(数组) 这几个字段，3个对象的数组。"""

PROMPT_TEMPLATE = """你是爆款短视频编剧，擅长情感治愈/实用干货/轻剧情反转风格。

今天的热点列表：
{hotspots}

任务：从以上热点中，选出3个最适合制作8秒短视频的选题（优先选情感共鸣强、有反转、干货实用的）。

对每个选题，严格输出JSON格式，返回一个包含3个对象的JSON数组，不要有任何其他文字：
[
  {{
    "rank": 1,
    "source_topic": "原始热点标题",
    "title": "抓眼球的视频标题（带数字或疑问词或情绪词，15字以内）",
    "hook": "开头第一句话，1秒内抓住注意力，10字以内",
    "script": "完整口播文案，30-50字，自然口语，节奏感强，适合配音",
    "scenes": [
      "分镜1：画面描述+人物动作+情绪（10字左右）",
      "分镜2：...",
      "分镜3：...",
      "分镜4：..."
    ],
    "style": "画面风格描述，10字以内",
    "hashtags": ["#标签1", "#标签2", "#标签3"]
  }},
  {{...}},
  {{...}}
]"""


def call_claude(hotspots_text: str, mode: str = "hot") -> str:
    """调用Claude生成文案"""
    template = PROMPT_TEMPLATE_FINANCE if mode == "finance" else PROMPT_TEMPLATE
    prompt = template.format(hotspots=hotspots_text)

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": MODEL,
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}]
    }

    print("  调用 Claude API...")
    r = requests.post(
        f"{ANTHROPIC_BASE_URL}/v1/messages",
        headers=headers,
        json=payload,
        timeout=60,
        proxies={"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
    )
    r.raise_for_status()
    data = r.json()
    return data["content"][0]["text"]


def parse_scripts(raw: str) -> list:
    """从LLM输出中提取JSON"""
    # 去掉```json```包裹
    text = re.sub(r"```json\s*", "", raw)
    text = re.sub(r"```\s*", "", text)
    text = text.strip()

    start = text.find("[")
    end = text.rfind("]") + 1
    if start == -1 or end == 0:
        raise ValueError(f"未找到JSON数组，原始输出：\n{raw}")
    json_str = text[start:end]

    # 修复常见问题：省略号、多余逗号
    json_str = re.sub(r",\s*\.\.\.", "", json_str)  # 去掉 , ...
    json_str = re.sub(r",\s*}", "}", json_str)       # 去掉尾部逗号
    json_str = re.sub(r",\s*]", "]", json_str)       # 去掉数组尾部逗号

    # 先尝试标准解析，失败则用json_repair
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        if HAS_REPAIR:
            fixed = repair_json(json_str)
            return json.loads(fixed)
        raise


def main(hotspots_file=None, mode="hot"):
    today = datetime.date.today().strftime("%Y-%m-%d")

    # 找hotspots文件
    if not hotspots_file:
        hotspots_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "output", today, "hotspots.json"
        )

    if not os.path.exists(hotspots_file):
        print(f"❌ 找不到热点文件: {hotspots_file}")
        print("请先运行 step1_hotspot.py")
        return

    print(f"\n✍️  文案生成开始 [{today}]")
    print("=" * 40)

    with open(hotspots_file, encoding="utf-8") as f:
        data = json.load(f)

    all_items = data["items"]

    # finance模式：只取金融相关来源
    if mode == "finance":
        finance_sources = {"CoinGecko", "GoldPrice", "CoinDesk", "CoinTelegraph", "FT财经", "MarketWatch"}
        items = [x for x in all_items if x["source"] in finance_sources][:25]
        print(f"  金融模式：筛选出 {len(items)} 条金融/加密/黄金内容")
    else:
        items = all_items[:20]

    hotspots_text = "\n".join(
        f"{i+1}. [{item['source']}] {item['title']}" + (f" - {item['desc']}" if item.get('desc') else "")
        for i, item in enumerate(items)
    )

    print(f"  输入热点数: {len(items)} 条，模式: {mode}")

    # 调用Claude
    raw = call_claude(hotspots_text, mode=mode)
    print("  ✅ Claude返回成功")

    # 解析
    try:
        scripts = parse_scripts(raw)
    except Exception as e:
        print(f"  ❌ JSON解析失败: {e}")
        print(f"  原始输出已保存到 raw_llm.txt，内容片段：\n{raw[:500]}")
        raise
    print(f"  解析到 {len(scripts)} 个脚本")

    # debug：保存原始输出
    debug_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", today, "raw_llm.txt")
    os.makedirs(os.path.dirname(debug_file), exist_ok=True)
    with open(debug_file, "w", encoding="utf-8") as f:
        f.write(raw)

    # 保存
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", today)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "scripts.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"date": today, "count": len(scripts), "scripts": scripts}, f, ensure_ascii=False, indent=2)

    print(f"📁 已保存: {out_file}")

    # 预览
    print("\n📋 生成脚本预览：")
    for s in scripts:
        print(f"\n  [{s['rank']}] {s['title']}")
        print(f"      hook: {s['hook']}")
        print(f"      文案: {s['script'][:40]}...")
        print(f"      标签: {' '.join(s['hashtags'])}")

    return out_file, scripts


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="hot", choices=["hot", "finance"], help="选题模式")
    parser.add_argument("--file", default=None, help="指定hotspots.json路径")
    args = parser.parse_args()
    main(hotspots_file=args.file, mode=args.mode)
