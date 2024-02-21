
''' 
this is v1 version of this script. It barely does more than just taking the image of each page, doing ocr, and then storing it back into
the doc format. After this it should be passed through calibre for mobi or awz conversion.
This script is very primitive and not organized. Should work on the future. Things to be worked on:
    * resize the scanning area of pytesseracdt to miss the page numbers that are present in the pages (should be parameterized for individual pdfs)
        * First part done, cropping of image is possible, the parameterization is still left
    * Try to figure out a way to retain all the formatting in the format of an epub preferabley for better conversion tactics
    * Figure out chapters and headers, and add them to the pages in the list
    * Use better code for writing this lol
    * Using logging library to log each page
'''

# Importing all required libs
import os
from PIL import Image,ImageOps
import pytesseract

from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from docx import Document
import sys
import logging
import argparse

parser = argparse.ArgumentParser(description='OCR conversion of ಕನ್ನಡ books')
parser.add_argument('--inputBookName',type=str,help='Name of the book to be converted')
parser.add_argument('--outputBookName',type=str,help='Name of the output file to be saved')

args = parser.parse_args()

BookName = args.inputBookName
OutDocName = args.outputBookName
# BookName = 'MAILA ANCHAL - KANNADA - RENU.pdf' # can be changed to anything, maybe using sys library,activate  for gaining the variables
# OutDocName = 'Test3.docx'
here = os.path.dirname(os.path.abspath(__file__)) # getting current directory, this seems to work only in my env
images = convert_from_path(here+'\\'+BookName,fmt='jpeg',output_folder=here+'\ocroutput\p3') # more parameters can be checked from https://pypi.org/project/pdf2image/

OutDoc = Document()

#arbitrary definition of border for cropping image (currently crops lower parts for books with lower page numbers, different for upper pages)
border = (0,70,0,0)

#parsing through each of the pages and then adding them to the document
for pages in images:
    # cropping the image to remove page numbers
    t = ImageOps.crop(pages,border)
    # t.show()
    # running the ocr to extra string from the image
    words = pytesseract.image_to_string(t,lang='kan').replace('\n\n','NewLine').replace('\n','').replace('NewLine','\n\n') # hilariously stupid logic, but it works, and I don't have time to learn regex
    # adding the string to the document as paragrphs
    # print(words)
    OutDoc.add_paragraph(words)

#saving the output
OutDoc.save(here+'\\'+OutDocName)
