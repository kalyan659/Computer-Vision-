# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pytesseract
from img2table.document import Image as IMG
from img2table.ocr import TesseractOCR

custom_config = r' -l eng --oem 3 --psm 6'
ocr_engine = 'tesseract'
                   
#Image to Text Convertor Module
def Image_To_Text(table):
    try:
        image = IMG(table, detect_rotation=False)
        # Instantiation of OCR
        if ocr_engine=='tesseract':
            ocr = TesseractOCR(n_threads=1, lang="eng")
        # Table extraction
        extracted_tables = image.extract_tables(ocr=ocr,
                                              implicit_rows= False,
                                              borderless_tables= True,
                                              min_confidence=50)
        #post processing extracted table 
        if len(extracted_tables)!=0:
            #store extracted data in dataframe df
            df = extracted_tables[0].df
                        
    except Exception as e:
        print(str(e))
    return df

