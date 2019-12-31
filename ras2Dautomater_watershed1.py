# -*- coding: utf-8 -*-

"""
Created on Tue May 28 16:13:53 2019
@author: admin

"""

import os
os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate')
from USGS_Data_Grabber import *
from USGS_Data_Grabber_test import *
from NOAA_data_download import *
from NOAA_data_download_no_flow import *
from TIDES_CURRENTS_NOAA_6T import*

#import sys
import math
#import urllib
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

import warnings
warnings.filterwarnings("ignore")
#from keypass import NOAA_api

os.chdir('E:\\Selina\\RAS2D\\Potomac_RAS_Model\\RASwithWatershed_v3automate')
##--------Check working directory and change the directory as required----------------##
#os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\version1_to_upload\\version1_test2')
#---Set paths, filenames
wk_dir = r'E:\Selina\RAS2D\Potomac_RAS_Model\RASwithWatershed_v3automate'
in_file = os.path.join(wk_dir, r'watershed1.txt')
out_file = os.path.join(wk_dir, r'watershed1.p01')
f = 'watershed1.u01'                                                 # Ouput Unsteady Flow FIle
proj = 'watershed1.prj'

## STORM NAME:
## STORM DURATION:

#--Datetime for data download
storm_start_date = datetime(2012,10,24,0,0)     ## Time Zone: EST 
storm_end_date =   datetime(2012,11,2,23,0)      ## Time Zone: EST 


#--Datetime for USGS data download (EST)
y0, m0, d0 = storm_start_date.year, storm_start_date.month, storm_start_date.day    # Start date (year, month, day)
y1, m1, d1 = storm_end_date.year, storm_end_date.month, storm_end_date.day          # End date


#--Datetime for NOAA data download (UTC/GMT = EST + 5 hours)
interval = '3600s' # interval 1 hour
range_start =(storm_start_date + timedelta(hours = 5)).strftime(format = '%m/%d/%Y %H:%M:%S')
range_end = (storm_end_date + timedelta(hours = 5)).strftime(format = '%m/%d/%Y %H:%M:%S')
start, freq = (storm_start_date + timedelta(hours = 5)).strftime(format = '%m-%Y-%d %H:%M'), interval                    #---Date Format: %m-%Y-%d %H:%M
noaa_idx =  pd.date_range(range_start,range_end,freq = 'H')
#period = len(noaa_idx)
    
#--Format datetime objects, create input line (insert_line)
ras_start = storm_start_date.strftime(format = '%d%b%Y')
ras_end = (storm_end_date - timedelta(hours=1)).strftime(format = '%d%b%Y')


# Fix the gage data start time and end time 
start_index = storm_start_date.strftime(format = '%Y-%m-%d %H:%M:%S')
end_index = storm_end_date.strftime(format = '%Y-%m-%d %H:%M:%S')                   # end date for the index with hr,min and sec


#--Fix the simulation time window
sim_start_hr = '%02d' % storm_start_date.hour
sim_start_min = '%02d' % storm_start_date.minute

sim_end_hr =  '%02d' % (storm_end_date - timedelta(hours=1)).hour                   # simulation hour in 00:00 format
sim_end_min = '%02d' % storm_end_date.minute                                        # simulation minute in 00:00 format
                   
                   
# Simulation date, hour, minute
insert_line = 'Simulation Date=' + str(ras_start) +',{}:00,'.format(sim_start_hr) + str(ras_end) + ',{}:00\n'.format(sim_end_hr)


#--NOAA Tide and Currents Station ID    
tide_gage = '8635750' # Lewisetta


#--NOAA gage names (see in NOAA data download) 
bld = 'BLDM2'
lwt = 'LWTV2'
ncd = 'NCDV2'
alex = 'AXTV2'    
cbbt = 'CBBV2'
wadc ='WASD2'
gtwn ='GTND2'
l_falls = 'BRKM2'
mach_ck = 'NCDV2'
anapolis = 'APAM2'                                                                                          
aqua='ANAD2'


#---Select USGS parameter 
flow  = "00060"
stage = "00065"
elev = "62620"

