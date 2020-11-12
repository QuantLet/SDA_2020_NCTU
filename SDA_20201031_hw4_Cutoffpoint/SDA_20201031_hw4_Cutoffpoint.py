#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import pylab


# In[2]:


mu= 0
sigma = 1
number = 100000


# In[3]:


dataset = np.random.normal(mu, sigma, number)


# In[4]:


count, bins, ignored=plt.hist(dataset, 50, density=True)
plt.plot(bins, 1/(sigma * np.sqrt(2*np.pi))*np.exp(-(bins-mu)**2/(2*sigma**2)), linewidth=2, color='y')
plt.show()


# In[5]:


q25= np.quantile(dataset, 0.25)
q75= np.quantile(dataset, 0.75)


# In[6]:


print("\nQuantile 25%: ", q25)
print("\nQuantile 75%: ", q75)


# In[7]:


w=q75+1.5*(q75-q25)
print("\nUpper cut off point: ", w)


# In[8]:


pylab.rcParams['figure.figsize']=(9.0,6.0)


# In[9]:


plt.boxplot(dataset)
plt.ylabel(("values"))
plt.title("Boxplot")


# In[10]:


from scipy import stats
phi = stats.norm.cdf(w, loc=0, scale=1)
print("cdf of w is: ", phi)


# In[11]:


p=2*(1-phi)
print("probability of data outside the upper cut point= ", p)


# In[ ]:




