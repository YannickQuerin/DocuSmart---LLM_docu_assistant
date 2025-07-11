
"""
Module de résumé automatique
Utilise LangChain pour générer des résumés de documents longs
"""

from langchain.chains.summarize import load_summarize_chain
from langchain_openai import OpenAI
from langchain.schema import Document


def summarize_text(raw_text):
    """
    Génère un résumé automatique du texte
    
    Args:
        raw_text (str): Texte complet à résumer
    
    Returns:
        str: Résumé généré par l'IA
    
    Méthode:
    - Utilise la stratégie "map_reduce" de LangChain
    - Map: résume chaque chunk individuellement
    - Reduce: combine les résumés partiels en un résumé final
    """
    
    # Conversion du texte en format Document LangChain
    docs = [Document(page_content=raw_text)]
    
    # Initialisation du modèle OpenAI
    llm = OpenAI(temperature=0)  # temperature=0 pour des résultats déterministes
    
    # Chargement de la chaîne de résumé avec stratégie map_reduce
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    
    # Génération du résumé
    summary = chain.run(docs)
    
    return summary
