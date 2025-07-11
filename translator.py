
from langchain_openai import ChatOpenAI

def translate_text(text: str, target_lang: str) -> str:
    system_prompt = f"You are a professional translator. Translate the following text into {target_lang}."
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    result = llm.predict(f"{system_prompt}\n\n{text}")
    return result
