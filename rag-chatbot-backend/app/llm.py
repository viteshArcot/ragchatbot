import httpx
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class ResponseGenerator:
    """
    Handles the "generation" part of RAG - taking retrieved context and user questions
    and generating coherent responses using a language model.
    
    I chose OpenRouter over direct OpenAI API because:
    - Often better pricing for experimentation
    - Easy to switch between different models
    - More flexible rate limits
    
    The prompt engineering here is deliberately simple - just context + question.
    More sophisticated systems might use few-shot examples, chain-of-thought, etc.
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.api_base_url = "https://openrouter.ai/api/v1"
        
        # Using GPT-3.5-turbo as it's available on OpenRouter's free tier
        # Could easily switch to GPT-4, Claude, or other models
        self.model_name = "openai/gpt-3.5-turbo"
        
    async def generate_answer(self, user_question: str, retrieved_context: List[str]) -> str:
        """
        This is where the "augmented" part happens - give the LLM context before asking.
        
        The prompt structure matters more than I initially thought. Early versions
        just dumped the context and question together, which confused the model.
        Now I clearly separate context from question and explicitly tell it to
        stick to the provided info.
        
        Temperature 0.7 came from trial and error:
        - 0.1-0.3 felt robotic and repetitive
        - 0.8+ got too creative and started adding stuff not in the context
        - 0.7 gives natural language while usually staying grounded
        
        The "say so if you don't know" instruction is crucial. Without it,
        the model tries to be helpful and makes up confident-sounding answers
        when the context doesn't actually contain what's needed.
        
        Still happens sometimes though - I've seen it hallucinate specific
        numbers even when told to stick to the context. LLMs gonna LLM.
        """
        if not self.api_key:
            return "Error: OpenRouter API key not configured. Please add your API key to the .env file."
        
        # Combine the top retrieved chunks into context
        # I limit to 3 chunks to keep the prompt manageable and costs reasonable
        # Could make this configurable but 3 seems to work well for most questions
        context_text = "\n\n".join(retrieved_context[:3])
        
        # Construct the prompt with clear structure
        # The LLM performs better when the context and question are clearly separated
        prompt = (
            f"Context from documents:\n{context_text}\n\n"
            f"Question: {user_question}\n\n"
            f"Please answer the question based on the provided context. "
            f"If the context doesn't contain enough information to answer fully, "
            f"say so rather than making up information."
        )
        
        # Prepare the API request
        request_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        request_payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200,  # Reasonable length for most answers
            "temperature": 0.7,  # Balance between consistency and creativity
            "top_p": 0.9       # Focus on most likely tokens
        }
        
        try:
            # Make the API call with proper timeout and error handling
            async with httpx.AsyncClient() as http_client:
                api_response = await http_client.post(
                    f"{self.api_base_url}/chat/completions",
                    headers=request_headers,
                    json=request_payload,
                    timeout=30.0  # Reasonable timeout for API calls
                )
                api_response.raise_for_status()
                
                response_data = api_response.json()
                generated_text = response_data["choices"][0]["message"]["content"]
                
                return generated_text.strip()
                
        except httpx.HTTPStatusError as e:
            # Handle specific HTTP errors with helpful messages
            if e.response.status_code == 401:
                return "Error: Invalid API key. Please check your OpenRouter API key."
            elif e.response.status_code == 429:
                return "Error: Rate limit exceeded. Please try again in a moment."
            else:
                return f"Error: API request failed with status {e.response.status_code}"
                
        except httpx.TimeoutException:
            return "Error: Request timed out. The API might be experiencing high load."
            
        except Exception as e:
            # Catch-all for other errors
            return f"Error generating response: {str(e)}"

# Global response generator instance
# Using a singleton pattern to avoid recreating the client for each request
llm_client = ResponseGenerator()