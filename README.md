# RAG智能问答系统

基于本地知识库的RAG（检索增强生成）智能问答系统，支持离线运行，无需联网。

## 功能特点

- 📚 支持PDF、DOCX、TXT文档格式的上传和解析
- 🔍 使用Chroma向量数据库进行文档向量化存储和相似性检索
- 💬 支持多轮对话，具备会话记忆功能
- 🌐 基于Streamlit的Web可视化界面
- 📦 可打包成独立的exe可执行文件

## 技术栈

- **框架**: LangChain
- **大模型**: Ollama (Qwen2:7B)
- **嵌入模型**: Nomic-Embed-Text
- **向量数据库**: Chroma
- **Web界面**: Streamlit

## 环境要求

- Python 3.10+
- Ollama (已安装并下载模型)

## 安装步骤

### 1. 安装Ollama

从 [Ollama官网](https://ollama.com/) 下载并安装Ollama。

### 2. 下载模型

```bash
ollama pull qwen2:7b
ollama pull nomic-embed-text
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 使用说明

### 运行Web应用

```bash
streamlit run app.py
```

### 使用步骤

1. 在Web界面左侧上传文档（支持PDF、DOCX、TXT格式）
2. 点击"构建/更新知识库"按钮
3. 在右侧问答交互区输入问题并点击"提问"
4. 查看回答结果

### 命令行版本

```bash
python rag_qa.py
```

## RAG流程

1. **文档加载**: 读取PDF/DOCX/TXT文档内容
2. **文本分块**: 使用RecursiveCharacterTextSplitter进行分块（chunk_size=1000, chunk_overlap=200）
3. **向量化**: 使用Nomic-Embed-Text模型将文本块转换为向量
4. **存储**: 将向量存入Chroma向量数据库
5. **检索**: 根据用户问题进行相似性检索，返回最相关的3个文本块
6. **生成**: 将检索结果作为上下文，调用Qwen2模型生成回答

## 项目结构

```
RAG-QA-System/
├── app.py              # Streamlit Web应用
├── rag_qa.py           # RAG问答系统核心逻辑
├── knowledge_base.py   # 知识库管理模块
├── test_ollama.py      # Ollama测试脚本
├── test_rag.py         # RAG测试脚本
├── requirements.txt    # 依赖列表
├── .gitignore          # Git忽略配置
├── docs/               # 文档目录
└── chroma_db/          # Chroma向量数据库目录
```

## 注意事项

- 确保Ollama服务已启动（运行`ollama serve`）
- 首次运行会下载模型，需要一定时间
- 建议在配置较高的机器上运行（推荐16GB以上内存）

## 许可证

MIT License