#--Select gages from NOAA and USGS
gage_1 = "01651000"    # NW Anacostia      (flow-USGS)
gage_2 = "01649500"    # NE Anacostia      (flow-USGS) 
                                                                                                                           
###----gage_1 flow + gage_2 flow = Anacostia Lower flow----###
                                                                                                                           
gage_3 = "01646500"   # Potomac upper     (flow-USGS)
gage_4 = tide_gage    # NOAA tide gage    (stage-NOAA)     Lewisetta, potomac lower 

#gage_4 = lwt         # NOAA prediction   (stage-NOAA)     Lewisetta, potomac lower                                                                                                                                    
#gage = "01653000"    # Cameron Run       (flow-USGS) 

gage_keybrdg = "01647595"
gage_WA = "01647600"
gage_alex = "0165258890"
gage_aqua = "01651750"

###############################################################################
#                                                                             #
#                              GAGE-1                                         #
#                                                                             #
###############################################################################

#---Get Gage 1 Data (df1 for flow) [cfs]
df1 = GrabData(gage_1, y0, m0, d0, y1, m1, d1, flow)
#df1 = df1*0.0283  # convert cfs to cms (0.0283)
#for i in range (0,len(df1)):
#    if df1['StreamFlow'].iloc[i]<0:
#        df1['StreamFlow'].iloc[i]=''        
#df1.count()                                                                        # count total data available

#---Get the time interval of data
df1['deltaT'] = df1.index.to_series().diff().dt.seconds.div(60, fill_value=0)       # time interval for whole dataset
dd1=int(df1["deltaT"].iloc[-1])                                                     # value of the time interval (uniform in this data set)
#--Handling the missing values in usgs gage  data
#start_index = start_date.strftime(format = '%Y-%m-%d 00:00:00')                     # start date for the corrected time index including missing data date
idx = pd.date_range(start_index, end_index, freq='{}Min'.format(dd1))               # indexing the time for date interval
df1 = df1.reindex(idx, fill_value = '')
#df1 = df1.dropna()
                                               # fill the missing places of indexed gage data with empty space
######################################################                                                                       
#df1.isnull().count()                                                               # count including  missing data                                              
#count_NULL1=df1.interpolate().count()               
#df1=df1.interpolate(method='time')                                                 #interpolate using any method
######################################################
#---Get the streamflow data from whole data frame                                                                          
#print(df1.iloc[-1])                                                                # Check the last date and time
#df1.index                                                                          # Check index of the dataframe
#df1['StreamFlow'].plot()                                                           # Plot gage data
#gage_1_data = list(df1['StreamFlow']) 
                                                                          
for i in range(0,len(df1)):
    if df1['StreamFlow'][i] == '': 
        df1['StreamFlow'][i] =df1['StreamFlow'][i-1]

#gage_1_data =  list(df1['StreamFlow'])  

#gage_1_data = [round(float(i), 3) for i in gage_1_data]


###############################################################################
#                                                                             #
#                                 GAGE-2                                      #
#                                                                             #
###############################################################################

#---Get Gage 3 Data (df2 for Stage)[cfs]
df2 = GrabData(gage_2, y0, m0, d0, y1, m1, d1,flow)
#df2 = df2*0.0283
#---Get the time interval of data
df2['deltaT'] = df2.index.to_series().diff().dt.seconds.div(60, fill_value=0)       # time interval for whole dataset
dd2=int(df2["deltaT"].iloc[-1])                                                     # value of the time interval (uniform in this data set)
#--Handling the missing values in usgs gage data
idx = pd.date_range(start_index, end_index, freq='{}Min'.format(dd2))               # indexing the time for date interval
df2 = df2.reindex(idx, fill_value = '')

#df2.plot()
#count_NULL2=df2.interpolate().count()
#df2['StreamFlow']=df2['StreamFlow'].interpolate(method='linear')
#print(df2.iloc[-1])
#---Get the flow data from whole data frame 
#gage_2_data_raw = list(df2['StreamFlow'])
##---Interpolate missing values
#g2 = pd.DataFrame(gage_2_data_raw)
# 
#if sum(g2.isnull().values.ravel())> 0:
#    for col in g2:
#         g2[col] = pd.to_numeric(g2[col], errors='coerce')
#         num = sum(g2.isnull().values.ravel())  
#         gg2 = g2.interpolate(method='quadratic',order=2,limit=num)
#         #gg2.types
#         #gg2.plot()
#    gage_2_data = []
#    for i in range(0,len(gg2)):
#         gg2.iloc[i] = round(gg2.iloc[i])   
#         g2g2 = gg2[0].values.tolist()
#         if type(g2g2[i]) is float:
#             p=int(g2g2[i])
#             gage_2_data.append(p)
#else:
#    gage_2_data=gage_2_data_raw      

