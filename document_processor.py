
"""
Module de traitement des documents
Ce module gère le chargement, la segmentation et la vectorisation des documents
"""

# Imports des bibliothèques nécessaires
import os
import tempfile
import tiktoken  # Pour compter les tokens OpenAI
import pypdf    # Pour lire les PDF
import chromadb # Base de données vectorielle

# ✅ Import moderne pour les embeddings OpenAI
from langchain_openai import OpenAIEmbeddings

# ✅ Imports LangChain pour le traitement de texte
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader

# ✅ Chargement des variables d'environnement (clés API)
from dotenv import load_dotenv
load_dotenv()


def load_file(uploaded_file):
    """
    Fonction de chargement universel de fichiers
    
    Args:
        uploaded_file: Fichier uploadé (peut être BytesIO ou file-like object)
    
    Returns:
        List[Document]: Liste des documents chargés par LangChain
    
    Processus:
    1. Détecte le type de fichier (PDF, TXT, DOCX)
    2. Crée un fichier temporaire pour le traitement
    3. Utilise le bon loader LangChain selon l'extension
    """
    
    # Gestion des fichiers sans attribut .name (ex: BytesIO de Streamlit)
    if not hasattr(uploaded_file, 'name'):
        # Crée un fichier temporaire avec extension .pdf par défaut
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        suffix = ".pdf"
    else:
        # Extrait l'extension du fichier
        suffix = os.path.splitext(uploaded_file.name)[-1].lower()
        # Crée un fichier temporaire avec la bonne extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

    # Sélection du loader approprié selon le type de fichier
    if suffix == ".pdf":
        loader = PyPDFLoader(tmp_path)      # Pour les PDF
    elif suffix == ".txt":
        loader = TextLoader(tmp_path)       # Pour les fichiers texte
    elif suffix == ".docx":
        loader = Docx2txtLoader(tmp_path)   # Pour les documents Word
    else:
        raise ValueError(f"Type de fichier non supporté : {suffix}")

    # Charge et retourne les documents
    return loader.load()


def process_document(uploaded_file):
    """
    Fonction principale de traitement des documents
    
    Args:
        uploaded_file: Fichier à traiter
    
    Returns:
        tuple: (texte_brut, chunks, vectorstore)
    
    Processus:
    1. Charge le document avec load_file()
    2. Extrait le texte brut
    3. Découpe le texte en chunks (morceaux)
    4. Crée des embeddings vectoriels
    5. Stocke dans une base vectorielle Chroma
    """
    
    # 1. Chargement du document
    documents = load_file(uploaded_file)
    
    # 2. Extraction du texte brut (concaténation de toutes les pages)
    raw_text = "\n".join([doc.page_content for doc in documents])

    # 3. Configuration du splitter pour découper le texte
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,      # Taille max de chaque chunk (800 caractères)
        chunk_overlap=150    # Chevauchement entre chunks (150 caractères)
    )
    # Découpage en chunks
    chunks = splitter.split_documents(documents)

    # 4. Création des embeddings avec OpenAI
    embeddings = OpenAIEmbeddings()
    
    # 5. Création de la base vectorielle Chroma
    # Les chunks sont convertis en vecteurs et stockés localement
    vectorstore = Chroma.from_documents(
        chunks, 
        embeddings, 
        persist_directory="./chroma_db"  # Dossier de persistance
    )
    
    return raw_text, chunks, vectorstore
