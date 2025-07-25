import argparse
import os
from dotenv import load_dotenv
from rag.pipeline import RAGPipeline

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Ask a question to the RAG pipeline.")
    parser.add_argument("query", type=str, help="The question to ask.")
    args = parser.parse_args()

    # Initialize the RAG pipeline
    pipeline = RAGPipeline()

    # Get the answer
    result = pipeline.ask(args.query)

    # Print the result
    print("Answer:", result.get("answer"))

if __name__ == "__main__":
    main()
