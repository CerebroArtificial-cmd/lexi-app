from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN") or os.getenv("HF_TOKEN")
CHAT_MODEL = os.getenv("CHAT_MODEL", "meta-llama/Llama-3.2-3B-Instruct")

_client = InferenceClient(model=CHAT_MODEL, token=HF_TOKEN)

SYSTEM_PROMPT = "Responda as perguntas de forma correta e precisa."

def ensure_system_first(messages):
    if not messages or messages[0].get("role") != "system":
        return [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    return messages

def abrir_chat(messages, temperature=0.7, top_p=0.9):
    """
    messages: lista de dicts [{"role":"system"|"user"|"assistant","content": "..."}]
    Retorna: string com a resposta do assistente.
    """
    msgs = ensure_system_first(messages)
    try:
        resp = _client.chat_completion(
            messages=msgs,
            temperature=temperature,
            top_p=top_p,
        )
        return resp.choices[0].message["content"]
    except TypeError:
        # compat com variantes antigas do huggingface_hub
        resp = _client.chat_completion(
            msgs,
            temperature=temperature,
            top_p=top_p,
        )
        return getattr(resp, "generated_text", str(resp))

# compat com código antigo
chat_reply = abrir_chat
