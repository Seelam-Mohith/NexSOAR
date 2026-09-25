from langchain_chroma import Chroma

import config
from utils.splitter import split_document
from utils.embeddings import embeddings


def create_vector_db():
    chunks = split_document()

    vector_db = Chroma(
        collection_name=config.COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(config.DB_DIR),
    )
    vector_db.reset_collection()
    vector_db.add_documents(chunks)

    techniques = {chunk.metadata.get("technique_id") for chunk in chunks}
    techniques.discard(None)

    print(
        f"Stored {len(chunks)} chunks from {len(techniques)} techniques "
        f"in collection '{config.COLLECTION_NAME}' at {config.DB_DIR}."
    )

    return vector_db


if __name__ == "__main__":
    create_vector_db()
