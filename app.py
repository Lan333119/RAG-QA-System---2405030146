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
                with st.spinner("正在处理文档..."):
                    documents = []
                    for uploaded_file in uploaded_files:
                        temp_path = f"./temp_{uploaded_file.name}"
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        try:
                            text = DocumentLoader.load_document(temp_path)
                            documents.append((uploaded_file.name, text))
                            os.remove(temp_path)
                        except Exception as e:
                            st.error(f"加载文件 {uploaded_file.name} 失败: {e}")
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
                    
                    if documents:
                        qa_system.add_documents_to_kb(documents)
                        st.success(f"成功添加 {len(documents)} 个文档到知识库")
            else:
                st.warning("请先上传文档")
        
        stats = qa_system.get_knowledge_base_stats()
        st.info(f"📊 当前知识库文本块数量: {stats['chunk_count']}")
        
        if st.button("🗑️ 清空对话历史"):
            qa_system.clear_memory()
            st.session_state.chat_history = []
            st.success("对话历史已清空")
    
    with col2:
        st.subheader("💬 问答交互")
        
        for i, (question, answer) in enumerate(st.session_state.chat_history):
            with st.chat_message("user"):
                st.write(question)
            with st.chat_message("assistant"):
                st.write(answer)
        
        question = st.text_input("请输入您的问题：")
        
        if st.button("📤 提问"):
            if question.strip():
                with st.spinner("正在思考..."):
                    answer = qa_system.ask(question)
                
                st.session_state.chat_history.append((question, answer))
                
                with st.chat_message("user"):
                    st.write(question)
                with st.chat_message("assistant"):
                    st.write(answer)

if __name__ == "__main__":
    main()