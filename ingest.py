import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import openai
ASSETS_DIR = "./assets"
INDEX_PATH = "./faiss_index"
# Load OpenAI API key
load_dotenv()
#print(os.getenv("OPENAI_API_KEY")) 
api_key = os.getenv("OPENAI_API_KEY")
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Step 1: Load and extract text from PDF
def load_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"
    return full_text


# Step 2: Split text into chunks
def split_text(text, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap
)
    return splitter.split_text(text)


# Step 3: Create embeddings and store in FAISS
# Process all PDFs in /assets and build vector DB
def ingest_all_pdfs():
    texts = []
    metadatas = []

    for filename in os.listdir(ASSETS_DIR):
        if filename.endswith(".pdf"):
            path = os.path.join(ASSETS_DIR, filename)
            print(f"📄 Ingesting: {filename}")
            text = load_pdf_text(path)
            chunks = split_text(text)

            texts.extend(chunks)
            metadatas.extend([{"source": filename}] * len(chunks))

    print(f"🧠 Total chunks to embed: {len(texts)}")
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts, embedding=embeddings, metadatas=metadatas)
    vectorstore.save_local(INDEX_PATH)
    print(f"✅ Vector store saved at: {INDEX_PATH}")



if __name__ == "__main__":
    ingest_all_pdfs()
    #print(chunks)  # For debugging purposes