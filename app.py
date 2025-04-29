import streamlit as st
import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt
import tempfile

st.set_page_config(page_title="ZAS Report Generator", layout="wide")

st.title("ZAS Financial Report Generator")
st.markdown("Upload your Excel file to generate a one-page PDF summary.")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, skiprows=3)
    df.columns = ["Account", "Mar 2025", "Feb 2025"]

    st.subheader("Preview of Uploaded File")
    st.write(df.head())

    # Revenue and Expenses filters
    revenue = df[df['Account'].str.contains('Trading|Sales|Revenue', case=False, na=False)].sum(numeric_only=True)
    expenses = df[~df['Account'].str.contains('Trading|Sales|Revenue', case=False, na=False)].sum(numeric_only=True)

    # Calculate KPIs
    kpis = {
        "Total Revenue": revenue.sum(),
        "Total Expenses": expenses.sum(),
        "Net Profit": revenue.sum() - expenses.sum()
    }

    st.subheader("Key Metrics")
    for k, v in kpis.items():
        st.write(f"**{k}**: {v:,.2f} KWD")

    st.subheader("Download Report")
    if st.button("Generate PDF"):

        # Clean text for Unicode-safe output
        def clean_text(s):
            return str(s).encode('latin-1', 'ignore').decode('latin-1')

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="ZAS Financial Report", ln=True, align="C")
            pdf.ln(10)
            for k, v in kpis.items():
                pdf.cell(200, 10, txt=clean_text(f"{k}: {v:,.2f} KWD"), ln=True)
            pdf.ln(10)
            pdf.cell(200, 10, txt=clean_text("Powered by ZAS – AlZayed Advisory Services"), ln=True)
            pdf.output(tmpfile.name, 'F')

            with open(tmpfile.name, "rb") as f:
                st.download_button("Download PDF", f.read(), file_name="ZAS_Report.pdf")
