import os

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 500

CLEANED_TEXT_PATH = os.path.join(os.path.dirname(__file__), 'cleaned_text.txt')
CHUNKS_PATH = os.path.join(os.path.dirname(__file__), 'chunks.txt')


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        if end == len(text):
            break
        start += chunk_size - overlap
    return chunks

if __name__ == "__main__":
    with open(CLEANED_TEXT_PATH, 'r', encoding='utf-8') as f:
        text = f.read()
    chunks = chunk_text(text)
    with open(CHUNKS_PATH, 'w', encoding='utf-8') as f:
        for i, chunk in enumerate(chunks):
            f.write(f"---chunk_{i}---\n{chunk}\n")
    print(f"Chunked text into {len(chunks)} chunks. Saved to chunks.txt.") 