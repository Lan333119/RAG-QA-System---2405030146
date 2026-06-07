import requests
import json

# 直接测试Ollama API（不通过类）
def test_direct():
    print("测试1: 直接调用Ollama API")
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "qwen2:1.5b",
        "prompt": "Hello",
        "stream": False,
        "temperature": 0.1
    }
    response = requests.post(url, json=data, timeout=60)
    if response.status_code == 200:
        result = response.json()
        print(f"回答: {result.get('response', '')}")
    else:
        print(f"错误: {response.status_code}")

test_direct()

# 测试通过类调用（不加载知识库）
from rag_qa import RAGQASystem

print("\n测试2: 通过类调用（不加载知识库）")
# 创建一个不加载知识库的实例
qa = RAGQASystem()
# 重置 vector_db 为 None，模拟未加载状态
qa.kb.vector_db = None

print("调用 _call_ollama...")
answer = qa._call_ollama("Hello")
print(f"回答: {answer}")
