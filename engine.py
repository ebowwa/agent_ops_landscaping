import os
from dotenv import load_dotenv
from openai import OpenAI
from agentops import ToolEvent, ErrorEvent, record, init, start_session, end_session

def get_env_vars():
    load_dotenv()
    return os.getenv('AGENTOPS_API_KEY'), os.getenv('MINDSDB_API_KEY')

def create_openai_client(mindsdb_api_key):
    return OpenAI(api_key=mindsdb_api_key, base_url="https://llm.mdb.ai")

def start_agentops_session(agentops_api_key):
    init(agentops_api_key)
    start_session()

def end_agentops_session(agentops_api_key, status):
    end_session(status)

def get_openai_completion(openai_client, prompt):
    tool_event = ToolEvent(name='OpenAI Completion', params={'prompt': prompt})
    try:
        completion = openai_client.chat.completions.create(model="claude-3-haiku", messages=[{"role": "user", "content": prompt}])
        tool_event.returns = completion.choices[0].message.content
    except Exception as e:
        record(ErrorEvent(message=e, trigger_event=tool_event))
        raise e
    record(tool_event)
    return completion

def main(prompt, status='Success'):
    agentops_key, mindsdb_key = get_env_vars()
    openai_client = create_openai_client(mindsdb_key)

    start_agentops_session(agentops_key)
    try:
        completion = get_openai_completion(openai_client, prompt)
        print(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")
    end_agentops_session(agentops_key, status)

# if __name__ == "__main__":
#     main("Hello world")