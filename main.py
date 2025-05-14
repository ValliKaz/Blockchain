from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, List
import requests
from llm_service import LLMService

app = FastAPI(title="Crypto Assistant")

# Путь к вашей модели (скачайте заранее TinyLlama или другую совместимую GGUF модель)
LLM_MODEL_PATH = "./models/tinyllama-1.1b-chat-v1.0-q4_k_m.gguf"
llm_service = LLMService(model_path=LLM_MODEL_PATH)

# Словарь популярных символов монет
SYMBOL_TO_ID = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "bnb": "binancecoin",
    "sol": "solana",
    "ada": "cardano",
    "dot": "polkadot",
    "xrp": "ripple",
    "doge": "dogecoin",
    "link": "chainlink",
    "ltc": "litecoin",
    # ... можно добавить больше
}

def get_top_50_ids() -> List[str]:
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=1"
        resp = requests.get(url)
        if resp.status_code != 200:
            print(f"Error fetching top 50: API returned status code {resp.status_code}")
            return []
        data = resp.json()
        if not isinstance(data, list):
            print(f"Error fetching top 50: Unexpected response format")
            return []
        return [coin["id"] for coin in data if isinstance(coin, dict) and "id" in coin]
    except Exception as e:
        print(f"Error fetching top 50: {e}")
        return []

def resolve_coin_id(query: str) -> Optional[str]:
    q = query.strip().lower()
    # Если пользователь ввёл символ
    if q in SYMBOL_TO_ID:
        return SYMBOL_TO_ID[q]
    # Если пользователь ввёл id
    top_50 = get_top_50_ids()
    if q in top_50:
        return q
    # Поиск по CoinGecko search API
    try:
        resp = requests.get(f"https://api.coingecko.com/api/v3/search?query={q}")
        data = resp.json()
        for coin in data.get("coins", []):
            if coin["id"] in top_50:
                return coin["id"]
        # Если не нашли в топ-50, вернуть первый найденный id
        if data.get("coins"):
            return data["coins"][0]["id"]
    except Exception as e:
        print(f"Error in resolve_coin_id: {e}")
    return None

class Query(BaseModel):
    text: str
    model_config = ConfigDict(from_attributes=True)

class Response(BaseModel):
    answer: str
    data: Optional[dict] = None
    model_config = ConfigDict(from_attributes=True)

def get_coin_price(coin_id: str) -> Optional[float]:
    try:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd")
        data = response.json()
        return data.get(coin_id, {}).get("usd")
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

def get_coin_info(coin_id: str) -> Optional[Dict]:
    try:
        response = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin_id}")
        if response.status_code != 200:
            print(f"Error fetching coin info: API returned status code {response.status_code}")
            return None
        data = response.json()
        if not isinstance(data, dict):
            print(f"Error fetching coin info: Unexpected response format")
            return None
        return {
            "name": data.get("name", "Unknown"),
            "symbol": data.get("symbol", "Unknown"),
            "market_cap": data.get("market_data", {}).get("market_cap", {}).get("usd", 0),
            "market_cap_rank": data.get("market_cap_rank", 0)
        }
    except Exception as e:
        print(f"Error fetching coin info: {e}")
        return None

def get_coin_news(coin_id: str, limit: int = 3) -> List[Dict]:
    try:
        response = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin_id}/status_updates")
        if response.status_code != 200:
            print(f"Error fetching news: API returned status code {response.status_code}")
            return []
        data = response.json()
        if not isinstance(data, dict) or "status_updates" not in data:
            print(f"Error fetching news: Unexpected response format")
            return []
        return [
            {
                "title": item.get("description", "No title available"),
                "published_at": item.get("created_at", "Unknown date")
            }
            for item in data.get("status_updates", [])[:limit]
            if isinstance(item, dict)
        ]
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

@app.post("/query", response_model=Response)
async def process_query(query: Query):
    try:
        coin_id = resolve_coin_id(query.text)
        if not coin_id:
            raise HTTPException(status_code=404, detail="Coin not found or not in top 50 by market cap.")
        
        # Проверяем топ-50
        top_50 = get_top_50_ids()
        in_top_50 = coin_id in top_50
        
        # Получаем данные
        price = get_coin_price(coin_id)
        info = get_coin_info(coin_id)
        news = get_coin_news(coin_id)
        
        data = {
            "price": price,
            "info": info,
            "news": news,
            "in_top_50": in_top_50
        }
        
        # Формируем промпт для LLM
        prompt = f"""You are a helpful crypto assistant.\nUser question: {query.text}\nFacts:\n- Price: {price if price else 'N/A'}\n- Market cap: {info['market_cap'] if info else 'N/A'}\n- Rank: {info['market_cap_rank'] if info else 'N/A'}\n- News: {', '.join([n['title'] for n in news]) if news else 'No recent news.'}\nGive a concise, informative answer for a non-expert user."""
        answer = llm_service.generate(prompt)
        return Response(answer=answer, data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 