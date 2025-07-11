
"""
Module de traduction
Utilise ChatGPT pour traduire du texte dans différentes langues
"""

from langchain_openai import ChatOpenAI


def translate_text(text: str, target_lang: str) -> str:
    """
    Traduit un texte dans la langue cible
    
    Args:
        text (str): Texte à traduire
        target_lang (str): Code de la langue cible (fr, en, es, de, it)
    
    Returns:
        str: Texte traduit
    
    Utilise:
    - ChatGPT-3.5-turbo pour la traduction
    - Un prompt système pour définir le rôle de traducteur
    """
    
    # Définition du prompt système
    system_prompt = f"You are a professional translator. Translate the following text into {target_lang}."
    
    # Initialisation du modèle ChatGPT
    llm = ChatOpenAI(
        temperature=0,              # Traduction déterministe
        model_name="gpt-3.5-turbo"  # Modèle ChatGPT
    )
    
    # Génération de la traduction
    result = llm.predict(f"{system_prompt}\n\n{text}")
    
    return result
