# -*- coding: utf-8 -*-
"""
Created on Sat May  3 11:47:50 2025

@author: kalya
"""

import streamlit as st
from PIL import Image
from ocr import Image_To_Text
import pandas as pd
import io
import os

st.title("🖼️ OCR Image to Table")

# Set folder path
IMAGE_FOLDER = "images"

# Supported image extensions
SUPPORTED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".tif", ".tiff")

# List available image files
image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(SUPPORTED_EXTENSIONS)]
image_files.insert(0, "-- Select an image --")


# Show dropdown menu
selected_file = st.selectbox("Choose an image:", image_files)
if selected_file != "-- Select an image --":
    image_path = os.path.join(IMAGE_FOLDER, selected_file)
    # Load and display image
    image = Image.open(image_path)
    #image_name = uploaded_image.name
    image_name = os.path.splitext(selected_file)[0]
    #st.write(image_path)
    st.image(image, caption=selected_file, use_column_width=True)

    # OCR the image
    with st.spinner("Performing OCR..."):
        df = Image_To_Text(image_path)
        df=df.reset_index(drop=True)
        # Try to convert text into DataFrame
        try:
            st.subheader("📊 Parsed Table:")
            st.dataframe(df, use_container_width=True)
            

        except Exception as e:
            st.error(f"Error parsing OCR output: {e}")
        if len(df) != 0:
            # Convert to Excel and add download button
            with io.BytesIO() as buffer:
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name="OCR_Data")
                    #writer.save()
                buffer.seek(0)

                st.download_button(
                    label="📥 Download as Excel",
                    data=buffer,
                    file_name=image_name.split('.')[0] +".xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.success("No text extracted!")
        
    
        


    
