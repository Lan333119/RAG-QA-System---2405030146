from knowledge_base import KnowledgeBase

kb = KnowledgeBase()
kb.load_knowledge_base()

query = 'Transformer模型'
results = kb.search(query, k=3)

print(f'搜索 "{query}" 的结果:')
for i, (content, metadata, score) in enumerate(results, 1):
    print(f'\n结果 {i}:')
    print(f'来源: {metadata["source"]}')
    print(f'相似度: {score:.4f}')
    print(f'内容预览: {content[:150]}...')
