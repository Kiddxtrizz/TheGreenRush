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


#modules needed for function
import pandas as pd
from sodapy import Socrata


def get_dataset_name(x):
    
    """
    Create a function to pull 
    in the name of the dataset
    for the corresponding api endpoint 
    """
    
    #formatting for the final table
    #want to display the full name 
    #of the dataset
    pd.options.display.max_colwidth = 200
    
    #setup a basic client
    client = Socrata("opendata.mass-cannabis-control.com", None)
    
    # list comprehension to capture relevant metadata (i.e. Name)
    dataset_name = [client.get_metadata(y)['name'] for y in x]
    
    # combine the api-endpoints
    # with the name of the assoc.
    # dataset 
    data = list(zip(x, dataset_name))
    
    #store final result into dataframe
    api_table = pd.DataFrame(data, columns=['api_endpoints', 'Name']).drop_duplicates().reset_index(drop=True)

    return api_table


# function to select dataset 
import time
import pandas as pd
from sodapy import Socrata 

def choose_dataset(x, limit):
    """
    Create a function to take
    in an api endpoint and 
    output the results
    """
    
    #setup a basic client
    client = Socrata("opendata.mass-cannabis-control.com", None)
    
    # get columns
    cols = x.columns
    
    # store api keys in a list
    list_of_endpts = x[cols[0]].to_list()

    # store user input 
    user_input = input("Which dataset are you interested in viewing?\nPlease choose an index (i.e. row number) from the table above: ")
    
    time.sleep(2)
    
    limit = 2000
    
    #transform string
    user_input = int(user_input) 
    
    # endpoint selection
    try:
        submit = list_of_endpts[user_input]
    except (KeyError, IndexError):
        print('\n\nYou did not choose a number listed in the table above; Try again...\n\n')
        
        time.sleep(1)
        
        user_input = input("Which dataset are you interested in viewing?\nPlease choose an index (i.e. row number) from the table above: ")
        submit = list_of_endpts[user_input]
    else:
    
        # Pull data via api enpoint 
        results = client.get(f"{submit}", limit=limit)

        # Convert to pandas DataFrame
        results_df = pd.DataFrame.from_records(results)
    
    return results_df

# Converters
import pandas as pd


def convert_to_csv(x):
    
    # store user input 
    user_input = input("What would you like to name your file?:  ")
    
    # convert dataframe to csv
    x.to_csv(f"{user_input}"+".csv")
    
    