#gage_2_data =  list(df2['StreamFlow'])  
#gage_2_data = [round(float(i), 3) for i in gage_2_data]

for i in range(0,len(df2)):
    if df2['StreamFlow'][i] == '': 
        df2['StreamFlow'][i] =df2['StreamFlow'][i-1]
        
###############################################################################                                                            #
#                 Anacostia lower =  GAGE-1 flow + GAGE - 2 flow              #                                                                        #
###############################################################################

test_idx = pd.date_range(start_index, end_index, freq = '{}Min'.format(dd1))
df2_test = df2.reindex(test_idx, fill_value = '')
df1 = df1.reindex(test_idx, fill_value = '')
#df1_df2_add = df1 + df2_test
#df1_df2_add.isnull().sum()

#----------------------------------------------------------------------------------

#gage1_2_data_test =  list(df1['StreamFlow']*0.0283 + df2_test['StreamFlow']*0.0283)  # convert cfs to cms (0.0283)

gage1_2_data_test =  list(df1['StreamFlow']*0.0283 + df2_test['StreamFlow']*0.0283)  # convert cfs to cms (0.0283)
#gage1_2_data_test.dropna()

#----------------------------------------------------------------------------------

gage1_2_data_test = [round(float(i),3) for i in gage1_2_data_test]
gage_1_data = gage1_2_data_test # gage_1_data name not changed as the combined flow is assumed in gage_1
      
#anac_lower['flow'] =  pd.DataFrame(gage_1_data) 
  
  
###############################################################################
#                                                                             #
#                                 GAGE-3                                      #
#                                                                             #
###############################################################################

#---Get Gage 3 Data (df1 for StreamFlow) [cfs]
df3 = GrabData(gage_3, y0, m0, d0, y1, m1, d1,flow)
#df3.count()                                                                        # count total data available
#---Get the time interval of data
df3['deltaT'] = df3.index.to_series().diff().dt.seconds.div(60, fill_value=0)       # time interval for whole dataset
dd3 = int(df3["deltaT"].iloc[-1])                                                   # value of the time interval (uniform in this data set)

dd3 = df3.index.to_series().diff().dt.seconds.div(60, fill_value=0) 
dd3 = int(dd3.iloc[-1])  

#--Handling the missing values in usgs gage  data

#index_time = datetime.now()-timedelta(minutes = 95) 
#start_index = start_date.strftime(format = '%Y-%m-%d 00:00:00')                    # start date for the corrected time index including missing data date
#end_index = index_time.strftime(format = '%Y-%m-%d %H:%M:%S')                      # end date for the index with hr,min and sec

#idx = pd.date_range(start_index, end_index, freq='{}Min'.format(dd3))              # indexing the time for date interval
#df3 = df3.reindex(idx, fill_value="")                                              # fill the missing places of indexed gage data with empty space

######################################################                                                                       
#df3.isnull().count()                                                               # count including  missing data                                              
#count_NULL3=df3.interpolate().count()
#df3=df3.interpolate(method='time')                                                 # interpolate using any method
######################################################

#---Get the streamflow data from whole data frame 

##Assuming that 60% water is flowing downstream and 40% going to aqueduct                                                                       
#-----------------------------------------------------------------------------
gage_3_data = list(df3['StreamFlow']*0.0283)  # convert cfs to cms (0.0283)
#-----------------------------------------------------------------------------      
gage_3_data=[round(float(i), 1) for i in gage_3_data]
#print(df3.iloc[-1])                                                                # Check the last date and time
#df3.index                                                                          # Check index of the dataframe
#df3.plot()                                                                         # Plot gage data

## Frequency of saved observed data depends on the computation time interval of HEC-RAS
frequency = 'H'

