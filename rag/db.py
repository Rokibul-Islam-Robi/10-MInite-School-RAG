import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from rag.embedding import embed_query
from pgvector.psycopg2 import register_vector

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432') # Ensure this port matches your Docker setup (e.g., '5433')
DB_NAME = os.getenv('DB_NAME', 'ragdb')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', '12345') # Ensure this password matches your Docker setup

def get_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    register_vector(conn)
    return conn

def create_tables():
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('CREATE EXTENSION IF NOT EXISTS vector;')
        conn.commit()
        cur.close()

        # CRITICAL FIX: Add DROP TABLE IF EXISTS to ensure clean recreation
        # And fix embedding vector size to 768 for models/embedding-001
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''
            DROP TABLE IF EXISTS chunks;
            CREATE TABLE IF NOT EXISTS chunks (
                id SERIAL PRIMARY KEY,
                chunk_id INT,
                text TEXT,
                embedding vector(768) -- CORRECTED: Gemini embedding size for models/embedding-001 is 768
            );
        ''')
        conn.commit()
        print("DEBUG: Tables created/verified successfully with vector(768).")
    except psycopg2.Error as e:
        print(f"ERROR: Database error during table creation: {e}")
        if conn:
            conn.rollback()
        raise e
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def insert_chunks(chunks_with_embeddings):
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        execute_values(
            cur,
            "INSERT INTO chunks (chunk_id, text, embedding) VALUES %s",
            chunks_with_embeddings
        )
        conn.commit()
        print(f"DEBUG: Inserted {len(chunks_with_embeddings)} chunks into DB.")
    except psycopg2.Error as e:
        print(f"ERROR: Database error during chunk insertion: {e}")
        if conn:
            conn.rollback()
        raise e
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def search_similar_chunks(query_text, top_k=4):
    try:
        # Unpack the tuple to get only the embedding vector from embed_query
        _, _, query_embedding_vector = embed_query(query_text)
    except Exception as e:
        print(f"ERROR: Failed to embed query in search_similar_chunks: {e}")
        raise

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT chunk_id, text, embedding <#> %s::vector AS distance
            FROM chunks
            ORDER BY embedding <#> %s::vector
            LIMIT %s;
            """,
            (query_embedding_vector, query_embedding_vector, top_k)
        )
        results = cur.fetchall()
        print(f"DEBUG: Found {len(results)} similar chunks for query.")
        return results
    except psycopg2.Error as e:
        print(f"ERROR: Database error during similarity search: {e}")
        if conn:
            conn.rollback()
        raise e
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()