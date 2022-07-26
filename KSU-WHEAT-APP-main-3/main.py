#app.py
import dataupload
import dataupload_other_data
import labels
import canopy_c
import combinedata
import seeds
import merge_data

import streamlit as st
from PIL import Image


PAGES = {  
    'Partitioning Data Uploader': dataupload ,
    'Labels Generator': labels, 
    'Biomass/Other Data Uploader': dataupload_other_data,
    'Canopy Cover Uploader': canopy_c, 
    'Seed counter': seeds, 
    'Combine Data Uploader': combinedata, 
    'Merge Data': merge_data
}

st.title('IDataField')
#st.header('Labels generator and data uploading apps')
#st.subheader('developed by N Giordano, JA Romero Soler, LO Pradella, L Simao, LP Ryan, A Patrignani and RP Lollato')

st.sidebar.empty()
logoksuwheat = Image.open('logo_ksuwheat.jpg')
st.sidebar.image(logoksuwheat, use_column_width=True)

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()

#with st.sidebar.container():
#    image = Image.open('logo_ksuwheat.jpg')
#    st.image(image, use_column_width=True)
#    
#with st.sidebar.title('Apps'):
#    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
#    page = PAGES[selection]
#    page.app()
#
#with st.sidebar.container():
#    image = Image.open('logo_ksuwheat.jpg')
#    st.image(image, use_column_width=True)
#    
#with st.sidebar:
#    selected = option_menu("Main Menu", ["Home", 'Data Uploader'], icons=['house', 'upload'], menu_icon="cast", default_index=1)
#    selected

