# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 13:38:53 2025

@author: kalya
"""

import streamlit as st
from PIL import Image
import pytesseract
from ocr_tesseract import Image_To_Text
import fitz

st.title("Medhi OCR")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "pdf"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image("File", caption="Uploaded File")
    except Exception as e:
        file_name = uploaded_file.name
        pdf_document = fitz.open(stream=uploaded_file.read(), repair=True)
        st.success("PDF file uploaded successfully!")
        st.write(f"Page count: {pdf_document.page_count}")
    ocr_text = ''
    if st.button("Run OCR"):
        st.info("Performing OCR...")
        progress_bar = st.progress(0)
        status_text = st.empty()  # To display status messages
        ocr_time, ocr_text = Image_To_Text(file_name, pdf_document, progress_bar)
        st.success("OCR Completed!")
        st.text_area("Extracted Text", ocr_text, height=300)
        st.write('Per page time of ocr ', round(ocr_time,2), ' second')
        # Specify the filename for the downloaded file
        filename = file_name.split('.')[0] + ".txt"
    if ocr_text != '':
        # Create the download button
        st.download_button(
            label="Download Text File",
            data=ocr_text,
            file_name=filename,
            mime="text/plain",
        )
        
