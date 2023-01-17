#!/usr/bin/env python
# coding: utf-8

# # Amazon Web Scrapper

# In[ ]:


# Install Selenium and BeautifulSoup


# In[2]:


get_ipython().system('pip install selenium')
from selenium import webdriver


# In[3]:


get_ipython().system('pip install beautifulsoup4')
from bs4 import BeautifulSoup


# In[4]:


import csv


# # Startup webdriver

# In[5]:


driver = webdriver.Chrome()


# In[6]:


url = "https://www.amazon.com"
driver.get(url)


# In[7]:


def get_url(search_term):
    #generate url from search term
    template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss"
    search_term = search_term.replace(" ", "+")
    return template.format(search_term)


# In[8]:


url = get_url("ultrawide monitor")
print(url)


# In[9]:


driver.get(url)


# In[10]:


soup = BeautifulSoup(driver.page_source, "html.parser") 


# In[11]:


results = soup.find_all("div", {"data-component-type": "s-search-result"})


# In[12]:


len(results)


# # Extract Collection

# In[ ]:


# Extract item's price


# In[14]:


item = results [0]


# In[15]:


atag = item.h2.a


# In[17]:


description = atag.text.strip()


# In[18]:


url = "https://www.amazon.com" + atag.get("href")


# In[19]:


price_parent = item.find( "span", "a-price")


# In[49]:


price = price_parent.find("span", "a-offscreen").text


# In[21]:


# Extract item's rating 


# In[53]:


rating = item.i.text


# In[54]:


rating_count = item.find('span', 'a-size-base s-underline-text').text


# # Generalize the Pattern

# In[173]:


# extract and return data from a single record 


# In[212]:


def extract_records(item):
    
    #item's description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = "https://www.amazon.com" + atag.get("href")
    
    #item's price
    price_parent = item.find( "span", "a-price")
    price = price_parent.find("span", "a-offscreen").text
    
    #item's rank
    rating = item.i.text
    rating_count = item.find('span', 'a-size-base s-underline-text').text
    
    result = (description, price, rating, rating_count, url)
    
    return result
    


# In[213]:


records = []
results = soup.find_all("div", {"data-component-type": "s-search-result"})

for item in results:
    records.append(extract_records(item))


# # Error Handling

# In[218]:


def extract_records(item):
    
    #item's description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = "https://www.amazon.com" + atag.get("href")
    
    
    try:
        #item's price
        price_parent = item.find( "span", "a-price")
        price = price_parent.find("span", "a-offscreen").text
    except AttributeError:
        return
    try:
        #item's rank
        rating = item.i.text
        rating_count = item.find('span', 'a-size-base s-underline-text').text
    except AttributeError:
        rating = ""
        rating_count= ""
    
    result = (description, price, rating, rating_count, url)
    
    return result


# In[219]:


records = []
results = soup.find_all("div", {"data-component-type": "s-search-result"})

for item in results:
    record = extract_record(item)
    if record:
        records.append(record)


# In[220]:


records [0]


# In[221]:


for row in records:
    print(row[1])


# # Extract Data from Next page

# In[222]:


def get_url(search_term):
    
    #generate url from search term
    template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss"
    search_term = search_term.replace(" ", "+")
    return template.format(search_term)

    # add term query to url
    url = template.format(search_term)
    
    # add page query to placeholder
    url += '&page{}'
    
    return url


# # Combine all extract data 

# In[223]:


import csv
from selenium import webdriver
from bs4 import BeautifulSoup

def get_url(search_term):
    
    #generate url from search term
    template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss"
    search_term = search_term.replace(" ", "+")
    return template.format(search_term)

    # add term query to url
    url = template.format(search_term)
    
    # add page query to placeholder
    url += '&page{}'
    
    return url

def extract_records(item):
    
    #item's description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = "https://www.amazon.com" + atag.get("href")
    
    
    try:
        #item's price
        price_parent = item.find( "span", "a-price")
        price = price_parent.find("span", "a-offscreen").text
    except AttributeError:
        return
    try:
        #item's rank
        rating = item.i.text
        rating_count = item.find('span', 'a-size-base s-underline-text').text
    except AttributeError:
        rating = ""
        rating_count= ""
    
    result = (description, price, rating, rating_count, url)
    
    return result

def main(search_term):
    #run main program routine
    
    #startup webdriver
    driver = webdriver.Chrome()
    
    records = []
    url = get_url(search_term)
    
    for page in range (1, 21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.find_all("div", {"data-component-type": "s-search-result"})
        
    for item in results:
        record = extract_record(item)
        if record:
            records.append(record) 
            
    driver.close()
    
    #save data to csv file
    with open("result.csv", "w", newline = "" , encoding = "utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Description", "Price", "Rating", "Rating_count", "Url"])
        writer.writerows(records)


# In[224]:


main("ultrawide monitor")

