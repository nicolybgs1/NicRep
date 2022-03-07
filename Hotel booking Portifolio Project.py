#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


hotel_df=pd.read_csv(r'C:\Users\ninic\Downloads\hotel_bookings.csv')
hotel_df.head()


# In[3]:


#Performing Data Cleaning and Data Pre-Processing on data

hotel_df.shape


# In[4]:


hotel_df.isnull().values.any()


# In[5]:


hotel_df.isnull().sum()


# In[6]:


hotel_df.fillna(0,inplace=True)
hotel_df.isnull().sum()


# In[7]:


hotel_df['meal'].value_counts()


# In[8]:


hotel_df['children'].unique()


# In[9]:


hotel_df['adults'].unique()


# In[10]:


hotel_df['babies'].unique()


# In[11]:


filter=(hotel_df['children']==0) & (hotel_df['adults']==0) & (hotel_df['babies']==0)
hotel_df[filter]


# In[12]:


data=hotel_df[~filter]


# In[13]:


data.head()


# In[14]:


#Where do the guests come from and also Perform Spatial Analysis
resort=data[(data['hotel']=='Resort Hotel') & (data['is_canceled']==0)]
city=data[(data['hotel']=='City Hotel') & (data['is_canceled']==0)] 


# In[15]:


resort.shape


# In[16]:


get_ipython().system('pip install plotly')
import plotly.graph_objs as go
from plotly.offline import iplot
import plotly.express as px


# In[17]:


labels=resort['country'].value_counts().index
values=resort['country'].value_counts() 


# In[18]:


trace=go.Pie(labels=labels,values=values,hoverinfo='label+percent', textinfo='value')


# In[19]:


iplot([trace])


# In[20]:


country_wise_data=data[data['is_canceled']==0]['country'].value_counts().reset_index()


# In[21]:


country_wise_data.columns=['country','No of guests']
country_wise_data.head()


# In[22]:


px.choropleth(country_wise_data,
             locations=country_wise_data['country'],
              color=country_wise_data['No of guests'],
              hover_name=country_wise_data['country'],
              title='Home country of guests'
             )


# In[23]:


#We can conclude that the hotel has guests from all over the worls but most of them are from Europe, especially Portugal.


# In[24]:


#How much do guests pay for a room per night?
data.head()


# In[25]:


data2=data[data['is_canceled']==0]


# In[26]:


plt.figure(figsize=(12,8))
sns.boxplot(x='reserved_room_type',y='adr',data=data2,hue='hotel')
plt.title('Average price of room type per night', fontsize=16)
plt.xlabel('Room type')
plt.ylabel('Price in [EUR] per night')
plt.show()


# In[42]:


#How does the price per night vary over the year?


# In[41]:


data_resort=resort[resort['is_canceled']==0]


# In[28]:


data_city=city[city['is_canceled']==0]


# In[29]:


data_resort.head()


# In[30]:


data_city.head()


# In[31]:


resort_hotel=data_resort.groupby('arrival_date_month')['adr'].mean().reset_index()


# In[32]:


resort_hotel.head()


# In[33]:


city_hotel=data_city.groupby('arrival_date_month')['adr'].mean().reset_index()                        


# In[34]:


city_hotel.head()


# In[35]:


final_data=resort_hotel.merge(city_hotel,on='arrival_date_month')
final_data.columns=['Month','Price for Resort hotel','Price for City hotel']


# In[36]:


final_data.head()


# In[39]:


get_ipython().system('pip install sorted-months-weekdays')
get_ipython().system('pip install sort-dataframeby-monthorweek')


# In[40]:


import sort_dataframeby_monthorweek as sd


# In[47]:


final_data2=sd.Sort_Dataframeby_Month(final_data,'Month')


# In[49]:


final_data2.head()


# In[57]:


px.line(data_frame=final_data2,x='Month',
             y=['Price for Resort hotel','Price for City hotel'],
             title='Room price per night over the year')


# In[58]:


#Distribution of nights spent at Hotels by Market Segment and Hotel Type


# In[59]:


data.head()


# In[61]:


plt.figure(figsize=(15,10))
sns.boxplot(x='market_segment',y='stays_in_weekend_nights',data=data,hue='hotel')


# In[64]:


