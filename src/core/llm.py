import os
from openai import OpenAI
from src.core.logging_config import get_logger

logger = get_logger(__name__)


class LLMService:
    def __init__(self):
        # Point to the AI Node's Ollama OpenAI-compatible endpoint
        self.ai_node_ip = os.getenv("AI_NODE_IP", "192.168.29.96")
        self.client = OpenAI(
            base_url=f"http://{self.ai_node_ip}:11434/v1",
            api_key="ollama",  # Ollama doesn't strictly check the key, but the SDK requires it
        )
        self.model = os.getenv("LLM_MODEL", "llama3.1:8b")

    def generate_response(self, system_prompt: str, user_query: str) -> str:
        logger.info(
            f"Sending RAG context to AI Node ({self.ai_node_ip}) for inference..."
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ],
            temperature=0.3,  # Keep it factual, professional, and grounded
        )
        return response.choices[0].message.content
