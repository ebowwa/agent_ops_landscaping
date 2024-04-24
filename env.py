# env.py
from dotenv import load_dotenv
import os

load_dotenv()

AGENTOPS_API_KEY = os.environ['AGENTOPS_API_KEY']
MINDSDB_API_KEY = os.environ['MINDSDB_API_KEY']

# FOUND OPENAI API KEY 16fca6be-b5af-482c-97d7-398f786a4179