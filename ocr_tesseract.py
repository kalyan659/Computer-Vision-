# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 17:02:52 2024

@author: kalyan
"""

import pytesseract
import time
import os
import multiprocessing
import psutil
import fitz
import numpy as np
from PIL import Image
import io
import math

custom_config = r' -l eng --oem 3 --psm 3 '
#Set tesseract.exe full path. 
pytesseract.pytesseract.tesseract_cmd = r'c:\Program Files\Tesseract-OCR\tesseract.exe'
batch_size = 50
#========================Multiprocessing===============
def worker(image):
    #Performs OCR on an image and returns the text
    text = pytesseract.image_to_string(image,lang='eng', config=custom_config)
    return text
#==================== process in batch =========================
def batch_process(pages_all,  file_name, core, batch_size):
    global all_text
    print("Processed file " + file_name + " to image batch of " + str(batch_size))   
    #============================START Reading Image in pool=====================
    # Create a pool of worker processes.
    pool = multiprocessing.Pool(core)
    # Submit the images to the pool for processing.
    results = pool.map(worker, pages_all)
    # Close the pool.
    pool.close()
    pool.join()
    print("Processed file " + file_name +" to text batch of " + str(batch_size))
    # Process the results.
    for text in results:
        text =text.strip()
        all_text = all_text + '\n' + text
        #write file into text file
        try:
            with open('Out_Text'+'/'+ file_name + ".txt", "a", encoding="utf-8") as f:
              f.write(text)
            f.close()
        except:
            print('Error :')
            pass         
#==================== Image to Text Convertor Module  ============================
def Image_To_Text(file_path, pdf_document, progress_bar):
    global all_text
    all_text = ''
    #make a output folder for text output
    if os.path.exists('Out_Text'):
        pass
    else:
        os.makedirs('Out_Text')
    
    all_file_page=0
    per_page_time = 'NA'
    #count physical core
    core = psutil.cpu_count(logical=False)
    print('Physical Core: ',core)
    #start timer for  OCR
    start_time_program = time.time()
    if  file_path.upper().endswith('.PDF'):
            pages_all = []
            #=================  pdf2image  ===========================
            #split out file name
            file_name=file_path[:-4].split('/')[-1]
            # #convert pdf into image
            dpi = 300
            output_format = 'png'
            doc = pdf_document
            page_in_file = doc.page_count
            pages_all = []
            zoom = dpi / 72  # 72 is the default DPI of PDF
            mat = fitz.Matrix(zoom, zoom)
            batch_no = 1
            progress = 0
            for i, page in enumerate(doc, start=1):
                pix = page.get_pixmap(matrix=mat)
                #image_name = f"Page_{i}.{output_format}"
                #pix.save(image_name)
                # Convert pixmap to a PIL Image
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                # Convert the PIL Image to a NumPy array
                img = np.array(img)
                pages_all.append(img)
                # process first 50 pages
                if i%batch_size == 0:
                    batch_process(pages_all, file_name, core, batch_size)
                    progress = int((batch_no*batch_size) / page_in_file * 100)
                    progress_bar.progress(progress / 100.0)
                    batch_no = batch_no + 1
                    #reset pages
                    pages_all = []
                
            if len(pages_all)!=0:
                batch_process(pages_all, file_name, core, len(pages_all))
                print('progress----', progress)
                progress = progress + math.ceil((len(pages_all)) / page_in_file * 100)
                print('last--------',math.ceil((len(pages_all)) / page_in_file * 100))
                progress_bar.progress(progress / 100.0)
            all_file_page = all_file_page + page_in_file
            print('The text file is in folder: Out_Text')
    else:
        print('Select one pdf')
    
    total_time= (time.time() - start_time_program)
    if all_file_page>0:
        per_page_time=(total_time/all_file_page)
        print("--- %s Per Page Reading Time in seconds ---" % per_page_time)
    print('\n')
    return per_page_time, all_text


