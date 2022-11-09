#Import Libraries
import pandas as pd 
import numpy as np
# QR code libraries
import qrcode
#PDF Libraries
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileReader, PdfFileWriter
import streamlit as st

def app():
    st.title('Labels Generator App')
    
    out_filepath = 'output/labels/'
    
    df1 = pd.DataFrame()
    TIME = None
    # Allow only .csv and .xlsx files to be uploaded
    uploaded_file = st.file_uploader("Upload spreadsheet", type=["csv", "xlsx"])
    # Check if file was uploaded
    if uploaded_file:
        if uploaded_file.type == "text/csv":
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        st.dataframe(data.head())
    
    
    if st.button('GENERATE BAG LABELS'):    

        data = data.dropna().reset_index()
        data['SAMPLING'] = data['SAMPLING'].str.replace(' ', '').str.split(pat = ",",  expand = False)
        data['Trt1'] = pd.Series(dtype = 'object')
        data['Rep1'] = pd.Series(dtype = 'object')
        
        for k,row in data.iterrows():
            data.at[k,'Trt1'] = np.arange(1,int(data.at[k,'Trt'])+1)
            data.at[k,'Rep1'] = np.arange(1,int(data.at[k,'Reps'])+1)
            
        df = data.explode('SAMPLING').explode('Rep1').explode('Trt1')
        df['Plot'] = df['Rep1']*100 + df['Trt1']
        df['LABEL'] = df['TRIAL_SHORT'].astype(str) + '-' + df['LOC_SHORT'].astype(str) + '-' + df['YEAR'].astype(str) + '-' + df['SAMPLING'].astype(str) + '-' + df['Plot'].astype(str)
        df = df.reset_index()        
        st.dataframe(df)

        
        df.to_csv(f"{out_filepath}labels.csv", index = False)
        
    if st.button('GENERATE PLOT LABELS'):    

        data = data.dropna().reset_index()
        data['SAMPLING'] = data['SAMPLING'].str.replace(' ', '').str.split(pat = ",",  expand = False)
        data['Trt1'] = pd.Series(dtype = 'object')
        data['Rep1'] = pd.Series(dtype = 'object')
        
        for k,row in data.iterrows():
            data.at[k,'Trt1'] = np.arange(1,int(data.at[k,'Trt'])+1)
            data.at[k,'Rep1'] = np.arange(1,int(data.at[k,'Reps'])+1)
            
        df = data.explode('Rep1').explode('Trt1')
        df['Plot'] = df['Rep1']*100 + df['Trt1']
        df['LABEL'] = df['TRIAL_SHORT'].astype(str) + '-' + df['LOC_SHORT'].astype(str) + '-' + df['YEAR'].astype(str) + '-' + df['Plot'].astype(str)
        df = df.reset_index()        
        st.dataframe(df)

        
        df.to_csv(f"{out_filepath}labels.csv", index = False)
    
    labels = pd.read_csv(f'{out_filepath}labels.csv')
    TIME = st.multiselect('PHENOLOGICAL STAGE', labels['SAMPLING'].unique())  
    LOCATION = st.multiselect('LOCATION', labels['LOC_SHORT'].unique())
    TRIAL = st.multiselect('TRIAL', labels['TRIAL_SHORT'].unique())
    
    SIZE = st.multiselect('Size to Print', ['BIG', 'SMALL'])
    FILENAME = st.text_input('FILE NAME')
        
    idx = labels['SAMPLING'].isin(TIME) & labels['LOC_SHORT'].isin(LOCATION) & labels['TRIAL_SHORT'].isin(TRIAL)
    data = labels[idx]
    st.write(data)
    
    
    
    if st.button('DOWNLOAD LABELS'):
        data = data
        size = SIZE[0] 
        filename = FILENAME
        
        #FUNCTION
        output = PdfFileWriter()
    
        if size == 'BIG':
            h = 2.4
            w = 3.9
            y = -0.5*inch
            x = 0.67*inch
            txt_size = 20
            y2 = 9
            x2 = 1.1*inch
            qrsize = 3
            qrx = 0.1 * inch
            qry = -0.9*inch
        elif size == 'SMALL':
            h = 1.4
            w = 3.5
            y = -0.5 * inch
            x = - 0.3 * inch
            txt_size = 18
            y2 = - 0.1 * inch
            x2 = 0.1 * inch
            qrsize = 1.5
            qrx = 0.45 * inch
            qry = -0.9 * inch

        for labels in data.index[0:]:
            label = data['LABEL'][labels]
            c = canvas.Canvas(f"{out_filepath}pdf1.pdf", pagesize=(w*72, h*72))

            height = h * inch
            width = w * inch

            c.translate(inch,inch)
            # Define font type and size
            c.setFont("Helvetica", txt_size)


            c.setStrokeColorRGB(1,1,1)
            c.setFillColorRGB(0,0,0)
            # Draw label
            c.drawString(y, x , f"{label}")
            c.setFont("Helvetica", 15)
            c.drawString(y2,x2 , "@KSU_WHEAT")

            # Draw a QR code
            img = qrcode.make()

            qr = qrcode.QRCode(
                version = 1,
                error_correction = qrcode.constants.ERROR_CORRECT_H,
                box_size = qrsize,
                border = 4)

            qr.add_data(label)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            c.drawInlineImage(image = img, x = qrx , y = qry, preserveAspectRatio= True)
            # Save file
            c.showPage()

            c.save()
            pdfOne = PdfFileReader(open(f"{out_filepath}pdf1.pdf", "rb"))
            output.addPage(pdfOne.getPage(0))
        outputStream = open(f"{out_filepath}{filename}.pdf", "wb")
        output.write(outputStream)
        outputStream.close()
                
                
   
   