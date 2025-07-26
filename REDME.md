# RAG System for Bengali PDF Documents

## Project Overview

This project implements a Retrieval-Augmented Generation (RAG) system designed to answer questions based on content extracted from Bengali PDF documents. It leverages Google's Gemini models for text embedding and answer generation, with PostgreSQL and `pgvector` for efficient vector storage and similarity search.

The system processes a PDF document, chunks its content, embeds these chunks, stores them in a vector database, and then, for a given user query, retrieves relevant chunks, and uses a Large Language Model (LLM) to generate a concise answer based on the retrieved context.

## Features

- **PDF Text Extraction:** Extracts and cleans text from PDF documents.
- **Text Chunking:** Divides the document into manageable, overlapping text chunks.
- **Gemini Embeddings:** Generates high-quality vector embeddings for text chunks and queries using Google's `models/embedding-001`.
- **Vector Database:** Stores text chunks and their embeddings in PostgreSQL with the `pgvector` extension for efficient similarity search.
- **Semantic Search:** Retrieves semantically similar document chunks to a user's query.
- **Gemini Generation:** Utilizes Google's `gemini-1.5-flash-latest` model to generate precise answers based on retrieved context.
- **FastAPI Backend:** Provides a simple REST API endpoint for asking questions.
- **Command-Line Client:** A basic client for interacting with the RAG system.

## Setup Guide

Follow these steps to set up and run the RAG system.

### Prerequisites

