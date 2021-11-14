import streamlit as st
import pandas as pd
import datetime
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials




scope=['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']

totaldays=26
weekdays=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
frequency=['1','2','4']
fortnight=['1&3 Week','2&4 Week']
client_type=['Retailer','Indirect Distributor','Direct Distributor','Super Stockist']



def main():
    st.markdown('<h1 style="text-align: center;">Swiss Beauty Beat Form</h1>', unsafe_allow_html=True) 
    st.markdown('''---------------------------------------------------------------------------------------------------------''')
    # st.markdown('''---------------------------------------------------------------------------------------------------------''')
    # st.markdown('''---------------------------------------------------------------------------------------------------------''')
    
    data=pd.read_excel("./RetailData_12-11-2021_02_49_PM.xlsx",sheet_name='RetailData')
    zone = st.selectbox('Select Zone: ',data['Employee Zone'].unique())

    ASM_Name = st.selectbox('Select ASM Name: ',data['ASM Name'].unique())

    Link_ASM_to_SO=data.loc[data['ASM Name']==ASM_Name,['SO Name']]

    SO_Name = st.selectbox('Select SO Name: ',Link_ASM_to_SO['SO Name'].unique())

    Link_SO_to_phone_number=data.loc[data['SO Name']==SO_Name,['SO Phone']]

    phone = st.selectbox('Select Phone No: ',Link_SO_to_phone_number['SO Phone'].unique())

    SO_HQ=data.loc[data['SO Name']==SO_Name,['SO HQ']]

    Link_SO_to_HQ = st.selectbox('Select HQ: ',SO_HQ['SO HQ'].unique())

    DISTRIBUTOR=data.loc[data['SO Name']==SO_Name,['Distributor Name']]

    Link_SO_to_Distributor = st.selectbox('Select Distributor: ',DISTRIBUTOR['Distributor Name'].unique())

    BEATS=data.loc[data['SO Name']==SO_Name,['Beats']]

    Link_SO_to_BEATS = st.selectbox('Select Beat: ',BEATS['Beats'].unique())

    CLIENT_NAME=st.text_input('Enter Client Name: ')

    CLIENT_PHONE=st.text_input('Enter Client Phone Number: ')

    CLIENT_TYPE=st.selectbox('Select Client Type: ',client_type)

    SUB_TYPE=st.text_input('Enter Sub Type: ')

    CLIENT_STATE=st.selectbox('Select Client State: ',data['Client State'].unique())

    CLIENT_CITY=data.loc[data['Client State']==CLIENT_STATE,['Client City']]

    SELECT_CLIENT_CITY=st.selectbox('Select Client City: ',CLIENT_CITY['Client City'].unique())


    DISTRIBUTOR_PHONE=data.loc[data['Distributor Name']==Link_SO_to_Distributor,['Distributor Phone']]

    Link_PHONE = st.selectbox('Select Distributor Phone: ',DISTRIBUTOR_PHONE['Distributor Phone'].unique())

    FREQUENCY=st.selectbox('Select Frequency: ',frequency)
    if FREQUENCY=='1':
        fort=st.selectbox('Fortnight Selected As: ',['Monthly'])
    elif FREQUENCY=='2':
        fort=st.selectbox('Select Fortnight: ',fortnight)
    elif FREQUENCY=='4':
        fort=st.selectbox('Fortnight Selected As: ',['Weekly'])

    DAY = st.selectbox('Select Day: ',weekdays)

    RATING=st.selectbox('Select Rating: ',data['Rating'].unique())

    CITY_TOWN=data.loc[data['SO HQ']==Link_SO_to_HQ,['Town/City']]

    SELECT_CITY_TOWN_NAME=st.selectbox('Select City/Town: ',CITY_TOWN['Town/City'].unique())

    DIVISION=st.selectbox('Select Division: ',['SWISS BEAUTY','HILARY RHODA'])




    # option5 = st.date_input('Select your Date: ')
    # date1=option5.strftime('%d-%b-%Y')
    # st.write('You selected:', date1)
    # # selectedday=option5.strftime('%A')

    googlesheeturl='https://docs.google.com/spreadsheets/d/1wcSrQEj2ttGpONbH8XnfYzxUp81WQw4bdn38J2r4Hoo/edit#gid=0'
    creds=ServiceAccountCredentials.from_json_keyfile_name("./keys.json",scope)
    client=gspread.authorize(creds)
    sheet=client.open_by_url(googlesheeturl)
    worksheet=sheet.worksheet('Sheet1')
    # worksheet=sheet.get_worksheet(0)
    # sheet_runs = sheet.get_worksheet(0)


    submitbutton=st.button('Submit')
    m = st.markdown("""<style>div.stButton > button:first-child {
    background-color: rgb(255, 255, 0); border: 2px solid black;padding: 0px 15px;font-size: 30px; cursor: pointer;
    text-align: center; color: black;}</style>""", unsafe_allow_html=True)
    
    fort_to_list=list(fort.split())
    sonametolist=list(SO_Name.split())

    
    if submitbutton:
        datatosheet={'Employee Zone':[zone],'ASM Name':[ASM_Name],'SO Name':[SO_Name],'SO Phone':[phone],'SO HQ':[Link_SO_to_HQ],
        'Distributor Name':[Link_SO_to_Distributor],'Beats':[Link_SO_to_BEATS],'Client Name':[CLIENT_NAME],'Client Ph Number':[CLIENT_PHONE],
        'Client Type':[CLIENT_TYPE],'Sub Type':[SUB_TYPE],'Client State':[CLIENT_STATE],'Client City':[SELECT_CLIENT_CITY],'Client Id':['NA'],
        'Distributor Phone':[Link_PHONE],'Frequency':[FREQUENCY],'Visit Day':[DAY],'Fortnight':[fort],'Rating':[RATING],'City/Town':[SELECT_CITY_TOWN_NAME],
        'Division':[DIVISION],'Date':[datetime.datetime.now().strftime('%d-%b-%Y %H:%M:%S')]}
        datadf=pd.DataFrame(datatosheet)
        if worksheet.get_all_records()==[]:
            worksheet.append_rows(datadf.values.tolist())
            st.success('Data Submitted Successfully')

        else:
            # worksheet.append_rows(datadf.values.tolist())
            # st.success('Data Submitted Successfully')
            df1=worksheet.get_all_values()
            df2=pd.DataFrame(df1,columns=df1[0])
            df2=df2.drop(0,axis=0)
            # st.write(df2)
            # st.write(df2['SO Name'].values)

            if SO_Name in df2['SO Name'].values:
                df3=df2.groupby(['SO Name']).get_group(SO_Name)
                if df3.loc[df3['Fortnight']==fort_to_list[0],'Fortnight'].count()>=1 and df3.loc[df3['Visit Day']==DAY,'Visit Day'].count()>=1:
                    st.error('You have already entered 4 visits for fortnight {} for {}'.format('Weekly',DAY) + '------------------------------Please select another Day..')

                else:
                    worksheet.append_rows(datadf.values.tolist())
                    st.success('Data Submitted Successfully')


            else:
                worksheet.append_rows(datadf.values.tolist())
                st.success('Data Submitted Successfully')
                

                
                
            #     worksheet.append_rows(datadf.values.tolist())
            #     st.success('Data Submitted Successfully')
            #     df3=df2.groupby(['SO Name']).get_group(SO_Name)
            #     if SO_Name not in df3['SO Name'].values:
            #         print(SO_Name not in df3['SO Name'].values)
            #         worksheet.append_rows(datadf.values.tolist())
            #         st.success('Data Submitted Successfully')
            #         st.write(df3)
            #         if fort_to_list[0]=='Weekly':
            #             if df3.loc[df3['Fortnight']==fort_to_list[0],'Fortnight'].count()>=1:
            #                 st.error('You have already entered 4 visits for fortnight {} for {}'.format('Weekly',DAY) + '------------------------------Please select another Day..')


        



           
        # for i in fort_to_list:
        #     if SO_Name in df2.SO_Name.values and df2.loc[df2.Fortnight==i,'Fortnight'].count()>=4 and df2.loc[df2['Visit_Day']==DAY,'Visit_Day'].count()>=4:
        #         st.error('You have already entered 4 visits for fortnight {} for {}'.format(i,DAY) + '------------------------------Please select another Day..')
        #     else:
        #         worksheet.append_rows(datadf.values.tolist())
        #         st.success('Data Submitted Successfully')
          


    
    st.markdown('**Developer**: [Rajinder Singh]' , unsafe_allow_html=True)














if __name__ == '__main__':
    main()
