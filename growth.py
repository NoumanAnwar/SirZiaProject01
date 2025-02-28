import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS
st.markdown("""
<style>
.stApp {
    background-color: black;
    color: white;
}
</style>            
""", unsafe_allow_html=True)

# Title and description
st.title("Data Sweeper Sterling Integrator by Nouman Anwar")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for Quarter 3!")

# File upload
uploaded_files = st.file_uploader("Upload your files (accepts CSV and Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_ext = os.path.splitext(uploaded_file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(uploaded_file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # File details
        st.write("Preview the head of the DataFrame")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("Data Cleaning options")
        if st.checkbox(f"Clean data for {uploaded_file.name}"):

            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove duplicates from the file: {uploaded_file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values for {uploaded_file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns    
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled!")

        st.subheader("Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for {uploaded_file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data visualization
        st.subheader("Data visualization")
        if st.checkbox(f"Show visualization for {uploaded_file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion Options
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {uploaded_file.name} to:", ["CSV", "Excel"], key=uploaded_file.name)
        
        if st.button(f"Convert {uploaded_file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = uploaded_file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = uploaded_file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"Download {uploaded_file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type,
            )

st.success("All files processed successfully!")
