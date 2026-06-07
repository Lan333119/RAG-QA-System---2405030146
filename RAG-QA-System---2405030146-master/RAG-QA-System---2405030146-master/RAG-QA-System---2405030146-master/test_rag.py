from rag_qa import RAGQASystem

def test_rag_system():
    print("初始化RAG问答系统...")
    qa_system = RAGQASystem()
    
    if not qa_system.load_knowledge_base():
        print("构建知识库...")
        qa_system.build_knowledge_base_from_docs()
    
    test_questions = [
        "什么是自然语言处理？",
        "Transformer模型的核心组件有哪些？",
        "BERT模型的预训练任务是什么？",
        "自然语言处理有哪些应用？",
        "GPT是什么？",
        "今天天气怎么样？",
        "人工智能和机器学习的区别是什么？"
    ]
    
    print("\n测试问答效果：")
    for i, question in enumerate(test_questions, 1):
        print(f"\n问题 {i}: {question}")
        answer = qa_system.ask(question)
        print(f"回答: {answer}")

if __name__ == "__main__":
    test_rag_system()