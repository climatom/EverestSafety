#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This program takes summit wind, pressure, and ozone and interpolates to the 
times that mountaineers were above 8,000 m
"""

import datetime, numpy as np, pandas as pd
from scipy import ndimage

# Params
k=8000. # Must have climbed this high on Everest

# Function definitions 
def himDate(datecol,hourcol,verb=False):
    
    """
    Simply iterates over datestrings (day/month/year)
    and returns a vector of datetimes
    
    In:
        - datecol     : of form "day/month/year"
        - hourcol     : decimal form
        - verb        : if verb, print outcome from except
        
    Out:
    
        - uc (m/s)    : datetime.datetime
        
    """
    date=[]; years=[]; months=[]; days=[]; hours=[]
    for i in range(len(datecol)):
        year=np.nan; month=np.nan; day=np.nan; day=np.nan
        day=np.int(datecol.values[i][:2])
        month=np.int(datecol.values[i][3:5])
        year=np.int(datecol.values[i][6:10])
        if ~np.isnan(hourcol.values[i]):
            hour=np.int(np.floor(hourcol.values[i]/100.))
        else: hour = np.nan
        if hour >23: hour=0; day+=1
        if np.isnan(hour): hour=best_est
        d=datetime.datetime(year=year,month=month,day=day,hour=hour)
        date.append(d)
        years.append(year); months.append(month); days.append(day)
        hours.append(hour)
        
        
    return date,[years,months,days,hours]

def extract(var,var_dates,target_dates,thresh,stdv):
    
    """
    Simply iterates over target datetimes and extracts all rows in var
    that are within thresh hours of that time. All those values are then 
    averaged using a Gaussian kernel with standard deviation = stdv
    ""
    
    In:
        - var           : the variable we want to align
        - var_dates     : the dates of the variable 
        - target_dates  : the dates we want the variable for
        - thresh        : the number of hours either side of each date we want
                          to extract
        - stdv          : standard deviation (rows) to use in the Gaussian
                          kernel
        
    Out:
    
        - vout:         : the weighted average of the extracted variable 
        
    """    
    
    dt=datetime.timedelta(hours=thresh)
    out=np.zeros(len(target_dates))
    for i in range(len(target_dates)):
        
        idx=np.logical_and(var_dates>=target_dates[i]-dt,\
                           var_dates<=target_dates[i]+dt)
        if np.sum(idx)==2*thresh+1:
            out[i]=ndimage.gaussian_filter1d(var[idx],stdv)[(thresh+1)]
        else: out[i]=np.nan
        
    return out

# Infiles
indir="/home/lunet/gytm3/Everest2019/Research/HueyCollab/"
fi=indir+"log.txt"
fo=indir+"Climbs_Met.csv"
indir="/home/lunet/gytm3/Everest2019/Research/HueyCollab/"
wfile=indir+"Wind.csv"
pfile=indir+"Pressure.csv"
o3file=indir+"Ozone.csv"

# Formatting
sep="#"

# Best est 
best_est=8 # Best estimate of summit climbing time -- it's the mean summit hour
# Across all those summit where the time was recorded 

# Read
data=pd.read_csv(fi,sep="#")
wind=pd.read_csv(wfile,index_col=0,parse_dates=True); 
p=pd.read_csv(pfile,index_col=0,parse_dates=True);
o3=pd.read_csv(o3file,index_col=0,parse_dates=True); 

# Get the dates
dates,meta=himDate(data["msmtdate"],data["msmttime"],verb=False)

## Extract the met -- 12-hour mean centred on the respectiuve dates/times
# Winds
data["Wind_Gust"]=extract(wind.values[:],wind.index[:],dates,6,3.5)
# O2
data["Air_Pressure"]=extract(p.values[:],p.index[:],dates,6,3.5)
# O3
data["Ozone"]=extract(o3.values[:],o3.index[:],dates,6,3.5)

## Write out
data.to_csv(fo)
