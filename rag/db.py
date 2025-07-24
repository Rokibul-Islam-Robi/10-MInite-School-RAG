import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'ragdb')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'password')


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def create_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE EXTENSION IF NOT EXISTS vector;
        CREATE TABLE IF NOT EXISTS chunks (
            id SERIAL PRIMARY KEY,
            chunk_id INT,
            text TEXT,
            embedding vector(1536) -- Gemini embedding size
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

def insert_chunks(chunks_with_embeddings):
    conn = get_connection()
    cur = conn.cursor()
    execute_values(
        cur,
        "INSERT INTO chunks (chunk_id, text, embedding) VALUES %s",
        chunks_with_embeddings
    )
    conn.commit()
    cur.close()
    conn.close()

def search_similar_chunks(query_embedding, top_k=4):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT chunk_id, text, embedding <#> %s AS distance
        FROM chunks
        ORDER BY embedding <#> %s
        LIMIT %s;
        """,
        (query_embedding, query_embedding, top_k)
    )
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

if __name__ == "__main__":
    create_tables()
    print("Database and table ready.") 