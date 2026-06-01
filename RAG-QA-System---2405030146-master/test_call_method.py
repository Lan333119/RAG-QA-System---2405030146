from rag_qa import RAGQASystem

# 创建实例
qa = RAGQASystem()

# 直接调用 _call_ollama 方法
print("直接调用 _call_ollama...")
answer = qa._call_ollama("Hello")
print(f"回答: {answer}")