## POTOMAC UPPER (TO COMPARE WITH RAS WSE)

## LF-LITTLE FALLS
df_little_falls = pd.DataFrame()
df3_LF = GrabData(gage_3, y0, m0 ,d0, y1, m1 ,d1,stage)  #stage in ft
df3_LF = df3_LF*0.3048
idx = pd.date_range(start_index, end_index, freq = frequency)
df3_LF2 = df3_LF.reindex(idx, fill_value="")
#plt.plot(df3_LF2['Stage'])
df_little_falls = df3_LF2.round(3)
df_little_falls.to_csv('Little_Falls.csv',sep='\t',encoding='utf-8')


#file_name = 'little_falls.csv'
#file_path = r'E:\Selina\REALTIME_UPDATED_AND_OLD_FILES_HERE\REALTIME_RAS\Seth_Potomac_Anacostia\VERSION0_MODEL_DEC2017_automate\{}'.format('little_falls.csv')
#test = pd.read_csv(file_path,sep='\t',index_col=None) #in meter
#plt.plot(test['Stage'])


## WISCONSIN AVENUE 
#df_WA = pd.DataFrame()
df3_WA = GrabData(gage_WA, y0, m0, d0, y1, m1, d1, stage)  #stage in ft
df3_WA = df3_WA*0.3048
idx = pd.date_range(start_index, end_index, freq=frequency)
df3_WA2 = df3_WA.reindex(idx, fill_value = '')  # missing values '' or np.nan
#plt.plot(df3_LF2['Stage'])
#df3_WA3 = df3_WA2.dropna(axis=0, how='any')
#df_Wis_Ave = df3_WA3.round(3) 
df_Wis_Ave = df3_WA2
df_Wis_Ave.to_csv('Wisconsin_Avenue.csv',sep='\t',encoding='utf-8')


## POTOMAC LOWER (TO COMPARE WITH RAS WSE)

## ALEXANDRIA
df3_alex = GrabData_test(gage_alex, y0, m0, d0, y1, m1, d1, elev)  #stage in ft time EDT
df3_alex = df3_alex*0.3048
df3_alex2 = df3_alex[~df3_alex.index.duplicated(keep='first')]  # EDT
df3_alex2.index = df3_alex2.index-timedelta(hours=1)  # EST = EDT-1hr
idx = pd.date_range(start_index, end_index, freq=frequency)
df3_alex3 = df3_alex2.reindex(idx, fill_value="")
#plt.plot(df3_LF2['Stage'])
df_alexandria = df3_alex3.round(3)
df_alexandria.to_csv('Alexandria.csv',sep='\t',encoding='utf-8')


## ANACOSTIA LOWER (TO COMPARE WITH RAS WSE)

## AQUATIC GARDEN
try:
    df3_aqua = GrabData_test(gage_aqua, y0, m0, d0, y1, m1, d1, stage)  #stage in ft time EDT
    df3_aqua = df3_aqua*0.3048
    idx = pd.date_range(start_index, end_index, freq=frequency)
    df3_aqua2 = df3_aqua.reindex(idx, fill_value="")
    #plt.plot(df3_LF2['Stage'])
    df_aquatic = df3_aqua2.round(3)
    df_aquatic.to_csv('Aquatic_Garden.csv',sep='\t',encoding='utf-8')
except IndexError:
    print('AQUATIC GARDEN HAS DATA ERROR')
    pass
    

###############################################################################
#                                                                             #
#               GAGE-4  (USGS or NOAA data for downstream boundary)           #
#                                                                             #
###############################################################################
tide_gage = '8635750'  # LWT
freq = '360s'
noaa_idx =  pd.date_range(range_start,range_end,freq = '6T')
## UTC time for NOAA tides and currents
df4 = NOAA_TIDES(tide_gage,start,noaa_idx,freq)
##Already grabbed the data for fixing index
#---Get Gage 4 Data (df3 for Stage ft)
#df4 = NOAA(gage_4)                                    # NOAA
#df4 = GrabData(gage_2, y0, m0 ,d0, y1, m1 ,d1,stage) # USGS
#df4 = NOAA(gage_4)
#---Get the time interval of data [ft]
df4['deltaT'] = df4.index.to_series().diff().dt.seconds.div(60, fill_value=0)       # time interval for whole dataset
dd4 = int(df4["deltaT"].iloc[-1])                                                   # value of the time interval (uniform in this data set)
#--Handling the missing values in usgs gage data
#idx = pd.date_range(start_index, end_index, freq='{}Min'.format(dd4))               # indexing the time for date interval
#df4 = df4.reindex(idx, fill_value="")

