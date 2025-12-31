import streamlit as st
from rag_core import research_agent

st.set_page_config("Diagnostics Research Agent")
st.title("🚗 ISO 14229 Diagnostics Research Agent")

query = st.text_input(
    "Ask diagnostics question (UDS, NRC, DTC, Services)"
)

if st.button("Research"):
     if query:
        with st.spinner("Running mandatory web + PDF research..."):
            try:
                answer = research_agent(query)
                st.markdown(answer)
            except Exception as e:
                st.error(
                    "❌ Web search is mandatory but failed.\n\n"
                    "Please check SERPAPI availability or try again."
                )