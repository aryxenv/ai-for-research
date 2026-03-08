import os
from openai import AzureOpenAI


def get_embedding_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2024-02-01",
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    )


def get_embedding(client: AzureOpenAI, text: str) -> list[float]:
    text = text.replace("\n", " ")
    return client.embeddings.create(
        input=[text],
        model="text-embedding-3-large",
    ).data[0].embedding


def embed_chunks(chunked_data: list[dict]) -> list[dict]:
    """Add 'values' (embedding vector) to each chunk dict in-place."""
    client = get_embedding_client()
    print(f"Embedding {len(chunked_data)} chunks...")

    for i, chunk in enumerate(chunked_data):
        try:
            chunk["values"] = get_embedding(client, chunk["text"])
            if i % 10 == 0:
                print(".", end="", flush=True)
        except Exception as e:
            print(f"\nError on chunk {i}: {e}")

    print("\nDone! Embeddings generated.")
    return chunked_data
