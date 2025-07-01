from flask import Flask, jsonify, request
from flask_cors import CORS
import openai
import numpy as np
import json
import logging
import asyncio
from apis.guardian import fetch_guardian_articles
from scraping.semianalysis import scrape_semianalysis_articles
import hashlib
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from const import *

# --- Initialize OpenAI Client ---
try:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    logging.error(f"Failed to initialize OpenAI client: {e}")
    # Fallback to basic initialization
    client = openai.OpenAI()
    client.api_key = OPENAI_API_KEY

app = Flask(__name__)
CORS(app)

async def classify_sector_and_topic(article_title, article_description, existing_topics_in_sector):
    """
    Classifies an article into a market sector, identifies its topic, and ranks its importance.
    It checks for similarity against existing topics to group them.
    """
    existing_topics_str = json.dumps(existing_topics_in_sector, indent=2) if existing_topics_in_sector else "None"

    prompt = f"""
    Given the following news article title and description, first classify it into ONE of these primary market sectors:
    {', '.join(MARKET_SECTORS)}
    You must fit the provided article in one of these sectors, fit as closely as possible. If it does not fit into any of these sectors
    or has no clear connection to any of these sectors, return "General".


    Then, identify the core topic of this article. The topic should turn the article title into a general, unbiased topic that encapsulates 
    the same idea.
    Consider these existing topics in the relevant sector (if any):
    {existing_topics_str}

    If this article's topic is *substantially similar* to an existing topic, use the exact "Topic Name" of that existing topic.
    If it is a *distinct new topic* or has *important distinctions* from existing topics, create a concise, descriptive "Topic Name" for it.
    Aim for granularity in topics: similar articles should group, but distinct narratives should be separate.

    Lastly, rank the importance of the topic from 1 to 10, 10 being the most important and 1 being the least important, within the sector.
    This should encompass how much this topic is likely to impact the sector or the overall market. This should be based on your observed
    history of topics / events and their impact on their sector.

    Title: {article_title}
    Description: {article_description}

    Provide your response in JSON format only:
    {{
        "sector": "Sector Name",
        "topic_name": "New or Existing Topic Name",
        "topic_importance": "1-10"
    }}
    """
    try:
        # OpenAI client methods are synchronous, not async
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that classifies news articles into market sectors, identifies topics, and ranks their importance. Your output must be a JSON object with 'sector', 'topic_name', and 'topic_importance' keys. Ensure 'topic_importance' is an integer between 1 and 10."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.1,
            response_format={ "type": "json_object" }
        )
        response_json = json.loads(response.choices[0].message.content.strip())
        
        sector_name = response_json.get("sector")
        topic_name = response_json.get("topic_name")
        topic_importance_raw = response_json.get("topic_importance")

        try:
            topic_importance = int(topic_importance_raw)
            if not 1 <= topic_importance <= 10:
                raise ValueError("Importance out of range")
        except (ValueError, TypeError):
            logging.warning(f"LLM returned invalid importance '{topic_importance_raw}' for '{topic_name}'. Defaulting to 5.")
            topic_importance = 5

        if sector_name not in MARKET_SECTORS:
            logging.warning(f"LLM returned unknown sector '{sector_name}'. Defaulting to 'General'. Article: {article_title}")
            sector_name = "General" 

        return sector_name, topic_name, topic_importance
    except Exception as e:
        logging.error(f"Error classifying sector and topic for '{article_title}': {e}")
        return "General", "Uncategorized News", 10

async def summarize_content(texts):
    """
    Summarizes a list of texts into a single coherent summary using OpenAI Chat API.
    summary_type: "short" (few sentences/paragraph) or "in-depth" (two paragraphs)
    """
    combined_text = "\n\n".join(texts)
    
    prompt_instruction = (
        "Synthesize the following news content into a comprehensive summary that preserves information but avoids redundancy and is concise. "
        "Identify the core topic, provide key details, and integrate information from all sources to avoid redundancy. "
        "Focus on being informative and concise without unnecessary fluff or quotes, unless the quote is integral to the topic. "
        "This summary should give a full picture of the specific topic."
    )
    max_tokens = 2000

    prompt = f"{prompt_instruction}\n\nContent:\n{combined_text}"

    try:
        # OpenAI client methods are synchronous, not async
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes news content concisely and accurately."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.4
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error summarizing content: {e}")
        return f"Summary could not be generated due to an error."


async def fetch_and_store_news():
    logging.info("Starting fetch_and_store_news...")
    # guardian_articles = await asyncio.to_thread(fetch_guardian_articles)
    semianalysis_articles = await asyncio.to_thread(scrape_semianalysis_articles)
    articles = semianalysis_articles
    
    hashed_articles = {}
    for article in articles:
        article_hash_input = f"{article.get('title')}{article.get('url')}{article.get('publishedAt')}"
        article_hash = hashlib.sha256(article_hash_input.encode('utf-8')).hexdigest()
        hashed_articles[article_hash] = article
    
    with open("hashed_articles.json", "w", encoding='utf-8') as f:
        json.dump(hashed_articles, f, indent=4, ensure_ascii=False)
    logging.info(f"Finished fetch_and_store_news. Stored {len(hashed_articles)} unique articles.")


