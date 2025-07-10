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

# Auth & Init
login(token=st.secrets["hf_token"])
ssl._create_default_https_context = ssl._create_unverified_context

st.set_page_config(page_title="📄 AI Doc Chat", layout="wide")
st.title("🧠 Conversational Document Assistant")


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

# Upload and extract
uploaded_files = st.file_uploader("📎 Upload files (PDF, DOCX, XLSX)", type=["pdf", "docx", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    all_text = ""
    excel_dfs = []
    for file in uploaded_files:
        filetype = file.name.split(".")[-1]
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
    qa_chain = chat_utils.create_qa_chain(llm, retriever)
    st.session_state.qa_chain = qa_chain
    st.session_state.excel_dfs = excel_dfs
    st.success("✅ Documents indexed. You can now chat below.")

# Chat Input
if "qa_chain" in st.session_state:
    mode = st.radio("Choose input mode", ["⌨️ Text", "🎙️ Voice"], horizontal=True)
    user_query = None

    if mode == "⌨️ Text":
        user_query = st.chat_input("Ask something about your docs...")
    else:
        audio = st.audio_input("Speak your question")
        if audio:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio.getvalue())
                user_query = asr_model.transcribe(tmp.name)["text"]
                st.info(f"🗣️ You said: {user_query}")

    if user_query:
        st.chat_message("user").markdown(user_query)
        response = st.session_state.qa_chain.run(user_query)
        st.chat_message("assistant").markdown(response)

        # Autoplay voice
        tts_path = os.path.join(os.getcwd(), "response.mp3")
        gTTS(text=response).save(tts_path)
        with open(tts_path, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
            st.markdown(f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            """, unsafe_allow_html=True)

        # Chart from Excel if applicable
        for df in st.session_state.excel_dfs:
            charts.render_chart_from_query(user_query, df)

        # Email or WhatsApp
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
