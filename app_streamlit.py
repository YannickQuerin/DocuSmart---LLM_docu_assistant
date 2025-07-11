"""
Application Streamlit principale - Interface utilisateur
DocuSmart: Analyse IA de documents avec résumé, Q&A et traduction
"""

import streamlit as st
from document_processor import process_document
from summarizer import summarize_text
from qa_chain import initialize_qa_chain, ask_question
from translator import translate_text
from langchain.callbacks import get_openai_callback
from PIL import Image
import io
import base64
import fitz  # PyMuPDF pour l'extraction d'images


def extract_images_from_pdf(file_bytes):
    """
    Extrait toutes les images d'un fichier PDF
    
    Args:
        file_bytes: Contenu binaire du PDF
    
    Returns:
        List[PIL.Image]: Liste des images extraites
    
    Utilise PyMuPDF (fitz) pour:
    1. Parcourir chaque page du PDF
    2. Identifier les images intégrées
    3. Extraire et convertir en objets PIL.Image
    """
    images = []
    
    # Ouverture du PDF depuis les bytes
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    
    # Parcours de chaque page
    for page_index in range(len(doc)):
        page = doc.load_page(page_index)
        
        # Extraction des images de la page
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]  # Référence de l'image
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Conversion en objet PIL.Image
            images.append(Image.open(io.BytesIO(image_bytes)))
    
    return images


