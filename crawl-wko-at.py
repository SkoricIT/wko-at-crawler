# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import math  # For rounding up the number of pages

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0'
}

# The base URL to scrape data from
base_url = "https://firmen.wko.at/-/wien/?branche=25376&branchenname=immobilienmakler&page="

# List to store all data
all_data = []

# Start with the first page to extract total results and results per page
print("Processing page: 1")
first_page_url = base_url + "1"

# Send a GET request to the first page URL
response = requests.get(first_page_url, headers=headers)

# Parse the HTML content of the page with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract total number of results
try:
    result_counter = soup.find('div', {'class': 'result-counter'})
    total_results_text = result_counter.find('span', {'class': 'treffer'}).text.strip()
    total_results = int(''.join(filter(str.isdigit, total_results_text)))
    print(f"Total results found: {total_results}")
except Exception as e:
    print(f"Error extracting total results: {e}")
    total_results = 0

# Determine the number of results per page
rows = soup.find_all("article", {"class": "search-result-article"})
results_per_page = len(rows)
print(f"Results per page: {results_per_page}")

# Calculate total number of pages needed
if results_per_page > 0:
    total_pages = math.ceil(total_results / results_per_page)
else:
    total_pages = 1
print(f"Total pages to process: {total_pages}")

# Function to extract data from a single row
def extract_data(row):
    data = {}
    # Extract the company name
    try:
        data['name'] = row.find('h3').text.strip()
    except:
        data['name'] = ''

    # Extract the street address
    try:
        data['street'] = row.find('div', {'class': 'street'}).text.strip()
    except:
        data['street'] = ''

    # Extract the place and split into zip and city
    try:
        place_text = row.find('div', {'class': 'place'}).text.strip()
        # Replace non-breaking spaces and split
        zip_and_city = place_text.replace('\xa0', ' ').split()
        data['zip'] = zip_and_city[0]
        data['city'] = ' '.join(zip_and_city[1:])
    except:
        data['zip'] = ''
        data['city'] = ''

    # Extract contact info
    contact_info = row.find('div', {'class': 'contact-info'})
    data['phone'] = ''
    data['email'] = ''
    data['web'] = ''

    if contact_info:
        contact_links = contact_info.find_all('a', {'class': 'link link-with-icon-left'})
        for link in contact_links:
            href = link.get('href', '')
            text = link.find('span').text.strip() if link.find('span') else ''
            if 'kontaktinfo-mobile-phone-click' in link.get('data-gtm-event', '') or href.startswith('tel:'):
                data['phone'] = text
            elif 'kontaktinfo-mail-click' in link.get('data-gtm-event', '') or href.startswith('mailto:'):
                data['email'] = text
            elif 'kontaktinfo-web-click' in link.get('data-gtm-event', '') or href.startswith('http'):
                data['web'] = text
    return data

# Extract data from the first page
for row in rows:
    data = extract_data(row)
    all_data.append(data)

# Iterate through the remaining pages
for page in range(2, total_pages + 1):
    print(f"Processing page: {page}")
    # Construct the page URL
    page_url = base_url + str(page)

    # Send a GET request to the URL
    response = requests.get(page_url, headers=headers)

    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all articles that contain the needed information
    rows = soup.find_all("article", {"class": "search-result-article"})

    # Extract information from each article
    for row in rows:
        data = extract_data(row)
        all_data.append(data)

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(all_data)

# Save the DataFrame to an Excel file
df.to_excel("wko_at.xlsx", index=False)

# Print the first 5 rows of the DataFrame
print(df.head())
