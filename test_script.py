from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

# Load your .env file
load_dotenv()

# Initialize the embedding model and load your vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)

# Set up the retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Set up the LLM
llm = ChatOpenAI(model_name="gpt-4o-mini")

# Build RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# Example query
query = "What are the rules for emergency procedures in procurement?"
response = qa_chain(query)

# Print answer and sources
print("Answer:", response["result"])
print("\n--- Sources ---")
for doc in response["source_documents"]:
    print(doc.page_content[:300], "\n")