async def sort_by_sector_and_topic():
    logging.info("Starting sort_by_sector_and_topic...")
    try:
        with open("hashed_articles.json", "r", encoding='utf-8') as f:
            hashed_articles = json.load(f)
    except FileNotFoundError:
        logging.error("hashed_articles.json not found. Run fetch_and_store_news first.")
        return

    logging.info(f"Processing {len(hashed_articles)} articles for classification and topic grouping...")
    
    sector_topic_map = {sector: {} for sector in MARKET_SECTORS}

    for article_hash, article_content in hashed_articles.items():
        article_title = article_content.get("title", "No Title")
        article_description = article_content.get("description", "No Description")
        
        existing_topics_llm_format = []
        # Correctly iterate over all existing topics identified so far
        for s_name, t_map in sector_topic_map.items():
            for t_name, t_info in t_map.items():
                existing_topics_llm_format.append({
                    "sector": s_name,
                    "topic_name": t_name,
                    "summary_preview": t_name 
                })

        try:
            sector, topic_name, topic_importance = await classify_sector_and_topic(
                article_title,
                article_description,
                existing_topics_llm_format
            )

            if sector not in MARKET_SECTORS:
                continue

            logging.info(f"Article '{article_title}' classified as '{sector}' with topic '{topic_name}' and importance '{topic_importance}'.")

            if sector not in sector_topic_map:
                sector_topic_map[sector] = {}

            if topic_name not in sector_topic_map[sector]:
                sector_topic_map[sector][topic_name] = {
                    "hashes": [],
                    "importance": [],
                    "description": ""
                }
            
            sector_topic_map[sector][topic_name]["hashes"].append(article_hash)
            sector_topic_map[sector][topic_name]["importance"].append(topic_importance)

        except Exception as e:
            logging.error(f"Error classifying or grouping article '{article_title}': {e}")
            continue 

    with open("sector_topic_map.json", "w", encoding='utf-8') as f:
        json.dump(sector_topic_map, f, indent=4, ensure_ascii=False)
    logging.info(f"Finished sort_by_sector_and_topic. Processed {len(hashed_articles)} articles.")


async def summarize_sector_topic_map():
    logging.info("Starting summarize_sector_topic_map...")
    try:
        with open("sector_topic_map.json", "r", encoding='utf-8') as f:
            sector_topic_map = json.load(f)
        with open("hashed_articles.json", "r", encoding='utf-8') as f:
            hashed_articles = json.load(f)
    except FileNotFoundError:
        logging.error("sector_topic_map.json or hashed_articles.json not found. Run previous steps first.")
        return

    final_content_output = {sector: {'landingSummary': '', 'topics': []} for sector in MARKET_SECTORS}

    for sector_name, topics_in_sector in sector_topic_map.items():
        if not topics_in_sector:
            continue


        sorted_topics_list = []
        for topic_name, topic_info in topics_in_sector.items():
            combined_texts_for_topic = []
            for article_hash in topic_info["hashes"]:
                article_data = hashed_articles.get(article_hash)
                if article_data:
                    combined_texts_for_topic.append(article_data.get('content'))
            
            if not combined_texts_for_topic:
                logging.warning(f"No valid content for topic '{topic_name}' in sector '{sector_name}'. Skipping.")
                continue

            last_article_hash = topic_info["hashes"][-1]
            last_article_content = hashed_articles[last_article_hash]

            in_depth_summary = await summarize_content(combined_texts_for_topic)
            
            avg_importance = np.mean(topic_info["importance"]) if topic_info["importance"] else 1

            sorted_topics_list.append({
                "name": topic_name,
                "description": last_article_content["description"],
                "summary": in_depth_summary,
                "sources": [hashed_articles[h]["source"] for h in topic_info["hashes"] if h in hashed_articles],
                "urls": [hashed_articles[h]["url"] for h in topic_info["hashes"] if h in hashed_articles],
                "importance": avg_importance
            })


        sorted_topics_list.sort(key=lambda x: x['importance'])
        final_content_output[sector_name]['topics'] = sorted_topics_list

        num_considered = min(3, len(sorted_topics_list))
        landing_summary = ''
        for topic in sorted_topics_list[:num_considered]:
            desc = topic['description']
            formatted_description = desc + '. ' if desc[-1] != '.' else desc + ' '
            landing_summary += formatted_description
        final_content_output[sector_name]['landingSummary'] = landing_summary

    with open("full_content.json", "w", encoding='utf-8') as f:
        json.dump(final_content_output, f, indent=4, ensure_ascii=False)
    logging.info("Finished summarize_sector_topic_map. full_content.json generated.")


async def run_full_processing_pipeline():
    logging.info("Starting full news processing pipeline...")
    await fetch_and_store_news()
    await sort_by_sector_and_topic()
    await summarize_sector_topic_map()
    logging.info("Full news processing pipeline completed successfully.")


@app.route('/api/summarize_news', methods=['GET'])
async def serve_summarized_news():
    try:
        with open("full_content.json", "r", encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        logging.error("full_content.json not found. Processing pipeline may not have run yet.")
        return jsonify({"error": "Data not ready. Please wait for processing to complete or trigger it manually."}), 503
    except Exception as e:
        logging.error(f"Error serving summarized news: {e}")
        return jsonify({"error": f"Failed to retrieve data: {str(e)}"}), 500

@app.route('/api/trigger_processing', methods=['POST'])
async def trigger_processing_endpoint():
    try:
        asyncio.create_task(run_full_processing_pipeline())
        return jsonify({"message": "News processing pipeline triggered. Data will be updated shortly."}), 202
    except Exception as e:
        logging.error(f"Error triggering processing pipeline: {e}")
        return jsonify({"error": f"Failed to trigger processing: {str(e)}"}), 500


@app.route('/')
def health_check():
    return "News Summarizer Backend is running!"

if __name__ == '__main__':
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    loop.run_until_complete(run_full_processing_pipeline()) 
    
    app.run(debug=True, port=5000, use_reloader=False)