"""
RAG Pipeline — CLI entrypoint

Usage:
    python -m src.main ingest          # OCR → chunk → embed → upload
    python -m src.main query "question" # retrieve + answer
    python -m src.main query           # interactive prompt
"""

import sys
import dotenv

from src.ocr import run_ocr
from src.chunking import chunk_documents
from src.embedding import embed_chunks
from src.indexing import upload_to_search
from src.query import ask


def ingest(data_dir: str = "data") -> None:
    """Run the full ingestion pipeline: OCR → chunk → embed → upload."""
    print("=== Step 1: OCR ===")
    ocr_results = run_ocr(data_dir)

    print("\n=== Step 2: Chunking ===")
    chunks = chunk_documents(ocr_results)

    print("\n=== Step 3: Embedding ===")
    chunks = embed_chunks(chunks)

    print("\n=== Step 4: Upload to Azure AI Search ===")
    upload_to_search(chunks)

    print("\nPipeline complete.")


def query(question: str | None = None) -> None:
    """Ask a question against the indexed data."""
    if question is None:
        question = input("What would you like to know? ")
    answer = ask(question)
    print(f"\nAnswer:\n{answer}")


def main() -> None:
    dotenv.load_dotenv()

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "ingest":
        data_dir = sys.argv[2] if len(sys.argv) > 2 else "data"
        ingest(data_dir)
    elif command == "query":
        question = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
        query(question)
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
