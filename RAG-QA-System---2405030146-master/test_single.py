from rag_qa import RAGQASystem

qa = RAGQASystem()
qa.kb.persist_directory = "./chroma_db_new"
qa.kb.load_knowledge_base()

print("开始问答...")
answer = qa.ask("什么是BERT?")
print(f"回答: {answer}")
