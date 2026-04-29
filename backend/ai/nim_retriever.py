"""
NVIDIA NIM API Integration for NeuroQuest
"""
import requests
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class NIMClient:
    """Client for NVIDIA NIM API."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the NIM client.

        Args:
            api_key: NVIDIA NIM API key
            base_url: Base URL for NIM API
        """
        self.api_key = api_key or os.getenv("NIM_API_KEY")
        self.base_url = base_url or os.getenv("NIM_BASE_URL", "https://integrate.api.nvidia.com/v1")

        if not self.api_key:
            raise ValueError("NIM_API_KEY not found in environment variables")

        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })

    def chat_completion(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send a chat completion request to NIM.

        Args:
            model: Model name (e.g., 'meta/llama-3.1-405b-instruct')
            messages: List of message dictionaries
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters

        Returns:
            Response from the API
        """
        url = f"{self.base_url}/chat/completions"

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }

        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error calling NIM API: {e}")
            raise

    def text_completion(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send a text completion request to NIM.

        Args:
            model: Model name
            prompt: Text prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters

        Returns:
            Response from the API
        """
        messages = [{"role": "user", "content": prompt}]
        return self.chat_completion(model, messages, temperature, max_tokens, **kwargs)

    def get_available_models(self) -> List[str]:
        """
        Get list of available models.

        Returns:
            List of model names
        """
        # Common NIM models that support chat/completion
        return [
            'meta/llama-3.1-405b-instruct',
            'meta/llama-3.1-70b-instruct',
            'meta/llama-3.1-8b-instruct',
            'mistralai/mistral-large',
            'mistralai/mixtral-8x7b-instruct-v0.1',
            'google/gemma-7b',
            'ai21/jamba-1b-large',
        ]

    def synthesize_results(
        self,
        query: str,
        search_results: List[Dict[str, Any]],
        model: str = 'meta/llama-3.1-405b-instruct',
        max_length: int = 500
    ) -> str:
        """
        Synthesize search results into a coherent summary.

        Args:
            query: Original search query
            search_results: List of search results
            model: Model to use for synthesis
            max_length: Maximum length of the summary

        Returns:
            Synthesized summary
        """
        # Build context from search results (limit to avoid token limits)
        context_parts = []
        for i, result in enumerate(search_results[:3]):  # Limit to 3 papers
            abstract = result.get('abstract', '')
            # Truncate abstract to avoid token limits
            if len(abstract) > 200:
                abstract = abstract[:200] + "..."
            context_parts.append(
                f"Paper {i+1}: {result['title']}\n{abstract}"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""Summarize these papers about {query}:

{context}

Focus on key findings. Keep under {max_length} words."""

        try:
            response = self.text_completion(
                model=model,
                prompt=prompt,
                temperature=0.7,
                max_tokens=min(max_length * 2, 1000)  # Limit tokens
            )

            # Extract the generated text
            if 'choices' in response and len(response['choices']) > 0:
                return response['choices'][0]['message']['content']
            else:
                return "Unable to generate summary"

        except Exception as e:
            print(f"Error synthesizing results: {e}")
            return "Summary generation failed"

    def answer_question(
        self,
        question: str,
        context: str,
        model: str = 'meta/llama-3.1-405b-instruct'
    ) -> str:
        """
        Answer a question based on provided context.

        Args:
            question: Question to answer
            context: Context information
            model: Model to use

        Returns:
            Answer to the question
        """
        prompt = f"""Context: {context}

Question: {question}

Answer the question based on the provided context. Be specific and cite relevant information."""

        try:
            response = self.text_completion(
                model=model,
                prompt=prompt,
                temperature=0.3,
                max_tokens=500
            )

            if 'choices' in response and len(response['choices']) > 0:
                return response['choices'][0]['message']['content']
            else:
                return "Unable to generate answer"

        except Exception as e:
            print(f"Error answering question: {e}")
            return "Answer generation failed"


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = NIMClient()

    # Test basic completion
    print("Testing NIM API...")

    try:
        response = client.text_completion(
            model='meta/llama-3.1-8b-instruct',
            prompt="What is machine learning?",
            max_tokens=100
        )

        if 'choices' in response and len(response['choices']) > 0:
            print("Response:", response['choices'][0]['message']['content'])
        else:
            print("No response generated")

    except Exception as e:
        print(f"Error: {e}")
