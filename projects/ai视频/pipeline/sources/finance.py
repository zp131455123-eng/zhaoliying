# -*- coding: utf-8 -*-
"""金融/加密/黄金热点抓取"""
import requests, json, re

PROXIES = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0"}


def fetch_coindesk():
    """CoinDesk RSS - 加密货币新闻"""
    results = []
    try:
        import xml.etree.ElementTree as ET
        r = requests.get(
            "https://www.coindesk.com/arc/outboundfeeds/rss/",
            headers=HEADERS, proxies=PROXIES, timeout=10
        )
        root = ET.fromstring(r.content)
        items = root.findall(".//item")
        for item in items[:15]:
            title = item.findtext("title", "").strip()
            desc = item.findtext("description", "").strip()
            desc = re.sub(r"<[^>]+>", "", desc)[:100]
            link = item.findtext("link", "")
            if title:
                results.append({
                    "source": "CoinDesk",
                    "title": title,
                    "desc": desc,
                    "hot": 0,
                    "url": link
                })
        print(f"  CoinDesk: {len(results)} 条")
    except Exception as e:
        print(f"  CoinDesk 失败: {e}")
    return results


def fetch_cointelegraph():
    """CoinTelegraph RSS - 加密货币"""
    results = []
    try:
        import xml.etree.ElementTree as ET
        r = requests.get(
            "https://cointelegraph.com/rss",
            headers=HEADERS, proxies=PROXIES, timeout=10
        )
        root = ET.fromstring(r.content)
        items = root.findall(".//item")
        for item in items[:15]:
            title = item.findtext("title", "").strip()
            desc = item.findtext("description", "").strip()
            desc = re.sub(r"<[^>]+>", "", desc)[:100]
            if title:
                results.append({
                    "source": "CoinTelegraph",
                    "title": title,
                    "desc": desc,
                    "hot": 0,
                    "url": item.findtext("link", "")
                })
        print(f"  CoinTelegraph: {len(results)} 条")
    except Exception as e:
        print(f"  CoinTelegraph 失败: {e}")
    return results


def fetch_crypto_prices():
    """CoinGecko API - BTC/ETH/黄金实时价格（免key）"""
    results = []
    try:
        # 加密货币价格
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=bitcoin,ethereum,solana,binancecoin,ripple"
            "&vs_currencies=usd&include_24hr_change=true",
            headers=HEADERS, proxies=PROXIES, timeout=10
        )
        data = r.json()
        coin_names = {
            "bitcoin": "比特币(BTC)",
            "ethereum": "以太坊(ETH)",
            "solana": "Solana(SOL)",
            "binancecoin": "BNB",
            "ripple": "瑞波币(XRP)"
        }
        for coin_id, name in coin_names.items():
            if coin_id in data:
                price = data[coin_id].get("usd", 0)
                change = data[coin_id].get("usd_24h_change", 0)
                direction = "📈" if change > 0 else "📉"
                results.append({
                    "source": "CoinGecko",
                    "title": f"{name} {direction} ${price:,.0f} (24h: {change:+.1f}%)",
                    "desc": f"当前价格 ${price:,.2f}，24小时变动 {change:+.2f}%",
                    "hot": abs(change),  # 涨跌幅越大越热
                    "price": price,
                    "change_24h": round(change, 2)
                })
        print(f"  CoinGecko价格: {len(results)} 条")
    except Exception as e:
        print(f"  CoinGecko 失败: {e}")

    # 黄金价格（通过CoinGecko的XAU数据）
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=pax-gold,tether-gold&vs_currencies=usd&include_24hr_change=true",
            headers=HEADERS, proxies=PROXIES, timeout=10
        )
        data = r.json()
        # pax-gold 是黄金代币，1枚=1盎司黄金
        for coin_id, name in [("pax-gold", "黄金(PAXG/oz)"), ("tether-gold", "黄金(XAUT/oz)")]:
            if coin_id in data:
                price = data[coin_id].get("usd", 0)
                change = data[coin_id].get("usd_24h_change", 0)
                direction = "📈" if change > 0 else "📉"
                results.append({
                    "source": "GoldPrice",
                    "title": f"黄金 {direction} ${price:,.1f}/oz (24h: {change:+.2f}%)",
                    "desc": f"黄金现货价格参考 ${price:,.2f}/盎司",
                    "hot": abs(change),
                    "price": price,
                    "change_24h": round(change, 2)
                })
                print(f"  黄金价格({name}): ${price:,.1f}")
                break
    except Exception as e:
        print(f"  黄金价格 失败: {e}")

    return results


def fetch_ft_finance():
    """Financial Times RSS - 财经新闻"""
    results = []
    try:
        import xml.etree.ElementTree as ET
        r = requests.get(
            "https://www.ft.com/rss/home/uk",
            headers=HEADERS, proxies=PROXIES, timeout=10
        )
        root = ET.fromstring(r.content)
        items = root.findall(".//item")
        for item in items[:10]:
            title = item.findtext("title", "").strip()
            desc = item.findtext("description", "").strip()
            desc = re.sub(r"<[^>]+>", "", desc)[:100]
            if title:
                results.append({
                    "source": "FT财经",
                    "title": title,
                    "desc": desc,
                    "hot": 0,
                    "url": item.findtext("link", "")
                })
        print(f"  FT财经: {len(results)} 条")
    except Exception as e:
        print(f"  FT财经 失败: {e}")

    # 备用：MarketWatch RSS
    if not results:
        try:
            import xml.etree.ElementTree as ET
            r = requests.get(
                "https://feeds.marketwatch.com/marketwatch/topstories/",
                headers=HEADERS, proxies=PROXIES, timeout=10
            )
            root = ET.fromstring(r.content)
            items = root.findall(".//item")
            for item in items[:10]:
                title = item.findtext("title", "").strip()
                if title:
                    results.append({
                        "source": "MarketWatch",
                        "title": title,
                        "desc": "",
                        "hot": 0,
                        "url": item.findtext("link", "")
                    })
            print(f"  MarketWatch: {len(results)} 条")
        except Exception as e:
            print(f"  MarketWatch 失败: {e}")
    return results


def fetch_all_finance():
    results = []
    results += fetch_crypto_prices()
    results += fetch_coindesk()
    results += fetch_cointelegraph()
    results += fetch_ft_finance()
    return results


if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    items = fetch_all_finance()
    print(f"\n✅ 金融/加密/黄金 共抓取 {len(items)} 条")
    print("\n--- 价格行情 ---")
    for item in items:
        if item["source"] in ("CoinGecko", "GoldPrice"):
            print(f"  {item['title']}")
    print("\n--- 新闻资讯 ---")
    for i, item in enumerate([x for x in items if x["source"] not in ("CoinGecko", "GoldPrice")][:10], 1):
        print(f"  {i:2d}. [{item['source']}] {item['title'][:60]}")
