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
pytesseract.pytesseract.tesseract_cmd = r'E:\Program Files\Tesseract-OCR\tesseract.exe'

def worker(image):
    #Performs OCR on an image and returns the text
    text = pytesseract.image_to_string(image,lang='eng', config=custom_config)
    print('text')
    return text
#============================================================ Image to Text Convertor Module  ================================================
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
            #=================================================================pdf2image================================================
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



'''
def CMD_Call():

    global    output_list,  log_folder, output_file, input_folder
    #Read input argument from CMD
    for i in range(len(sys.argv)):
        sys.argv[i] = sys.argv[i].replace("/", "\\")

    input_folder = os.path.join(sys.argv[2])
    input_folder_path = os.path.join(sys.argv[1],sys.argv[2])
    output_folder = sys.argv[3]
    output_list= sys.argv[1].split('\\')
    output_file = os.path.join(sys.argv[3],sys.argv[2] +".csv")
    #change escape characters
    input_folder_escape_replace = input_folder.replace('\\', '/')
    input_folder_path_escape_replace= input_folder_path.replace('\\', '/')
    output_folder_escape_replace= output_folder.replace('\\', '/')
    #log_folder_escape_replace = log_folder.replace('\\', '/')
    input_path = False
    out_path = False
    log_path = False
    #Check given paths are correct or not
    if os.path.exists(input_folder_path_escape_replace):
        input_path = True
    else:
        input_path = False
        LOG = 'input path| ' + input_folder_path + ' does not exist'
        #Error_Log(LOG)
        print('input path| ' + input_folder_path + ' does not exist')

    if os.path.exists(output_folder_escape_replace):
        out_path = True
    else:
        out_path = False
        os.makedirs(output_folder)

    #If all paths/folder exist call Image_To_Text()
    if input_path  :
        # Call Image_To_Text
        Image_To_Text(input_folder_path, output_folder)

    else:
        print('Error')

'''
if __name__ == "__main__":
    Image_To_Text()
