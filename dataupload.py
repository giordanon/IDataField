
import streamlit as st
import pandas as pd
#import cv2
#from PIL import Image
from streamlit_option_menu import option_menu
from streamlit_multipage import MultiPage
import numpy as np
import os as os

#folder_path = 'output/data/'
#filename = folder_path + 'data.csv'
def app():
    st.title('KSU Wheat Data Uploader App')
    
    ID = st.text_input('SCAN QR CODE IN LABEL')
        
    TRAIT = 'Whole Plant Weight'
    MASS = st.number_input('Whole Plant Biomass (g)')
    
    TRAIT_2 = 'Head Weight'
    MASS_2 = st.number_input(f'{TRAIT_2} (g)')
    
    TRAIT_3= 'Head Number'
    MASS_3 = st.number_input(f'{TRAIT_3}')
    
    TRAIT_4 = 'Stover Weight'
    MASS_4 = st.number_input(f'{TRAIT_4} (g)')
        
    if st.button('LOAD DATAPOINT'):
        
        
        TRIAL,SITE, YEAR, SAMPLING, PLOT = ID.split('-')
        
        prev_year = 2000 + int(YEAR) - 1
        year_folder = f'SEASON {prev_year}-{YEAR}'
        folder_path = f'../{year_folder}/01-Data/{TRIAL}'
        
        filename = f'{folder_path}/{TRIAL}.csv'
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        if not os.path.isfile(f'{filename}'): 
            df_create = pd.DataFrame(columns = ['ID', 'TRAIT', 'VALUE', 'TRIAL','SITE', 'YEAR', 'SAMPLING', 'PLOT'])
            df_create.to_csv(filename, index = False)      
        
        #else: 
        df = pd.read_csv(filename)
                
 
        values_to_add = {'ID': [ID], 'TRAIT': [TRAIT], 'VALUE':[MASS], 'TRIAL':[TRIAL], 'SITE':[SITE], 'YEAR':[YEAR], 'SAMPLING':[SAMPLING], 'PLOT':[PLOT]}
        values_to_add_2 = {'ID': [ID], 'TRAIT': [TRAIT_2], 'VALUE':[MASS_2], 'TRIAL':[TRIAL], 'SITE':[SITE], 'YEAR':[YEAR], 'SAMPLING':[SAMPLING], 'PLOT':[PLOT]}
        values_to_add_3 = {'ID': [ID], 'TRAIT': [TRAIT_3], 'VALUE':[MASS_3], 'TRIAL':[TRIAL], 'SITE':[SITE], 'YEAR':[YEAR], 'SAMPLING':[SAMPLING], 'PLOT':[PLOT]}
        values_to_add_4 = {'ID': [ID], 'TRAIT': [TRAIT_4], 'VALUE':[MASS_4], 'TRIAL':[TRIAL], 'SITE':[SITE], 'YEAR':[YEAR], 'SAMPLING':[SAMPLING], 'PLOT':[PLOT]}
        
        df_new = pd.DataFrame(values_to_add)
        df_new_2 = pd.DataFrame(values_to_add_2)
        df_new_3 = pd.DataFrame(values_to_add_3)
        df_new_4 = pd.DataFrame(values_to_add_4)
        
        df = pd.concat([df, df_new, df_new_2, df_new_3, df_new_4])
        df.to_csv(filename, index = False)
        
        df = pd.read_csv(filename)
        st.dataframe(df)