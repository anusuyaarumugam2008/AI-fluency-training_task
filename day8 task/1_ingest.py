
import shutil
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from lc_config import DB_DIR, EMBED_PROVIDER, get_vectorstore


# Find the data folder next to this Python file
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


# Step 1: Load the library documents
documents = []

for file_path in sorted(DATA_DIR.glob("*.md")):
    text = file_path.read_text(encoding="utf-8")

    documents.append(
        Document(
            page_content=text,
            metadata={"source": file_path.name},
        )
    )

if not documents:
    raise SystemExit(
        "No Markdown files found. Add .md files inside the data folder."
    )

print(f"Loaded {len(documents)} documents")


# Step 2: Split documents into smaller chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=350,
    chunk_overlap=50,
)

chunks = splitter.split_documents(documents)

print(f"Split into {len(chunks)} chunks")


# Step 3: Remove the old database before creating a fresh one
shutil.rmtree(DB_DIR, ignore_errors=True)


# Step 4: Store the chunks in Chroma
store = get_vectorstore()

ids = store.add_documents(chunks)

print(f"Stored {len(ids)} chunks in Chroma")
print(f"Embedding provider: {EMBED_PROVIDER}")

vector = store.embeddings.embed_query("library opening hours")
print(f"Vector length: {len(vector)}")
print("Ingestion completed successfully!")