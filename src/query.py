import os
from openai import AzureOpenAI, OpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery


def retrieve_context(query_text: str, top_k: int = 3) -> str:
    """Embed the query, run hybrid search, return formatted context string."""
    embedding_client = AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2024-02-01",
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    )

    search_client = SearchClient(
        endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
        index_name=os.environ["AZURE_SEARCH_INDEX_NAME"],
        credential=AzureKeyCredential(os.environ["AZURE_SEARCH_API_KEY"]),
    )

    print("Generating query embedding...", end=" ")
    query_vector = (
        embedding_client.embeddings.create(input=query_text, model="text-embedding-3-large")
        .data[0]
        .embedding
    )
    print("Done.")

    print("Searching vector index...", end=" ")
    vector_query = VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=top_k,
        fields="contentVector",
    )
    results = search_client.search(
        search_text=query_text,
        vector_queries=[vector_query],
        select=["content", "location"],
        top=top_k,
    )

    context_parts = [
        f"Source: {r['location']}\nContent: {r['content']}" for r in results
    ]
    print(f"Found {len(context_parts)} relevant chunks.")
    return "\n\n".join(context_parts)


def ask(query: str) -> str:
    """Retrieve context and generate an answer via Mistral."""
    context = retrieve_context(query)

    chat_client = OpenAI(
        base_url=os.environ["AZURE_OPENAI_INFERENCE"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )

    system_prompt = (
        "You are a helpful assistant. Use the provided 'Context' to answer the user's question.\n"
        "If the answer is not in the context, say you don't know.\n"
        "Always cite your sources using the format [Source: filename, Page: page]."
    )

    completion = chat_client.chat.completions.create(
        model="Mistral-Large-3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"},
        ],
    )
    return completion.choices[0].message.content
