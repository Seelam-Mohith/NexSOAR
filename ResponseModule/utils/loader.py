from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader

import config
from utils.atomics import describe_playbook, is_playbook


def _relative_source(source):
    try:
        return Path(source).resolve().relative_to(config.BASE_DIR).as_posix()
    except ValueError:
        return source


def load_documents(data_path=None):
    root = Path(data_path) if data_path else config.DATA_DIR

    loader = DirectoryLoader(
        path=str(root),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
        silent_errors=True,
    )
    documents = loader.load()

    playbooks = []
    skipped = 0
    for document in documents:
        source = document.metadata.get("source", "")
        if not is_playbook(source):
            skipped += 1
            continue
        document.metadata["source"] = _relative_source(source)
        document.metadata.update(describe_playbook(source, document.page_content))
        playbooks.append(document)

    print(f"Loaded {len(documents)} markdown files.")
    print(f"Indexed {len(playbooks)} playbooks, skipped {skipped} non-playbook files.")

    return playbooks


if __name__ == "__main__":
    docs = load_documents()

    print("\nFirst Document")
    print("-" * 50)
    print("Source:", docs[0].metadata["source"])
    print("Technique:", docs[0].metadata["technique_id"], "-", docs[0].metadata["technique_name"])
    print(docs[0].page_content[:500])
