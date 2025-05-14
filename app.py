import streamlit as st
import pandas as pd

st.set_page_config(page_title="INC to CSV Converter", page_icon="📄")

st.title("📄 INC to CSV File Converter")
st.markdown("Upload your `.INC` file and download it as `.CSV`.")

uploaded_file = st.file_uploader("Choose an INC file", type="inc")

if uploaded_file is not None:
    try:
        content = uploaded_file.read().decode("utf-8")
        lines = content.strip().split("\n")
        data = [line.strip().split() for line in lines]
        df = pd.DataFrame(data)

        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", csv, "converted.csv", "text/csv")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
