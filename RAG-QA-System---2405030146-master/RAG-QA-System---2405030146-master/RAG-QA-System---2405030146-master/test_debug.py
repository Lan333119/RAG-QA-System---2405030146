from rag_qa import RAGQASystem
import traceback

try:
    qa = RAGQASystem()
    qa.kb.persist_directory = "./chroma_db_new"
    qa.kb.load_knowledge_base()
    
    print("知识库加载完成")
    
    # 测试检索
    retriever = qa.kb.vector_db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke("BERT")
    print(f"检索到 {len(docs)} 个文档")
    
    # 测试问答
    print("开始调用问答...")
    answer = qa.ask("什么是BERT?")
    print(f"回答长度: {len(answer)}")
    print(f"回答内容: {answer}")
    
except Exception as e:
    print(f"错误: {e}")
    traceback.print_exc()
