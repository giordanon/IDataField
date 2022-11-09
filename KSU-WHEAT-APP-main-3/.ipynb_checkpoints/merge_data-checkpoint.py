import pandas as pd
import streamlit as st
import os


def app():
    st.title('Merge Combine and HI data files')
    uploaded_file = st.file_uploader("Upload Harvest Index Data", type=["csv", "xlsx"])
    # Check if file was uploaded
    if uploaded_file:
        if uploaded_file.type == "text/csv":
            df_hi = pd.read_csv(uploaded_file)
        else:
            df_hi = pd.read_excel(uploaded_file)
            
        pivoted = df_hi.pivot(index=["ID"], columns=["SAMPLING","TRAIT"], values= ["VALUE"])
        pivoted.columns = pivoted.columns.swaplevel().map('_'.join)
        pivoted['ID'] = pivoted.index
        # shift column 'C' to first position
        first_column = pivoted.pop('ID')
  
        # insert column using insert(position,column_name,first_column) function
        pivoted.insert(0, 'ID', first_column)
        pivoted[['Trial', 'Location', 'Year', 'Sampling', 'Plot']] = pivoted['ID'].str.split('-', expand=True)
        
        pivoted['Year'] = pivoted['Year'].astype(int) + 2000 - 1 
        
        year2 = pivoted['Year'][1] - 2000 + 1
        
        pivoted['Year'] = pivoted['Year'].astype(str) + "-" + year2.astype(str)
        
        #pivoted.drop('SAMPLING', inplace=True, axis=1)
        del pivoted["Sampling"]
        del pivoted["ID"]
    
        st.dataframe(pivoted)
            
    uploaded_file_cb = st.file_uploader("Upload Combine Data", type=["csv", "xlsx"])
    
    if uploaded_file_cb:
        if uploaded_file_cb.type == "text/csv":
            dfc = pd.read_csv(uploaded_file_cb)
        else:
            dfc = pd.read_excel(uploaded_file_cb)      
            
        st.dataframe(dfc)
        
    if st.button('Merge Files'): 
        
        dfc['Plot'] = dfc['Plot'].astype(int)
        pivoted['Plot'] = pivoted['Plot'].astype(int)
        
        df1 = dfc.merge(pivoted, on=["Plot","Trial", "Location", "Year"])
        
        #df1.columns = df1.columns.str.rstrip("VALUE_")
        df1.columns = df1.columns.str.replace("VALUE_", "")
        
        season = df1['Year'][1]
        TRIAL = df1['Trial'][1]
        year_folder = f'SEASON {season}'
        folder_path = f'../{year_folder}/01-Data/{TRIAL}'            
        filename = f'{folder_path}/{TRIAL}_Merged_Data.csv'
            
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        if not os.path.isfile(f'{filename}'):
            #df_create = pd.DataFrame(columns = ['ID', 'TRAIT', 'VALUE', 'TRIAL','SITE', 'YEAR', 'SAMPLING', 'PLOT'])
            df1.to_csv(filename, index = False)

        st.dataframe(df1)
            