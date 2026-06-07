from rag_qa import RAGQASystem
import traceback

try:
    qa = RAGQASystem()
    qa.kb.persist_directory = "./chroma_db_new"
    qa.kb.load_knowledge_base()
    
    print("步骤1: 检查知识库状态")
    stats = qa.get_knowledge_base_stats()
    print(f"知识库状态: {stats}")
    
    question = "什么是BERT?"
    
    print("\n步骤2: 检索相关文档")
    retriever = qa.kb.vector_db.as_retriever(search_kwargs={"k": 3})
    relevant_docs = retriever.invoke(question)
    print(f"检索到 {len(relevant_docs)} 个文档")
    
    print("\n步骤3: 构建上下文")
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    print(f"上下文长度: {len(context)}")
    
    print("\n步骤4: 构建完整提示词")
    history_str = "\n".join([f"用户: {msg['question']}\n助手: {msg['answer']}" for msg in qa.chat_history])
    
    template = qa.system_prompt + """

    参考文档：
    {context}

    对话历史：
    {chat_history}

    用户问题：
    {question}

    请根据参考文档回答问题：
    """
    
    from langchain_core.prompts import PromptTemplate
    prompt = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template=template
    )
    
    formatted_prompt = prompt.format(
        context=context,
        chat_history=history_str,
        question=question
    )
    
    print(f"提示词长度: {len(formatted_prompt)}")
    print(f"提示词预览(前200字符): {formatted_prompt[:200]}...")
    
    print("\n步骤5: 调用Ollama API")
    answer = qa._call_ollama(formatted_prompt)
    print(f"回答长度: {len(answer)}")
    print(f"回答: {answer}")
    
except Exception as e:
    print(f"错误: {e}")
    traceback.print_exc()