#Analysing Preference of Guests, what they basically prefer?


# In[65]:


data['meal'].value_counts()


# In[66]:


px.pie(data,values=data['meal'].value_counts(),names=data['meal'].value_counts().index,hole=0.5)


# In[67]:


#Analyse special request done by customers


# In[68]:


data.head()


# In[69]:


sns.countplot(data['total_of_special_requests'])


# In[70]:


#Create a Pivot table of relationship between special requests and cancellation booking status.


# In[71]:


data.columns


# In[76]:


pivot=data.groupby(['total_of_special_requests','is_canceled']).agg({'total_of_special_requests':'count'}).rename(columns={'total_of_special_requests':'total_count'}).unstack()


# In[78]:


pivot.plot(kind='bar',title='Relationship between cancelled bookings and special requests')


# In[79]:


#Which are the most busy month or in which month guests are high?


# In[81]:


data_resort.head()


# In[85]:


busy_resort=data_resort['arrival_date_month'].value_counts().reset_index()
busy_resort.columns=['Month','No of guests']
busy_resort


# In[86]:


data_city.head()


# In[87]:


busy_city=data_city['arrival_date_month'].value_counts().reset_index()
busy_city.columns=['Month','No of guests']
busy_city


# In[88]:


final_busy=busy_resort.merge(busy_city,on='Month')


# In[90]:


final_busy.columns=['Month','No of guests in resort','No of guests in city']
final_busy


# In[91]:


import sort_dataframeby_monthorweek as sd


# In[92]:


final_busy=sd.Sort_Dataframeby_Month(final_busy,'Month')


# In[93]:


final_busy.head()


# In[97]:


px.line(data_frame=final_busy,x='Month',
             y=['No of guests in resort','No of guests in city'],
             title='Total of guests by month in each hotel')


# In[98]:


#How long do people stay at the hotels?


# In[99]:


data.head()


# In[100]:


filter=data['is_canceled']==0
clean_data=data[filter]


# In[102]:


clean_data['total_nights']=clean_data['stays_in_weekend_nights'] + clean_data['stays_in_week_nights']


# In[103]:


clean_data.head()


# In[108]:


final_clean=clean_data.groupby(['total_nights','hotel']).agg('count').reset_index()
final_clean=final_clean.iloc[:,0:3]
final_clean.head()


# In[109]:


final_clean=final_clean.rename(columns={'is_canceled':"number of stays"})


# In[110]:


final_clean.head()


# In[117]:


plt.figure(figsize=(20,8))
sns.barplot(data=final_clean, x='total_nights', y='number of stays', hue='hotel', hue_order=['City Hotel', 'Resort Hotel'])


# In[118]:


#Bookings by market segment


# In[119]:


clean_data.columns


# In[122]:


mkt_data=clean_data['market_segment'].value_counts()
mkt_data


# In[124]:


px.pie(clean_data, values=mkt_data, names=mkt_data.index, title='Bookings by market segment')


# In[125]:


#Price per night (ADR) and person based on booking and room


# In[126]:


clean_data.columns


# In[128]:


plt.figure(figsize=(20,10))
sns.barplot(data=clean_data, x='market_segment',y='adr', hue='reserved_room_type')


# In[129]:


#How many booking were cancelled?


# In[132]:


cancel=data[data['is_canceled']==1]
cancel.head()


# In[133]:


len(cancel[cancel['hotel']=='Resort Hotel'])


# In[134]:


len(cancel[cancel['hotel']=='City Hotel'])


# In[136]:


px.pie(values=[11120,33079],names=['Resort Hotel cancellations', 'City Hotel cancellations'],title='Numbers of cancellation in each hotel')


# In[137]:


#Which month has the highest number of cancellations?


# In[142]:


cancelm=cancel['arrival_date_month'].value_counts().reset_index()
cancelm.columns=['Month','Number of cancellations']
cancelm


# In[143]:


import sort_dataframeby_monthorweek as sd


# In[144]:


final_cancelm=sd.Sort_Dataframeby_Month(cancelm,'Month')


# In[145]:


final_cancelm.head()


# In[147]:


plt.figure(figsize=(20,8))
sns.barplot(data=final_cancelm, x='Month', y='Number of cancellations')


# In[ ]:




