

### summarizer.py

from langchain.chains.summarize import load_summarize_chain
from langchain_openai import OpenAI  # ✅ MAJ
from langchain.schema import Document  # ✅ MAJ


def summarize_text(raw_text):
    docs = [Document(page_content=raw_text)]
    llm = OpenAI(temperature=0)
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(docs)
    return summary

