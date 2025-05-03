# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pytesseract
import time
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from img2table.document import Image as IMG
from img2table.ocr import TesseractOCR
import re
import pandas as pd


#start timer for  program
start_time_program = time.time()
custom_config = r' -l eng --oem 3 --psm 6'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
ocr_engine = 'tesseract'
#table with all borders detection    
def Table_HR_VR_Line_ROI(image):
    #find the shape of imahe
    (height, width) = image.shape[:2]
    #keep copy of image to other variavles
    im_table = image.copy()
    table = image.copy()
    #convert to grayscale image
    image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #table roi initialize
    table_roi =[]
    #convert to binary image
    ret,thresh_value = cv2.threshold(image,220,255,cv2.THRESH_BINARY_INV)
    #create kernel of size 2 by 1
    kernel = np.ones((2,1),np.uint8)#with all lines //with horizontal lines kernel = np.ones((1,1),np.uint8)
    #dialtate image to fill broken part
    dilated_value = cv2.dilate(thresh_value,kernel,iterations = 5)
    #show dialated image in console
    plotting = plt.imshow(dilated_value,cmap='gray')
    plt.show()
    # Detect contours for following box detection
    contours, hierarchy = cv2.findContours(dilated_value, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #find table from the detected contours
    for c in contours:
        #find bounding box points
        x,y,w,h = cv2.boundingRect(c)
        #detect table with appropiate size
        if (int(width/1.5)<w<=width and int(width/15)<h):
            margin = 10
            im_table = cv2.rectangle(im_table,(x,y),(x+w,y+h),(0,255,0),4)
            #draw rextangle on detected table
            cv2.imwrite('table_ROI.jpg',im_table)
            table_roi.append( table[y-margin:y+h+margin, x-margin:x+w+margin])

    plotting = plt.imshow(im_table,cmap='gray')
    plt.show()
    return  table_roi

# Function to clean df
def clean_data(col):
    
    # Remove extra characters
    #text = col.replace('[Â]', '', regex=True) 
    
    return col.replace('\u00A0', '', regex=True) 

# Function to clean and convert dates
def clean_and_convert_date(date_str):
    #handle null values
    if pd.isnull(date_str):
        return None   
    # Remove extra characters and standardize format
    date_str = re.sub(r"[^a-zA-Z0-9,\n ]", "", date_str)    
    try:
        return pd.to_datetime(date_str, format='mixed' ).strftime('%d/%m/%Y')
    except ValueError:
        # Handle invalid dates 
        return date_str


                   
#Image to Text Convertor Module
def Image_To_Text(table):
    try:
        #decrease size of image
        #table = cv2.resize(img, None, fx=.7, fy=.7, interpolation=cv2.INTER_CUBIC)#increase resize
        # #create kernel of size 2 by 1
        # kernel = np.ones((1,1),np.uint8)#with all lines //with horizontal lines kernel = np.ones((1,1),np.uint8)
        # #dialtate image to fill broken part
        # table = cv2.dilate(table,kernel,iterations = 3)
        print('inside ocr')
        # cv2.imwrite('table.png',table)
        # image = IMG('table.png', detect_rotation=False)
        image = IMG(table, detect_rotation=False)
        # Instantiation of OCR
        if ocr_engine=='tesseract':
            ocr = TesseractOCR(n_threads=1, lang="eng")
        # Table extraction
        extracted_tables = image.extract_tables(ocr=ocr,
                                              implicit_rows= False,
                                              borderless_tables= True,
                                              min_confidence=50)
        #remove table image
        #os.remove('table.png')
        #post processing extracted table 
        if len(extracted_tables)!=0:
            #store extracted data in dataframe df
            df = extracted_tables[0].df
            print(df)
            #clean text
            df = df.apply(clean_data)
                        
    except Exception as e:
        print(str(e))
    total_time= (time.time() - start_time_program)
    print("--- %s Per Page Reading Time in seconds ---" % total_time)
    print('\n')
    return df

