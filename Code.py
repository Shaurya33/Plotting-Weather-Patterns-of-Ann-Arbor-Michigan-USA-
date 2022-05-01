# The following coding has been done in Jupyter Notebook.


import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import datetime as dt
%matplotlib notebook

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

#leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')

df=pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df['Date']=pd.to_datetime(df['Date'])
df['year'] = pd.DatetimeIndex(df['Date']).year


# In[2]:

df=df.sort_values(by=['Date'])


# In[3]:

rec_high=df.where(df['Element']=='TMAX')


# In[4]:

rec_high=rec_high.dropna()


# In[5]:

rec_low=df.where(df['Element']=='TMIN')
rec_low.dropna(inplace=True)


# In[6]:

rec_high=rec_high.groupby('Date')['Data_Value'].max()
rec_low=rec_low.groupby('Date')['Data_Value'].min()


# In[7]:

rec_high=rec_high.to_frame()
rec_low=rec_low.to_frame()


# In[8]:

rec_high.reset_index(inplace=True)
rec_low.reset_index(inplace=True)


# In[9]:

rec_high['Year']=pd.DatetimeIndex(rec_high['Date']).year
rec_low['Year']=pd.DatetimeIndex(rec_low['Date']).year


# In[10]:

date=df['Date'].unique()


# In[11]:


plt.plot(date,rec_high['Data_Value'],color='#DC143C',label='Max. Temperatures',linewidth=0.5)
plt.plot(date,rec_low['Data_Value'],color='b',label='Min. Temperatures',linewidth=0.5)

plt.fill_between(date,rec_high['Data_Value'],rec_low['Data_Value'],label='Shaded Area',color='#FBDD7E',interpolate=True)

filt= (rec_high["Year"]==2015)
rec_high=rec_high[filt]

filt= (rec_low["Year"]==2015)
rec_low=rec_low[filt]

filt=rec_low['Data_Value']== rec_low['Data_Value'].min()
x=rec_low[filt]['Date']
y=rec_low[filt]['Data_Value']

plt.plot(x,y,marker='v',c='r',label='Min_Record_Temp')

plt.legend(fontsize=7)
plt.title("Ann Arbor Temperature Patterns",fontsize=15)
plt.xlabel("Year",fontsize=15)
plt.ylabel("Temperature(Tenths of *C)",fontsize=15)
plt.tight_layout()
