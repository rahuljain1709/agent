import streamlit as st
import os
from tavily_client import TavilyClient
from tavily_nosni import TavilyClientNoSNI
# other imports e.g. Researcher, GDriveUploader...

st.title("Research Assistant — Tavily + OpenAI + Google Drive")
query = st.text_input("Enter topic:")
max_results = st.slider("Number of articles", 1, 20, 5)

if st.button("Run research") and query:
    try:
        tav = TavilyClient(os.getenv("TAVILY_API_KEY"))
    except Exception as e:
        st.error("Tavily client init failed: " + str(e))
        st.stop()

    # Try normal TLS first
    results = None
    try:
        with st.spinner("Searching Tavily (normal TLS)..."):
            results = tav.search(query, max_results=max_results)
        st.success(f"Found {len(results)} articles")
    except Exception as e:
        err_msg = str(e)
        st.warning("Primary Tavily request failed: " + err_msg)
        st.info("Attempting diagnostic retry with No-SNI (temporary workaround)...")
        # Try No-SNI fallback
        try:
            tav_nosni = TavilyClientNoSNI(os.getenv("TAVILY_API_KEY"))
            with st.spinner("Searching Tavily (No-SNI fallback)..."):
                results = tav_nosni.search(query, max_results=max_results)
            st.success(f"Found {len(results)} articles (via No-SNI fallback)")
        except Exception as e2:
            st.error("Both normal and No-SNI requests failed. See logs for details.")
            st.write("Error (primary):", err_msg)
            st.write("Error (No-SNI):", str(e2))
            st.stop()

    # proceed with researcher/build doc/upload using `results`
    # ... your existing summarization/upload code ...
