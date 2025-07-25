<<<<<<< HEAD
<<<<<<< HEAD
# 10 MiniteSchool RAG

A Retrieval-Augmented Generation (RAG) pipeline for answering English and Bengali queries using the HSC26 Bangla 1st paper PDF as a knowledge base.

## Features
- Accepts queries in English and Bangla
- Retrieves relevant document chunks from a knowledge base
- Generates answers grounded in retrieved content
- Uses Gemini embeddings and LLM, and Postgres vector DB
- n8n workflow integration

## Project Structure
- `book/`: PDF processing and chunking
- `rag/`: RAG pipeline code
- `n8n/`: n8n workflow

## Setup
- Install requirements from `requirements.txt3.txt`:
  ```
  pip install -r requirements.txt3.txt
  ```
- Set your `GEMINI_API_KEY` in a `.env` file.

## Usage
TBD

## Evaluation
TBD

## Sample Test Cases
- User Question: অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?  
  Expected Answer: শুম্ভুনাথ
- User Question: কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?  
  Expected Answer: মামাকে
- User Question: বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?  
  Expected Answer: ১৫ বছর 
=======
# 10-MIniteSchool-RAG
>>>>>>> 5deff4ba8c7b4ca99ca697f9a5a3873ccb6cfbd5
=======
# 10-MInite-School-RAG
>>>>>>> b200322de12b473d36329fc02d6e4eeffe880fc9
