# -*- coding: utf-8 -*-
"""
Step 1: 热点抓取
- 微博热搜
- 百度热搜
- 抖音热搜（通过公开接口）
输出：hotspots.json
"""
import sys, io, json, re, datetime, os
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources"))
from hackernews import fetch_hackernews
from youtube import fetch_youtube_trending

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

PROXIES = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def fetch_weibo():
    """微博热搜"""
    results = []
    try:
        url = "https://weibo.com/ajax/side/hotSearch"
        r = requests.get(url, headers=HEADERS, timeout=10)
        data = r.json()
        items = data.get("data", {}).get("realtime", [])
        for item in items[:15]:
            word = item.get("word", "")
            note = item.get("note", "")
            hot = item.get("num", 0)
            if word:
                results.append({
                    "source": "微博",
                    "title": word,
                    "desc": note,
                    "hot": hot
                })
        print(f"  微博热搜: 抓取 {len(results)} 条")
    except Exception as e:
        print(f"  微博热搜失败: {e}")
    return results


def fetch_baidu():
    """百度热搜"""
    results = []
    try:
        url = "https://top.baidu.com/board?tab=realtime"
        r = requests.get(url, headers=HEADERS, timeout=10)
        # 从HTML中提取热搜词
        matches = re.findall(r'"pure_text":"([^"]+)"', r.text)
        for i, word in enumerate(matches[:15]):
            results.append({
                "source": "百度",
                "title": word,
                "desc": "",
                "hot": 15 - i
            })
        print(f"  百度热搜: 抓取 {len(results)} 条")
    except Exception as e:
        print(f"  百度热搜失败: {e}")
    return results


def fetch_douyin():
    """抖音热搜（公开榜单接口）"""
    results = []
    try:
        url = "https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/"
        r = requests.get(url, headers=HEADERS, timeout=10)
        data = r.json()
        items = data.get("word_list", [])
        for item in items[:15]:
            results.append({
                "source": "抖音",
                "title": item.get("word", ""),
                "desc": item.get("sentence_id", ""),
                "hot": item.get("hot_value", 0)
            })
        print(f"  抖音热搜: 抓取 {len(results)} 条")
    except Exception as e:
        print(f"  抖音热搜失败: {e}")
    return results


def fetch_zhihu():
    """知乎热榜"""
    results = []
    try:
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=15"
        headers = {**HEADERS, "x-api-version": "3.0.91"}
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        items = data.get("data", [])
        for item in items:
            target = item.get("target", {})
            title = target.get("title", "") or target.get("question", {}).get("title", "")
            if title:
                results.append({
                    "source": "知乎",
                    "title": title,
                    "desc": target.get("excerpt", ""),
                    "hot": item.get("detail_text", "")
                })
        print(f"  知乎热榜: 抓取 {len(results)} 条")
    except Exception as e:
        print(f"  知乎热榜失败: {e}")
    return results


def filter_hotspots(all_items):
    """过滤规则：去重 + 去政治敏感词"""
    BLACKLIST = ["政治", "领导人", "习", "党", "军事", "台湾", "新疆", "西藏", "香港政府", "示威"]
    seen = set()
    filtered = []
    for item in all_items:
        title = item["title"]
        if title in seen:
            continue
        if any(kw in title for kw in BLACKLIST):
            continue
        seen.add(title)
        filtered.append(item)
    return filtered


def main():
    today = datetime.date.today().strftime("%Y-%m-%d")
    print(f"\n🔥 热点抓取开始 [{today}]")
    print("=" * 40)

    all_items = []
    all_items += fetch_weibo()
    all_items += fetch_baidu()
    all_items += fetch_douyin()
    all_items += fetch_zhihu()
    all_items += fetch_hackernews(limit=15)
    all_items += fetch_youtube_trending()

    filtered = filter_hotspots(all_items)
    print(f"\n✅ 过滤后共 {len(filtered)} 条热点")

    # 输出
    out_dir = os.path.join(OUTPUT_DIR, "output", today)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "hotspots.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"date": today, "count": len(filtered), "items": filtered}, f, ensure_ascii=False, indent=2)

    print(f"📁 已保存: {out_file}")

    # 预览前10条
    print("\n📋 热点预览（前10条）：")
    for i, item in enumerate(filtered[:10], 1):
        print(f"  {i:2d}. [{item['source']}] {item['title']}")

    return out_file, filtered


if __name__ == "__main__":
    main()
