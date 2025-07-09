# AI-voice-reporting
This is a rich multi-featured AI driven document assistant.

📁 Folder Structure

ai_document_assistant/
│
├── main.py                         # 🌐 Streamlit app entry point
├── requirements.txt                # 📦 Python dependencies
├── .streamlit/
│   └── secrets.toml                # 🔐 API keys, email creds, etc.
│
├── utils/
│   ├── auth.py                     # 🔐 Login & session utils
│   ├── file_utils.py               # 📄 File upload & parsing (PDF/DOCX/XLSX)
│   ├── chat_utils.py               # 🤖 LLM QA chains + memory
│   ├── charts.py                   # 📊 Plotly chart builder
│   ├── email_utils.py              # 📧 Email summary sender
│   └── whatsapp_utils.py           # 💬 WhatsApp sender
│
├── user_data/
│   └── {username}/                 # 🗂️ Per-user uploaded docs
│       ├── vectorstore.faiss       # 🧠 Vector memory
│       └── summary.pdf             # 📃 Last summary/report
│
└── data/
    └── db.json                     # 🗃️ Maps users to uploaded docs


🧠 Architecture Summary
| Component       | Tech Used                             |
| --------------- | ------------------------------------- |
| Login/Auth      | Streamlit + session state / Auth0     |
| File Storage    | Local file system / S3                |
| Text Extraction | PyPDF2, python-docx, pandas           |
| Embedding       | HuggingFaceEmbeddings (FAISS backend) |
| LLM             | `flan-t5` / `mistral` + LangChain     |
| Charts          | `plotly`, `matplotlib`, `pandas`      |
| Memory          | `ConversationBufferMemory` or FAISS   |
| Email           | `smtplib`, `sendgrid`, `mailjet`      |
| WhatsApp        | `Twilio`, Meta Cloud API              |
| Voice           | `whisper`, `gTTS`, `st.audio_input()` |
