import requests
import json

def ask_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "qwen2:1.5b",
        "prompt": prompt,
        "stream": False,
        "temperature": 0.1
    }
    
    try:
        response = requests.post(url, json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
        else:
            print(f"API错误: {response.status_code}")
            return ""
    except Exception as e:
        print(f"请求错误: {e}")
        return ""

# 构建提示词
context = """
BERT（Bidirectional Encoder Representations from Transformers）是由Google在2018年提出的预训练语言模型。

BERT的核心创新在于使用了双向Transformer编码器，并通过掩码语言模型（Masked Language Model, MLM）和下一句预测（Next Sentence Prediction, NSP）两个预训练任务进行训练。

BERT模型架构：
- 使用多层Transformer编码器
- 支持双向上下文理解
- 采用WordPiece分词方法
- 引入位置编码表示词序信息
"""

prompt = f"""
你是一个基于知识库的智能问答助手。请根据提供的参考文档回答问题。

参考文档：
{context}

用户问题：什么是BERT?

请根据参考文档回答问题：
"""

print("发送请求到Ollama...")
answer = ask_ollama(prompt)
print(f"回答: {answer}")
