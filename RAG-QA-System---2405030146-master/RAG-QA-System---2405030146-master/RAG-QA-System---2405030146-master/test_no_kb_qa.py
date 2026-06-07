from rag_qa import RAGQASystem

# 创建实例但不加载知识库
qa = RAGQASystem()

# 不加载知识库，直接测试问答
print("测试不加载知识库时的问答...")
answer = qa.ask("什么是人工智能？")
print(f"回答: {answer}")
