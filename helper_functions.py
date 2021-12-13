# import requests module 
import requests
import re
from bs4 import BeautifulSoup
import time

def get_endpoints(url):
   
    # We need a URl to start the process
    # Make a request to the URL 
    # Check for status code 200... 

    prefix = url #store url 
    response = requests.get(prefix)
    time.sleep(1)
    
    """
    Use bs4 to build a grapg to loop 
    through the available webpages and 
    capture relevant links with API endpoints.
    """
    # store the content from the url
    # into a variable (e.g. content)
    context = response.content
    
    #parse native HTML tags
    soup = BeautifulSoup(context, "html.parser")
    
        
    # Create Variables to store results from loop     
    pages = list()
     

    """
    Get the next page prefix 
    
    """
    for links in soup.find_all('a'):
        #if type is equal to str 
        if type(links.get('href')) == str:
             #if string contains dev or opendata 
            if re.findall(r'[/browse]\W+(page)', links.get('href') ):
                pages.append(links.get('href'))
    
    
    """
    Create a while loop
    to capture all of the 
    endpoints
    
    """
    
    
    count= 0
    api_endpoints = list()
    # opendata = list()
    page_sort = sorted(list(pages))
    
    while count < len(set(pages)):
    
    
        webpage = requests.get(prefix[:-7]+page_sort[count])
        content = webpage.content
        apis = BeautifulSoup(content, "html.parser")


        for api in apis.find_all('a'):
        #if type is equal to str 
            if type(api.get('href')) == str:
             #if string contains dev or opendata 
                if re.findall(r'\w+\W+(foundry)', api.get('href') ):
                    api_endpoints.append(api.get('href'))
                # elif re.findall(r'\w+\W+(opendata)', api.get('href') ):
                #     api_endpoints.append(api.get('href'))

        count += 1
        time.sleep(1)
    
    """
    Parse the links 
    to get the coveted 
    enpoints
    """
    
    ep = [endpoints[-9:].strip() for endpoints in api_endpoints]
    
    return ep