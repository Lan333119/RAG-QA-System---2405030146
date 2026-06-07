import streamlit as st
import os
from rag_qa import RAGQASystem
from knowledge_base import DocumentLoader

def main():
    st.set_page_config(
        page_title="RAG智能问答系统",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 RAG智能问答系统")
    
    if "qa_system" not in st.session_state:
        st.session_state.qa_system = RAGQASystem()
        st.session_state.chat_history = []
    
    qa_system = st.session_state.qa_system
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📁 知识库管理")
        
        uploaded_files = st.file_uploader(
            "上传文档（支持PDF、DOCX、TXT）",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True
        )
        
        if st.button("🔄 构建/更新知识库"):
            if uploaded_files:
                st.write("📝 正在加载文档...")
                documents = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for idx, uploaded_file in enumerate(uploaded_files):
                    status_text.text(f"加载文档 {idx+1}/{len(uploaded_files)}: {uploaded_file.name}")
                    
                    temp_path = f"./temp_{uploaded_file.name}"
                    try:
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        text = DocumentLoader.load_document(temp_path)
                        documents.append((uploaded_file.name, text))
                        status_text.text(f"✅ 成功加载: {uploaded_file.name} (长度: {len(text)} 字符)")
                        
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                    except Exception as e:
                        st.error(f"加载文件 {uploaded_file.name} 失败: {str(e)}")
                        import traceback
                        st.text(traceback.format_exc())
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                    
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                
                progress_bar.progress(1.0)
                
                if documents:
                    try:
                        status_text.text("正在向量化文档...")
                        qa_system.add_documents_to_kb(documents)
                        st.success(f"✅ 成功添加 {len(documents)} 个文档到知识库")
                        stats = qa_system.get_knowledge_base_stats()
                        st.info(f"📊 当前知识库文本块数量: {stats['chunk_count']}")
                    except Exception as e:
                        st.error(f"添加文档到知识库失败: {str(e)}")
                        import traceback
                        st.text(traceback.format_exc())
            else:
                st.warning("请先上传文档")
        
        stats = qa_system.get_knowledge_base_stats()
        st.info(f"📊 当前知识库文本块数量: {stats['chunk_count']}")
        
        if st.button("🗑️ 清空对话历史"):
            qa_system.clear_memory()
            st.session_state.chat_history = []
            st.success("对话历史已清空")
        
        if st.button("🗑️ 清空知识库"):
            try:
                qa_system.clear_knowledge_base()
                st.success("知识库已清空")
                stats = qa_system.get_knowledge_base_stats()
                st.info(f"📊 当前知识库文本块数量: {stats['chunk_count']}")
            except Exception as e:
                st.error(f"清空知识库失败: {str(e)}")
    
    with col2:
        st.subheader("💬 问答交互")
        
        # 先显示对话历史（在表单外面）
        for i, (question, answer) in enumerate(st.session_state.chat_history):
            with st.chat_message("user"):
                st.write(question)
            with st.chat_message("assistant"):
                st.write(answer)
        
        # 表单只负责输入和提交
        with st.form(key='question_form', clear_on_submit=True):
            question = st.text_input("请输入您的问题：", key='question_input')
            submit_button = st.form_submit_button("📤 提问")
            
            if submit_button and question.strip():
                with st.spinner("正在思考..."):
                    try:
                        # 先尝试显示检索到的相关文档（如果方法存在）
                        try:
                            if hasattr(qa_system, 'search_relevant_docs'):
                                st.write("📚 检索到的相关文档：")
                                relevant_docs = qa_system.search_relevant_docs(question)
                                
                                if relevant_docs:
                                    for i, (content, metadata, score) in enumerate(relevant_docs):
                                        with st.expander(f"文档 {i+1} (相似度: {score:.2f}, 来源: {metadata.get('source', '未知')}"):
                                            st.write(content)
                                else:
                                    st.warning("未找到相关文档")
                        except Exception as search_error:
                            st.info("跳过文档检索显示")
                        
                        # 获取回答并添加到历史
                        answer = qa_system.ask(question)
                        st.session_state.chat_history.append((question, answer))
                        
                        # 自动刷新页面以显示新对话
                        st.rerun()
                    except Exception as e:
                        st.error(f"问答失败: {str(e)}")
                        import traceback
                        st.text(traceback.format_exc())

if __name__ == "__main__":
    main()