import requests, json

url = "https://api.tavily.com/search"
headers = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}
data = {
    "query": "AI latest news",
    "max_results": 3,
    "search_depth": "basic"
}

try:
    resp = requests.post(url, headers=headers, json=data, timeout=10)
    result = resp.json()
    with open("tavily_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print("OK - saved to tavily_result.json")
    print(f"Found {len(result.get('results', []))} results")
except Exception as e:
    print(f"Error: {e}")
