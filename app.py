import streamlit as st
import os
from tavily_client import TavilyClient
from summarizer import Researcher
from gdrive_uploader import GDriveUploader

st.title("Research Assistant — Tavily + OpenAI + Google Drive")

query = st.text_input("Enter topic:")
max_results = st.slider("Number of articles", 1, 20, 5)

if st.button("Run research") and query:
    tav = TavilyClient(os.getenv("TAVILY_API_KEY"))
    with st.spinner("Searching web..."):
        results = tav.search(query, max_results=max_results)
    st.success(f"Found {len(results)} articles")

    researcher = Researcher(os.getenv("OPENAI_API_KEY"))
    with st.spinner("Summarizing & generating .docx"):
        doc_bytes, filename = researcher.build_document(query, results)

    st.download_button("Download document", doc_bytes, filename)

    if st.button("Upload to Google Drive"):
        uploader = GDriveUploader(os.getenv("GOOGLE_CREDENTIALS_JSON"),
                                 os.getenv("GOOGLE_DRIVE_FOLDER_ID"))
        file_id = uploader.upload_bytes(doc_bytes, filename)
        st.success(f"Uploaded to Google Drive (file_id: {file_id})")
