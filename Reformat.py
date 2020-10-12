#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This program takes summit wind, pressure, and ozone and interpolates to the 
times that mountaineers were above 8,000 m
"""

import numpy as np, pandas as pd

# Params
k=8000. # Must have climbed this high on Everest

# Infiles
himfile=\
"/home/lunet/gytm3/Everest2019/Research/HueyCollab/members_and_hired_everest.csv"
indir="/home/lunet/gytm3/Everest2019/Research/HueyCollab/"
wfile=indir+"Wind.csv"
pfile=indir+"Pressure.csv"
o3file=indir+"Ozone.csv"
logout=indir+"log.txt"

# Formatting
sep="#"

# Read
himdata=pd.read_csv(himfile)
ever=himdata.loc[himdata["peakid"]=="EVER"]
wind=pd.read_csv(wfile,index_col=0,parse_dates=True); 
o2=pd.read_csv(pfile,index_col=0,parse_dates=True);
o3=pd.read_csv(o3file,index_col=0,parse_dates=True); 

# Extract all those who ventured above k m on Everest
everhigh=ever.loc[ever["mperhighpt"]>=8000.]
cols=[ii for ii in everhigh.columns if "msmt" not in ii]
# Fix date/time cols to be str
for i in range(1,4):
    everhigh["msmtdate%.0f"%i].iloc[:]=everhigh["msmtdate%.0f"%i].astype(str)
    everhigh["msmttime%.0f"%i].iloc[:]=everhigh["msmttime%.0f"%i].astype(str)
# Loop over all climbs and duplicate row if smtcnt >1
meta=[]
dates=[]
times=[]
summitno=[]
header=sep+sep.join(cols)+sep+"msmtdate"+sep+"msmttime\n"
with open(logout,"w") as fo:
    fo.write(header)
    
    for i in range(len(everhigh)):
        
        strout=''
        count=0
        for item in everhigh.iloc[i]:
                
            if "msmt" not in everhigh.columns[count]:
                if type(item)==str:
                    strout=strout+sep+item
                else:
                    strout=strout+sep+"%.2f"%item
            count+=1
    
        if  everhigh.iloc[i]["smtcnt"]==1:
            
            strout=strout+sep+everhigh.iloc[i]["msmtdate1"]
            strout=strout+sep+everhigh.iloc[i]["msmttime1"] +"\n"
            fo.write(strout)
            
        else:

            for j in range(everhigh.iloc[i]["smtcnt"].astype(np.int)):
                
                fo.write(strout + sep+ everhigh.iloc[i]["msmtdate%.0f"%(j+1)] +\
                    sep+everhigh.iloc[i]["msmttime%.0f"%(j+1)] +"\n")

        
        
            
    
    