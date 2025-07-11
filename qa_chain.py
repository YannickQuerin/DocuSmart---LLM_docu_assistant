"""
Module de Questions-Réponses (Q&A)
Permet de poser des questions sur le contenu du document
"""

from langchain.chains import RetrievalQA
from langchain_openai import OpenAI


def initialize_qa_chain(vectorstore):
    """
    Initialise la chaîne de Q&A avec recherche vectorielle
    
    Args:
        vectorstore: Base vectorielle contenant les embeddings du document
    
    Returns:
        RetrievalQA: Chaîne de Q&A configurée
    
    Fonctionnement:
    1. Configure un retriever pour chercher les passages pertinents
    2. Utilise la similarité cosinus pour trouver les meilleurs chunks
    3. Retourne les 3 chunks les plus similaires (k=3)
    """
    
    # Configuration du retriever (système de recherche)
    retriever = vectorstore.as_retriever(
        search_type="similarity",    # Recherche par similarité
        search_kwargs={"k": 3}      # Retourne les 3 meilleurs résultats
    )
    
    # Initialisation du modèle LLM
    llm = OpenAI(temperature=0)
    
    # Création de la chaîne RetrievalQA
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",    # Stratégie "stuff": concatène tous les chunks trouvés
        retriever=retriever
    )
    
    return qa_chain


def ask_question(qa_chain, question):
    """
    Pose une question à la chaîne de Q&A
    
    Args:
        qa_chain: Chaîne de Q&A initialisée
        question (str): Question à poser
    
    Returns:
        str: Réponse générée par l'IA
    
    Processus:
    1. La question est vectorisée
    2. Recherche des chunks les plus pertinents
    3. Génération d'une réponse basée sur ces chunks
    """
    return qa_chain.run(question)
