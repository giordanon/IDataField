import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.color import rgb2gray, label2rgb
from skimage.filters import threshold_otsu
from skimage.morphology import area_opening, disk, binary_closing
from skimage.measure import find_contours, label, regionprops_table
import streamlit as st
import pandas as pd
from PIL import Image

images_path = 'seeds/Seeds_Double_Check_Images/'
folder_path = 'output/data/'
filename = folder_path + 'data.csv'
    
def app():
    st.title('KSU Wheat Canopy Cover Uploader App')
    
    ID = st.text_input('SCAN QR CODE IN LABEL')
    GRAIN_WEIGHT = st.number_input('Mass of the grains sample (g)')
    #STAGE = st.selectbox('STAGE', ['F6', 'F105', 'SD'])
    seeds_file = st.file_uploader("UPLOAD GO-PRO CC PICTURE", type=["jpg"])
    
    if seeds_file:

        RGB = mpimg.imread(seeds_file)
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
        plt.savefig(f'{images_path}{ID}.jpg')
        
    if st.button('Check Grains Arrangement'):
        seeds = Image.open(f'{images_path}{ID}.jpg')
        st.image(seeds)
        
       
      
    if st.button('LOAD TKW DATAPOINT'):
        
        df = pd.read_csv(filename)
        TRIAL,SITE, YEAR, SAMPLING, PLOT = ID.split('-')
        
        values_to_add = {'ID': [ID], 'TRAIT': ['TKW'], 'VALUE':[TKW], 'TRIAL':[TRIAL], 'SITE':[SITE], 'YEAR':[YEAR], 'SAMPLING':[SAMPLING], 'PLOT':[PLOT]}
        df_new = pd.DataFrame(values_to_add)
        
        df = pd.concat([df, df_new])
        df.to_csv(filename, index = False)
        
    df = pd.read_csv(filename)
    st.dataframe(df)