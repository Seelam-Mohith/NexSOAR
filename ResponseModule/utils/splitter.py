from langchain_text_splitters import RecursiveCharacterTextSplitter

import config
from utils.atomics import chunk_header
from utils.loader import load_documents


def split_document():
    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = splitter.split_documents(documents)

    for chunk in chunks:
        header = chunk_header(chunk.metadata)
        if header and not chunk.page_content.lstrip().startswith(header.strip()):
            chunk.page_content = header + chunk.page_content

    techniques = {chunk.metadata.get("technique_id") for chunk in chunks}
    techniques.discard(None)

    print(f"Loaded Documents : {len(documents)}")
    print(f"Created Chunks : {len(chunks)}")
    print(f"Techniques Covered : {len(techniques)}")

    return chunks


if __name__ == "__main__":

    chunks = split_document()

    print("\nFirst Chunk")
    print("-" * 50)
    print(chunks[0].page_content[:500])
    print("-" * 50)
    print("Metadata:", chunks[0].metadata)
