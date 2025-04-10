import streamlit as st
from pdf_utils import extract_text_from_pdf
from diff_utils import get_diff, highlight_diff, summarize_diff

st.set_page_config(page_title="PDF Comparison Tool", layout="wide")

st.title("📄 PDF Comparison Tool")
st.write("Upload two PDF files to compare and visualize their differences.")

# File upload
pdf1 = st.file_uploader("Upload First PDF", type="pdf", key="pdf1")
pdf2 = st.file_uploader("Upload Second PDF", type="pdf", key="pdf2")

if pdf1 and pdf2:
    with st.spinner("Extracting and comparing text..."):
        text1 = extract_text_from_pdf(pdf1)
        text2 = extract_text_from_pdf(pdf2)

        diff = get_diff(text1, text2)
        summary = summarize_diff(diff)
        highlighted = highlight_diff(diff)

    st.subheader("📝 Summary of Changes")
    st.write(f"- ✅ Added: **{summary['Added']}** words")
    st.write(f"- ❌ Removed: **{summary['Removed']}** words")
    st.write(f"- ⚠️ Modified: **{summary['Modified']}** words")

    st.subheader("🔍 Comparison Result")
    st.markdown(highlighted, unsafe_allow_html=True)
