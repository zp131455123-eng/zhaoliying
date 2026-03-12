# -*- coding: utf-8 -*-
"""YouTube 热点抓取 - 免key公开接口（trending RSS + 搜索接口）"""
import requests, re, json, xml.etree.ElementTree as ET

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
}
PROXIES = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

def fetch_youtube_trending():
    """抓取 YouTube 趋势视频（中国/香港区）"""
    results = []

    # 方法1：YouTube trending 页面（解析初始数据）
    try:
        regions = [("HK", "香港"), ("TW", "台湾")]
        for region_code, region_name in regions:
            url = f"https://www.youtube.com/feed/trending?bp=4gINGgt5dGQtdHJlbmRpbmc%3D&gl={region_code}&hl=zh-TW"
            r = requests.get(url, headers=HEADERS, proxies=PROXIES, timeout=15)
            # 从页面HTML提取ytInitialData
            match = re.search(r'var ytInitialData = ({.*?});</script>', r.text, re.DOTALL)
            if not match:
                print(f"  YouTube {region_name}: 未找到数据")
                continue

            data = json.loads(match.group(1))
            # 遍历找到视频列表
            videos = []
            try:
                tabs = data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]
                for tab in tabs:
                    try:
                        contents = tab["tabRenderer"]["content"]["sectionListRenderer"]["contents"]
                        for section in contents:
                            items = section.get("itemSectionRenderer", {}).get("contents", [])
                            for item in items:
                                vr = item.get("videoRenderer", {})
                                if not vr:
                                    continue
                                title = vr.get("title", {}).get("runs", [{}])[0].get("text", "")
                                channel = vr.get("ownerText", {}).get("runs", [{}])[0].get("text", "")
                                views = vr.get("viewCountText", {}).get("simpleText", "")
                                vid = vr.get("videoId", "")
                                if title:
                                    videos.append({
                                        "source": f"YouTube/{region_name}",
                                        "title": title,
                                        "desc": channel,
                                        "hot": views,
                                        "url": f"https://youtube.com/watch?v={vid}"
                                    })
                    except:
                        continue
            except:
                pass

            results.extend(videos[:10])
            print(f"  YouTube {region_name}: {len(videos)} 条")

    except Exception as e:
        print(f"  YouTube trending 失败: {e}")

    # 方法2：YouTube RSS（频道订阅不需要key）
    # 用热门搜索词的RSS
    try:
        trending_queries = ["热门", "viral", "trending"]
        for q in trending_queries[:1]:
            url = f"https://www.youtube.com/results?search_query={q}&sp=CAISAhAB"  # 本周热门
            r = requests.get(url, headers=HEADERS, proxies=PROXIES, timeout=15)
            matches = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"\}', r.text)
            vids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', r.text)
            for i, (title, vid) in enumerate(zip(matches[:10], vids[:10])):
                if len(title) > 5 and not any(x["url"].endswith(vid) for x in results):
                    results.append({
                        "source": "YouTube/搜索",
                        "title": title,
                        "desc": "",
                        "hot": 10 - i,
                        "url": f"https://youtube.com/watch?v={vid}"
                    })
            print(f"  YouTube 搜索: {min(10, len(matches))} 条")
    except Exception as e:
        print(f"  YouTube 搜索失败: {e}")

    return results


if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    items = fetch_youtube_trending()
    print(f"\n✅ YouTube 共抓取 {len(items)} 条")
    for i, item in enumerate(items[:10], 1):
        print(f"  {i:2d}. [{item['source']}] {item['title'][:60]}")
