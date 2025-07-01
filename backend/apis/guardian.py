import requests
import json
import logging
from const import *
from bs4 import BeautifulSoup 
import re

def fetch_guardian_articles():

    if GUARDIAN_API_KEY: # Only proceed if key exists
        guardian_params = {
            "q": MARKET_SEARCH_QUERY,
            "api-key": GUARDIAN_API_KEY,
            "show-fields": "body,trailText", # Request full body HTML and a trailText snippet
            "page-size": 50,
            "from-date": PUBLISHED_FROM_DATE # Use YYYY-MM-DD for from-date
        }
        try:
            logging.info(f"Attempting to fetch from The Guardian with params: {guardian_params}")
            guardian_response = requests.get(GUARDIAN_BASE_URL, params=guardian_params)
            guardian_response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            guardian_data = guardian_response.json()
            results = guardian_data.get('response', {}).get('results', [])
            print(f"Successfully fetched {len(results)} articles from The Guardian.")
            
            formatted_results = []
            for result_item in results: # Renamed 'results' to 'result_item' to avoid conflict
                raw_html_content = result_item.get('fields', {}).get('body')
                clean_text_content = ""

                if raw_html_content:
                    # Use BeautifulSoup to parse the HTML and extract text
                    soup = BeautifulSoup(raw_html_content, 'html.parser')
                    # Find common tags that contain main article text, e.g., <p> tags
                    paragraphs = soup.find_all('p')
                    clean_text_content = "\n".join([p.get_text() for p in paragraphs])
                    
                    # Fallback or additional cleaning: if no paragraphs, try getting all text
                    if not clean_text_content.strip():
                        clean_text_content = soup.get_text(separator='\n', strip=True)
                
                # If still no content from body, fallback to trailText
                if not clean_text_content.strip():
                    clean_text_content = result_item.get('fields', {}).get('trailText', '')

                raw_html_description = result_item.get('fields', {}).get('trailText')

                if raw_html_description:
                    soup = BeautifulSoup(raw_html_description, 'html.parser')
                    text_without_html = soup.get_text()
                    clean_text_description = re.sub(r'^(Editorial|Guardian view):\s*', '', text_without_html, flags=re.IGNORECASE).strip()

                formatted_results.append({
                    "title": result_item.get('webTitle'),
                    "description": clean_text_description,
                    "content": clean_text_content, # Now this will be clean plain text
                    "source": "The Guardian",
                    "url": result_item.get('webUrl'),
                    "publishedAt": result_item.get('webPublicationDate')
                })
            
            # Print sample to verify clean content
            # if formatted_results:
            #     print(f"Sample Guardian article content (after cleaning):")
            #     print(formatted_results[0].get('content')[:500] + "...") # Print first 500 chars

            return formatted_results

        except requests.exceptions.RequestException as e:
            logging.error(f"HTTP Error fetching from The Guardian: {e}")
            if e.response is not None:
                logging.error(f"The Guardian Response Status: {e.response.status_code}")
                logging.error(f"The Guardian Response Content: {e.response.text}")
        except json.JSONDecodeError as e:
            logging.error(f"JSON Decode Error from The Guardian: {e}")
            logging.error(f"The Guardian Raw Response Content that caused error: {guardian_response.text if 'guardian_response' in locals() else 'N/A'}")
        except Exception as e:
            logging.error(f"Unexpected error with The Guardian fetch: {e}")
    return [] # Ensure an empty list is returned if API key is missing or an error occurs

# When testing this function directly:
if __name__ == '__main__':
    # Ensure your const.py has PUBLISHED_FROM_DATE and MARKET_SEARCH_QUERY
    # And your .env has GUARDIAN_API_KEY
    articles = fetch_guardian_articles()
    print(articles[0])
    print(articles[1])
    print(articles[2])
    if articles:
        print(f"\nSuccessfully retrieved and processed {len(articles)} articles from The Guardian.")
        # You can inspect articles[0].get('content') here for the full text.
    else:
        print("\nFailed to retrieve articles from The Guardian or no articles found.")