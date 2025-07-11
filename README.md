
# 📄 DocuSmart - Analyse IA de Documents

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**DocuSmart** est une application d'analyse intelligente de documents utilisant l'IA pour extraire, résumer, analyser et traduire le contenu de vos fichiers PDF, DOCX et TXT.

![DocuSmart Interface](assets/doc_analysis_illustration.png)

## 🚀 Fonctionnalités

- **📝 Résumé automatique** : Génération de résumés intelligents de documents longs
- **💬 Q&A contextuel** : Posez des questions sur le contenu de vos documents
- **🌍 Traduction multilingue** : Traduction instantanée en 5 langues (FR, EN, ES, DE, IT)
- **🖼️ Extraction d'images** : Extraction et analyse des images intégrées dans les PDF
- **💰 Suivi des coûts** : Monitoring en temps réel des coûts OpenAI
- **🎨 Interface moderne** : Interface utilisateur sombre et responsive

## 🏗️ Architecture du Projet

```
DocuSmart/
├── app_streamlit.py          # Interface utilisateur (Streamlit)
├── document_processor.py     # Extraction, vectorisation, embeddings
├── qa_chain.py               # Chaîne de questions-réponses avec LLM
├── summarizer.py             # Résumé de texte via OpenAI
├── translator.py             # Traduction via OpenAI
├── assets/
│   └── doc_analysis_illustration.png
├── .env                      # Contient ta clé OPENAI_API_KEY
├── requirements.txt          # Dépendances Python
├── README.md                 # Documentation du projet
└── chroma_db/               # Base de données vectorielle (générée automatiquement)
```

## 🛠️ Technologies Utilisées

