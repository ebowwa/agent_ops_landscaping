# inference.py
from utils import get_clients
import logging

def inference(prompt):
    try:
        agentops_client, mindsdb_client = get_clients()

        completion = mindsdb_client.completion.create(
            model="claude-3-haiku",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7
        )
        additional_info = completion.choices[0].text

        report = {
            "additional_info": additional_info
        }

        return report

    except Exception as e:
        logging.error(f"Error occurred during inference: {e}")
        raise e