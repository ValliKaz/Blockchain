from pycoingecko import CoinGeckoAPI
from typing import Dict, Optional
from config import get_settings

class PriceService:
    def __init__(self):
        self.cg = CoinGeckoAPI()
        self.settings = get_settings()
    
    def get_price(self, symbol: str) -> Optional[Dict]:
        """
        Get current price for a cryptocurrency
        Args:
            symbol: Trading pair symbol (e.g., 'BTC')
        Returns:
            Dict containing price information
        """
        try:
            # Convert symbol to CoinGecko ID (lowercase)
            coin_id = symbol.lower()
            price_data = self.cg.get_price(ids=coin_id, vs_currencies='usd')
            
            if coin_id in price_data:
                return {
                    "symbol": symbol,
                    "price": price_data[coin_id]['usd'],
                    "source": "CoinGecko"
                }
            return None
        except Exception as e:
            print(f"Error fetching price from CoinGecko: {e}")
            return None
    
    def get_24h_stats(self, symbol: str) -> Optional[Dict]:
        """
        Get 24-hour statistics for a cryptocurrency
        """
        try:
            coin_id = symbol.lower()
            stats = self.cg.get_coin_by_id(id=coin_id)
            
            return {
                "symbol": symbol,
                "price_change": stats["market_data"]["price_change_24h"],
                "price_change_percent": stats["market_data"]["price_change_percentage_24h"],
                "volume": stats["market_data"]["total_volume"]["usd"],
                "source": "CoinGecko"
            }
        except Exception as e:
            print(f"Error fetching 24h stats from CoinGecko: {e}")
            return None 