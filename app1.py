
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from pdf_utils import extract_text_from_pdf
from langchain_core.messages import HumanMessage
import os
import base64

# Load environment variables
load_dotenv()

# load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyBwwz3Zp8QHUeKoPzYVuhj4DfesL5gGW5U"

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
)


# Streamlit page config
st.set_page_config(page_title="Gemini PDF Comparison", layout="wide")

st.title("📄 PDF Comparison with Gemini LLM")
st.write("Upload two PDF files. Gemini will summarize the differences.")

# PDF upload
pdf1 = st.file_uploader("Upload First PDF (Old)", type="pdf", key="pdf1")
pdf2 = st.file_uploader("Upload Second PDF (New)", type="pdf", key="pdf2")

if pdf1 and pdf2:
    with st.spinner("Extracting and analyzing..."):
        # Extract text
        text1 = extract_text_from_pdf(pdf1)
        text2 = extract_text_from_pdf(pdf2)

        # Side-by-side PDF preview
        st.markdown("### 📑 Side-by-Side PDF Preview and Extracted Text")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📄 Old PDF (Document 1)")
            st.download_button("Download PDF 1", data=pdf1.getvalue(), file_name=pdf1.name)
           # Display PDF 1
            base64_pdf1 = base64.b64encode(pdf1.getvalue()).decode("utf-8")
            pdf_display1 = f'<iframe src="data:application/pdf;base64,{base64_pdf1}" width="100%" height="600" type="application/pdf"></iframe>'
            st.markdown(pdf_display1, unsafe_allow_html=True)

            with st.expander("📝 Extracted Text from Document 1"):
                st.text(text1[:2000])

        with col2:
            st.markdown("#### 📄 New PDF (Document 2)")
            st.download_button("Download PDF 2", data=pdf2.getvalue(), file_name=pdf2.name)
            # Display PDF 2
            base64_pdf2 = base64.b64encode(pdf2.getvalue()).decode("utf-8")
            pdf_display2 = f'<iframe src="data:application/pdf;base64,{base64_pdf2}" width="100%" height="600" type="application/pdf"></iframe>'
            st.markdown(pdf_display2, unsafe_allow_html=True)

            with st.expander("📝 Extracted Text from Document 2"):
                st.text(text2[:2000])
        # Prepare the prompt
        prompt = f"""
You are a document comparison assistant.

Compare the content between the two documents below.

Instructions:
Tasks:
1. Highlight <span style="background-color:lightgreen">added content</span>.
2. Highlight <span style="background-color:#ffcccb">removed content</span>.
3. Highlight <span style="background-color:yellow">modified content</span>.
4. At the top, include a summary count: number of added, removed, and modified items.
5. Provide a side-by-side comparison if possible.
6. Generate a **summary** with counts of added, removed, and modified items.

Please return only HTML with inline styles — no Markdown or code formatting.


--- Document 1 (Old Version) ---
{text1}

--- Document 2 (New Version) ---
{text2}
"""

        # Send to Gemini
        response = llm.invoke([HumanMessage(content=prompt)])
        output = response.content

    # Output section
    st.subheader("📝 Gemini Summary of Differences")
    with st.expander("Show Comparison Results"):
        st.markdown(output, unsafe_allow_html=True)
