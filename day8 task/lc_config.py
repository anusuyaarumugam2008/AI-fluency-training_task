
import os
import hashlib
import math
import re

from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "groq").strip().lower()
EMBED_PROVIDER = os.getenv("EMBED_PROVIDER", "fastembed").strip().lower()
MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")

DB_DIR = "chroma_db"
COLLECTION = "smart_library"


class HashEmbeddings(Embeddings):
    """Simple offline keyword embeddings."""

    STOP = set(
        "a an the is are was to of in on for and or by at be it "
        "this that with what how do does i my can".split()
    )

    def _vec(self, text):
        vector = [0.0] * 256

        for word in re.findall(r"[a-z0-9]+", text.lower()):
            if word in self.STOP:
                continue

            if word.endswith("s") and len(word) > 3:
                word = word[:-1]

            index = int(
                hashlib.md5(word.encode()).hexdigest(), 16
            ) % 256

            vector[index] += 1.0

        norm = math.sqrt(sum(x * x for x in vector)) or 1.0
        return [x / norm for x in vector]

    def embed_documents(self, texts):
        return [self._vec(text) for text in texts]

    def embed_query(self, text):
        return self._vec(text)


def get_embeddings():
    if EMBED_PROVIDER == "hash":
        return HashEmbeddings()

    if EMBED_PROVIDER == "fastembed":
        from langchain_community.embeddings import FastEmbedEmbeddings

        model_name = os.getenv(
            "EMBED_MODEL",
            "BAAI/bge-small-en-v1.5",
        )

        return FastEmbedEmbeddings(model_name=model_name)

    raise SystemExit(
        "EMBED_PROVIDER must be hash or fastembed."
    )


def get_model(temperature=0):
    """Connect to a hosted chat model. This does not use Ollama."""

    from langchain_openai import ChatOpenAI

    if PROVIDER == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        base_url = "https://api.groq.com/openai/v1"
    elif PROVIDER == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = None
    elif PROVIDER == "huggingface":
        api_key = os.getenv("HF_TOKEN")
        base_url = "https://router.huggingface.co/v1"
    else:
        raise SystemExit(
            "PROVIDER must be groq, openai, or huggingface."
        )

    if not api_key:
        raise SystemExit(
            "Please add the appropriate API key to your .env file."
        )

    settings = {
        "model": MODEL,
        "api_key": api_key,
        "temperature": temperature,
    }

    if base_url:
        settings["base_url"] = base_url

    return ChatOpenAI(**settings)


def get_vectorstore():
    from langchain_chroma import Chroma

    return Chroma(
        collection_name=COLLECTION,
        embedding_function=get_embeddings(),
        persist_directory=DB_DIR,
        collection_metadata={"hnsw:space": "cosine"},
    )