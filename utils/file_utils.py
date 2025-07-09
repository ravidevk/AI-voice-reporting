import pandas as pd
from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    return "\n".join([page.extract_text() or "" for page in reader.pages])

def extract_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_from_excel(file):
    df = pd.read_excel(file)
    return "\n".join(df.astype(str).apply(lambda x: " | ".join(x), axis=1).tolist())