def home():
    """
    Page d'accueil principale de l'application
    
    Fonctionnalités:
    1. Upload de documents (PDF, DOCX, TXT)
    2. Génération de résumés automatiques
    3. Système de Q&A sur le document
    4. Extraction et affichage des images (PDF uniquement)
    """
    
    # ===== STYLES CSS PERSONNALISÉS =====
    st.markdown("""
        <style>
            .main {
                background-color: #121519;  /* Fond sombre */
                color: #e1e1e1;            /* Texte clair */
            }
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            .upload-area {
                border: 2px dashed #2a3140;  /* Zone d'upload stylisée */
                border-radius: 12px;
                padding: 3rem;
                text-align: center;
                color: #8a95a1;
                margin-bottom: 2rem;
            }
            .stButton > button {
                background-color: #1e88e5;   /* Boutons bleus */
                color: white;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                font-weight: bold;
            }
            .stTextInput > div > input {
                background-color: #1e1e1e;   /* Champs de saisie sombres */
                color: #f5f5f5;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 0.3rem;
            }
        </style>
    """, unsafe_allow_html=True)

    # ===== INTERFACE UTILISATEUR =====
    
    # Image d'illustration (si elle existe)
    st.image("assets/doc_analysis_illustration.png", width=480)

    # Titre et description
    st.title("📄 DocuSmart – Analyse IA de documents")
    st.markdown("""
    **DocuSmart** permet :
    - Résumé automatique de PDF, DOCX, TXT
    - Q&A intelligent sur le contenu du document
    - Traduction instantanée du texte ou réponses
    - Extraction et annotation d'images contenues dans le PDF
    """)

    # ===== UPLOAD DE FICHIER =====
    uploaded_file = st.file_uploader(
        "📂 Glissez-déposez un document ou cliquez ici", 
        type=["pdf", "txt", "docx"], 
        label_visibility="collapsed"
    )

    if uploaded_file:
        st.success("✅ Document chargé avec succès")
        
        # Lecture du fichier en bytes
        file_bytes = uploaded_file.read()
        uploaded_file.seek(0)  # Reset du pointeur de fichier

        # ===== TRAITEMENT DU DOCUMENT =====
        with st.spinner("⏳ Analyse en cours..."):
            # Appel de la fonction de traitement principal
            raw_text, chunks, vectorstore = process_document(io.BytesIO(file_bytes))

        st.markdown("---")
        
        # ===== GÉNÉRATION DE RÉSUMÉ =====
        if st.button("📝 Générer un résumé"):
            # Utilisation du callback pour tracker les coûts OpenAI
            with get_openai_callback() as cb:
                summary = summarize_text(raw_text)
            
            # Affichage du résumé avec style
            st.markdown(f"""
                <div style='background-color:#2e7d32; padding:1rem; border-radius:8px; color:white;'>
                    <strong>Résumé généré :</strong><br>{summary}
                </div>
            """, unsafe_allow_html=True)
            
            # Affichage des métriques de coût
            st.info(f"Coût OpenAI : {cb.total_cost:.6f} $ | Tokens : {cb.total_tokens}")

        # ===== SYSTÈME DE Q&A =====
        question = st.text_input("💬 Posez une question sur le document :")
        if question:
            with get_openai_callback() as cb:
                # Initialisation de la chaîne Q&A
                qa_chain = initialize_qa_chain(vectorstore)
                # Génération de la réponse
                answer = ask_question(qa_chain, question)
            
            # Affichage de la réponse
            st.markdown(f"""
                <div style='background-color:#f9a825; padding:1rem; border-radius:8px; color:black;'>
                    <strong>Réponse :</strong><br>{answer}
                </div>
            """, unsafe_allow_html=True)
            
            st.info(f"Coût OpenAI : {cb.total_cost:.6f} $ | Tokens : {cb.total_tokens}")

        # ===== EXTRACTION D'IMAGES (PDF UNIQUEMENT) =====
        st.markdown("---")
        if uploaded_file.name.endswith(".pdf"):
            st.subheader("🖼 Images intégrées dans le document")
            
            # Extraction des images
            images = extract_images_from_pdf(file_bytes)
            
            if images:
                # Affichage de chaque image avec possibilité d'annotation
                for idx, image in enumerate(images):
                    st.image(image, caption=f"Image extraite {idx+1}", use_column_width=True)
                    
                    # Zone de saisie pour annotation (fonctionnalité future)
                    prompt = st.text_input(
                        f"💬 Question ou annotation pour l'image {idx+1}:", 
                        key=f"prompt_{idx}"
                    )
                    
                    if prompt:
                        # Placeholder pour future fonctionnalité d'analyse d'image
                        st.markdown("""
                            <div style='background-color:#4527a0; padding:0.8rem; border-radius:8px; color:white;'>
                                Annotation IA à venir (OCR / légende automatique).
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Aucune image détectée dans ce document.")


def translation():
    """
    Page de traduction de texte
    
    Permet de traduire du texte libre dans différentes langues
    en utilisant ChatGPT comme moteur de traduction
    """
    st.title("🌏 Traduction intelligente de texte")
    
    # Zone de saisie du texte
    text = st.text_area("Entrez le texte à traduire :")
    
    # Sélection de la langue cible
    target_lang = st.selectbox("Langue cible", ["fr", "en", "es", "de", "it"])

    # Bouton de traduction
    if st.button("Traduire") and text:
        with st.spinner("Traduction en cours..."):
            with get_openai_callback() as cb:
                # Appel de la fonction de traduction
                translated = translate_text(text, target_lang)
            
            # Affichage du résultat
            st.subheader("Texte traduit")
            st.write(translated)
            
            # Métriques de coût
            st.info(f"Coût OpenAI : {cb.total_cost:.6f} $ | Tokens : {cb.total_tokens}")


def main():
    """
    Fonction principale de l'application Streamlit
    
    Configure:
    - La page et le layout
    - La navigation par sidebar
    - Le routage entre les pages
    """
    
    # Configuration de la page Streamlit
    st.set_page_config(page_title="DocuSmart", layout="wide")

    # ===== SIDEBAR DE NAVIGATION =====
    with st.sidebar:
        st.title("🗂 Navigation")
        menu = st.radio("Aller vers :", ["Accueil", "Traduction"])

    # ===== ROUTAGE DES PAGES =====
    if menu == "Accueil":
        home()
    elif menu == "Traduction":
        translation()


# ===== POINT D'ENTRÉE DE L'APPLICATION =====
if __name__ == "__main__":
    main()
