# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 17:02:52 2024

@author: kalyan
"""

import pytesseract
import time
import os
import multiprocessing
from pdf2image import convert_from_path
import psutil
from tkinter import filedialog
from tkinter import *

#start timer for  program
start_time_program = time.time()
custom_config = r' -l eng --oem 3 --psm 3 '
#Set tesseract.exe full path. 
pytesseract.pytesseract.tesseract_cmd = r'E:\Program Files\Tesseract-OCR\tesseract.exe'
#========================Multiprocessing===============
def worker(image):
    #Performs OCR on an image and returns the text
    text = pytesseract.image_to_string(image,lang='eng', config=custom_config)
    return text
#==================== Image to Text Convertor Module  ============================
def Image_To_Text():
    global  input_folder
    #set input File path from from directory
    gui = Tk()
    input_folder_path = filedialog.askopenfilename()
    #destroy open file dialog
    gui.destroy() 
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
    #read all images of folder in loop and convert into text files
    file_path= input_folder_path.upper()
    if  file_path.endswith('.PDF'):
            pages_all = []
            #=================  pdf2image  ===========================
            #split out file name
            file_name=file_path[:-4].split('/')[-1]
            #convert pdf into image
            pages = convert_from_path(file_path, 350)
            page_number=len(pages)
            i = 1
            for page in pages:
                image_name = "Page_" + str(i) + ".tif"
                # Set the DPI
                dpi = (300.0, 300.0)
                page.save(image_name, "PNG", quality=100, dpi=dpi)                   
                pages_all.append( "Page_" + str(i) + ".tif")
                i = i+1    
            #set totalnumber of pages in file              
            all_file_page = all_file_page + page_number
            #============================START Reading Image in pool=====================
            # Create a pool of worker processes.
            pool = multiprocessing.Pool(core)
            # Submit the images to the pool for processing.
            results = pool.map(worker, pages_all)
            # Close the pool.
            pool.close()
            pool.join()
            print("Processing file " + file_path +" to text")
            # Process the results.
            for text in results:
                text =text.strip()
                #write file into text file
                try:
                    with open('Out_Text'+'/'+ file_name + ".txt", "a", encoding="utf-8") as f:
                      f.write(text)
                    f.close()
                except:
                    print('Error :')
                    pass         
            #Now remove temp image files
            for page in range(page_number):
                os.remove( "Page_" + str(page+1) + ".tif") 
            print('The text file is in folder: Out_Text')
    else:
        print('Select one pdf')
    
    total_time= (time.time() - start_time_program)
    if all_file_page>0:
        per_page_time=(total_time/all_file_page)
        print("--- %s Per Page Reading Time in seconds ---" % per_page_time)
    print('\n')


if __name__ == "__main__":
    Image_To_Text()
