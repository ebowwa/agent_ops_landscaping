import json
import pandas as pd
from workflow import execute_workflow, execute_self_conversation, execute_user_conversation, search_workflow_responses

def main(workflow_file, compact_sequentially=True, max_steps=None):
    try:
        # Load the workflow from the JSON file
        with open(workflow_file, 'r') as f:
            workflow = json.load(f)
        
        # Load the additional data
        additional_data = load_data()
        
        # Execute the workflow
        workflow_responses = execute_workflow(workflow, additional_data=additional_data, compact_sequentially=compact_sequentially, max_steps=max_steps)
        
        # Save all the workflow responses to a JSON file
        with open("workflow_responses.json", "w") as f:
            json.dump(workflow_responses, f, indent=2)
    
    except Exception as e:
        print(f"Error in main: {e}")
        raise

def self_conversation():
    try:
        initial_prompt = input("Enter the initial prompt for the self-conversation: ")
        max_conversations = int(input("Enter the maximum number of conversations: "))
        
        conversation_responses = execute_self_conversation(initial_prompt, max_conversations=max_conversations)
        
        pd.DataFrame(conversation_responses).to_json("self_conversation_responses.json", indent=2)
    
    except Exception as e:
        print(f"Error in self_conversation: {e}")
        raise

def user_conversation():
    try:
        initial_prompt = input("Enter the initial prompt for the user conversation: ")
        max_conversations = int(input("Enter the maximum number of conversations: "))
        
        conversation_responses = execute_user_conversation(initial_prompt, max_conversations=max_conversations)
        
        pd.DataFrame(conversation_responses).to_json("user_conversation_responses.json", indent=2)
    
    except Exception as e:
        print(f"Error in user_conversation: {e}")
        raise

def search_responses():
    try:
        query = input("Enter the search query: ")
        top_responses = search_workflow_responses(query)
        
        for prompt, response in top_responses:
            print(f"Prompt: {prompt}")
            print(f"Response: {response}")
            print()
    
    except Exception as e:
        print(f"Error in search_responses: {e}")
        raise

def load_data():
    # Load the additional data required for the workflow
    # This could be data from CSV files, databases, or other sources
    # The specific implementation will depend on your use case

    # Example implementation:
    output_data = pd.read_csv('output/output.csv')

    company_name = "Goldson Landscaping"
    company_services = output_data['Service'].unique().tolist()

    service_coverage = {}
    for service in company_services:
        service_coverage[service] = output_data.loc[output_data['Service'] == service, 'City & Neighborhoods'].str.split(': ', expand=True)[1].tolist()

    return {
        "company_name": company_name,
        "services": company_services,
        "service_coverage": service_coverage
    }

if __name__ == "__main__":
    main("input/sample_workflow.json", compact_sequentially=False, max_steps=5)