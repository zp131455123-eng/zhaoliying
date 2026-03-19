#!/usr/bin/env python3
"""
Tavily 网络搜索脚本
用法: python search.py "搜索关键词"
"""
import sys
import json
import os
import requests

def search(query, max_results=5):
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return {"error": "TAVILY_API_KEY not set"}
    
    url = "https://api.tavily.com/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "query": query,
        "max_results": max_results,
        "search_depth": "basic"
    }
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=15)
        result = resp.json()
        
        # 格式化输出
        output = {
            "query": query,
            "count": len(result.get("results", [])),
            "results": []
        }
        
        for r in result.get("results", []):
            output["results"].append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": r.get("content", "")[:300] + "..." if len(r.get("content", "")) > 300 else r.get("content", ""),
                "score": round(r.get("score", 0), 3)
            })
        
        return output
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python search.py <搜索关键词>")
        sys.exit(1)
    
    query = sys.argv[1]
    result = search(query)
    
    # 输出结果
    if "error" in result:
        print(f"[Error] {result['error']}")
    else:
        print(f"Search: {result['query']}")
        print(f"Found {result['count']} results:\n")
        for i, r in enumerate(result["results"], 1):
            print(f"{i}. {r['title']}")
            print(f"   {r['url']}")
            print(f"   {r['snippet']}")
            print()
