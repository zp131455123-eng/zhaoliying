# -*- coding: utf-8 -*-
"""Reddit 热点抓取 - 免登录公开接口"""
import requests, json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; HotspotBot/1.0)"
}
PROXIES = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
SESSION = requests.Session()
SESSION.proxies.update(PROXIES)
SESSION.headers.update(HEADERS)

# 抓取这些板块
SUBREDDITS = [
    ("popular", "综合热门"),
    ("worldnews", "国际新闻"),
    ("technology", "科技"),
    ("explainlikeimfive", "知识科普"),
    ("tifu", "反转故事"),
    ("AmItheAsshole", "情感故事"),
]

def fetch_reddit(limit=30):
    results = []
    for sub, label in SUBREDDITS:
        try:
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit=10"
            r = SESSION.get(url, timeout=10)
            data = r.json()
            posts = data.get("data", {}).get("children", [])
            for p in posts:
                d = p["data"]
                if d.get("stickied") or d.get("over_18"):
                    continue
                results.append({
                    "source": f"Reddit/{sub}",
                    "title": d.get("title", ""),
                    "desc": d.get("selftext", "")[:100],
                    "hot": d.get("score", 0),
                    "comments": d.get("num_comments", 0),
                    "url": f"https://reddit.com{d.get('permalink','')}"
                })
            print(f"  Reddit/{sub}: {len(posts)} 条")
        except Exception as e:
            print(f"  Reddit/{sub} 失败: {e}")

    # 按热度排序
    results.sort(key=lambda x: x["hot"], reverse=True)
    return results[:limit]


if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    items = fetch_reddit()
    print(f"\n✅ Reddit 共抓取 {len(items)} 条")
    for i, item in enumerate(items[:10], 1):
        print(f"  {i:2d}. [{item['source']}] {item['title'][:50]}  👍{item['hot']:,}")
