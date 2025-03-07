import streamlit as st
import pandas as pd
from io import BytesIO
import os

# Set up the Streamlit app
st.set_page_config(page_title="Data Sweeper & Converter", layout='wide')

st.title("📀 Data Sweeper & Converter")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# File uploader
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read the uploaded file
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display file information
        st.markdown(f"**📔File Name:** {file.name}")
        st.markdown(f"**📝File Size:** {file.size / 1024:.2f} KB")

        # Show a preview of the DataFrame
        st.subheader("🔍 Preview the DataFrame")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("🛠 Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}", key=f"remove_duplicates_{file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}", key=f"fill_missing_{file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing Values have been Filled!")

        # Select specific columns to keep or convert
        st.subheader("📊 Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data visualization
        st.subheader("📈 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            if not df.select_dtypes(include='number').empty:
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
            else:
                st.warning("⚠️ No numeric columns available for visualization.")

        # Conversion options
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}", key=f"convert_{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Download button
            st.download_button(
                label=f"📥 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type,
                key=f"download_{file.name}"
            )

st.success("✅ All files processed!")