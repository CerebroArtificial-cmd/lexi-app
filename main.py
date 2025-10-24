# main.py
import streamlit as st
from hfapi_summarization import resumir
from hfapi_textgeneration import gerar_texto
from hfapi_chatcompletion import abrir_chat as abrir_chat_api, SYSTEM_PROMPT


# -----------------------------
# Helpers de UI
# -----------------------------
def _title():
    # Dica: set_page_config deve ser chamado antes de criar qualquer elemento de UI
    st.set_page_config(page_title="HashIAs", page_icon="✨")
    st.header("HashIAs", divider=True)
    st.markdown("#### Selecione a IA que mais te ajuda, envie seu prompt e seja feliz")


# -----------------------------
# GERAR TEXTO
# -----------------------------
def interface_gerar_texto():
    st.markdown("**Geração de texto**")
    st.caption("Peça para que o sistema gere um texto para você.")
    prompt = st.chat_input("Digite aqui seu prompt")
    if not prompt or not prompt.strip():
        st.info("Digite um prompt acima para gerar o texto.")
        return
    with st.spinner("Gerando texto..."):
        try:
            texto_resposta = gerar_texto(prompt.strip())
            st.write(texto_resposta)
        except Exception as e:
            st.error(f"Erro ao gerar texto: {type(e).__name__}: {e}")


# -----------------------------
# RESUMIR TEXTO
# -----------------------------
def interface_resumir_texto():
    st.markdown("**Resumo de texto**")
    st.caption("Cole abaixo o texto que deseja resumir.")
    texto = st.text_area(
        "Cole aqui o texto para resumir",
        height=220,
        placeholder="Cole um texto longo aqui..."
    )
    if st.button("Resumir", type="primary"):
        if not texto or not texto.strip():
            st.info("Cole um texto para resumir.")
            return
        with st.spinner("Resumindo..."):
            try:
                texto_resposta = resumir(texto.strip())
                st.write(texto_resposta)
            except Exception as e:
                st.error(f"Erro ao resumir: {type(e).__name__}: {e}")


# -----------------------------
# CHAT (interface Streamlit)
# -----------------------------
def abrir_chat():
    st.markdown("**Chat**")
    st.caption("Converse com a IA. O histórico fica visível abaixo.")

    # Estado inicial do chat
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    # Renderiza histórico (pula a system)
    for msg in st.session_state.chat_messages:
        if msg["role"] == "system":
            continue
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Entrada do usuário
    user_msg = st.chat_input("Digite sua mensagem")
    if user_msg and user_msg.strip():
        # adiciona a msg do usuário
        st.session_state.chat_messages.append(
            {"role": "user", "content": user_msg.strip()}
        )
        with st.chat_message("user"):
            st.write(user_msg.strip())

        # chama o modelo e mostra a resposta
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    # limite de histórico para caber no contexto
                    history = st.session_state.chat_messages[-12:]  # system + últimas 11
                    answer = abrir_chat_api(history)  # sem max_tokens para evitar bugs
                except Exception as e:
                    answer = f"Erro: {type(e).__name__}: {e}"
            st.write(answer)

        # salva resposta no histórico
        st.session_state.chat_messages.append(
            {"role": "assistant", "content": answer}
        )


# -----------------------------
# APP
# -----------------------------
def main_app():
    _title()

    opcoes = ["Gerar Texto", "Resumir Texto", "Abrir Chat"]
    ferramenta_selecionada = st.selectbox(
        "Selecione a ferramenta de IA que você vai usar",
        options=opcoes,
        index=0
    )

    if ferramenta_selecionada == "Gerar Texto":
        interface_gerar_texto()

    elif ferramenta_selecionada == "Resumir Texto":
        interface_resumir_texto()

    else:  # Abrir Chat
        abrir_chat()


if __name__ == "__main__":
    main_app()

