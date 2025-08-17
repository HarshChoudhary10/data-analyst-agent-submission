import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/List_of_highest-grossing_films'

try:
    response = requests.get(url)
    response.raise_for_status() 
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the first table, which is the main list of films
    table = soup.find('table', {'class': 'wikitable'})
    
    if table:
        # Use pandas to read the HTML table for simplicity
        df = pd.read_html(str(table))[0]
        
        summary = f"""Data Source URL: {url}
Table Columns: {df.columns.tolist()}

First 3 rows:
{df.head(3).to_string()}
"""
        
        with open('uploads/52bd1d13-7919-43c2-bcc0-fa1bcc8ee048/metadata.txt', 'w') as f:
            f.write(summary)
        print("Successfully scraped basic info and saved to metadata.txt")
    else:
        print("Could not find the main data table on the page.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching URL: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
