import json
import uuid
import sqlite3
import numpy as np
from scipy.spatial.distance import cosine
from engine import get_env_vars, create_openai_client, start_agentops_session, end_agentops_session, get_openai_completion
from data_handler import load_data
def store_workflow_responses(workflow_responses, db_file='workflow_responses.db'):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        # Create the table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS workflow_responses
                     (id TEXT PRIMARY KEY, prompt TEXT, response TEXT)''')

        # Insert the workflow responses into the database
        for response in workflow_responses:
            c.execute("INSERT INTO workflow_responses (id, prompt, response) VALUES (?, ?, ?)",
                     (response['step_id'], response['prompt'], response['response']))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error in store_workflow_responses: {e}")
        raise

def execute_workflow(workflow, additional_data=None, compact_sequentially=True, max_steps=None):
    try:
        # Get the environment variables
        agentops_key, mindsdb_key = get_env_vars()
        
        # Create the OpenAI client
        openai_client = create_openai_client(mindsdb_key)
        
        # Start the AgentOps session
        start_agentops_session(agentops_key)
        
        # Initialize the list to store the workflow responses
        workflow_responses = []
        
        # Iterate through the workflow steps
        for i, step in enumerate(workflow):
            # Generate a unique step ID
            step_id = str(uuid.uuid4())
            step["id"] = step_id
            
            # Get the prompt for the current step
            prompt = step["prompt"]
            
            # Replace the placeholders with the actual data
            prompt = prompt.format(
                company_name=additional_data["company_name"],
                services=", ".join(additional_data["services"])
            )
            
            # Iterate over the services and create a new prompt for each service
            for service in additional_data["services"]:
                service_prompt = prompt.format(service=service, service_coverage=additional_data["service_coverage"][service])
                
                # If compact_sequentially is True, append the previous responses to the prompt
                if compact_sequentially and workflow_responses:
                    service_prompt = f"Previous responses: {' | '.join([str(r) for r in workflow_responses])}\nCurrent prompt: {service_prompt}"
                
                # Get the completion from OpenAI
                completion = get_openai_completion(openai_client, service_prompt)
                
                # Create a response dictionary and append it to the workflow_responses list
                response = {
                    "step_id": step_id,
                    "prompt": service_prompt,
                    "response": completion.choices[0].message.content
                }
                workflow_responses.append(response)
            
            # Check if we've reached the maximum number of steps
            if max_steps is not None and len(workflow_responses) >= max_steps:
                break
        
        # Store the workflow responses in the SQLite database
        store_workflow_responses(workflow_responses)
        
        # End the AgentOps session
        end_agentops_session(agentops_key, 'Success')
        
        return workflow_responses
    
    except Exception as e:
        # Handle any exceptions that occur during the workflow execution
        print(f"Error in execute_workflow: {e}")
        raise

def execute_self_conversation(prompt, max_tokens=1024, num_responses=1, temperature=0.7, max_conversations=None):
    try:
        # Get the environment variables
        agentops_key, mindsdb_key = get_env_vars()
        
        # Create the OpenAI client
        openai_client = create_openai_client(mindsdb_key)
        
        # Start the AgentOps session
        start_agentops_session(agentops_key)
        
        # Initialize the list to store the conversation responses
        conversation_responses = []
        
        # Execute the self-conversation
        for i in range(max_conversations or 1):
            # Get the completion from OpenAI
            completion = get_openai_completion(openai_client, prompt, max_tokens=max_tokens, num_responses=num_responses, temperature=temperature)
            
            # Create a response dictionary and append it to the conversation_responses list
            response = {
                "conversation_id": str(uuid.uuid4()),
                "prompt": prompt,
                "response": completion.choices[0].message.content
            }
            conversation_responses.append(response)
            
            # Update the prompt with the previous response
            prompt = response["response"]
        
        # End the AgentOps session
        end_agentops_session(agentops_key, 'Success')
        
        return conversation_responses
    
    except Exception as e:
        # Handle any exceptions that occur during the self-conversation
        print(f"Error in execute_self_conversation: {e}")
        raise

def execute_user_conversation(user_prompt, max_tokens=1024, temperature=0.7, max_conversations=None):
    try:
        # Get the environment variables
        agentops_key, mindsdb_key = get_env_vars()
        
        # Create the OpenAI client
        openai_client = create_openai_client(mindsdb_key)
        
        # Start the AgentOps session
        start_agentops_session(agentops_key)
        
        # Initialize the list to store the conversation responses
        conversation_responses = []
        
        # Execute the user conversation
        for i in range(max_conversations or 1):
            # Get the completion from OpenAI
            completion = get_openai_completion(openai_client, user_prompt, max_tokens=max_tokens, temperature=temperature)
            
            # Create a response dictionary and append it to the conversation_responses list
            response = {
                "conversation_id": str(uuid.uuid4()),
                "prompt": user_prompt,
                "response": completion.choices[0].message.content
            }
            conversation_responses.append(response)
            
            # Update the user prompt with the model's response
            user_prompt = response["response"]
        
        # End the AgentOps session
        end_agentops_session(agentops_key, 'Success')
        
        return conversation_responses
    
    except Exception as e:
        # Handle any exceptions that occur during the user conversation
        print(f"Error in execute_user_conversation: {e}")
        raise

def search_workflow_responses(query, db_file='workflow_responses.db', top_k=5):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        # Fetch all the workflow responses from the database
        c.execute("SELECT prompt, response FROM workflow_responses")
        responses = c.fetchall()

        # Convert the prompts and responses to numpy arrays
        prompts = np.array([np.array(prompt.split()) for prompt, _ in responses])
        responses_arr = np.array([np.array(response.split()) for _, response in responses])

        # Compute the cosine similarity between the query and the responses
        query_vec = np.array(query.split())
        similarities = [1 - cosine(query_vec, response_vec) for response_vec in responses_arr]

        # Sort the responses by similarity and return the top k
        sorted_indices = np.argsort(similarities)[::-1]
        top_responses = [responses[i] for i in sorted_indices[:top_k]]

        # Close the database connection
        conn.close()

        return top_responses
    except Exception as e:
        print(f"Error in search_workflow_responses: {e}")
        raise