# main.py
import streamlit as st
import tempfile
from utils import file_utils, chat_utils, charts, email_utils, whatsapp_utils
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import whisper
import os
import base64
import pandas as pd
import ssl
from huggingface_hub import login
from gtts import gTTS

from utils.auth import require_role
from textblob import TextBlob
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import (
    StuffDocumentsChain, LLMChain, ConversationalRetrievalChain
)
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import AIMessage, HumanMessage
import time


# RBA
if require_role(["admin", "user"]) and st.user.is_logged_in:
    st.error("UNAUTHORIZED ACCESS")
    st.stop()

# Auth & Init
with st.spinner("Connection to LLM.."):
    login(token=st.secrets["hf_token"])
    ssl._create_default_https_context = ssl._create_unverified_context

st.set_page_config(page_title="📄 AI Doc Chat", layout="centered")
st.subheader("🧠 Conversational Document Assistant")

with st.spinner("Caching..."):
    @st.cache_resource
    def load_llm():
        model_id = "google/flan-t5-base"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
        pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
        return HuggingFacePipeline(pipeline=pipe)


    @st.cache_resource
    def load_embeddings():
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


    @st.cache_resource
    def load_whisper():
        return whisper.load_model("base")


    llm = load_llm()

    embeddings = load_embeddings()

    asr_model = load_whisper()


# Correct spelling
def correct_spelling(text):
    return str(TextBlob(text).correct())


# Suggest follow-up questions
def suggest_questions(context, answer):
    suggestion_prompt = f"""
    Based on the following answer, suggest 3 related follow-up questions.\n\n
    Context: 
    {context}\n
    Answer: 
    {answer}
    """
    result = llm.invoke(suggestion_prompt)
    st.write(f'result of fillow up question : {result}')
    return result.strip().split("\n")


# Upload and extract
uploaded_files = st.file_uploader("📎 Upload files (PDF, DOCX, XLSX)", type=["pdf", "docx", "xlsx", "txt"],
                                  accept_multiple_files=True)
with st.spinner("Uploading and Indexing Document.."):
    if uploaded_files:
        all_text = ""
        excel_dfs = []
        for file in uploaded_files:
            filetype = file.name.split(".")[-1]
            if filetype == "txt":
                all_text += file_utils.extract_text_from_textfile(file)
            if filetype == "pdf":
                all_text += file_utils.extract_text_from_pdf(file)
            elif filetype == "docx":
                all_text += file_utils.extract_from_docx(file)
            elif filetype == "xlsx":
                df = pd.read_excel(file)
                all_text += file_utils.extract_from_excel(file)
                excel_dfs.append(df)

        splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
        chunks = splitter.create_documents([all_text])
        vectorstore = FAISS.from_documents(chunks, embeddings)
        retriever = vectorstore.as_retriever()

        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise."
            "\n\n"
            "{context}"
        )

        custom_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        history_aware_retriever = create_history_aware_retriever(
            llm=llm,
            retriever=retriever,
            prompt=contextualize_q_prompt,
        )

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        st.session_state.rag_chain = rag_chain
        st.session_state.excel_dfs = excel_dfs
        st.session_state.setdefault("chat_history", [])
        st.session_state.setdefault("voice_chat_history", [])
        st.session_state.voice_mode = False
        st.success("✅ Documents indexed. You can now chat below.")

# Chat Input
if "rag_chain" in st.session_state:
    mode = st.radio("Choose input mode", ["⌨️ Text", "🎙️ Voice"], horizontal=True)
    user_query = None

    if mode == "⌨️ Text":
        user_query = st.chat_input("Ask something about your docs...")
        # Display entire chat history
        if "chat_history" in st.session_state and st.session_state.rag_chain:
            for message in st.session_state.chat_history:
                if isinstance(message, HumanMessage):
                    st.chat_message("user").markdown(message.content)
                elif isinstance(message, AIMessage):
                    st.chat_message("assistant").markdown(message.content)

        if user_query:
            with st.spinner("💡 Thinking..."):
                st.chat_message("user").markdown(user_query)
                response = st.session_state.rag_chain.invoke({"input": user_query,
                                                              "chat_history": st.session_state.chat_history})
                st.session_state.chat_history.extend(
                    [
                        HumanMessage(content=user_query),
                        AIMessage(content=response["answer"]),
                    ]
                )
                # formatted_response = response.strip().replace("\n", "  \n")
                st.chat_message("assistant").markdown(response["answer"])
                st.rerun()

        for df in st.session_state.excel_dfs:
            charts.render_chart_from_query(user_query, df)

        # Email or WhatsApp
        if user_query:
            if "email" in user_query.lower():
                email_utils.send_email(
                    recipient=st.secrets["email_to"],
                    subject="📊 AI Summary",
                    body=response,
                    sender_email=st.secrets["email_user"],
                    sender_pass=st.secrets["email_pass"]
                )
                st.success("📧 Summary sent via email!")

            if "whatsapp" in user_query.lower():
                whatsapp_utils.send_whatsapp(
                    to_number=st.secrets["whatsapp_to"],
                    body=response,
                    account_sid=st.secrets["twilio_sid"],
                    auth_token=st.secrets["twilio_token"]
                )
                st.success("📲 Summary sent via WhatsApp!")

    elif mode == "🎙️ Voice":
        audio = st.audio_input("Speak your question")
        # Display entire chat history
        if "voice_chat_history" in st.session_state and st.session_state.rag_chain:
            for message in st.session_state.voice_chat_history:
                if isinstance(message, HumanMessage):
                    st.chat_message("user").markdown(message.content)
                elif isinstance(message, AIMessage):
                    st.chat_message("assistant").markdown(message.content)

        if audio:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio.getvalue())
            with st.spinner("🎧 Transcribing your voice..."):
                user_query = asr_model.transcribe(tmp.name)["text"]
                st.info(f"🗣️ You said: {user_query}")
            if user_query:
                with st.spinner("💡 Thinking..."):
                    response = st.session_state.rag_chain.invoke({"input": user_query,
                                                                  "chat_history": st.session_state.voice_chat_history})
                    st.chat_message("assistant").markdown(response["answer"])
                    st.session_state.voice_chat_history.extend(
                        [
                            HumanMessage(content=user_query),
                            AIMessage(content=response["answer"]),
                        ]
                    )

                    with st.spinner("🔊 Generating speech..."):
                        tts_path = os.path.join(os.getcwd(), "response.mp3")
                        gTTS(text=response["answer"]).save(tts_path)
                        with open(tts_path, "rb") as f:
                            audio_bytes = f.read()
                            b64 = base64.b64encode(audio_bytes).decode()
                            st.markdown(f"""
                                <audio  autoplay>
                                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                                </audio>
                            """, unsafe_allow_html=True)


