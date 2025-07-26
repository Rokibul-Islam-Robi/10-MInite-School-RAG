# Pipeline uses Gemini embeddings
import os
import sys
sys.path.append(os.path.dirname(__file__))
from book import preprocess, chunker
from rag import embedding, db

BOOK_DIR = os.path.join(os.path.dirname(__file__), '../book')

# Step 1: Preprocess PDF
print('Extracting and cleaning text from PDF...')
preprocess.extract_text_from_pdf()

# Step 2: Chunk text
print('Chunking text...')
with open(os.path.join(BOOK_DIR, 'cleaned_text.txt'), 'r', encoding='utf-8') as f:
    text = f.read()
chunks = chunker.chunk_text(text)
print(f"DEBUG: Number of chunks created: {len(chunks)}") # DEBUG PRINT

# Step 3: Embed chunks
print('Embedding chunks...')
embedded = embedding.embed_chunks(chunks)
print(f"DEBUG: Number of embedded chunks: {len(embedded)}") # DEBUG PRINT
if embedded:
    print(f"DEBUG: First embedded chunk (id, text_start, embedding_length): {embedded[0][0]}, {embedded[0][1][:50]}..., len={len(embedded[0][2])}") # DEBUG PRINT

# Step 4: Store in DB
print('Creating DB tables (if needed)...')
db.create_tables()
print('Inserting chunks into DB...')
db.insert_chunks(embedded)
print('DEBUG: insert_chunks call completed.') # DEBUG PRINT

print('Pipeline complete!')

# rag/pipeline.py

class RAGPipeline:
    def __init__(self):
        from rag import db
        self.db = db

    def ask(self, query):
        # load vector store and perform similarity search
        return self.db.search_similar_chunks(query)