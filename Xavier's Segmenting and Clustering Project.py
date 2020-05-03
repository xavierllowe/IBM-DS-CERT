#!/usr/bin/env python
# coding: utf-8

# In[18]:


import numpy as np # library to handle data in a vectorized manner
import pandas as pd # library for data analsysis
import requests # Library for web scraping

print('Libraries imported.')


# In[19]:


import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import csv

print('BeautifulSoup  & csv imported.')


# #### Extracting Raw Table

# In[20]:


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print('SSL certificate errors ignored.')


# In[21]:


source = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text

soup = BeautifulSoup(source, 'lxml')

#print(soup.prettify())
print('soup ready')


# In[22]:


table = soup.find('table',{'class':'wikitable sortable'})


# In[23]:


table_rows = table.find_all('tr')


# In[25]:


data = []
for row in table_rows:
    data.append([t.text.strip() for t in row.find_all('td')])

df = pd.DataFrame(data, columns=['PostalCode', 'Borough', 'Neighbourhood'])
df = df[~df['PostalCode'].isnull()]  # to filter out bad rows

df.head(5)


# In[26]:


df.info()


# In[27]:


df.shape


# ### DataFrame Cleaning

# In[29]:


import pandas
import requests
from bs4 import BeautifulSoup
website_text = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text
soup = BeautifulSoup(website_text,'lxml')

table = soup.find('table',{'class':'wikitable sortable'})
table_rows = table.find_all('tr')

data = []
for row in table_rows:
    data.append([t.text.strip() for t in row.find_all('td')])

df = pandas.DataFrame(data, columns=['PostalCode', 'Borough', 'Neighbourhood'])
df = df[~df['PostalCode'].isnull()]  # to filter out bad rows

df.head(15)


# In[30]:


df.drop(df[df['Borough']=="Not assigned"].index,axis=0, inplace=True)
df.head()


# In[31]:


df1 = df.reset_index()
df1.info()


# In[32]:


df1.shape


# In[33]:


df2= df1.groupby('PostalCode').agg(lambda x: ','.join(x))
df2.head()


# In[34]:


df2.info()


# In[35]:


df2.shape


# In[36]:


df2.loc[df2['Neighbourhood']=="Not assigned",'Neighbourhood']=df2.loc[df2['Neighbourhood']=="Not assigned",'Borough']
df2.head()


# In[37]:


df3 = df2.reset_index()
df3['Borough']= df3['Borough'].str.replace('nan|[{}\s]','').str.split(',').apply(set).str.join(',').str.strip(',').str.replace(",{2,}",",")
df3.head()


# In[ ]:




