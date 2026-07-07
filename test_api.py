import requests

API_KEY = "sk-dc69187ef16944c9aeec2beeddf73533"
url = "https://api.deepseek.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "你好"}],
    "max_tokens": 50
}

try:
    response = requests.post(url, headers=headers, json=data, timeout=30)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
except Exception as e:
    print(f"错误: {e}")