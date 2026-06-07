import os
from typing import List, Optional
from PyPDF2 import PdfReader
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

class DocumentLoader:
    @staticmethod
    def load_pdf(file_path: str) -> str:
        text = ""
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text

    @staticmethod
    def load_docx(file_path: str) -> str:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    @staticmethod
    def load_txt(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    @staticmethod
    def load_document(file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return DocumentLoader.load_pdf(file_path)
        elif ext == ".docx":
            return DocumentLoader.load_docx(file_path)
        elif ext == ".txt":
            return DocumentLoader.load_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    @staticmethod
    def load_documents_from_folder(folder_path: str) -> List[tuple]:
        documents = []
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                ext = os.path.splitext(filename)[1].lower()
                if ext in [".pdf", ".docx", ".txt"]:
                    try:
                        text = DocumentLoader.load_document(file_path)
                        documents.append((filename, text))
                        print(f"Loaded {filename}")
                    except Exception as e:
                        print(f"Failed to load {filename}: {e}")
        return documents

class KnowledgeBase:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        self.vector_db = None

    def build_knowledge_base(self, documents: List[tuple]):
        try:
            print(f"开始构建知识库，共 {len(documents)} 个文档")
            
            all_chunks = []
            all_metadata = []
            
            for idx, (filename, text) in enumerate(documents):
                print(f"处理文档 {idx+1}/{len(documents)}: {filename}")
                chunks = self.text_splitter.split_text(text)
                print(f"  切分为 {len(chunks)} 个文本块")
                
                for i, chunk in enumerate(chunks):
                    all_chunks.append(chunk)
                    all_metadata.append({
                        "source": filename,
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    })
            
            print(f"正在向量化 {len(all_chunks)} 个文本块...")
            self.vector_db = Chroma.from_texts(
                texts=all_chunks,
                embedding=self.embeddings,
                metadatas=all_metadata,
                persist_directory=self.persist_directory
            )
            print(f"知识库构建成功: {len(all_chunks)} 个文本块")
        except Exception as e:
            print(f"构建知识库时出错: {e}")
            import traceback
            traceback.print_exc()
            raise

    def load_knowledge_base(self):
        if os.path.exists(self.persist_directory):
            try:
                self.vector_db = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
                print("知识库加载成功")
                return True
            except Exception as e:
                print(f"加载知识库时出错: {e}")
                import traceback
                traceback.print_exc()
                return False
        return False

    def search(self, query: str, k: int = 3) -> List[tuple]:
        if self.vector_db is None:
            raise ValueError("Knowledge base not loaded or built")
        
        results = self.vector_db.similarity_search_with_score(query, k=k)
        return [(doc.page_content, doc.metadata, score) for doc, score in results]

    def get_chunk_count(self) -> int:
        if self.vector_db is None:
            return 0
        return self.vector_db._collection.count()

    def add_documents(self, documents: List[tuple]):
        if self.vector_db is None:
            self.build_knowledge_base(documents)
            return
        
        print(f"开始添加 {len(documents)} 个文档到现有知识库")
        try:
            total_chunks = 0
            
            for idx, (filename, text) in enumerate(documents):
                print(f"处理文档 {idx+1}/{len(documents)}: {filename}")
                chunks = self.text_splitter.split_text(text)
                print(f"  切分为 {len(chunks)} 个文本块")
                
                metadatas = [{
                    "source": filename,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                } for i in range(len(chunks))]
                
                self.vector_db.add_texts(texts=chunks, metadatas=metadatas)
                total_chunks += len(chunks)
            
            print(f"成功添加 {len(documents)} 个文档，共 {total_chunks} 个文本块")
        except Exception as e:
            print(f"添加文档时出错: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def clear_all(self):
        if self.vector_db is not None:
            try:
                if os.path.exists(self.persist_directory):
                    import shutil
                    shutil.rmtree(self.persist_directory)
                    print(f"已删除知识库目录: {self.persist_directory}")
                self.vector_db = None
                print("知识库已清空")
            except Exception as e:
                print(f"清空知识库时出错: {e}")
                import traceback
                traceback.print_exc()

def main():
    kb = KnowledgeBase()
    
    if not kb.load_knowledge_base():
        docs_folder = "./docs"
        documents = DocumentLoader.load_documents_from_folder(docs_folder)
        
        if documents:
            kb.build_knowledge_base(documents)
        else:
            print("No documents found in docs folder")
            return
    
    query = "自然语言处理中的Transformer模型是什么？"
    results = kb.search(query)
    
    print(f"\n搜索结果 ({len(results)}):")
    for i, (content, metadata, score) in enumerate(results, 1):
        print(f"\n结果 {i}:")
        print(f"来源: {metadata['source']}")
        print(f"相似度: {score:.4f}")
        print(f"内容预览: {content[:200]}...")

if __name__ == "__main__":
    main()