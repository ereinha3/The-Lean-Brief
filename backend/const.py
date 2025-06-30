import os
import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logging.error("OPENAI_API_KEY environment variable not set. Please set it in .env file.")
    exit("OPENAI_API_KEY is not set.")

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
if not NEWSAPI_KEY:
    logging.error("NEWSAPI_KEY environment variable not set. Please set it in .env file.")
    exit("NEWSAPI_KEY is not set.")

GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")
if not GUARDIAN_API_KEY:
    logging.error("GUARDIAN_API_KEY environment variable not set. Please set it in .env file.")
    exit("GUARDIAN_API_KEY is not set.")

WEBZ_API_KEY = os.getenv("WEBZ_API_KEY")
if not WEBZ_API_KEY:
    logging.error("WEBZ_API_KEY environment variable not set. Please set it in .env file.")
    exit("WEBZ_API_KEY is not set.")

NEWSAPI_BASE_URL = "https://newsapi.org/v2/everything"
GUARDIAN_BASE_URL = "https://content.guardianapis.com/search"
WEBZ_BASE_URL = "https://api.webz.io/newsApiLite"

MARKET_SECTORS = [
    "Technology & Software",
    "Finance & Economy",
    "Healthcare & Biotech",
    "Energy & Materials",
    "Defense & Warfare",
    "Geopolitics & Trade",
    "Cryptocurrency & Blockchain",
    "Artificial Intelligence & Robotics",
    "Retail & Consumer Goods",
    "Automotive & Mobility",
    "Real Estate & Infrastructure",
    "Politics & Government"
]

MARKET_SEARCH_QUERY = (
    "(technology OR software OR AI OR robotics OR "
    "finance OR economy OR market OR business OR trade OR "
    "health OR healthcare OR biotech OR "
    "energy OR materials OR oil OR gas OR renewables OR "
    "defense OR geopolitics OR military OR conflict OR international relations OR "
    "crypto OR cryptocurrency OR blockchain OR bitcoin OR ethereum OR defi OR "
    "retail OR consumer goods OR e-commerce OR shopping OR "
    "automotive OR auto OR vehicles OR electric vehicles OR EV OR mobility OR "
    "real estate OR property OR housing OR infrastructure OR construction OR rare OR precious OR metals)"
)

PUBLISHED_FROM_TIMESTAMP = int((datetime.now() - timedelta(days=1)).replace(hour=7, minute=0, second=0, microsecond=0).timestamp())
PUBLISHED_FROM_DATE = (datetime.now() - timedelta(days=1)).replace(hour=7, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d")