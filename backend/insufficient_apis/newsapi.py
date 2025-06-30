import requests
import json
import logging
from const import *

def fetch_newsapi_articles(search_query, from_date, language='en', page_size=100):
    if NEWSAPI_KEY: # Only proceed if key exists
        params = {
            "q": search_query,
            "language": language,
            "pageSize": page_size,
            "from": from_date,
            "sortBy": "publishedAt",
            "apiKey": NEWSAPI_KEY
        }
        try:
            logging.info(f"Attempting to fetch from NewsAPI.org with params: {params}")
            response = requests.get(NEWSAPI_BASE_URL, params=params)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        
            response_data = response.json()
            results = response_data.get('articles', [])
            print(results[0])
            print(f"Successfully fetched {len(results)} articles from NewsAPI.org.")
        except requests.exceptions.RequestException as e:
            logging.error(f"HTTP Error fetching from NewsAPI.org: {e}")
            if e.response is not None:
                logging.error(f"NewsAPI.org Response Status: {e.response.status_code}")
                logging.error(f"NewsAPI.org Response Content: {e.response.text}")
        except json.JSONDecodeError as e:
            logging.error(f"JSON Decode Error from NewsAPI.org: {e}")
            logging.error(f"NewsAPI.org Raw Response Content that caused error: {response.text if 'response' in locals() else 'N/A'}")
        except Exception as e:
            logging.error(f"Unexpected error with NewsAPI.org fetch: {e}")

fetch_newsapi_articles("business OR market OR technology OR finance OR health OR defense OR crypto OR AI OR politics", "2025-06-28")