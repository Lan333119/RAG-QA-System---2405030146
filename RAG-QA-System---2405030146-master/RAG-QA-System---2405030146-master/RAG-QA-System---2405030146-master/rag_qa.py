import requests
import json
from langchain_core.prompts import PromptTemplate
from knowledge_base import KnowledgeBase, DocumentLoader
import os

class RAGQASystem:
    def __init__(self, model_name: str = "qwen2:1.5b"):
        self.model_name = model_name
        self.kb = KnowledgeBase()
        self.chat_history = []
        # 尝试自动加载已有的知识库
        try:
            loaded = self.kb.load_knowledge_base()
            if loaded:
                print("知识库加载成功")
            else:
                print("知识库未找到，将在添加文档时创建")
        except Exception as e:
            print(f"加载知识库时出错: {e}")
            import traceback
            traceback.print_exc()
        
        self.system_prompt = """
        你是一个基于知识库的智能问答助手。请仔细阅读提供的参考文档，并根据文档内容回答用户的问题。
        
        回答规则：
        1. 优先使用文档中的信息进行回答
        2. 如果文档中有相关信息，请直接引用或总结文档内容
        3. 如果文档中没有找到相关信息，回答"文档中未找到相关答案"
        4. 回答要简洁清晰，直接针对问题
        """
    
    def _call_ollama(self, prompt):
        url = "http://localhost:11434/api/generate"
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.1
        }
        
        try:
            response = requests.post(url, json=data, timeout=120)
            if response.status_code == 200:
                result = response.json()
                
                # 问答完成后卸载模型释放资源
                import subprocess
                subprocess.run(["ollama", "stop", self.model_name], capture_output=True, shell=True)
                
                return result.get("response", "")
            else:
                print(f"Ollama API错误: {response.status_code} - {response.text}")
                return f"Ollama API错误: {response.status_code} - {response.text}"
        except requests.exceptions.ConnectionError:
            print("无法连接到 Ollama 服务！")
            return "无法连接到 Ollama 服务！请确保 Ollama 正在运行。"
        except Exception as e:
            print(f"Ollama请求错误: {e}")
            import traceback
            traceback.print_exc()
            return f"Ollama请求错误: {str(e)}"

    def load_knowledge_base(self, persist_dir: str = "./chroma_db"):
        self.kb.persist_directory = persist_dir
        return self.kb.load_knowledge_base()

    def build_knowledge_base_from_docs(self, docs_folder: str = "./docs"):
        documents = DocumentLoader.load_documents_from_folder(docs_folder)
        if documents:
            self.kb.build_knowledge_base(documents)
            return True
        return False

    def add_documents_to_kb(self, documents: list):
        self.kb.add_documents(documents)

    def ask(self, question: str) -> str:
        try:
            if self.kb.vector_db is None:
                if not self.kb.load_knowledge_base():
                    return "知识库未初始化，请先构建知识库"
            
            print(f"\n===== 用户问题: {question} =====")
            
            retriever = self.kb.vector_db.as_retriever(search_kwargs={"k": 3})
            relevant_docs = retriever.invoke(question)
            
            print(f"找到 {len(relevant_docs)} 个相关文档块：")
            for i, doc in enumerate(relevant_docs):
                print(f"\n--- 文档 {i+1} ---")
                print(f"内容预览: {doc.page_content[:100]}...")
                print(f"元数据: {doc.metadata}")
            
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            print(f"\n合并后的上下文长度: {len(context)} 字符")
            
            history_str = "\n".join([f"用户: {msg['question']}\n助手: {msg['answer']}" for msg in self.chat_history])
            
            template = """你是一个基于知识库的智能问答助手。请仔细阅读提供的参考文档，并根据文档内容回答用户的问题。

如果文档中有相关信息，请直接引用或总结文档内容。
如果文档中没有找到相关信息，也请如实说明，不要编造。
请简洁明了地回答。

参考文档：
{context}

对话历史：
{chat_history}

用户问题：
{question}

请根据参考文档回答问题："""
            
            prompt = PromptTemplate(
                input_variables=["context", "chat_history", "question"],
                template=template
            )
            
            formatted_prompt = prompt.format(
                context=context,
                chat_history=history_str,
                question=question
            )
            
            print("\n正在调用LLM...")
            print(f"提示词长度: {len(formatted_prompt)} 字符")
            answer = self._call_ollama(formatted_prompt)
            print("LLM调用完成")
            print(f"原始回答: {answer}")
            
            self.chat_history.append({"question": question, "answer": answer})
            return answer
        except Exception as e:
            print(f"Error in QA: {e}")
            import traceback
            traceback.print_exc()
            return f"问答出错: {str(e)}"

    def get_knowledge_base_stats(self):
        return {
            "chunk_count": self.kb.get_chunk_count()
        }
    
    def search_relevant_docs(self, question: str):
        if self.kb.vector_db is None:
            return []
        
        results = self.kb.search(question, k=3)
        return results

    def clear_memory(self):
        self.chat_history = []
    
    def clear_knowledge_base(self):
        self.kb.clear_all()
        print("知识库已清空")

def main():
    print("初始化RAG问答系统...")
    qa_system = RAGQASystem()
    
    if not qa_system.load_knowledge_base():
        print("未找到已存在的知识库，尝试从docs文件夹构建...")
        if not qa_system.build_knowledge_base_from_docs():
            print("docs文件夹中没有文档，请先添加文档")
            return
    
    print("\nRAG问答系统已就绪！")
    print("输入'quit'退出，输入'clear'清空对话历史")
    
    while True:
        question = input("\n请输入问题：")
        
        if question.lower() == 'quit':
            break
        if question.lower() == 'clear':
            qa_system.clear_memory()
            print("对话历史已清空")
            continue
        
        print("正在思考...")
        answer = qa_system.ask(question)
        print(f"回答：{answer}")

if __name__ == "__main__":
    main()