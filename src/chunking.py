from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter


HEADERS_TO_SPLIT_ON = [
    ("#", "section"),
    ("##", "subsection"),
    ("###", "subsubsection"),
]

CHUNK_SIZE = 3000
CHUNK_OVERLAP = 500


def chunk_documents(ocr_results: list[dict]) -> list[dict]:
    """
    Two-stage markdown-aware chunking:
    1. Split by markdown headers (preserves section context as metadata).
    2. Enforce size limits with RecursiveCharacterTextSplitter.
    """
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS_TO_SPLIT_ON,
        strip_headers=False,
    )
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],
    )

    chunked_data = []

    for doc in ocr_results:
        filename = doc["source_context"]

        for page in doc["pages"]:
            page_num = page["page_num"]
            md_chunks = md_splitter.split_text(page["text"])
            final_chunks = text_splitter.split_documents(md_chunks)

            for i, chunk in enumerate(final_chunks):
                section_parts = []
                for key in ("section", "subsection", "subsubsection"):
                    if key in chunk.metadata:
                        section_parts.append(chunk.metadata[key])
                section_path = " > ".join(section_parts) if section_parts else "Unknown Section"

                chunked_data.append(
                    {
                        "chunk_id": f"{filename}_p{page_num}_{i}",
                        "source": filename,
                        "page": page_num,
                        "section": section_path,
                        "text": chunk.page_content,
                    }
                )

    print(f"Generated {len(chunked_data)} chunks.")
    return chunked_data
