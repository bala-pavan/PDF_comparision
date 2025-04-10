from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from pdf_utils import extract_text_from_pdf
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os

# Load environment variables
load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyBwwz3Zp8QHUeKoPzYVuhj4DfesL5gGW5U"

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
)

st.set_page_config(page_title="Gemini PDF Comparison", layout="wide")

st.title("📄 PDF Comparison with Gemini LLM")
st.write("Upload two PDF files. Gemini will summarize the differences.")

pdf1 = st.file_uploader("Upload First PDF", type="pdf", key="pdf1")
pdf2 = st.file_uploader("Upload Second PDF", type="pdf", key="pdf2")

if pdf1 and pdf2:
    with st.spinner("Extracting and analyzing..."):
        text1 = extract_text_from_pdf(pdf1)
        text2 = extract_text_from_pdf(pdf2)

        prompt = f"""

        Compare the following two documents and show the differences in a readable plain text format.



Compare the content between the two documents below. Your tasks:
1. Highlight **added content** in green.
2. Highlight **removed content** in red.
3. Highlight **modified content** in yellow.
4. Generate a summary with total counts of added, removed, and modified items.

Return results side by side

--- Document 1 (Old) ---
{text1}

--- Document 2 (New) ---
{text2}
"""

        # Send prompt using LangChain's invoke method
        response = llm.invoke([HumanMessage(content=prompt)])
        output = response.content

    st.subheader("📝 Gemini Summary of Differences")
    st.markdown(output, unsafe_allow_html=True)
