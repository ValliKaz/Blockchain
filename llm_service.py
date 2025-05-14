from llama_cpp import Llama
import os

class LLMService:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.llm = None
        if os.path.exists(model_path):
            self.llm = Llama(model_path=model_path, n_ctx=2048, n_threads=4)
        else:
            print(f"Warning: Model file not found at {model_path}")

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        if self.llm is None:
            return "I apologize, but I'm currently unable to process your request as the AI model is not available. Please ensure the model file is properly installed."
        
        output = self.llm(
            prompt,
            max_tokens=max_tokens,
            stop=["</s>", "User:"],
            echo=False,
            temperature=0.7,
        )
        return output["choices"][0]["text"].strip() 