## Subtract 5 hour from UTC time to set EST time in df4 index
diff_time = datetime.utcnow() - datetime.now()
hr = int(diff_time.seconds/3600)
df4.index = df4.index-timedelta(hours=hr)

#count_NULL4=df4.interpolate().count()
#df4=df4.interpolate(method='time')

#---Get the flow data from whole data frame 
#------------------------------------------------------------------------------
gage_4_data = list(df4[tide_gage])  # in meter / no need to convert ft to meter (0.3048)
#------------------------------------------------------------------------------
if gage_4_data[0]=='':
    gage_4_data[0]= gage_4_data[1]
for i in range(0,len(gage_4_data)):
    if gage_4_data[i]=='': 
        gage_4_data[i]= gage_4_data[i-1]
        
gage_4_data=[round(float(i), 3) for i in gage_4_data]

print(df4.iloc[-1])
#df4.plot()
 
 
## POTOMAC LOWER (TO COMPARE WITH RAS WSE)
  
## LEWISETTA
df4 = NOAA_TIDES(tide_gage,start,noaa_idx,freq)
df4.index = df4.index-timedelta(hours=hr)
idx = pd.date_range(start_index, end_index, freq=frequency)
NOAA_lewisetta = df4.reindex(idx, fill_value="")
NOAA_lewisetta.to_csv('Lewisetta.csv',sep='\t',encoding='utf-8') 


## DAHLGREN 
try:
    tide_gage = "8635027" 
    df4_dahl = NOAA_TIDES(tide_gage,start,noaa_idx,freq)
    df4_dahl.index = df4_dahl.index-timedelta(hours=hr)
    idx = pd.date_range(start_index, end_index, freq=frequency)
    NOAA_dahl = df4_dahl.reindex(idx, fill_value="")
    NOAA_dahl.to_csv('Dahlgren.csv',sep='\t',encoding='utf-8') 
except TypeError:
    print('DAHLGREN HAS DATA ERROR')
    pass
        
        
#### DAHLGREN
#tide_gage = "8635027" 
#df4_dahl = NOAA_TIDES(tide_gage,start,noaa_idx,freq)
#df4_dahl.index = df4_dahl.index-timedelta(hours=5)
#idx = pd.date_range(start_index, end_index, freq=frequency)
#NOAA_dahl = df4_dahl.reindex(idx, fill_value="")
#NOAA_dahl.to_csv('Dahlgren.csv',sep='\t',encoding='utf-8') 

 
## POTOMAC UPPER (TO COMPARE WITH RAS WSE) 
 
## WASHINGTON DC
tide_gage = "8594900" 
df4_dc = NOAA_TIDES(tide_gage,start,noaa_idx,freq)
df4_dc.index = df4_dc.index-timedelta(hours=hr)
idx = pd.date_range(start_index, end_index, freq=frequency)
NOAA_dc = df4_dc.reindex(idx, fill_value="")
NOAA_dc.to_csv('Washington_DC.csv',sep='\t',encoding='utf-8')
print(df4_dc[1:20])
     

###############################################################################
#                                                                             #
#               GAGE-5  (NOAA NCDC Precipitation) \\ convert to runoff \\     #
#                                                                             #
###############################################################################
# Set api token
NOAA_api = 'zkrKwcRsNyHzGhgHnCBZOotoOwRoQQMC'
mytoken = NOAA_api

## Check the available dataid
url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/datasets/PRECIP_HLY"
# replace 'myToken' with the actual token, below
token = {'token': mytoken}
response = requests.get(url, headers = token)
response = response.json() 

#Use the same begin and end date for just one day's data. Format for the API request
begin_date = storm_start_date.strftime("%Y-%m-%d")
#end_date = (lastyear + timedelta(days=30)).strftime("%Y-%m-%d") 
end_date = storm_end_date.strftime("%Y-%m-%d")

