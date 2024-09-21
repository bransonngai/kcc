# -*- coding: utf-8 -*-
"""
Created on 18/9/2024 13:13

@author: TraderB
"""
file_path = 'C:\\Users\\tHOMAS\\我的雲端硬碟 (branson.ngai@gmail.com)\\KoboTest\\龍珠(完全版)卷_01.epub'

# change the file name from epub extension to zip extension in local disk
import os
import zipfile

# if epub file exists, rename the file extension to zip
if os.path.exists(file_path):
    os.rename(file_path, file_path.replace('.epub', '.zip'))

# unzip the file
with zipfile.ZipFile(file_path.replace('.epub', '.zip'), 'r') as zip_ref:
    zip_ref.extractall(file_path.replace('.epub', ''))
    # # remove the zip file
    # os.remove(file_path.replace('.epub', '.zip'))

# refer to the extracted file folder
extracted_folder = file_path.replace('.epub', '')

# read the html folder by filename sequence, read the image file name in the html code
import os
import re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

# read the html file
def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# read the image file name in the html code
def read_image_file_name(html_code):
    soup = BeautifulSoup(html_code, 'html.parser')
    return [img['src'] for img in soup.find_all('img')]

# loop through the extracted folder to read the html file and image file name
html_files = [f for f in os.listdir(extracted_folder + '/html') if f.endswith('.html')]

# read the html file and image file name

# filter the html file name with digit only
html_files = [f for f in html_files if re.match(r'\d+', f.split('.')[0])]

# sort it
html_files = sorted(html_files, key=lambda x: int(x.split('.')[0]))

image_file_names = []
for html_file in html_files:
    html_code = read_html_file(extracted_folder + '/html/' + html_file)
    image_file_names.extend(read_image_file_name(html_code))

# change the filename by sequence locally, replace the digit part of the filename with sequence number
def change_filename_by_sequence(file_path, sequence):
    file_name = os.path.basename(file_path)
    return os.path.join(os.path.dirname(file_path), re.sub(r'\d+', str(sequence).zfill(7), file_name))

# change the image file name by sequence
for i, image_file_name in enumerate(image_file_names):
    if 'cover.png' not in image_file_name:
        os.rename(extracted_folder + image_file_name.replace('..', '').replace('/', '\\'),
                  change_filename_by_sequence(extracted_folder + image_file_name.replace('..', '').replace('/', '\\'), i))

# remove createby.png in the folder, if exists
if os.path.exists(extracted_folder + '/image/createby.png'):
    os.remove(extracted_folder + '/image/createby.png')

# zip the folder, rename the zip back to epub
with zipfile.ZipFile(file_path.replace('.epub', '.zip'), 'w') as zip_ref:
    for root, dirs, files in os.walk(extracted_folder):
        for file in files:
            zip_ref.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(extracted_folder, '..')))


# remove the extracted folder
os.remove(extracted_folder)
