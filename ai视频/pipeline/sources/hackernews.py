# -*- coding: utf-8 -*-
"""Hacker News 热点抓取 - 完全开放API，无需任何key"""
import requests, json

PROXIES = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_hackernews(limit=20):
    results = []
    try:
        # 获取top stories ID列表
        r = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            headers=HEADERS, proxies=PROXIES, timeout=10
        )
        ids = r.json()[:limit]
        print(f"  HackerNews: 获取到 {len(ids)} 个ID，正在拉取详情...")

        for i, story_id in enumerate(ids):
            r2 = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                headers=HEADERS, proxies=PROXIES, timeout=5
            )
            item = r2.json()
            if not item or item.get("type") != "story":
                continue
            results.append({
                "source": "HackerNews",
                "title": item.get("title", ""),
                "desc": item.get("url", ""),
                "hot": item.get("score", 0),
                "comments": item.get("descendants", 0),
                "url": item.get("url", f"https://news.ycombinator.com/item?id={story_id}")
            })

        print(f"  HackerNews: 成功抓取 {len(results)} 条")
    except Exception as e:
        print(f"  HackerNews 失败: {e}")

    results.sort(key=lambda x: x["hot"], reverse=True)
    return results


if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    items = fetch_hackernews()
    print(f"\n✅ HackerNews 共抓取 {len(items)} 条")
    for i, item in enumerate(items[:10], 1):
        print(f"  {i:2d}. {item['title'][:60]}  👍{item['hot']}")