##----Without function for single station and single dataset
locationid = 'COOP:448906'  # Reagan Airport -COOP:448906   Dulles Airport - COOP:448903
datasetid =  'PRECIP_HLY'   # dataset for "Hourly Precipitation"  

## Data in local time and mm unit for metric
base_url_data = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid={}&stationid={}&units=metric&startdate={}&enddate={}'.format(datasetid,locationid,begin_date,end_date)            
r = requests.get(base_url_data, headers=token)
df = pd.DataFrame.from_dict(r.json()['results'])

df_prec = pd.DataFrame()
df_prec['Prec(mm)'] = df['value']*0.05  # total precip to runoff
df_prec.index = pd.to_datetime(df['date'])
df_prec.plot(marker='o',linestyle='--')
idx = pd.date_range(begin_date, end_date, freq='H')  
df_prec = df_prec.reindex(idx, fill_value = '0')

df5 = df_prec  
df5['deltaT'] = df5.index.to_series().diff().dt.seconds.div(60, fill_value=0)       # time interval for whole dataset
dd5 = int(df5["deltaT"].iloc[-1])                                                   # value of the time interval (uniform in this data set)
 
gage_5_data = list(df5['Prec(mm)'])  # in mm
gage_5_data = [round(float(i), 3) for i in gage_5_data]
                                                        
#------------------------------------------------------------------------------

os.chdir('E:\\Selina\\RAS2D\\Potomac_RAS_Model\\RASwithWatershed_v3')

#---Headers for unsteady flow file

header_1 = "Flow Title=watershed1\nProgram Version=5.07\nUse Restart= 0\n\
Boundary Location=                ,                ,        ,        ,                ,Perimeter 1     ,                ,UP1\n\
Interval={}MIN\n\
Flow Hydrograph= {}\n".format(dd1,len(gage_1_data))
#Add_line="Interpolate Missing Values=True\n"


header_3 ="Stage Hydrograph TW Check=0\n\
Flow Hydrograph Slope= 0.12\n\
DSS Path=\n\
Use DSS=False\n\
Use Fixed Start Time=True\n\
Fixed Start Date/Time={},{}:00\n\
Is Critical Boundary=False\n\
Critical Boundary Flow=\n\
Boundary Location=                ,                ,        ,        ,                ,Perimeter 1     ,                ,UP2\n\
Interval={}MIN\n\
Flow Hydrograph= {}\n".format(ras_start,sim_start_hr,dd3,len(gage_3_data))


header_4 ="Stage Hydrograph TW Check=0\n\
Flow Hydrograph Slope= 0.12\n\
DSS Path=\n\
Use DSS=False\n\
Use Fixed Start Time=True\n\
Fixed Start Date/Time={},{}:00\n\
Is Critical Boundary=False\n\
Critical Boundary Flow=\n\
Boundary Location=                ,                ,        ,        ,                ,Perimeter 1     ,                ,LOW\n\
Interval={}MIN\n\
Stage Hydrograph= {}\n".format(ras_start,sim_start_hr, dd4,len(gage_4_data))


header_5 ="Stage Hydrograph Use Initial Stage=-1\n\
Stage Hydrograph TW Check=0\n\
Flow Hydrograph Slope= 0.12\n\
DSS Path=\n\
Use DSS=False\n\
Use Fixed Start Time=True\n\
Fixed Start Date/Time={},{}:00\n\
Is Critical Boundary=False\n\
Critical Boundary Flow=\n\
Boundary Location=                ,                ,        ,        ,                ,Perimeter 1     ,                ,\n\
Interval={}MIN\n\
Precipitation Hydrograph= {}\n".format(ras_start,sim_start_hr, dd5,len(gage_5_data))


footer_1 ="DSS Path=\n\
Use DSS=False\n\
Use Fixed Start Time=True\n\
Fixed Start Date/Time={},{}:00\n\
Is Critical Boundary=False\n\
Critical Boundary Flow= ".format(ras_start,sim_start_hr) 
  

