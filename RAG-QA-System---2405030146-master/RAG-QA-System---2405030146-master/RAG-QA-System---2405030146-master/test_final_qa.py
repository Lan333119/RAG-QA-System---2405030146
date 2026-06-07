from rag_qa import RAGQASystem

# 使用新的数据库目录
qa = RAGQASystem()
qa.kb.persist_directory = "./chroma_db_new"
qa.kb.load_knowledge_base()

print("知识库状态:", qa.get_knowledge_base_stats())

test_questions = [
    "什么是BERT?",
    "Transformer模型的核心组件有哪些？",
    "什么是自然语言处理？",
    "GPT模型是什么？",
    "今天天气怎么样？"
]

print("\n测试问答效果：")
for question in test_questions:
    print(f"\n问题: {question}")
    answer = qa.ask(question)
    print(f"回答: {answer}")
