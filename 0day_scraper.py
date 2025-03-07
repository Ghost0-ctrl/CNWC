import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from transformers import pipeline
import csv
import subprocess  # Import subprocess to execute other scripts
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Insert your API keys below
SHODAN_API_KEY = os.getenv("<API_Key>")
VIRUSTOTAL_API_KEY = os.getenv("<API_Key>")

# Initialize the summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Scraping function for the Exploit Database
def scrape_exploit_db():
    url = 'https://www.exploit-db.com/exploits/'
    print("Scraping Exploit DB...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    exploits = []
    # Look for exploit entries in the updated HTML structure
    for row in soup.select('table#exploits > tbody > tr'):
        try:
            title = row.find('a', class_='exploit-title').text.strip()
            exploit_url = 'https://www.exploit-db.com' + row.find('a', class_='exploit-title')['href']
            description = row.find('td', class_='description').text.strip()
            date = row.find('td', class_='date').text.strip()

            exploits.append({
                'Title': title,
                'URL': exploit_url,
                'Description': description,
                'Date': date
            })
        except AttributeError:
            continue

    return exploits

# Function to get news articles on zero-day exploits
def fetch_zero_day_news():
    # Example API; replace with a real news API key
    news_url = 'https://newsapi.org/v2/everything?q=zero-day+exploit&apiKey=<API_Key>'
    response = requests.get(news_url)
    news_data = response.json()
    
    articles = []
    for article in news_data.get('articles', []):
        articles.append({
            'Title': article['title'],
            'Description': article['description'],
            'URL': article['url'],
            'Published At': article['publishedAt']
        })
    
    return articles

# Function to scrape Exploit DB (alternative)
def scrape_exploit_db_alternative():
    url = 'https://www.exploit-db.com/'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Failed to retrieve Exploit-DB page (status code: {response.status_code})")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    exploits = []
    
    for row in soup.select('table.exploits-table > tbody > tr'):
        try:
            title = row.find('a', class_='d-link').text.strip()
            exploit_url = 'https://www.exploit-db.com' + row.find('a', class_='d-link')['href']
            date = row.find('td', class_='date-display').text.strip()
            exploits.append({'Title': title, 'URL': exploit_url, 'Date': date})
        except AttributeError:
            continue

    return exploits

# Function to save data to CSV for the GUI
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f'Saved {len(data)} records to {filename}')

# Function to integrate with Shodan (example)
def fetch_shodan_data(query):
    url = f"https://api.shodan.io/shodan/host/search?key={SHODAN_API_KEY}&query={query}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

# Function to summarize exploits
def summarize_exploits(exploits):
    for exploit in exploits:
        try:
            # Summarize each exploit's description
            summary = summarizer(exploit['Description'], max_length=50, min_length=25, do_sample=False)
            exploit['Summary'] = summary[0]['summary_text']
        except Exception as e:
            print(f"Error summarizing exploit: {e}")
            exploit['Summary'] = 'Summary not available.'

def main():
    # Specify the path where the CSV will be saved
    csv_path = os.path.join(os.getcwd(), 'exploits.csv')

    # Scrape and gather data
    exploits = scrape_exploit_db()
    if not exploits:
        exploits = scrape_exploit_db_alternative()

    if exploits:
        print(f'Found {len(exploits)} exploits.')
        summarize_exploits(exploits)
        save_to_csv(exploits, csv_path)
        # Fetch additional data from APIs (Shodan, etc.)
        shodan_data = fetch_shodan_data(" exploit")
        if shodan_data:
            print("Shodan data fetched successfully.")
        else:
            print("Failed to fetch Shodan data.")
    else:
        print('No exploits found. Fetching latest zero-day news articles...')
        news_articles = fetch_zero_day_news()
        if news_articles:
            news_csv_path = os.path.join(os.getcwd(), 'zero_day_news.csv')
            save_to_csv(news_articles, news_csv_path)
        else:
            print('No news articles found.')

    # Execute the CSV reader GUI program
    try:
        subprocess.run(["python", "csv_reader_gui.py"], check=True)
    except Exception as e:
        print(f"Failed to run csv_reader_gui.py: {e}")
        

if __name__ == '__main__':
    main()
