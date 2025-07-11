import streamlit as st
from document_processor import process_document
from summarizer import summarize_text
from qa_chain import initialize_qa_chain, ask_question
from translator import translate_text
from langchain.callbacks import get_openai_callback
from PIL import Image
import io
import base64
import fitz

def extract_images_from_pdf(file_bytes):
    images = []
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    for page_index in range(len(doc)):
        page = doc.load_page(page_index)
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            images.append(Image.open(io.BytesIO(image_bytes)))
    return images

def home():
    st.markdown("""
        <style>
            .main {
                background-color: #121519;
                color: #e1e1e1;
            }
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            .upload-area {
                border: 2px dashed #2a3140;
                border-radius: 12px;
                padding: 3rem;
                text-align: center;
                color: #8a95a1;
                margin-bottom: 2rem;
            }
            .stButton > button {
                background-color: #1e88e5;
                color: white;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                font-weight: bold;
            }
            .stTextInput > div > input {
                background-color: #1e1e1e;
                color: #f5f5f5;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 0.3rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.image("assets/doc_analysis_illustration.png", width=480)

    st.title("\U0001F4C4 DocuSmart – Analyse IA de documents")
    st.markdown("""
    **DocuSmart** permet :
    - Résumé automatique de PDF, DOCX, TXT
    - Q&A intelligent sur le contenu du document
    - Traduction instantanée du texte ou réponses
    - Extraction et annotation d'images contenues dans le PDF
    """)

    uploaded_file = st.file_uploader("\U0001F4C2 Glissez-déposez un document ou cliquez ici", type=["pdf", "txt", "docx"], label_visibility="collapsed")

    if uploaded_file:
        st.success("\U00002705 Document chargé avec succès")
        file_bytes = uploaded_file.read()
        uploaded_file.seek(0)

        with st.spinner("\U000023F3 Analyse en cours..."):
            raw_text, chunks, vectorstore = process_document(io.BytesIO(file_bytes))

        st.markdown("---")
        if st.button("\U0001F4DD Générer un résumé"):
            with get_openai_callback() as cb:
                summary = summarize_text(raw_text)
            st.markdown(f"""
                <div style='background-color:#2e7d32; padding:1rem; border-radius:8px; color:white;'>
                    <strong>Résumé généré :</strong><br>{summary}
                </div>
            """, unsafe_allow_html=True)
            st.info(f"Coût OpenAI : {cb.total_cost:.6f} $ | Tokens : {cb.total_tokens}")

        question = st.text_input("\U0001F4AC Posez une question sur le document :")
        if question:
            with get_openai_callback() as cb:
                qa_chain = initialize_qa_chain(vectorstore)
                answer = ask_question(qa_chain, question)
            st.markdown(f"""
                <div style='background-color:#f9a825; padding:1rem; border-radius:8px; color:black;'>
                    <strong>Réponse :</strong><br>{answer}
                </div>
            """, unsafe_allow_html=True)
            st.info(f"Coût OpenAI : {cb.total_cost:.6f} $ | Tokens : {cb.total_tokens}")

        st.markdown("---")
        if uploaded_file.name.endswith(".pdf"):
            st.subheader("\U0001F5BC Images intégrées dans le document")
            images = extract_images_from_pdf(file_bytes)
            if images:
                for idx, image in enumerate(images):
                    st.image(image, caption=f"Image extraite {idx+1}", use_column_width=True)
                    prompt = st.text_input(f"\U0001F4AC Question ou annotation pour l'image {idx+1}:", key=f"prompt_{idx}")
                    if prompt:
                        st.markdown("""
                            <div style='background-color:#4527a0; padding:0.8rem; border-radius:8px; color:white;'>
                                Annotation IA à venir (OCR / légende automatique).
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Aucune image détectée dans ce document.")


def translation():
    st.title("\U0001F30F Traduction intelligente de texte")
    text = st.text_area("Entrez le texte à traduire :")
    target_lang = st.selectbox("Langue cible", ["fr", "en", "es", "de", "it"])

    if st.button("Traduire") and text:
        with st.spinner("Traduction en cours..."):
            with get_openai_callback() as cb:
                translated = translate_text(text, target_lang)
            st.subheader("Texte traduit")
            st.write(translated)
            st.info(f"Coût OpenAI : {cb.total_cost:.6f} $ | Tokens : {cb.total_tokens}")


def main():
    st.set_page_config(page_title="DocuSmart", layout="wide")

    with st.sidebar:
        st.title("\U0001F5C2 Navigation")
        menu = st.radio("Aller vers :", ["Accueil", "Traduction"])

    if menu == "Accueil":
        home()
    elif menu == "Traduction":
        translation()


if __name__ == "__main__":
    main()
