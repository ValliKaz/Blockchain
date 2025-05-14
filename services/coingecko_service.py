from pycoingecko import CoinGeckoAPI
from typing import Dict, List, Optional
from config import get_settings

class CoinGeckoService:
    def __init__(self):
        self.cg = CoinGeckoAPI()
        self.settings = get_settings()
    
    def get_top_coins(self) -> List[Dict]:
        """
        Get top coins by market cap
        """
        try:
            coins = self.cg.get_coins_markets(
                vs_currency='usd',
                order='market_cap_desc',
                per_page=self.settings.TOP_COINS_LIMIT,
                page=1,
                sparkline=False
            )
            return coins
        except Exception as e:
            print(f"Error fetching top coins from CoinGecko: {e}")
            return []
    
    def get_coin_info(self, coin_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific coin
        """
        try:
            coin_data = self.cg.get_coin_by_id(
                id=coin_id,
                localization=False,
                tickers=False,
                market_data=True,
                community_data=False,
                developer_data=False
            )
            
            return {
                "id": coin_data["id"],
                "name": coin_data["name"],
                "symbol": coin_data["symbol"],
                "market_cap": coin_data["market_data"]["market_cap"]["usd"],
                "market_cap_rank": coin_data["market_cap_rank"],
                "current_price": coin_data["market_data"]["current_price"]["usd"],
                "price_change_24h": coin_data["market_data"]["price_change_percentage_24h"],
                "source": "CoinGecko"
            }
        except Exception as e:
            print(f"Error fetching coin info from CoinGecko: {e}")
            return None 