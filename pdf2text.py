# Import libraries 
from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os 
import pandas as pd
from pytesseract import Output
import cv2
import numpy as np
import time




# Path of the pdf 
PDF_file = "pdf.pdf"
  
''' 
Part #1 : Converting PDF to images 
'''

# Counter to store images of each page of PDF to image 
image_counter = 1
header_offset = 80
footer_offset = 150 
first_page=10
last_page=943
step=20
total_pages=943
for i in range(first_page,last_page,step):
    pages = convert_from_path(PDF_file, dpi=200, first_page=i,last_page=min(i+step,last_page)) 
    # Store all the pages of the PDF in a variable 

  

  
    # Iterate through all the pages stored above 
    for page in pages: 
      
        # Declaring filename for each page of PDF as JPG 
        # For each page, filename will be: 
        # PDF page 1 -> page_1.jpg 
        # PDF page 2 -> page_2.jpg 
        # PDF page 3 -> page_3.jpg 
        # .... 
        # PDF page n -> page_n.jpg 
        filename = "page_"+str(image_counter)+".jpg"
        page=page.crop((0, header_offset, page.width, page.height-footer_offset))
        # Save the image of the page in system 
        page.save(filename, 'JPEG') 
        print (f'page {image_counter} is saved')
      
        # Increment the counter to update filename 
        image_counter = image_counter + 1
      
''' 
Part #2 - Recognizing text from the images using OCR 
'''
# Variable to get count of total number of pages 
filelimit = image_counter-1
  
# Creating a text file to write the output 
#outfile = "out_text.txt"
  
# Open the file in append mode so that  
# All contents of all images are added to the same file 
#f = open(outfile, "a") 



defined=0  
# Iterate from 1 to total number of pages 
for i in range(1, filelimit + 1): 
  
    # Set filename to recognize text from 
    # Again, these files will be: 
    # page_1.jpg 
    # page_2.jpg 
    # .... 
    # page_n.jpg 
    filename = "page_"+str(i)+".jpg"
    print(f'reading page {i}...')
          
    # Recognize the text as dictionary in image using pytesserct 
    text = (pytesseract.image_to_data(Image.open(filename), config='-c preserve_interword_spaces=1 --oem 1 --psm 1 -l nld', output_type=Output.DICT))
    
    if defined==0:
        df=pd.DataFrame(text)
        defined=1
    else:

        df=df.append(pd.DataFrame(text))


    
'''
    # clean up blanks
    df1 = df[(df.conf!='-1')&(df.text!=' ')&(df.text!='')]
    # sort blocks vertically
    sorted_blocks = df1.groupby('block_num').first().sort_values('top').index.tolist()

    for block in sorted_blocks:
        curr = df1[df1['block_num']==block]
        sel = curr[curr.text.str.len()>3]
        most_left=sel.left.min()
        char_w = (sel.width/sel.text.str.len()).mean()
        prev_par, prev_line, prev_left = 0, 0, 0
        text = ''

        for ix, ln in curr.iterrows():
            # add new line when necessary
            if prev_par != ln['par_num']:
                text += '\n'
                prev_par = ln['par_num']
                prev_line = ln['line_num']
                prev_left = 0
            elif prev_line != ln['line_num']:
                text += '\n'
                prev_line = ln['line_num']
                prev_left = 0

            added = 0  # num of spaces that should be added
            if ln['left']/char_w > prev_left + 1:
                added = int((ln['left']-most_left)/char_w) - prev_left
                text += ' ' * added 
            text += ln['text'] + ' '

            prev_left += len(ln['text']) + added + 1
        text += '\n'

        f.write(text) 
'''
#df1 = df[(df.conf!='-1')&(df.text!=' ')&(df.text!='')&(len(df.text)>=2)]
df1 = df[(df.conf!='-1')&(df.text.str.len()>=2)][['line_num','text']]

df1.to_csv('out.csv', index=False)    
# Close the file after writing all the text. 

#f.close() 