#--Open File, overwrite new file ===> WRITE Unsteady Flow File
with open(os.path.join(wk_dir,f),'w') as fout:  

     #---Gage 1 formatted unsteady flow data for HEC-RAS 
     data_length = len(gage_1_data)/10    
     nrows = math.ceil(data_length)
     fout.write(header_1)
   
     j=0
     for i in range(0,nrows):
        # print('row ',i)
        row_values = gage_1_data[j:j+10]
        #row_values[:] = [kk*0.0283 for kk in row_values]   # convert cfs to cms (0.0283)
        row_values = [round(float(jj), 1) for jj in row_values]
        myout = [str(q).rjust(10) for q in row_values]
        output = str(myout).strip('[]').replace("'"," ").replace(","," ")
        output1 = output.replace("   ", " ")                                       # Replace four white space with one
        fout.write('{}\n'.format(output1))
        j = j+10
        
        
     #---Gage 3 formatted unsteady flow data for HEC-RAS 
     data_length = len(gage_3_data)/10    
     nrows = math.ceil(data_length)
     fout.write(header_3)
    
     j=0
     for i in range(0,nrows):
        # print('row ',i)
        row_values = gage_3_data[j:j+10]
        #row_values = [kk*0.0283 for kk in row_values]   # convert cfs to cms (0.0283)
        row_values = [round(float(jj), 2) for jj in row_values]
        myout = [str(q).rjust(10) for q in row_values]
        output = str(myout).strip('[]').replace("'"," ").replace(","," ")
        output3= output.replace("    ", " ")
        fout.write('{}\n'.format(output3))
        j = j+10         
        
        
     #---Gage 4 formatted unsteady flow data for HEC-RAS 
     data_length = len(gage_4_data)/10    
     nrows = math.ceil(data_length)
     fout.write(header_4)
    
     j=0
     for i in range(0,nrows):
        #print('row ',i)
        row_values = gage_4_data[j:j+10]
        #row_values = [kk*0.3048 for kk in row_values]   # convert ft to meter (0.3048)
        row_values = [round(float(jj), 2) for jj in row_values]
        myout = [str(q).rjust(10) for q in row_values]
        output = str(myout).strip('[]').replace("'"," ").replace(","," ")
        output4= output.replace("   ", " ")
        fout.write('{}\n'.format(output4))
        j = j+10 
        
        
     #---Gage 5 formatted unsteady flow data for HEC-RAS 
     data_length = len(gage_5_data)/10    
     nrows = math.ceil(data_length)
     fout.write(header_5)
    
     j=0
     for i in range(0,nrows):
        #print('row ',i)
        row_values = gage_5_data[j:j+10]
        #row_values = [kk*0.3048 for kk in row_values]   # convert ft to meter (0.3048)
        row_values = [round(float(jj), 2) for jj in row_values]
        myout = [str(q).rjust(10) for q in row_values]
        output = str(myout).strip('[]').replace("'"," ").replace(","," ")
        output5 = output.replace("   ", " ")
        fout.write('{}\n'.format(output5))
        j = j+10 
        
     fout.write(footer_1)            
     
#------------------------------------------------------------------------------  
#--Open template, write new file===> Write Plan file
# Modify lines in input plan file 
#line0 ="Plan Title=Plan01\n" 
#line25="Computation Interval=1HOUR\n"
#line26="Output Interval=1HOUR\n"
#line27="Instantaneous Interval=1HOUR\n"
#line28="Mapping Interval=1HOUR\n"
#line29="Run HTab= 1\n"                                    
#line30="Run UNet= 1\n"
#line32="Run PostProcess= 1\n"
#line34="Run RASMapper= 1\n"  
#line35="UNET Theta= 0.6\n"   # change if tidal signal is not a boundary condition
#line40="UNET MxIter= 20\n"   # change if number of iteration is to be changed
 
with open(in_file, 'r') as fin:
    with open(out_file, 'w') as fout:
        for i in range(183):
            line = fin.readline()
            if i != 3 :
                fout.write(line)
            elif i == 3:
                fout.write(insert_line)
            else:
                fout.write(line)
#------------------------------------------------------------------------------                                            
#--Write project file
                
# for feet: line 510 = English Units\n\ 
                
