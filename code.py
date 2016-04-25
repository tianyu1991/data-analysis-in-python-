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
type_2011 = data_2011['Type_'].value_counts()
type_2012 = data_2012['Type_'].value_counts()
type_2013 = data_2013['Type_'].value_counts()
type_2014 = data_2014['Type_'].value_counts()
type_2015 = data_2015['Type_'].value_counts()
type_counts={'2011':type_2011[1:10],
             '2012':type_2012[1:10],
             '2013':type_2013[1:10],
             '2014':type_2014[1:10],
             '2015':type_2015[1:10],
            }
DataFrame(type_counts).plot(kind='bar').set_title('Types of Calls in 201-2015')
plt.savefig('C:/Users/tianyu/Desktop/0415/types.png', dpi=400, bbox_inches='tight')


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

%matplotlib inline
delta3=delta2.ix['11']
def cut_time(delta3):
    a=DataFrame(delta3[delta3 > 0 ],columns=['time'])
    li_t=np.arange(0,4.5,0.5)
    bins=list( 10**li_t)
    cut = pd.cut(a['time'], bins)
    cuts=cut.value_counts()
    cuts=cuts.sort_index()
    return cuts

time_counts={'2011':cut_time(delta2.ix['11']),
             '2012':cut_time(delta2.ix['12']),
             '2013':cut_time(delta2.ix['13']),
             '2014':cut_time(delta2.ix['14']),
             '2015':cut_time(delta2.ix['15']),
            }


time_counts=DataFrame(time_counts)


ax=time_counts.plot(kind='line',title='The distribution of response time')
labels = ax.set_xticklabels(['0-0.5','0.5-1', '1-1.5', '1.5-2', '2-2.5', '2.5-3','3-3.5','3.5-4'], rotation=30, fontsize='small')
ax.set_xlabel('log(Response time)')
ax.set_ylabel('the numbers of call')
plt.savefig('C:/Users/tianyu/Desktop/0415/figpath.png', dpi=400, bbox_inches='tight')



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
Type_2011=data_2011['Type_'].value_counts()
Type_2015=data_2015['Type_'].value_counts()
t=Types_diff[Types_diff==min(Types_diff)].index
float(Type_2011.ix['89']-Type_2015.ix['89'])/sum(Type_2011)
##0.00035087512961797733

##The disposition represents the action that was taken to address the serivce call. 
##Consider how the disposition of calls changes with the hour of the record's
##creation time. Find the disposition whose fraction of that hour's disposition 
##varies the most over a typical day. What is its change (maximum fraction minus minimum fraction)?


We can use the call locations to estimate the areas of the police districts. Represent each as an ellipse with semi-axes given by a single standard deviation of the longitude and latitude. What is the area, in square kilometers, of the largest district measured in this manner?


The calls are assigned a priority. Some types of calls will receive a greater variety of priorities. To understand which type of call has the most variation in priority, find the type of call whose most common priority is the smallest fraction of all calls of that type. What is that smallest fraction?