- **Python 3.8+**
- **pip** (Python package installer)
- **Docker** (for running PostgreSQL with `pgvector`)
- **Git** (for cloning the repository)
- **Google Gemini API Key**: Obtain one from [Google AI Studio](https://ai.google.dev/).

### 1. Clone the Repository

```bash
git clone <your_github_repo_url>
cd <your_project_directory> # e.g., cd RAG_System
```

---

**Setup Guide (Environment Variables)**

````markdown
### 2. Environment Variables Setup

Create a `.env` file in the root directory of your project (e.g., `H:\10 MiniteSchool RAG\.env`) with the following content. **Replace placeholders with your actual values.**

```dotenv
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
DB_HOST=localhost
DB_PORT=5433 # Or your desired PostgreSQL port
DB_NAME=ragdb
DB_USER=postgres
DB_PASS=12345 # Your PostgreSQL password
```
````

---

**Setup Guide (Install Dependencies)**

````markdown
### 3. Install Python Dependencies

It's recommended to use a virtual environment.

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```
````

---

**Setup Guide (PostgreSQL with Docker)**

````markdown
### 4. PostgreSQL Database Setup with Docker

This project uses PostgreSQL with the `pgvector` extension. The easiest way to set this up is using Docker.

Create a `docker-compose.yml` file (or use a `docker run` command) in your project root. If you don't have one, here's a basic `docker-compose.yml`:

```yaml
# docker-compose.yml
version: "3.8"
services:
  db:
    image: ankane/pgvector:latest
    restart: always
    environment:
      POSTGRES_DB: ragdb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 12345 # Make sure this matches DB_PASS in your .env file
    ports:
      - "5433:5432" # Map container port 5432 to host port 5433
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```
````

---

**Setup Guide (Run Data Pipeline & Start FastAPI)**

````markdown
### 5. Run the Data Pipeline

This step extracts text from the PDF, chunks it, embeds the chunks, and stores them in your PostgreSQL database.

```bash
python -m rag.pipeline
```
````

---

**Setup Guide (Interact with System)**

````markdown
### 7. Interact with the System

You can use the provided `ask.py` script to send queries to your RAG system.

```bash
python -m rag.ask "আপনার প্রজেক্টের প্রধান বিষয়বস্তু কী?"
# Or in English:
python -m rag.ask "What is the main subject of your project?"
```
````

---

**Used Tools, Libraries, and Packages**

```markdown
## Used Tools, Libraries, and Packages

The core components and libraries used in this project include:

- **Python 3.8+**
- **FastAPI:** For building the web API.
- **uvicorn:** ASGI server for FastAPI.
- **pdfplumber:** For robust PDF text extraction.
- **google-generativeai:** Official Google AI client library for interacting with Gemini models.
- **psycopg2-binary:** PostgreSQL adapter for Python.
- **pgvector:** PostgreSQL extension for vector similarity search.
- **python-dotenv:** For managing environment variables.
- **requests:** For making HTTP requests (used by `ask.py` and potentially direct API calls in older `generator.py` or `embedding.py` versions).
- **re (Standard Library):** For regular expression-based text cleaning.

(Note: `nltk`, `openai`, `pandas`, `scikit-learn`, `langdetect` are in `requirements.txt` but do not appear to be actively used in the provided core logic files like `preprocess.py`, `embedding.py`, `generator.py`, `db.py`, `retriever.py`, `chunker.py`. They might be remnants or for future extensions.)
```

## Sample Queries and Outputs

Here are some sample queries (in Bengali and English) and typical outputs you might expect. The exact answer will depend on the content of your `hsc26_bangla_1st_paper.pdf`.

**Example Questions (from `test_api.py`):**

| Question (Bengali)                                | Question (English Translation)                           | Expected Answer (from `test_api.py`) |
| :------------------------------------------------ | :------------------------------------------------------- | :----------------------------------- |
| `অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?`         | `In Anupam's language, who is called a handsome man?`    | `শুম্ভুনাথ` (Shumbhunath)            |
| `কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?` | `Who has been referred to as Anupam's deity of fortune?` | `মামাকে` (Uncle)                     |
| `বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?`        | `What was Kalyani's actual age at the time of marriage?` | `১৫ বছর` (15 years)                  |

**Example Output Format (when running `python -m rag.ask "your question"`):**

## API Documentation

The RAG system exposes a single API endpoint for answering questions.

### `/ask` (POST)

- **URL:** `http://127.0.0.1:8000/ask`
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Request Body:**
  ```json
  {
    "user": "string", // A unique identifier for the user (e.g., "cli_user")
    "query": "string" // The question you want to ask (e.g., "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?")
  }
  ```
- **Response Body (200 OK):**
  ```json
  {
    "answer": "string", // The generated answer to the question
    "retrieved_chunks": ["string"], // A list of relevant text chunks retrieved from the DB
    "chat_history": [] // Placeholder for future chat history implementation
  }
  ```
- **Error Responses:**
  - `400 Bad Request`: If the request payload is malformed.
  - `500 Internal Server Error`: If an error occurs during processing (e.g., API key issues, database errors, embedding failures).

## Evaluation Matrix (Not Explicitly Implemented)

An explicit evaluation matrix is not implemented as part of the current project code. However, for a production-ready RAG system, key metrics would include:

- **Relevance (Retrieval):** How accurately do the retrieved chunks relate to the query? (Can be measured manually or with metrics like Precision@K, Recall@K).
- **Faithfulness (Generation):** Does the generated answer strictly adhere to the information in the retrieved chunks, or does it hallucinate? (Manual review, or automated metrics comparing generated answer to source chunks).
- **Answer Correctness (Generation):** Is the generated answer factually correct based on the source document? (Requires ground truth answers for evaluation).
- **Conciseness/Fluency:** Is the answer easy to read and to the point?

Future improvements could involve integrating a quantitative evaluation framework.

## Answers to Specific Questions

### 1. What method or library did you use to extract the text, and why? Did you face any formatting challenges with the PDF content?

- **Method/Library:** We used `pdfplumber` to extract text from the PDF document (`hsc26_bangla_1st_paper.pdf`).
- **Why:** `pdfplumber` was chosen for its robustness in extracting text, including handling tables and layout (though table extraction wasn't explicitly utilized here, its capability provides a strong foundation). It's generally more reliable than simpler PDF parsers for complex layouts and supports precise text extraction from specific areas if needed.
- **Formatting Challenges:** Yes, typical challenges associated with PDF text extraction were faced:
  - **Extra Whitespace/Newlines:** PDFs often introduce excessive whitespace or incorrect line breaks. This was addressed using `re.sub(r'\s+', ' ', text)` to consolidate multiple spaces and newlines into single spaces.
  - **Non-Textual Artifacts:** PDFs can contain headers, footers, page numbers, and other non-content elements. While aggressive filtering was temporarily relaxed during development for debugging, the `clean_text` function (`re.sub(r'[^\\u0980-\\u09FFA-Za-z0-9.,?!;:()\\-\\'\\\" ]', '', text)`) is designed to remove characters outside a specified Unicode range (Bengali, English, numbers, common punctuation) to filter out unwanted symbols or control characters.
  - **Encoding Issues:** Ensuring correct UTF-8 handling for Bengali characters was crucial, which `pdfplumber` generally manages well, but subsequent cleaning steps must preserve it.

### 2. What chunking strategy did you choose (e.g., paragraph-based, sentence-based, character limit)? Why do you think it works well for semantic retrieval?

- **Chunking Strategy:** A fixed **character-limit based chunking** with overlap was chosen, specifically:
  - `CHUNK_SIZE = 1000` characters
  - `CHUNK_OVERLAP = 500` characters
- **Why it works well for semantic retrieval:**
  - **Consistent Size:** Ensures that each chunk is within a manageable length for the embedding model, which often has input token limits.
  - **Context Preservation (Overlap):** The overlap helps maintain context across chunk boundaries. If a key piece of information spans two chunks, the overlap ensures that both parts (or at least enough context) are present in one complete chunk, or in two overlapping chunks that can still be retrieved together due to high similarity. This is crucial because embedding models perform better on complete semantic units.
  - **Simplicity and Efficiency:** It's a straightforward and computationally inexpensive strategy to implement, making the pipeline efficient for initial setup and processing large documents.
  - **Semantic Units:** While not strictly paragraph or sentence-based, for longer texts, a character-limited chunk with sufficient overlap tends to capture relevant semantic units that are effective for vector search. Embeddings are designed to capture the meaning of a given piece of text, and a moderately sized, overlapping chunk often provides enough context for the embedding model to generate a meaningful representation.

### 3. What embedding model did you use? Why did you choose it? How does it capture the meaning of the text?

- **Embedding Model:** We used `models/embedding-001` from Google's Gemini family of models.
- **Why Chosen:**
  - **Official Google Embedding Model:** It's the recommended embedding model by Google for various applications, including retrieval tasks.
  - **Performance:** `embedding-001` is known for its strong performance in semantic similarity tasks, meaning it effectively maps text to a vector space where similar meanings are close together.
  - **Ease of Integration:** Seamless integration with the `google-generativeai` client library, making API calls straightforward.
  - **Multilingual Capability:** While not explicitly tested for mixed languages, Gemini models are generally robust across multiple languages, including Bengali, which is critical for this project.
- **How it Captures Meaning:**
  - The model converts a piece of text (a word, sentence, or chunk) into a high-dimensional numerical vector (768 dimensions for `embedding-001`).
  - This conversion is learned from vast amounts of text data, allowing the model to understand the semantic relationships between words and phrases.
  - Texts with similar meanings or contexts will have their corresponding embedding vectors located closer to each other in this high-dimensional space.
  - When a query is embedded, its vector is then compared to the vectors of document chunks. The closer the vectors, the more semantically similar the texts are deemed to be, effectively capturing their meaning.

### 4. How are you comparing the query with your stored chunks? Why did you choose this similarity method and storage setup?

- **Similarity Method:** We are comparing the query embedding with stored chunk embeddings using **cosine similarity**, implemented in PostgreSQL via the `pgvector` extension's "negative inner product" operator (`<#>`).
  - For normalized vectors (which embeddings usually are, or can be treated as such for similarity), negative inner product (`-A . B`) is equivalent to `1 - cosine_similarity(A, B)`. Minimizing negative inner product maximizes cosine similarity, meaning smaller distances indicate greater similarity.
- **Storage Setup:** We are storing the embeddings in a **PostgreSQL database** with the **`pgvector` extension**.
- **Why Chosen:**
  - **`pgvector` for Vector Storage:** `pgvector` is an excellent choice because it turns PostgreSQL into a capable vector database. It allows us to store high-dimensional vectors directly alongside our text chunks within a familiar relational database environment. This simplifies infrastructure, as we don't need a separate dedicated vector database.
  - **Efficient Similarity Search:** `pgvector` provides optimized indexing (e.g., HNSW, IVFFlat) for fast approximate nearest neighbor (ANN) search, making vector comparisons efficient even with a large number of chunks.
  - **Cosine Similarity for Semantic Meaning:** Cosine similarity is the standard metric for comparing text embeddings. It measures the cosine of the angle between two vectors and is highly effective at determining semantic closeness regardless of vector magnitude. This aligns perfectly with how embedding models capture meaning (vectors pointing in similar directions have similar meanings).
  - **Scalability & Reliability:** PostgreSQL is a mature, reliable, and scalable database, offering robust data management capabilities that are beneficial for RAG systems.

### 5. How do you ensure that the question and the document chunks are compared meaningfully? What would happen if the query is vague or missing context?

- **Ensuring Meaningful Comparison:**

  - **Semantic Embeddings:** The core mechanism is the use of `models/embedding-001`. This model maps both the query and the document chunks into the same high-dimensional vector space. The design of these embeddings ensures that texts with similar meanings are represented by vectors that are numerically close to each other.
  - **`task_type` Parameter:** When generating embeddings, we explicitly use `task_type="retrieval_query"` for the user's question and `task_type="retrieval_document"` for the document chunks. This instructs the embedding model to optimize the embeddings specifically for a retrieval task, where a query needs to find relevant documents. This ensures that the embeddings are generated in a way that makes them highly comparable for relevance.
  - **Cosine Similarity:** The use of cosine similarity in `pgvector` is well-suited for comparing these embeddings, as it focuses on the direction of the vectors, effectively capturing semantic alignment.
  - **Consistent Preprocessing:** Both query and document chunks undergo similar preprocessing steps (e.g., cleaning, though query cleaning is often implicit if it's just raw text) to ensure consistency before embedding.

- **What happens if the query is vague or missing context?**
  - **Retrieval of "Most Similar" but Potentially Irrelevant Chunks:** If the query is vague or the necessary context/answer is genuinely not present in the document, the embedding model will still try to find the "most similar" chunks available in the database. However, these "most similar" chunks might still be semantically distant from the query or not contain the specific answer.
  - **LLM's Role in Handling Irrelevance (Critical Guardrail):** This is where the prompt engineering for the generation model (`generator.py`) becomes crucial. The LLM is explicitly instructed:
    ```
    If the answer to the question cannot be found within the provided context,
    you MUST respond with "I cannot find the answer to your question in the provided context."
    Do NOT make up information.
    ```
    This instruction acts as a vital guardrail. If the retrieved chunks (even the "most similar" ones for a vague query) do not contain the answer, the LLM is designed to admit it rather than hallucinating. This prevents the system from providing incorrect or misleading information. The system aims for "faithfulness" to the provided context.

### 6. Do the results seem relevant? If not, what might improve them (e.g., better chunking, better embedding model, larger document)?

- **Relevance of Results:** Assuming the pipeline is set up correctly and the PDF content is relevant to the questions, the results should generally seem relevant due to the use of strong semantic embedding models and similarity search. The `test_api.py` includes expected answers, suggesting that for those specific questions, the system should ideally retrieve relevant chunks and generate correct answers.

- **Potential Improvements if Results are Not Relevant:**

  - **Better Chunking Strategy:**

    - **Semantic Chunking:** Instead of fixed character limits, analyze the document for natural breaks (e.g., paragraphs, sections, topics). Libraries like NLTK or SpaCy can help identify sentence or paragraph boundaries, leading to more semantically coherent chunks.
    - **Adaptive Chunking:** Vary chunk size based on content density or type (e.g., smaller for definitions, larger for descriptive passages).
    - **Recursive Chunking:** Break down documents into larger chunks, then further break those down if they are too large, ensuring context at multiple granularities.
    - **Overlap Optimization:** Experiment with different overlap sizes to ensure sufficient context transfer between chunks.

  - **Better Embedding Model:**

    - **Larger/More Specialized Embedding Models:** While `embedding-001` is good, for highly specialized domains or more nuanced semantics, a larger or domain-specific embedding model might yield better results.
    - **Fine-tuning Embeddings:** If you have a large dataset of query-document pairs, fine-tuning the embedding model on your specific domain data can significantly improve retrieval relevance.

  - **Larger/More Diverse Document Corpus:**

    - The quality of the RAG system is highly dependent on the quality and comprehensiveness of the source documents. If the answer isn't in the PDF, no RAG system can find it.
    - Adding more relevant documents or ensuring the existing document covers a broader range of topics pertinent to potential queries.

  - **Hybrid Retrieval:**

    - Combine vector similarity search (semantic) with traditional keyword-based search (e.g., BM25, TF-IDF). This can capture both exact keyword matches and semantic meaning, improving recall, especially for queries with specific terms.

  - **Re-ranking Retrieved Chunks:**

    - After initial retrieval, use a more sophisticated model (e.g., a cross-encoder or a larger reranker model) to re-score the top-k retrieved chunks. This helps prioritize truly relevant chunks over those that are only loosely similar.

  - **More Sophisticated Prompt Engineering:**

    - Experiment with different system prompts, few-shot examples, or chain-of-thought prompting for the generation model to guide it towards more accurate and relevant answers.
    - Consider adding instructions for summarization or synthesis if answers need to be derived from multiple chunks.

  - **Error Analysis and Iteration:**
    - Implement a feedback loop to analyze cases where the system provides irrelevant or incorrect answers. This analysis can inform adjustments to chunking, retrieval, or generation components.
