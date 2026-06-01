# AI使用日志

## 项目信息
- 项目名称：RAG智能问答系统
- 使用工具：Trae AI 编程助手
- 开发时间：2026年6月

## AI使用记录

### 1. 代码框架生成
- **提问**：如何使用LangChain和Ollama构建RAG问答系统？
- **回答**：AI提供了完整的RAG系统架构设计，包括文档加载、文本分块、向量化存储、相似性检索和问答链集成的代码骨架
- **使用位置**：`rag_qa.py`, `knowledge_base.py`

### 2. Streamlit界面开发
- **提问**：如何使用Streamlit构建RAG问答系统的Web界面？
- **回答**：AI提供了Streamlit应用的代码框架，包括文档上传、知识库构建、问答交互和对话历史展示功能
- **使用位置**：`app.py`

### 3. 文档加载器实现
- **提问**：如何实现支持PDF、DOCX、TXT格式的文档加载器？
- **回答**：AI提供了使用PyPDF2和python-docx库读取不同格式文档的代码
- **使用位置**：`knowledge_base.py`中的`DocumentLoader`类

### 4. 向量数据库集成
- **提问**：如何使用Chroma向量数据库存储和检索文本向量？
- **回答**：AI提供了Chroma数据库的初始化、文档添加、相似性检索等功能的实现
- **使用位置**：`knowledge_base.py`中的`KnowledgeBase`类

### 5. 系统提示词设计
- **提问**：如何设计RAG系统的系统提示词，确保模型基于文档回答？
- **回答**：AI提供了包含严格规则的系统提示词，要求模型在文档中找不到答案时明确拒绝回答
- **使用位置**：`rag_qa.py`中的`system_prompt`

### 6. 会话记忆实现
- **提问**：如何在Streamlit应用中实现会话记忆功能？
- **回答**：AI提供了使用`st.session_state`存储对话历史的实现方案
- **使用位置**：`app.py`, `rag_qa.py`

### 7. 打包脚本生成
- **提问**：如何使用pyinstaller将Streamlit应用打包成exe文件？
- **回答**：AI提供了打包脚本和配置说明
- **使用位置**：`run_app.py`, `build_exe.bat`

## 代码修改说明

### AI生成代码（标记为AI-GEN）
1. `knowledge_base.py`第1-55行：文档加载器相关代码
2. `knowledge_base.py`第57-128行：知识库管理相关代码
3. `rag_qa.py`第1-96行：RAG问答系统核心逻辑
4. `app.py`第1-88行：Streamlit Web应用界面

### 人工修改代码
1. `rag_qa.py`第13-23行：系统提示词优化，增强拒绝回答逻辑
2. `app.py`第56-57行：添加知识库状态显示
3. `requirements.txt`：更新依赖版本以确保兼容性

## 学习收获

通过AI辅助开发，学习到了：
1. LangChain框架的核心组件和使用方法
2. RAG技术的完整流程实现
3. Ollama本地大模型的集成方式
4. Streamlit Web应用开发技巧
5. 向量数据库Chroma的使用方法