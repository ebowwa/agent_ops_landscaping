import logging
import asyncio
from openai import OpenAI
import agentops
from dotenv import load_dotenv
import os
from typing import Any

# Load environment variables
load_dotenv()
AGENTOPS_API_KEY: str = os.environ['AGENTOPS_API_KEY']
MINDSDB_API_KEY: str = os.environ['MINDSDB_API_KEY']

# Set up logging
logging.basicConfig(level=logging.INFO)

# Main function
async def main() -> None:
    # Initialize AgentOps client
    agentops_client = agentops.init(AGENTOPS_API_KEY)

    # Create OpenAI client
    async with OpenAI(
        api_key=MINDSDB_API_KEY,
        base_url="https://llm.mdb.ai"
    ) as client:
        # Get completion from OpenAI
        await get_completion(client, agentops_client)

# Get completion from OpenAI
async def get_completion(client: OpenAI, agentops_client: Any) -> None:
    try:
        # Create completion
        response = await client.completions.create(
            model="gemini-1.5-pro",
            prompt="Hello, how are you today?",
            stream=False
        )

        # Log the completion
        logging.info(response.choices[0].text)
    except Exception as e:
        # Log the error
        logging.error(f"Error: {e}")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())