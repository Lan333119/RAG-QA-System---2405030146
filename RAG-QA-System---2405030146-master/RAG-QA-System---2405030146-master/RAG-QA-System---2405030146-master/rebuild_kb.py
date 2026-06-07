from rag_qa import RAGQASystem

# 使用新的数据库目录
qa = RAGQASystem()
qa.kb.persist_directory = "./chroma_db_new"

# 从docs目录构建知识库
qa.build_knowledge_base_from_docs("./docs")

# 检查构建结果
stats = qa.get_knowledge_base_stats()
print(f"知识库构建完成！文本块数量: {stats}")

# 测试检索
query = "什么是BERT?"
retriever = qa.kb.vector_db.as_retriever(search_kwargs={"k": 3})
results = retriever.invoke(query)
print(f"\n搜索 '{query}' 的结果:")
for i, doc in enumerate(results):
    print(f"\n结果{i+1}:")
    print(f"来源: {doc.metadata['source']}")
    print(f"内容预览: {doc.page_content[:100]}...")
