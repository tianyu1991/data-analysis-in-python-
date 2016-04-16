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
arrive_time=map(lambda x:datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p'),subdata2['TimeArrive'])
dispatch_time=map(lambda x:datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p'),subdata2['TimeDispatch'])
delta=map(lambda x,y:x-y, arrive_time, dispatch_time)
delta2=map(lambda x:x.seconds,delta)
delta3=delta2[delta2>=0]
np.median(delta3)
##1254.0
