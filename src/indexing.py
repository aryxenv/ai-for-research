import os
import uuid
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient


BATCH_SIZE = 1000


def build_documents(chunked_data: list[dict]) -> list[dict]:
    """Convert chunked data into the Azure AI Search document format."""
    documents = []
    for chunk in chunked_data:
        section_info = (
            f", Section: {chunk['section']}"
            if chunk.get("section") and chunk["section"] != "Unknown Section"
            else ""
        )
        documents.append(
            {
                "id": str(uuid.uuid4()),
                "content": chunk["text"],
                "contentVector": chunk["values"],
                "location": f"Source: {chunk['source']} (Page {chunk['page']}{section_info})",
            }
        )
    return documents


def upload_to_search(chunked_data: list[dict]) -> None:
    """Build documents and upload them to Azure AI Search in batches."""
    documents = build_documents(chunked_data)
    print(f"Uploading {len(documents)} documents...")

    credential = AzureKeyCredential(os.environ["AZURE_SEARCH_PRIMARY_API_KEY"])
    client = SearchClient(
        endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
        index_name=os.environ["AZURE_SEARCH_INDEX_NAME"],
        credential=credential,
    )

    for i in range(0, len(documents), BATCH_SIZE):
        batch = documents[i : i + BATCH_SIZE]
        try:
            client.upload_documents(documents=batch)
            print(f"  Batch {i}-{i + len(batch)}: OK")
        except Exception as e:
            print(f"  Error uploading batch {i}: {e}")

    print("Upload complete.")
