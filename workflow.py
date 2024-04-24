import json
import uuid
from engine import get_env_vars, create_openai_client, start_agentops_session, end_agentops_session, get_openai_completion

def execute_workflow(workflow, compact_sequentially=True, one_shot=False):
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
        for step in workflow:
            # Generate a unique step ID
            step_id = str(uuid.uuid4())
            step["id"] = step_id
            
            # Get the prompt for the current step
            prompt = step["prompt"]
            
            # If compact_sequentially is True, append the previous responses to the prompt
            if compact_sequentially and workflow_responses:
                prompt = f"Previous responses: {' | '.join([str(r) for r in workflow_responses])}\nCurrent prompt: {prompt}"
            
            # Get the completion from OpenAI
            if one_shot:
                completion = get_openai_completion(openai_client, prompt, max_tokens=1024)
            else:
                completion = get_openai_completion(openai_client, prompt)
            
            # Create a response dictionary and append it to the workflow_responses list
            response = {
                "step_id": step_id,
                "prompt": prompt,
                "response": completion.choices[0].message.content
            }
            workflow_responses.append(response)
        
        # End the AgentOps session
        end_agentops_session(agentops_key, 'Success')
        
        return workflow_responses
    
    except Exception as e:
        # Handle any exceptions that occur during the workflow execution
        print(f"Error in execute_workflow: {e}")
        raise