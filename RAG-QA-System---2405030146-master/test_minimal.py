import requests
import json

# 最小化测试：直接调用Ollama API
url = "http://localhost:11434/api/generate"
data = {
    "model": "qwen2:1.5b",
    "prompt": "Hello",
    "stream": False,
    "temperature": 0.1
}

print("发送请求...")
try:
    response = requests.post(url, json=data, timeout=60)
    if response.status_code == 200:
        result = response.json()
        print(f"回答: {result.get('response', '')}")
    else:
        print(f"错误: {response.status_code}")
except Exception as e:
    print(f"异常: {e}")
