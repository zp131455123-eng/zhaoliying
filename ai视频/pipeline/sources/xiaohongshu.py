# -*- coding: utf-8 -*-
"""小红书热点抓取 - 热门话题榜"""
import requests, re, json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.xiaohongshu.com/",
    "Accept-Language": "zh-CN,zh;q=0.9",
}
PROXIES = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}


def fetch_xiaohongshu():
    results = []

    # 方法1：小红书热门话题 API
    try:
        url = "https://www.xiaohongshu.com/api/sns/web/v1/search/hot_list"
        r = requests.get(url, headers=HEADERS, proxies=PROXIES, timeout=10)
        data = r.json()
        items = data.get("data", {}).get("items", [])
        for item in items[:15]:
            title = item.get("display_text", "") or item.get("title", "")
            hot = item.get("hot_score", 0)
            if title:
                results.append({
                    "source": "小红书",
                    "title": title,
                    "desc": item.get("desc", ""),
                    "hot": hot
                })
        print(f"  小红书 API: {len(results)} 条")
    except Exception as e:
        print(f"  小红书 API 失败: {e}")

    # 方法2：小红书探索页话题（备用）
    if not results:
        try:
            url = "https://www.xiaohongshu.com/explore"
            r = requests.get(url, headers={
                **HEADERS,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"
            }, proxies=PROXIES, timeout=10)
            # 从HTML提取话题
            matches = re.findall(r'"title":"([^"]{4,30})"', r.text)
            seen = set()
            for title in matches[:20]:
                if title not in seen and len(title) > 3:
                    seen.add(title)
                    results.append({
                        "source": "小红书",
                        "title": title,
                        "desc": "",
                        "hot": 0
                    })
            print(f"  小红书探索页: {len(results)} 条")
        except Exception as e:
            print(f"  小红书探索页失败: {e}")

    return results


if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    items = fetch_xiaohongshu()
    print(f"\n✅ 小红书共抓取 {len(items)} 条")
    for i, item in enumerate(items[:10], 1):
        print(f"  {i:2d}. {item['title']}  🔥{item['hot']}")
