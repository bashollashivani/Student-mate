import streamlit as st
import os
from backend.pdf_processor import extract_text_from_pdf, chunk_text
from backend.embedder import EmbeddingManager
from backend.llm_answer import generate_answer

st.set_page_config(page_title="StudyMate – AI PDF Assistant", layout="wide")

st.title("📘 StudyMate – AI-Powered Academic Assistant")

st.subheader("Upload PDFs and ask questions from your study materials")

uploaded_files = st.file_uploader("Upload one or more PDFs", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    st.success("PDFs uploaded successfully!")

    if st.button("Process PDFs"):
        full_text = ""
        for file in uploaded_files:
            temp_path = f"temp_{file.name}"
            with open(temp_path, "wb") as f:
                f.write(file.read())

            full_text += extract_text_from_pdf(temp_path)
            os.remove(temp_path)

        st.session_state["chunks"] = chunk_text(full_text)
        st.session_state["embedder"] = EmbeddingManager()
        st.session_state["embedder"].build_faiss(st.session_state["chunks"])

        st.success("PDFs processed successfully! You can now ask questions.")

question = st.text_input("Ask a question from the PDFs:")

if st.button("Get Answer") and question:
    embedder = st.session_state.get("embedder")

    if embedder is None:
        st.error("Please upload and process PDFs first.")
    else:
        retrieved = embedder.search(question)
        answer = generate_answer(question, retrieved)

        st.subheader("📌 Answer")
        st.write(answer)

        st.subheader("🔍 Retrieved Context")
        for c in retrieved:
            st.info(c)
