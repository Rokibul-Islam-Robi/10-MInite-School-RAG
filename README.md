# 10 Minute School RAG

A Retrieval-Augmented Generation (RAG) pipeline for answering English and Bengali queries using the HSC26 Bangla 1st paper PDF as a knowledge base.

## Features

- Accepts queries in English and Bangla
- Retrieves relevant document chunks from a knowledge base
- Generates answers grounded in retrieved content
- Uses Gemini embeddings and LLM, and Postgres vector DB
- n8n workflow integration

## Setup

### Prerequisites

- Python 3.10+
- `pip` for package installation
- PostgreSQL database

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/10-minute-school-rag.git
   cd 10-minute-school-rag
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Create a `.env` file in the root directory.
   - Add your `GEMINI_API_KEY` to the `.env` file:
     ```
     GEMINI_API_KEY=your_api_key
     ```

4. **Configure PostgreSQL:**
   - Ensure your PostgreSQL database is running.
   - Update the database connection details in `rag/db.py` if necessary.

### Running the Application

1. **Preprocess the PDF:**
   ```bash
   python -m book.preprocess
   ```

2. **Embed and store the chunks:**
   ```bash
   python -m book.chunker
   ```

3. **Start the FastAPI server:**
   ```bash
   uvicorn rag.main:app --reload
   ```

## API Documentation

The application exposes a single API endpoint for asking questions.

### `POST /ask`

This endpoint accepts a JSON payload with a "query" field and returns a JSON response with the "answer".

**Request:**

```json
{
  "query": "Your question in English or Bengali"
}
```

**Response:**

```json
{
  "answer": "The generated answer based on the knowledge base."
}
```

**Example using `curl`:**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/ask' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?"
}'
```

## Tools and Libraries

- **Backend:** FastAPI
- **Database:** PostgreSQL with `pgvector` extension
- **PDF Processing:** `pdfplumber`
- **Language Detection:** `langdetect`
- **Embeddings and LLM:** Google Gemini
- **Workflow Automation:** n8n

## Project Structure

- `book/`: PDF processing and chunking scripts.
- `rag/`: RAG pipeline implementation.
- `n8n/`: n8n workflow for orchestrating the pipeline.
- `test_api.py`: Script for testing the API endpoint.
- `requirements.txt`: Python dependencies.
- `README.md`: This file.

## Sample Test Cases

- **User Question:** অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?
  **Expected Answer:** শুম্ভুনাথ
- **User Question:** কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?
  **Expected Answer:** মামাকে
- **User Question:** বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?
  **Expected Answer:** ১৫ বছর