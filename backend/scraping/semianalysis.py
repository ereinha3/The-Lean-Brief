import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
import time
import re
import json
from const import * # Make sure const.py is in the same directory and defines PUBLISHED_FROM_TIMESTAMP

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_semianalysis_articles():
    """
    Scrapes recent articles from semianalysis.com's archives section.
    It stops when it encounters an article older than PUBLISHED_FROM_TIMESTAMP.

    Returns:
        list: A list of dictionaries, where each dictionary represents an article.
              Each article dict contains: 'title', 'description', 'content', 'url', 'publishedAt', 'source'.
    """
    base_url = "https://semianalysis.com"
    archives_url = f"{base_url}/archives/" # Corrected URL to archives channel

    articles_data = []

    # For testing: use 10-day lookback instead of PUBLISHED_FROM_TIMESTAMP from const.py
    test_timestamp = int((datetime.now() - timedelta(days=10)).timestamp())
    cutoff_timestamp_ms = test_timestamp * 1000
    
    logging.info(f"Starting scrape of {archives_url}. Collecting articles newer than timestamp: {test_timestamp}s (which is {datetime.fromtimestamp(test_timestamp).strftime('%Y-%m-%d %H:%M:%S')})")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9', # Good practice to include
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Connection': 'keep-alive'
        }
        response = requests.get(archives_url, headers=headers, timeout=20) # Increased timeout further
        response.raise_for_status()

        logging.info(response.text)
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the first ul element within the skip link target
        ul_element = soup.select_one('ul.archive-cards')
        if not ul_element:
            logging.error("Could not find ul element within archive-cards. Page structure may have changed.")
            return []

        # Get all li elements
        li_elements = ul_element.find_all('li')
        if not li_elements:
            logging.error("No li elements found in the ul. Page structure may have changed.")
            return []

        logging.info(f"Found {len(li_elements)} list items to process.")

        for li in li_elements:
            # Extract published timestamp from <time> tag with datetime attribute
            time_tag = li.find('time')
            
            published_datetime = None
            if time_tag and 'datetime' in time_tag.attrs:
                try:
                    # Parse datetime in format "2025-06-30T13:24:25+00:00"
                    datetime_str = time_tag['datetime']
                    published_datetime = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
                except ValueError:
                    logging.warning(f"Could not parse datetime for li element: {li.prettify()[:50]}... Skipping date check for this element.")
                    continue # Skip this element if datetime is bad

            if published_datetime is None:
                logging.warning(f"No valid datetime found for li element: {li.prettify()[:50]}... Skipping date check for this element.")
                continue # Skip if no valid datetime

            # Convert to timestamp for comparison
            published_timestamp = published_datetime.timestamp()
            
            # --- CRITICAL DATE CHECK AND STOP CONDITION ---
            # Stop if the article is OLDER than or equal to the cutoff
            if published_timestamp < test_timestamp:
                logging.info(f"Encountered old article (Published: {published_datetime.strftime('%Y-%m-%d %H:%M:%S')}). Stopping scrape of archive page.")
                break # Exit the loop, as articles are ordered newest to oldest

            # Extract the link from the figure with class "wp-block-post-featured-image"
            figure_element = li.find('figure', class_='wp-block-post-featured-image')
            if not figure_element:
                logging.warning(f"No figure with class 'wp-block-post-featured-image' found for li element: {li.prettify()[:50]}... Skipping.")
                continue # Skip if no valid figure in this li element

            link_element = figure_element.find('a')
            if not link_element or 'href' not in link_element.attrs:
                logging.warning(f"No valid link found in figure: {figure_element.prettify()[:50]}... Skipping.")
                continue # Skip if no valid link in this figure

            article_url = link_element['href']
            # If the URL is relative, make it absolute
            if not article_url.startswith('http'):
                article_url = base_url + article_url if article_url.startswith('/') else base_url + '/' + article_url
            
            # Try to extract title from the link or from other elements in the li
            article_title = link_element.get('title', '') or link_element.get_text(strip=True)
            if not article_title:
                # Fallback: look for title in other elements
                title_element = li.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                article_title = title_element.get_text(strip=True) if title_element else "No Title Found"
            
            logging.info(f"Processing recent article: {article_url} (Published: {published_datetime.strftime('%Y-%m-%d %H:%M:%S')})")
            
            # Fetch the individual article page
            try:
                article_response = requests.get(article_url, headers=headers, timeout=20) # Increased timeout
                article_response.raise_for_status()
                
                article_soup = BeautifulSoup(article_response.text, 'html.parser')

                title_meta = article_soup.find('meta', property='og:title')
                article_title = title_meta['content'].strip() if title_meta and 'content' in title_meta.attrs else "No Title Found"

                # Extract description/excerpt - often from meta property="og:description"
                description_meta = article_soup.select_one('h2.wp-block-semianalysis-sub-title')
                article_description = description_meta.get_text(strip=True).replace('/', '').strip() if description_meta else "No Description Found"

                # Extract full article content - Semianalysis uses <section class="gh-content gh-canvas">
                content_section = article_soup.find('main')

                full_content_text = ""
                if content_section:
                    paragraphs = content_section.find_all('p')
                    full_content_text = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                    
                    if not full_content_text.strip(): # Fallback for other content types
                        full_content_text = content_section.get_text(separator='\n', strip=True)
                
                # Final fallback if content extraction failed, use description
                if not full_content_text.strip() and article_description.strip():
                    logging.warning(f"No substantial content found for {article_url}. Using description as fallback for content.")
                    full_content_text = article_description 
                elif not full_content_text.strip():
                    logging.warning(f"No content or description found for {article_url}. Content will be empty.")
                
                articles_data.append({
                    "title": article_title,
                    "description": article_description,
                    "content": full_content_text,
                    "source": "Semianalysis",
                    "url": article_url,
                    "publishedAt": published_datetime.isoformat()
                })
                time.sleep(0.5) # Be polite: pause for 0.5 seconds between article fetches
            
            except requests.exceptions.RequestException as e:
                logging.error(f"Error fetching individual article {article_url}: {e}")
            except Exception as e:
                logging.error(f"Error processing article {article_url}: {e}")
            
        else: # This 'else' belongs to the for loop and executes if loop completes normally (no break)
            logging.info("End of archive page reached without encountering old articles.")


    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching archive page {archives_url}: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred during scraping: {e}")

    logging.info(f"Finished scraping. Found {len(articles_data)} recent articles from Semianalysis.")
    return articles_data

# Example of how to use this function (for testing directly)
if __name__ == '__main__':
    # Note: This script now uses a 10-day lookback for testing instead of PUBLISHED_FROM_TIMESTAMP from const.py
    # The test_timestamp is calculated as: int((datetime.now() - timedelta(days=10)).timestamp())

    recent_semianalysis_articles = scrape_semianalysis_articles()
    
    if recent_semianalysis_articles:
        print(f"\n--- Found {len(recent_semianalysis_articles)} Recent Semianalysis Articles ---")
        for i, article in enumerate(recent_semianalysis_articles):
            print(f"\nArticle {i+1}:")
            print(f"  Title: {article['title']}")
            print(f"  URL: {article['url']}")
            print(f"  Published: {article['publishedAt']}")
            print(f"  Description: {article['description']}")
            print(f"  Content Length: {len(article['content'])} characters")
            # print(f"  Content Snippet: {article['content'][:500]}...")
    else:
        print("\nNo recent articles found from Semianalysis.com or an error occurred during scraping.")