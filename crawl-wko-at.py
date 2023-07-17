# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# The URL to scrape data from
url = "https://firmen.wko.at/-/wien/?branche=25376&branchenname=immobilienmakler&page="

# List to store all data
all_data = []

# Iterate through the first 100 pages of the website
for page in range(1, 101):
    print(f"Processing page: {page}")
    # Append the page number to the URL
    new_url = url + str(page)

    # Send a GET request to the URL
    response = requests.get(new_url)

    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.content)

    # Find all rows in the HTML that contain the needed information
    rows = soup.find_all("div", {"class": "row", "class": "vcard"})

    # Extract information from each row
    for row in rows:
        # Dictionary to store the data for this row
        data = {}

        # Information to extract and where to find it
        elements_to_extract = [
            {"title": "name", "el": "h3", "class": ""},
            {"title": "street", "el": "div", "class": "street"},
            {"title": "zip", "el": "span", "class": "zip"},
            {"title": "city", "el": "span", "class": "locality"},
            {"title": "phone", "el": "div", "class": "icon-phone"},
            {"title": "fax", "el": "div", "class": "icon-fax"},
            {"title": "email", "el": "div", "class": "icon-email"},
            {"title": "web", "el": "div", "class": "icon-web"},
            {"title": "phone", "el": "div", "class": "icon-mobile"},
        ]

        # Try to extract each element
        for el in elements_to_extract:
            try:
                # Extract the text from the HTML element and strip leading/trailing whitespace
                data[el["title"]] = row.find(
                    el["el"], {"class": el["class"]}).text.strip()

                # If there's a newline in the text, only keep the part after it
                if "\n" in data[el["title"]]:
                    data[el["title"]] = data[el["title"]].split("\n")[1]
            except:
                pass  # If an error occurs, ignore it and move on to the next element

        # Add the data for this row to the main data list
        all_data.append(data)

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(all_data)

# Save the DataFrame to an Excel file
df.to_excel("wko_at.xlsx")