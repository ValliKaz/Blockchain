from typing import Dict, List

class AIService:
    def __init__(self):
        pass
    
    def generate_response(self, query: str, data: Dict) -> str:
        """
        Generate a natural language response based on the query and gathered data
        """
        try:
            # Prepare the context from gathered data
            context = self._prepare_context(data)
            
            # Generate response based on available data
            response_parts = []
            
            # Add price information if available
            if "price" in data:
                response_parts.append(f"The current price of {data.get('coin_name', 'the cryptocurrency')} is ${data['price']:,.2f}.")
            
            # Add market data if available
            if "market_cap" in data:
                response_parts.append(f"Its market cap is ${data['market_cap']:,.2f}.")
            if "market_cap_rank" in data:
                response_parts.append(f"It is ranked #{data['market_cap_rank']} by market cap.")
            
            # Add news if available
            if "news" in data and data["news"]:
                response_parts.append("\nLatest updates:")
                for news in data["news"][:3]:  # Include top 3 news items
                    response_parts.append(f"- {news['title']}")
            
            return " ".join(response_parts)
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I apologize, but I'm having trouble generating a response at the moment. Please try again later."
    
    def _prepare_context(self, data: Dict) -> str:
        """
        Prepare the context string from gathered data
        """
        context_parts = []
        
        # Add price information
        if "price" in data:
            context_parts.append(f"Current price: ${data['price']:,.2f}")
        
        # Add market data
        if "market_cap" in data:
            context_parts.append(f"Market cap: ${data['market_cap']:,.2f}")
        if "market_cap_rank" in data:
            context_parts.append(f"Market cap rank: #{data['market_cap_rank']}")
        
        # Add news
        if "news" in data and data["news"]:
            context_parts.append("\nLatest news:")
            for news in data["news"][:3]:  # Include top 3 news items
                context_parts.append(f"- {news['title']}")
        
        return "\n".join(context_parts) 