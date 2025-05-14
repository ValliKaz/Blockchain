# Crypto Assistant API

A powerful cryptocurrency information service that combines real-time crypto data with AI-powered natural language processing. Ask questions about cryptocurrencies in natural language and get intelligent responses backed by real-time data.

## Features

- 🤖 AI-powered responses using TinyLlama
- 💰 Real-time cryptocurrency data
- 📊 Market cap and price information
- 📰 Latest crypto news and updates
- 🔍 Support for top 50 cryptocurrencies
- 🚀 Fast and responsive API

## Tech Stack

- **Backend Framework**: FastAPI
- **LLM**: TinyLlama (1.1B parameters, quantized)
- **Data Source**: CoinGecko API
- **Language**: Python 3.x
- **Dependencies**:
  - fastapi
  - uvicorn
  - llama-cpp-python
  - requests
  - pydantic

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/ValliKaz/Blockchain.git
   cd crypto-assistant-api
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Unix/MacOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn llama-cpp-python requests
   ```

4. **Download the LLM model**
   - Download TinyLlama model (Q4_K_M quantized version)
   - Create a `models` directory
   - Place the model file in the `models` directory as `tinyllama-1.1b-chat-v1.0-q4_k_m.gguf`

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API**
   - API Documentation: http://127.0.0.1:8000/docs
   - Health Check: http://127.0.0.1:8000/health

## API Usage

### Query Endpoint
```bash
curl -X POST "http://127.0.0.1:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"text": "What is the current price of Bitcoin?"}'
```

### Example Questions
- "What's the current price of Bitcoin?"
- "Tell me about Ethereum's market cap"
- "What's the latest news about Solana?"
- "How is Dogecoin performing today?"

## Project Structure

```
crypto-assistant-api/
├── main.py              # Main application file
├── llm_service.py       # LLM integration service
├── models/             # Directory for LLM model
│   └── tinyllama-1.1b-chat-v1.0-q4_k_m.gguf
├── requirements.txt    # Project dependencies
└── README.md          # This file
```

## Key Functions

- `resolve_coin_id()`: Converts cryptocurrency symbols/names to IDs
- `get_top_50_ids()`: Fetches top 50 cryptocurrencies
- `get_coin_price()`: Gets current price data
- `get_coin_info()`: Retrieves detailed coin information
- `get_coin_news()`: Fetches latest news and updates

## Error Handling

The API includes robust error handling for:
- Missing or invalid cryptocurrency queries
- API rate limits
- Network issues
- Invalid data formats

## Acknowledgments

- [TinyLlama](https://github.com/TinyLlama/TinyLlama) for the LLM model
- [CoinGecko](https://www.coingecko.com/) for cryptocurrency data
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework 