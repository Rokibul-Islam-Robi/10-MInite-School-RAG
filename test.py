import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
    dbname=os.getenv("DB_NAME", "ragdb"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASS", "123456789")
)

cur = conn.cursor()
cur.execute("SELECT version();")
print("Connected to:", cur.fetchone())

cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
print("pgvector extension is available!")

cur.close()
conn.close()
