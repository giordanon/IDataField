import numpy as np
import matplotlib.image as mpimg
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_multipage import MultiPage

folder_path = 'output/data/'
filename = folder_path + 'data.csv'
    
def app():
    st.title('KSU Wheat Canopy Cover Uploader App')
    
    ID = st.text_input('SCAN QR CODE IN PLOT OR LABEL')
    STAGE = st.selectbox('STAGE', ['F6', 'F105', 'SD'])
    canopy_cover_file = st.file_uploader("UPLOAD GO-PRO CC PICTURE", type=["jpg"])
    
    if canopy_cover_file:
        rgb = mpimg.imread(canopy_cover_file)        
        # Extract data in separate variable for easier manipulation
        red = rgb[:, :, 0] # Extract matrix of red pixel values (m by n matrix)
        green = rgb[:, :, 1] # Extract matrix of green pixel values
        blue = rgb[:, :, 2] # Extract matrix of blue pixel values
        # Calculate red to green ratio for each pixel. The result is an m x n array.
        red_green_ratio = red/green

        # Calculate blue to green ratio for each pixel. The result is an m x n array.
        blue_green_ratio = blue/green

        # Excess green
        ExG = 2*green - red - blue
        bw = np.logical_and(red_green_ratio<0.95, blue_green_ratio<0.95, ExG>20) 
        canopy_cover = np.sum(bw) / np.size(bw) * 100 
    
    if st.button('LOAD CANOPY COVER DATAPOINT'):
        
        df = pd.read_csv(filename)
        TRIAL,SITE, YEAR, PLOT = ID.split('-')
        
        values_to_add = {'ID': [ID], 'TRAIT': ['CANOPY COVER'], 'VALUE':[canopy_cover], 'TRIAL':[TRIAL], 
                         'SITE':[SITE], 'YEAR':[YEAR], 'SAMPLING':[STAGE], 'PLOT':[PLOT]}
        df_new = pd.DataFrame(values_to_add)
        
        df = pd.concat([df, df_new])
        df.to_csv(filename, index = False)
        
    df = pd.read_csv(filename)
    st.dataframe(df)