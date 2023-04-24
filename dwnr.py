import os
import requests
from bs4 import BeautifulSoup
import time

# Enter the keywords you want to search for
keywords = 'access control using machine learning'

# Construct the base search URL
base_url = 'https://scholar.google.com/scholar?start=0&q=context+aware+machine+learning+in+access+control&hl=hi&as_sdt=0,5'

# Set the number of pages to fetch
num_pages = 5

# Create the downloads folder if it doesn't exist
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Loop over the search result pages
for i in range(num_pages):
    # Construct the search URL for the current page
    url = base_url + '+'.join(keywords.split()) + '&start=' + str(i*10)
    print(url)

    # Send a request to the URL to get the response
    #response = requests.get(url)
    response = requests.get(url, timeout=10)

    # Check if the request was successful
    if response.status_code == 200:
        # If successful, parse the response using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the links on the page
        links = soup.find_all('a')

        # Extract the links to downloadable documents
        document_links = []
        for link in links:
            href = link.get('href')
            if href and ('.pdf' in href or '.doc' in href or '.docx' in href):
                document_links.append(href)

        # Download the documents
        for link in document_links:
            # Send a request to the link to get the response
            document_response = requests.get(link)

            # Check if the request was successful
            if document_response.status_code == 200:
                # If successful, get the content of the file
                file_content = document_response.content

                # Write the content to a file in the downloads folder
                file_path = os.path.join('downloads', link.split('/')[-1])
                with open(file_path, 'wb') as file:
                    file.write(file_content)

                print('Downloaded', file_path)
                time.sleep(1)
            else:
                # If not successful, print an error message
                print('Error downloading', link, document_response.status_code)
    else:
        # If not successful, print an error message
        print('Error:', response.status_code)
