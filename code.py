from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_2011= pd.read_csv('C:/Users/tianyu/Desktop/0415/Calls_for_Service_2011.csv')
data_2012= pd.read_csv('C:/Users/tianyu\Desktop/0415/Calls_for_Service_2012.csv')
data_2013= pd.read_csv('C:/Users/tianyu\Desktop/0415/Calls_for_Service_2013.csv')
data_2014= pd.read_csv('C:/Users/tianyu\Desktop/0415/Calls_for_Service_2014.csv')
data_2015= pd.read_csv('C:/Users/tianyu\Desktop/0415/Calls_for_Service_2015.csv')

data_sum=pd.concat([data_2011, data_2012,data_2013, data_2014,data_2015])


##What fraction of calls are of the most common type?
type_counts = data_sum['Type_'].value_counts()
print float(type_counts[1])/data_sum['Type_'].count()
##0.167121426631

##Some calls result in an officer being dispatched to the scene, 
##and some log an arrival time. What is the median response time 
##(dispatch to arrival), in seconds, considering only valid (i.e. non-negative) times?
subdata=data_sum[['TimeDispatch','TimeArrive']]
subdata2=subdata[pd.notnull(subdata['TimeArrive'])&pd.notnull(subdata['TimeDispatch'])]
from datetime import datetime
arrive_time=pd.to_datetime(subdata2['TimeArrive'],format='%m/%d/%Y %I:%M:%S %p')
dispatch_time=pd.to_datetime(subdata2['TimeDispatch'],format='%m/%d/%Y %I:%M:%S %p')
delta=arrive_time-dispatch_time

delta2=map(lambda x:float(x.seconds),delta)
np.median(delta2)
##285.0

##Work out the average (mean) response time in each district. What is the difference 
##between the average response times of the districts with the longest and shortest times?
data = {'ResponseTime':delta2,'District': subdata2['PoliceDistrict']}
frame = DataFrame(data)
t_grouped = frame.groupby(['District'])[['ResponseTime']].mean()
np.max(t_grouped)-np.min(t_grouped)
##186.398124


##We can define surprising event types as those that occur more often in a district than 
##they do over the whole city. What is the largest ratio of the conditional probability
##of an event type given a district to the unconditional probably of that event type? 
##Consider only events types which have more than 100 events. Note that some events have 
##their locations anonymized and are reported as being in district "0". These should be ignored.
clean_data=data_sum[['Type_','PoliceDistrict']][data_sum['PoliceDistrict']!=0]
type_counts = clean_data['Type_'].value_counts()
types=type_counts[type_counts>100].index
maxfr=0.0
for t in types:
    sub_data_type=clean_data[clean_data['Type_']==t]
    t_grouped = sub_data_type.groupby(['PoliceDistrict']).count()
    fr=float(np.max(t_grouped))/np.mean(t_grouped)
    if (any(fr>maxfr)==True):
        maxfr=fr    
maxfr
##7.369143


##Find the call type that displayed the largest percentage decrease in volume between 
##2011 and 2015. What is the fraction of the 2011 volume that this decrease represents? 
##The answer should be between 0 and 1.
