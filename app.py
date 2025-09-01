import streamlit as st
from rag_pipeline import answer_query
import os

st.set_page_config(page_title="GovDoc Q&A", page_icon="📄", layout="centered")

# ---- Title Area ----
st.markdown(
    """
    <div style="text-align: center;">
        <h1>📄 Ask Questions About Government Policies</h1>
        <p style="font-size:16px;">Upload internal documents and ask natural language questions to get quick answers.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---- Question Input ----
with st.container():
    st.markdown("### 🧠 Ask a Question")
    question = st.text_input(
        "Enter your question:",
        placeholder="e.g. What is the approval process for purchases over $50,000?",
        label_visibility="collapsed"
    )

    ask_btn = st.button("🔎 Get Answer")

# ---- Response Area ----
if ask_btn and question:
    with st.spinner("🔍 Analyzing the document and formulating a response..."):
        try:
            answer, sources = answer_query(question)
            st.success("✅ Answer:")
            st.markdown(f"<div style='font-size:18px; padding: 10px; background-color:#f9f9f9; border-left: 4px solid #36a64f;'>{answer}</div>", unsafe_allow_html=True)

            with st.expander("📚 View Source Document Excerpts"):
                for i, doc in enumerate(sources):
                    source_name = doc.metadata.get("source", "[unknown source]")
                    st.markdown(f"**Source {i+1}: `{source_name}`**")
                    st.markdown(f"> {doc.page_content.strip()[:500]}...")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

st.markdown("---")

# ---- Document Preview and Download ----
st.markdown("### 📁 Preview Sample Documents")
assets_dir = "assets"
available_docs = [f for f in os.listdir(assets_dir) if f.endswith(".pdf")]
selected_doc = st.selectbox("Choose a document to view/download:", available_docs)

if selected_doc:
    file_path = os.path.join(assets_dir, selected_doc)
    with open(file_path, "rb") as f:
        st.download_button(
            label=f"⬇️ Download {selected_doc}",
            data=f,
            file_name=selected_doc,
            mime="application/pdf"
        )

st.markdown("---")

# ---- Footer ----
st.markdown(
    """
    <div style="text-align: center; font-size: 13px; margin-top: 20px;">
        Built by <b>Maurice J. Colon</b> – Baltimore, MD<br>
        <i>Powered by LangChain + FAISS + OpenAI</i>
    </div>
    """,
    unsafe_allow_html=True
)

