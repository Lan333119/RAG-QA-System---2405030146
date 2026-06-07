from rag_qa import RAGQASystem

print("初始化RAG问答系统...")
qa = RAGQASystem()
print("系统初始化完成")

print("\n检查知识库状态...")
stats = qa.get_knowledge_base_stats()
print(f"知识库文本块数量: {stats}")

test_questions = [
    "什么是自然语言处理？",
    "Transformer模型的核心组件有哪些？",
    "BERT模型是什么？",
    "今天天气怎么样？"
]

print("\n测试问答效果：")
for question in test_questions:
    print(f"\n问题: {question}")
    print("正在获取回答...")
    try:
        answer = qa.ask(question)
        print(f"回答: {answer}")
        print(f"回答长度: {len(answer)}")
    except Exception as e:
        print(f"错误: {e}")
