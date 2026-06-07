from langchain_ollama import ChatOllama

def test_ollama_connection():
    try:
        llm = ChatOllama(model="qwen2:7b", temperature=0.7)
        response = llm.invoke("Hello! How are you?")
        print("Ollama连接测试成功！")
        print("响应内容:", response.content)
        return True
    except Exception as e:
        print(f"Ollama连接测试失败: {e}")
        return False

if __name__ == "__main__":
    test_ollama_connection()