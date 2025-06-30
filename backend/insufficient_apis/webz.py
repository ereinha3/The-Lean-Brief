import requests
import json
import logging
from const import * # Make sure const.py is in the same directory or accessible via PYTHONPATH

# --- Define a temporary search query for testing webz.py directly ---
# In app.py, this 'q' will come from the function parameter or a default.
# For direct testing of webz.py, we'll hardcode a broad query.
TEST_SEARCH_QUERY = "(business OR market OR technology OR finance OR health OR defense OR crypto OR AI OR politics)" # <--- ADD PARENTHESES

if WEBZ_API_KEY: # Only proceed if key exists
        webz_params = {
            "token": WEBZ_API_KEY,
            "q": TEST_SEARCH_QUERY, # <--- ADD A 'q' (query) parameter for search terms
            "ts": PUBLISHED_FROM_TIMESTAMP, # <--- CORRECT FORMAT for "since timestamp"
            "sort": "crawled", # Keep sort, as it's a valid parameter
            "size": 100 # Add a size parameter to get more results if needed for testing
        }
        try:
            logging.info(f"Attempting to fetch from Webz.io with params: {webz_params}")
            webz_response = requests.get(WEBZ_BASE_URL, params=webz_params)
            webz_response.raise_for_status()
            webz_data = webz_response.json()
            
            posts = webz_data.get('posts', [])
            
            if posts:
                print(f"Successfully fetched {len(posts)} articles from Webz.io. First article:")
                print(json.dumps(posts[0], indent=2)) # Pretty print the first article
            else:
                logging.info("Fetched 0 articles from Webz.io. Check query or date range.")

            logging.info(f"Successfully fetched {len(webz_data.get('posts', []))} articles from Webz.io.")
            
        except requests.exceptions.RequestException as e:
            logging.error(f"HTTP Error fetching from Webz.io: {e}")
            if e.response is not None:
                logging.error(f"Webz.io Response Status: {e.response.status_code}")
                logging.error(f"Webz.io Response Content: {e.response.text}")
        except json.JSONDecodeError as e:
            logging.error(f"JSON Decode Error from Webz.io: {e}")
            logging.error(f"Webz.io Raw Response Content that caused error: {webz_response.text if 'webz_response' in locals() else 'N/A'}")
        except Exception as e:
            logging.error(f"Unexpected error with Webz.io fetch: {e}")