### Core Technologies
- **[Streamlit](https://streamlit.io/)** - Interface web interactive
- **[LangChain](https://langchain.com/)** - Framework pour applications LLM
- **[OpenAI GPT](https://openai.com/)** - Modèles de langage pour résumé, Q&A et traduction

### Traitement de Documents
- **[PyPDF](https://pypdf.readthedocs.io/)** - Lecture de fichiers PDF
- **[PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)** - Extraction d'images PDF
- **[python-docx](https://python-docx.readthedocs.io/)** - Traitement de fichiers Word
- **[docx2txt](https://github.com/ankushshah89/python-docx2txt)** - Conversion DOCX vers texte

### Base de Données Vectorielle
- **[ChromaDB](https://www.trychroma.com/)** - Stockage et recherche vectorielle
- **[OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)** - Vectorisation de texte

### Utilitaires
- **[tiktoken](https://github.com/openai/tiktoken)** - Comptage de tokens OpenAI
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** - Gestion des variables d'environnement
- **[Pillow (PIL)](https://pillow.readthedocs.io/)** - Traitement d'images

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- Clé API OpenAI

### 1. Cloner le repository
```bash
git clone https://github.com/votre-username/docusmart.git
cd docusmart
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv

# Sur Windows
venv\\Scripts\\activate

# Sur macOS/Linux
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration des variables d'environnement
Créez un fichier `.env` à la racine du projet :

```env
OPENAI_API_KEY=votre_clé_api_openai_ici
```

> **⚠️ Important** : Obtenez votre clé API sur [OpenAI Platform](https://platform.openai.com/api-keys)

## 🚀 Utilisation

### Lancement de l'application
```bash
streamlit run app_streamlit.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

### Interface utilisateur

#### 1. **Page d'accueil - Analyse de documents**
- Glissez-déposez ou sélectionnez un fichier (PDF, DOCX, TXT)
- Cliquez sur "Générer un résumé" pour obtenir un résumé automatique
- Posez des questions dans le champ "Posez une question sur le document"
- Visualisez les images extraites (pour les PDF)

#### 2. **Page de traduction**
- Saisissez le texte à traduire
- Sélectionnez la langue cible
- Cliquez sur "Traduire"

## 📋 Modules Détaillés

### 🔧 `document_processor.py`
**Responsabilité** : Traitement et vectorisation des documents

**Fonctions principales :**
- `load_file(uploaded_file)` : Chargement universel de fichiers
- `process_document(uploaded_file)` : Pipeline complet de traitement

**Processus :**
1. Détection automatique du type de fichier
2. Extraction du texte avec les loaders LangChain appropriés
3. Segmentation en chunks de 800 caractères (overlap de 150)
4. Génération d'embeddings avec OpenAI
5. Stockage dans ChromaDB pour la recherche vectorielle

### 💬 `qa_chain.py`
**Responsabilité** : Système de questions-réponses contextuel

**Fonctions principales :**
- `initialize_qa_chain(vectorstore)` : Initialisation de la chaîne Q&A
- `ask_question(qa_chain, question)` : Traitement des questions

**Mécanisme :**
1. Vectorisation de la question utilisateur
2. Recherche des 3 chunks les plus similaires
3. Génération d'une réponse contextuelle avec GPT

### 📝 `summarizer.py`
**Responsabilité** : Génération de résumés automatiques

**Stratégie "Map-Reduce" :**
1. **Map** : Résumé de chaque chunk individuellement
2. **Reduce** : Combinaison des résumés partiels en résumé final

### 🌍 `translator.py`
**Responsabilité** : Traduction multilingue

**Langues supportées :**
- Français (fr)
- Anglais (en)
- Espagnol (es)
- Allemand (de)
- Italien (it)

### 🖥️ `app_streamlit.py`
**Responsabilité** : Interface utilisateur et orchestration

**Fonctionnalités UI :**
- Upload de fichiers avec drag & drop
- Affichage des résumés avec style
- Système de Q&A interactif
- Extraction et affichage d'images PDF
- Suivi des coûts OpenAI en temps réel
- Navigation par sidebar

## 💡 Exemples d'Usage

### Résumé de document
```python
from document_processor import process_document
from summarizer import summarize_text

# Traitement du document
raw_text, chunks, vectorstore = process_document(uploaded_file)

# Génération du résumé
summary = summarize_text(raw_text)
print(f"Résumé : {summary}")
```

### Questions-Réponses
```python
from qa_chain import initialize_qa_chain, ask_question

# Initialisation de la chaîne Q&A
qa_chain = initialize_qa_chain(vectorstore)

# Poser une question
question = "Quels sont les points clés de ce document ?"
answer = ask_question(qa_chain, question)
print(f"Réponse : {answer}")
```

### Traduction
```python
from translator import translate_text

# Traduction en anglais
text_fr = "Bonjour, comment allez-vous ?"
text_en = translate_text(text_fr, "en")
print(f"Traduction : {text_en}")
```

## 📊 Métriques et Coûts

L'application suit automatiquement :
- **Nombre de tokens** utilisés par requête
- **Coût estimé** en dollars US
- **Temps de traitement** pour chaque opération

## 🔒 Sécurité et Confidentialité

- **Stockage local** : Les documents sont traités localement
- **Pas de sauvegarde cloud** : Vos données restent sur votre machine
- **Clé API sécurisée** : Stockage dans fichier .env (non versionné)
- **Fichiers temporaires** : Suppression automatique après traitement

## 🐛 Dépannage

### Erreurs courantes

**1. Erreur de clé API**
```
Error: OpenAI API key not found
```
**Solution** : Vérifiez que votre fichier `.env` contient `OPENAI_API_KEY=votre_clé`

**2. Erreur de dépendances**
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution** : Réinstallez les dépendances avec `pip install -r requirements.txt`

**3. Erreur de fichier non supporté**
```
ValueError: Type de fichier non supporté
```
**Solution** : Utilisez uniquement des fichiers PDF, DOCX ou TXT

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Roadmap

- [ ] **OCR intégré** : Analyse de texte dans les images
- [ ] **Support audio** : Transcription de fichiers audio
- [ ] **Export résultats** : Sauvegarde en PDF/Word
- [ ] **Interface multilingue** : Support de plus de langues
- [ ] **API REST** : Endpoints pour intégration externe
- [ ] **Authentification** : Système de comptes utilisateurs

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👨‍💻 Auteur

**Votre Nom**
- GitHub: [@votre-username](https://github.com/votre-username)
- LinkedIn: [Votre Profil](https://linkedin.com/in/votre-profil)
- Email: votre.email@example.com

## 🙏 Remerciements

- [OpenAI](https://openai.com/) pour les modèles GPT
- [LangChain](https://langchain.com/) pour le framework LLM
- [Streamlit](https://streamlit.io/) pour l'interface utilisateur
- [ChromaDB](https://www.trychroma.com/) pour la base vectorielle

---

⭐ **N'hésitez pas à donner une étoile si ce projet vous a été utile !**
```

Cette documentation complète couvre tous les aspects de votre projet DocuSmart avec :

## 📋 **Sections incluses :**

1. **Header avec badges** - Statut du projet et technologies
2. **Description et fonctionnalités** - Vue d'ensemble claire
3. **Architecture détaillée** - Structure des fichiers
4. **Technologies utilisées** - Stack technique complète
5. **Installation pas-à-pas** - Guide d'installation détaillé
6. **Guide d'utilisation** - Comment utiliser l'application
7. **Documentation des modules** - Explication de chaque composant
8. **Exemples de code** - Snippets d'utilisation
9. **Métriques et sécurité** - Aspects techniques importants
10. **Dépannage** - Solutions aux problèmes courants
11. **Contribution et roadmap** - Guide pour les contributeurs
12. **Licence et crédits** - Informations légales

