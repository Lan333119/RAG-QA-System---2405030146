from rag_qa import RAGQASystem
from langchain_ollama import ChatOllama

print("测试1: 直接测试LLM连接")
llm = ChatOllama(model="qwen2:1.5b", temperature=0.1)
try:
    response = llm.invoke("Hello, how are you?")
    print(f"LLM响应: {response.content[:50]}...")
    print(f"响应长度: {len(response.content)}")
except Exception as e:
    print(f"LLM错误: {e}")

print("\n测试2: 测试RAG问答")
qa = RAGQASystem()
stats = qa.get_knowledge_base_stats()
print(f"知识库状态: {stats}")

# 测试简单问题
print("\n测试问题: 什么是BERT?")
try:
    # 先测试检索
    retriever = qa.kb.vector_db.as_retriever(search_kwargs={"k": 3})
    relevant_docs = retriever.invoke("BERT")
    print(f"找到的相关文档数量: {len(relevant_docs)}")
    for i, doc in enumerate(relevant_docs):
        print(f"\n文档{i+1}来源: {doc.metadata['source']}")
        print(f"文档{i+1}内容预览: {doc.page_content[:100]}...")
    
    # 测试问答
    answer = qa.ask("什么是BERT?")
    print(f"\n最终回答: {answer}")
except Exception as e:
    print(f"问答错误: {e}")
