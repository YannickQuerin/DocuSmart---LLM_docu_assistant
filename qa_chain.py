

### qa_chain.py

from langchain.chains import RetrievalQA
from langchain_openai import OpenAI  # ✅ MAJ


def initialize_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    llm = OpenAI(temperature=0)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    return qa_chain


def ask_question(qa_chain, question):
    return qa_chain.run(question)
    