#---Sections for project file
header_project1="Proj Title=watershed1\n\
Current Plan=p01\n\
Default Exp/Contr=0.3,0.1\n\
SI Units\n\
Geom File=g01\n\
Unsteady File=u01\n\
Plan File=p01\n\
Y Axis Title=Elevation\n\
X Axis Title(PF)=Main Channel Distance\n\
X Axis Title(XS)=Station\n\
BEGIN DESCRIPTION:\n\
                  \n\
END DESCRIPTION:\n\
DSS Start Date=\n\
DSS Start Time=\n\
DSS End Date=\n\
DSS End Time=\n\
DSS File=dss\n\
DSS Export Filename=\n\
DSS Export Rating Curves= 0 \n\
DSS Export Rating Curve Sorted= 0 \n\
DSS Export Volume Flow Curves= 0 \n\
DXF Filename=\n\
DXF OffsetX= 0 \n\
DXF OffsetY= 0 \n\
DXF ScaleX= 1 \n\
DXF ScaleY= 10 \n\
GIS Export Profiles= 0\n"    


#header_project2 = "\nHRC.QuitRAS\n"

with open(os.path.join(wk_dir,proj ),'w') as fout:  
     fout.write(header_project1)
     #fout.write(header_project2)
        
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#     

## Plots to visualize the peaks and time to peak
import os
import h5py                 #(if h5py is the cause for 'kernel died' pip uninstall h5py from anaconda and then pip install h5py)
#import shutil
import numpy as np
import pandas as pd
#from shutil import copyfile
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
#from datetime import datetime, timedelta
#from matplotlib.offsetbox import AnchoredText
import matplotlib.image as mpimg
#import seaborn as sns

df_NW = df1['StreamFlow']*0.0283
df_NE = df1['StreamFlow']*0.0283
df_LF = df3['StreamFlow']*0.0283

df_water_levelsLew = df4['8635750']
df_water_levelsDC =  df4_dc['8594900']
df_time1 = df4.index[0].year

## Plot properties
storm_name_set = start
plot_interval = 60
f = 14
fig, ax1 = plt.subplots(1, 1, figsize=(4, 4), dpi = 150)
# Convert time to EST and unit to meter for plotting
#------------------------------
# Streamflow and Water level
ax1 = plt.subplot(111)
ax1.plot(df_LF, lw=2.5, linestyle = '--',color='b',label = 'Little Falls')
ax1.plot(df_NE, lw=2, color='b',alpha = 0.99,label = 'Northeast Anacostia')
ax1.plot(df_NW, lw=2, color='b',alpha = 0.5,label = 'Northwest Anacostia')
ax1.legend(loc='lower right',frameon=True, bbox_to_anchor=(0.60, 0.93),fancybox=True, shadow=False, ncol=3,fontsize=10)
ax1.set_ylabel('Streamflow (m3/s)',color='b',fontsize=16)
for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] + ax1.get_xticklabels() + ax1.get_yticklabels()):
   item.set_fontsize(f)
plt.xticks(rotation=0)
#ax1.grid()

ax2 = ax1.twinx() 
ax2.plot(df_water_levelsLew, lw=2, color='k',linestyle = '--',label = 'Lewisetta')
ax2.plot(df_water_levelsDC, lw=1.5, color='k', label = 'Washington DC')
plt.xticks(rotation=0)
#ax2.grid()
#y_max = ax1.get_ylim()[1]
ax2.legend(loc='lower right',frameon=True, bbox_to_anchor=(0.9, 0.93),fancybox=True, shadow=False, ncol=2,fontsize=10)
ax2.set_xlabel('Time (EST)')
ax2.set_ylabel('Water Level (m)',fontsize=16)
xfmt = mdates.DateFormatter('%b%d %I:%m%p')
ax2.xaxis.set_major_formatter(xfmt)
plt.title('Riverine Flood({})'.format (df_time1))
for item in ([ax2.title, ax2.xaxis.label, ax2.yaxis.label] + ax2.get_xticklabels() + ax2.get_yticklabels()):
    item.set_fontsize(f)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%I%p\n%b%d'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(byhour=range(24), interval = plot_interval))
#ax2.grid()
plt.subplots_adjust(hspace = 0.5)  # give space between plots