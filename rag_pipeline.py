from dotenv import load_dotenv
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()

# Initialize embeddings and vector DB
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Initialize language model
llm = ChatOpenAI(model_name="gpt-4o-mini")

# QA chain with LangChain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

def answer_query(question: str):
    """Take a user question and return the LLM-generated answer + source docs."""
    response = qa_chain(question)
    return response["result"], response["source_documents"]

# For quick CLI testing
if __name__ == "__main__":
    q = "What is the password policy?"
    result, sources = answer_query(q)
    print("Answer:", result)
    print("\nSources:")
    for doc in sources:
        print("-", doc.page_content[:200])
