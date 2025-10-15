import streamlit as st
import requests

st.set_page_config(page_title="JaniGPT", layout="wide")

st.title("JaniGPT")
st.subheader("Ask a question about your documents")

# Left panel
left_col, center_col = st.columns([1, 3])
with left_col:
    uploaded_files = st.file_uploader("Upload your documents", accept_multiple_files=True, type=['pdf','docx'])
    if st.button("Process"):
        for file in uploaded_files:
            response = requests.post("http://127.0.0.1:8000/api/upload_file", files={"file": (file.name, file.getvalue())})
            st.write(response.json())

with center_col:
    query = st.text_area("Your Question", placeholder="Type your question here...")
    if st.button("Ask"):
        response = requests.post("http://127.0.0.1:8000/api/query", data={"question": query})
        st.write(response.json())
