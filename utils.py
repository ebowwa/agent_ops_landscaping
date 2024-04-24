# utils.py
from agentops import init as agentops_init
from openai import OpenAI
from env import AGENTOPS_API_KEY, MINDSDB_API_KEY

def get_clients():
    agentops_client = agentops_init(AGENTOPS_API_KEY)
    mindsdb_client = OpenAI(
        api_key=MINDSDB_API_KEY,
        base_url="https://llm.mdb.ai"
    )
    return agentops_client, mindsdb_client