from rag_qa import RAGQASystem

qa = RAGQASystem()

print("测试1: 简单提示词")
answer1 = qa._call_ollama("Hello")
print(f"回答1: {answer1}")

print("\n测试2: 完整提示词")
full_prompt = """
你是一个基于知识库的智能问答助手。

参考文档：
BERT是Google在2018年提出的预训练语言模型。

用户问题：什么是BERT?

请回答问题：
"""
answer2 = qa._call_ollama(full_prompt)
print(f"回答2: {answer2}")
