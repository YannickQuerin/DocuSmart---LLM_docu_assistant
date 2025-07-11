

### imports utiles

import os
import tempfile
import tiktoken
import pypdf
import chromadb

# ✅ Nouveau chemin pour OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings

# ✅ Valides et non dépréciés
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader

# ✅ Chargement des variables d'environnement
from dotenv import load_dotenv
load_dotenv()


# Fonction de chargement du fichier

def load_file(uploaded_file):
    import os
    import tempfile
    from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader

    # Cas BytesIO sans .name (ex. : passé depuis un fichier Streamlit en mémoire)
    if not hasattr(uploaded_file, 'name'):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        suffix = ".pdf"  # ou déduire avec magic
    else:
        suffix = os.path.splitext(uploaded_file.name)[-1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

    # Sélection du bon loader
    if suffix == ".pdf":
        loader = PyPDFLoader(tmp_path)
    elif suffix == ".txt":
        loader = TextLoader(tmp_path)
    elif suffix == ".docx":
        loader = Docx2txtLoader(tmp_path)
    else:
        raise ValueError(f"Type de fichier non supporté : {suffix}")

    return loader.load()


# Fonction de CHunking, vectorisation de documents

def process_document(uploaded_file):
    documents = load_file(uploaded_file)
    raw_text = "\n".join([doc.page_content for doc in documents])

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
    return raw_text, chunks, vectorstore



