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


# In[27]:


#How does the price per night vary over the year?


# In[28]:


data_resort=resort[resort['is_canceled']==0]


# In[29]:


data_city=city[city['is_canceled']==0]


# In[30]:


data_resort.head()


# In[31]:


data_city.head()


# In[32]:


resort_hotel=data_resort.groupby('arrival_date_month')['adr'].mean().reset_index()


# In[33]:


resort_hotel.head()


# In[34]:


city_hotel=data_city.groupby('arrival_date_month')['adr'].mean().reset_index()                        


# In[35]:


city_hotel.head()


# In[36]:


final_data=resort_hotel.merge(city_hotel,on='arrival_date_month')
final_data.columns=['Month','Price for Resort hotel','Price for City hotel']


# In[37]:


final_data.head()


# In[38]:


get_ipython().system('pip install sorted-months-weekdays')
get_ipython().system('pip install sort-dataframeby-monthorweek')


# In[39]:


import sort_dataframeby_monthorweek as sd


# In[40]:


final_data2=sd.Sort_Dataframeby_Month(final_data,'Month')


# In[41]:


final_data2.head()


# In[46]:


px.line(data_frame=final_data2,x='Month',
             y=['Price for Resort hotel','Price for City hotel'],
             title='Room price per night over the year')


# In[44]:


#Distribution of nights spent at Hotels by Market Segment and Hotel Type


# In[45]:


data.head()


# In[46]:


plt.figure(figsize=(15,10))
sns.boxplot(x='market_segment',y='stays_in_weekend_nights',data=data,hue='hotel')


# In[47]:


#Analysing Preference of Guests, what they basically prefer?


# In[48]:


data['meal'].value_counts()


# In[48]:


px.pie(data,values=data['meal'].value_counts(),names=data['meal'].value_counts().index,hole=0.5)


# In[50]:


#Analyse special request done by customers


# In[51]:


data.head()


# In[52]:


sns.countplot(data['total_of_special_requests'])


# In[53]:


#Create a Pivot table of relationship between special requests and cancellation booking status.


# In[54]:


data.columns


# In[55]:


pivot=data.groupby(['total_of_special_requests','is_canceled']).agg({'total_of_special_requests':'count'}).rename(columns={'total_of_special_requests':'total_count'}).unstack()


# In[56]:


pivot.plot(kind='bar',title='Relationship between cancelled bookings and special requests')


# In[57]:


#Which are the most busy month or in which month guests are high?


# In[58]:


data_resort.head()


# In[59]:


busy_resort=data_resort['arrival_date_month'].value_counts().reset_index()
busy_resort.columns=['Month','No of guests']
busy_resort


# In[60]:


data_city.head()


# In[61]:


busy_city=data_city['arrival_date_month'].value_counts().reset_index()
busy_city.columns=['Month','No of guests']
busy_city


# In[62]:


final_busy=busy_resort.merge(busy_city,on='Month')


# In[63]:


final_busy.columns=['Month','No of guests in resort','No of guests in city']
final_busy


# In[64]:


import sort_dataframeby_monthorweek as sd


# In[65]:


final_busy=sd.Sort_Dataframeby_Month(final_busy,'Month')


# In[66]:


final_busy.head()


# In[67]:


px.line(data_frame=final_busy,x='Month',
             y=['No of guests in resort','No of guests in city'],
             title='Total of guests by month in each hotel')


# In[68]:


#How long do people stay at the hotels?


# In[69]:


data.head()


# In[70]:


filter=data['is_canceled']==0
clean_data=data[filter]


# In[71]:


clean_data['total_nights']=clean_data['stays_in_weekend_nights'] + clean_data['stays_in_week_nights']


# In[72]:


clean_data.head()


# In[73]:


final_clean=clean_data.groupby(['total_nights','hotel']).agg('count').reset_index()
final_clean=final_clean.iloc[:,0:3]
final_clean.head()


# In[74]:


final_clean=final_clean.rename(columns={'is_canceled':"number of stays"})


# In[75]:


final_clean.head()


# In[76]:


plt.figure(figsize=(20,8))
sns.barplot(data=final_clean, x='total_nights', y='number of stays', hue='hotel', hue_order=['City Hotel', 'Resort Hotel'])


# In[77]:


#Bookings by market segment


# In[78]:


clean_data.columns


# In[79]:


mkt_data=clean_data['market_segment'].value_counts()
mkt_data


# In[80]:


px.pie(clean_data, values=mkt_data, names=mkt_data.index, title='Bookings by market segment')


# In[81]:


#Price per night (ADR) and person based on booking and room


# In[82]:


clean_data.columns


# In[83]:


plt.figure(figsize=(20,10))
sns.barplot(data=clean_data, x='market_segment',y='adr', hue='reserved_room_type')


# In[84]:


#How many booking were cancelled?


# In[85]:


cancel=data[data['is_canceled']==1]
cancel.head()


# In[86]:


len(cancel[cancel['hotel']=='Resort Hotel'])


# In[87]:


len(cancel[cancel['hotel']=='City Hotel'])


# In[88]:


px.pie(values=[11120,33079],names=['Resort Hotel cancellations', 'City Hotel cancellations'],title='Numbers of cancellation in each hotel')


# In[89]:


#Which month has the highest number of cancellations?


# In[90]:


cancelm=cancel['arrival_date_month'].value_counts().reset_index()
cancelm.columns=['Month','Number of cancellations']
cancelm


# In[91]:


import sort_dataframeby_monthorweek as sd


# In[92]:


final_cancelm=sd.Sort_Dataframeby_Month(cancelm,'Month')


# In[93]:


final_cancelm.head()


# In[94]:


plt.figure(figsize=(20,8))
sns.barplot(data=final_cancelm, x='Month', y='Number of cancellations')


# In[49]:


iplot.init_notebook_mode()


# In[ ]:




