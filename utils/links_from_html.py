
# coding: utf-8

# In[12]:

import urllib
from bs4 import BeautifulSoup

f = open('links.txt', 'w')

x = urllib.request.urlopen("http://www.consultant.ru/popular/").read()
soup = BeautifulSoup(x, "lxml")

#soup.prettify()
for link in soup.find_all('a'):
    #print(link.get('href'))
    f.write(str(link.get('href')))
    f.write('\n')


f.close()


# In[ ]:



