from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 尝试加载现有数据库
vector_db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

print("集合列表:", vector_db._client.list_collections())

# 检查默认集合
try:
    collection = vector_db._client.get_collection("langchain")
    print(f"文档数量: {collection.count()}")
    
    # 获取一些文档
    docs = collection.get(limit=5)
    print(f"获取到的文档键: {list(docs.keys())}")
    if 'metadatas' in docs and docs['metadatas']:
        print(f"第一个文档的元数据: {docs['metadatas'][0]}")
    if 'documents' in docs and docs['documents']:
        print(f"第一个文档内容预览: {docs['documents'][0][:100]}...")
except Exception as e:
    print(f"Error: {e}")
