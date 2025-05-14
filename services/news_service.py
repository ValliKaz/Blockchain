import requests
from typing import Dict, List, Optional
from config import get_settings

class NewsService:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = "https://api.coingecko.com/api/v3"
    
    def get_news(self, coin: str, limit: int = 5) -> List[Dict]:
        """
        Get latest news for a specific cryptocurrency
        """
        try:
            # Get status updates from CoinGecko
            response = requests.get(f"{self.base_url}/coins/{coin.lower()}/status_updates")
            response.raise_for_status()
            
            data = response.json()
            news_items = []
            
            for item in data.get("status_updates", [])[:limit]:
                news_items.append({
                    "title": item["description"],
                    "url": item.get("url", ""),
                    "published_at": item["created_at"],
                    "source": "CoinGecko",
                    "source_url": "https://www.coingecko.com"
                })
            
            return news_items
        except Exception as e:
            print(f"Error fetching news from CoinGecko: {e}")
            return []
    
    def get_trending_news(self, limit: int = 5) -> List[Dict]:
        """
        Get trending news across all cryptocurrencies
        """
        try:
            # Get trending coins from CoinGecko
            response = requests.get(f"{self.base_url}/search/trending")
            response.raise_for_status()
            
            data = response.json()
            news_items = []
            
            for item in data.get("coins", [])[:limit]:
                coin_data = item["item"]
                news_items.append({
                    "title": f"Trending: {coin_data['name']} ({coin_data['symbol'].upper()})",
                    "url": f"https://www.coingecko.com/en/coins/{coin_data['id']}",
                    "published_at": "current",
                    "source": "CoinGecko",
                    "source_url": "https://www.coingecko.com",
                    "currencies": [coin_data["symbol"].upper()]
                })
            
            return news_items
        except Exception as e:
            print(f"Error fetching trending news from CoinGecko: {e}")
            return [] 