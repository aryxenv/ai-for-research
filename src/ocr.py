import glob
import os
import io
import base64
import requests
from pypdf import PdfReader, PdfWriter


BATCH_SIZE = 5  # Pages per batch (avoids Azure timeout for large PDFs)


def run_ocr(data_dir: str = "data") -> list[dict]:
    """
    Ingest PDFs from data_dir, run OCR via Mistral Document AI,
    and return a list of dicts with source_context, file_path, and pages.
    """
    pdf_files = glob.glob(os.path.join(data_dir, "*.pdf"))
    print(f"Found {len(pdf_files)} PDFs. Starting OCR job...\n")

    headers = {
        "Authorization": f"Bearer {os.environ['AZURE_OPENAI_API_KEY']}",
        "Content-Type": "application/json",
    }

    results = []

    for file_path in pdf_files:
        file_name = os.path.basename(file_path)
        print(f"Processing: {file_name}...", end=" ")

        try:
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            file_page_data = []

            for start_idx in range(0, total_pages, BATCH_SIZE):
                end_idx = min(start_idx + BATCH_SIZE, total_pages)

                writer = PdfWriter()
                for i in range(start_idx, end_idx):
                    writer.add_page(reader.pages[i])

                with io.BytesIO() as buf:
                    writer.write(buf)
                    buf.seek(0)
                    encoded_batch = base64.b64encode(buf.read()).decode("utf-8")
                    base64_string = f"data:application/pdf;base64,{encoded_batch}"

                payload = {
                    "model": "mistral-document-ai-2512",
                    "document": {
                        "type": "document_url",
                        "document_url": base64_string,
                    },
                    "include_image_base64": False,
                }

                response = requests.post(
                    os.environ["AZURE_MISTRAL_ENDPOINT"],
                    headers=headers,
                    json=payload,
                )

                if response.status_code == 200:
                    data = response.json()
                    for i, page in enumerate(data.get("pages", [])):
                        file_page_data.append(
                            {"page_num": start_idx + i + 1, "text": page["markdown"]}
                        )
                else:
                    print(f"\nError on batch {start_idx}-{end_idx}: {response.status_code} - {response.text}")
                    break

            if file_page_data:
                results.append(
                    {
                        "source_context": file_name,
                        "file_path": file_path,
                        "pages": file_page_data,
                    }
                )
                print("Done.")

        except Exception as e:
            print(f"Failed: {e}")

    print("\nAll files processed.")
    return results
