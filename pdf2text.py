# Import libraries 
from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os 
import pandas as pd
from pytesseract import Output
import numpy as np
import time




# Path of the pdf 
PDF_file = "pdf.pdf"
  
''' 
 Converting PDF to images 
'''

# Counter to store images of each page of PDF to image 
image_counter = 1
header_offset = 80
footer_offset = 150 
first_page=10
last_page=943
step=20 # to avoid memory allocation errors we process "step" pages at a time
for i in range(first_page,last_page,step):
    pages = convert_from_path(PDF_file, dpi=200, first_page=i,last_page=min(i+step,last_page)) 
    # Store all the pages of the PDF in a variable 

  

  
    # Iterate through all the pages stored above 
    for page in pages: 
      

        # PDF page n -> page_n.jpg 
        filename = "page_"+str(image_counter)+".jpg"
        page=page.crop((0, header_offset, page.width, page.height-footer_offset))
        page.save(filename, 'JPEG') 
        print (f'page {image_counter} is saved')
      
        # Increment the counter to update filename 
        image_counter = image_counter + 1
      
''' 
Recognizing text from the images using OCR 
'''
# Variable to get count of total number of pages 
filelimit = image_counter-1
  




defined=0  
# Iterate from 1 to total number of pages 
for i in range(1, filelimit + 1): 
  
    # Set filename to recognize text from 
    # page_n.jpg 
    filename = "page_"+str(i)+".jpg"
    print(f'reading page {i}...')
          
    # Recognize the text as dictionary using pytesserct 
    text = (pytesseract.image_to_data(Image.open(filename), config='-c preserve_interword_spaces=1 --oem 1 --psm 1 -l nld', output_type=Output.DICT))
    
    if defined==0:
        df=pd.DataFrame(text)
        defined=1
    else:

        df=df.append(pd.DataFrame(text))


    
#a bit of cleaning (some artefacts and the words that a too short to be meaningfull)
df1 = df[(df.conf!='-1')&(df.text.str.len()>=2)][['line_num','text']]

df1.to_csv('out.csv', index=False)    
