# -*- coding: utf-8 -*-

"""

Created on Wed May 29 14:36:20 2019
@author: admin

"""

import os
import sys
import time
import inspect
import pyautogui
import threading
import subprocess
import win32com.client  # link for the process: https://github.com/solomonvimal/PyFloods/blob/master/HEC_RAS_controller.py
from threading import Timer
from datetime import datetime, timedelta

##-----To clone the github repository (in git cmd)
#cd path to local directory
#git clone copied github repo address

def f():
    
    ##-----Run HEC-RAS repeatedly 
        
    ## Check directory and change the  directory to the required one
    cwd = os.getcwd()
    print(cwd)
    os.chdir('E:\\Selina\\RAS2D\\Potomac_RAS_Model\\RASwithWatershed_v3automate')
        
    ## Execute the ras_automater code 
    exec(open('./ras2Dautomater_watershed1.py').read())

    ##------Control HEC-RAS to run and quit
    RC = win32com.client.Dispatch("RAS507.HECRASCONTROLLER") # HEC-RAS Version 5.0.7
    ras_file = 'E:/Selina/RAS2D/Potomac_RAS_Model/RASwithWatershed_v3automate/watershed1.prj'
    RC.Project_Open(ras_file)
    RC.Compute_CurrentPlan()
    RC.ShowRas()
    time.sleep(120)
    #MsgBox ('Click Yes to close HEC-RAS')
    #RC.QuitRAS() 
    #inspect.getmembers(RC) 
    os.system("taskkill /f /im  Ras.exe")
    
    ## Execute the dss input writer 
    #subprocess.call("run_write_dss.cmd",shell=True)  
    
    ## Execute the hdf reader code 
    os.chdir('E:\\Selina\\RAS2D\\Potomac_RAS_Model\\RASwithWatershed_v3automate')
    exec(open('./hdf_reader_ras2D.py').read())
    #exec(open('./hdf_reader_loops_final_historical_subplot.py').read())      
    ## Execute the movie maker code 
    #exec(open('./movie_maker.py').read())
           
    ## Change directory to the repository folder
    os.chdir('E:\\MasonFloodHazardsResearchLab.github.io\\potomac_total_water\\images')  ## check which folder to push using gitpush
           
    ## Push the figures to github
   # subprocess.Popen("git_push.cmd")
           
    ## Check the time 
    t2=datetime.now().strftime(format = '%d-%b-%Y %H:%M:%S')
    print("Model run ended at {}".format(t2))
       
    ## Call f() again in specified seconds
    threading.Timer(3600, f).start() 

f() 

