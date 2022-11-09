import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.color import rgb2gray, label2rgb
from skimage.filters import threshold_otsu
from skimage.morphology import area_opening, disk, binary_closing
from skimage.measure import find_contours, label, regionprops_table
import streamlit as st
import pandas as pd
from PIL import Image
import os as os

images_path = 'seeds/Seeds_Double_Check_Images/'
folder_path = 'output/data/'
filename = folder_path + 'data.csv'
    
def app():
   
    ID = st.text_input('SCAN QR CODE IN LABEL')
    GRAIN_WEIGHT = st.number_input('Mass of the grains sample (g)')
    #STAGE = st.selectbox('STAGE', ['F6', 'F105', 'SD'])
    picture = st.file_uploader("Upload Grains Picture")

    if picture:
        st.image(picture)
        RGB = mpimg.imread(picture)
        I = rgb2gray(RGB)
        # Apply Otsu's method
        global_threshold  = threshold_otsu(I)
        BW = I < global_threshold
        #Smoothing 
        #Remove small areas
        BW = area_opening(BW, area_threshold = 1000, connectivity=2)
        # CLosing operation (Connects small patches of True pixels)
        BW = binary_closing(BW, disk(5))
        contours = find_contours(BW,0)
        seed_num = len(contours)
        TKW = (GRAIN_WEIGHT/seed_num)*1000 #introduce fx for defining tkw 
        
        plt.imshow(BW, cmap = 'gray')
        plt.axis('off')
        for contour in contours:
            plt.plot(contour[:,1], contour[:,0], '-r', linewidth = 1)
        plt.savefig(f'image_test.jpg')
        
    if st.button('Check Grains Arrangement'):
        seeds = Image.open(f'image_test.jpg')
        st.image(seeds)
        
       
      
    if st.button('LOAD TKW DATAPOINT'):
         
        TRIAL, SITE, YEAR, SAMPLING, PLOT = ID.split('-')
        
        prev_year = 2000 + int(YEAR) - 1
        year_folder = f'SEASON {prev_year}-{YEAR}'
        folder_path = f'../{year_folder}/01-Data/{TRIAL}'
        
        filename = f'{folder_path}/{TRIAL}.csv'
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        if not os.path.isfile(f'{filename}'): 
            df_create = pd.DataFrame(columns = ['ID', 'TRAIT', 'VALUE', 'TRIAL','SITE', 'YEAR', 'SAMPLING', 'PLOT'])
            df_create.to_csv(filename, index = False)      
        
        df = pd.read_csv(filename)
        
        values_to_add = {'ID': [ID], 'TRAIT': ['TKW'], 'VALUE':[TKW], 'TRIAL':[TRIAL], 'SITE':[SITE], 'YEAR':[YEAR], 'SAMPLING':[SAMPLING], 'PLOT':[PLOT]}
        df_new = pd.DataFrame(values_to_add)
        
        df = pd.concat([df, df_new])
        df.to_csv(filename, index = False)
        
        df = pd.read_csv(filename)
        st.dataframe(df)