
import streamlit as st
import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt
import tempfile
from io import BytesIO

st.set_page_config(page_title="ZAS Report Generator", layout="wide")

st.title("ZAS Financial Report Generator")
st.markdown("Upload your Excel file to generate a one-page PDF summary.")
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("Preview of Uploaded File")
    st.write(df.head())

    revenue = df[df['Account'].str.contains('Sales|Revenue', case=False, na=False)].sum(numeric_only=True)
    expenses = df[~df['Account'].str.contains('Sales|Revenue', case=False, na=False)].sum(numeric_only=True)
    kpis = {
        "Total Revenue": revenue.iloc[-1],
        "Total Expenses": expenses.iloc[-1],
        "Net Profit": revenue.iloc[-1] - expenses.iloc[-1]
    }

    st.subheader("Key Metrics")
    for k, v in kpis.items():
        st.write(f"**{k}**: {v:,.2f} KWD")

    st.subheader("Download Report")
    if st.button("Generate PDF"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="ZAS Financial Report", ln=True, align="C")
            for k, v in kpis.items():
                pdf.cell(200, 10, txt=f"{k}: {v:,.2f} KWD", ln=True)
            pdf.cell(200, 10, txt="Powered by ZAS – AlZayed Advisory Services", ln=True)
            pdf.output(tmpfile.name)
            with open(tmpfile.name, "rb") as f:
                st.download_button("Download PDF", f.read(), file_name="ZAS_Report.pdf")
