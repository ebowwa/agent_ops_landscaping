import json
from workflow import execute_workflow

def main(workflow_file, compact_sequentially=True, one_shot=False):
    try:
        # Load the workflow from the JSON file
        with open(workflow_file, 'r') as f:
            workflow = json.load(f)
        
        # Execute the workflow
        workflow_responses = execute_workflow(workflow, compact_sequentially, one_shot)
        
        # Save all the workflow responses to a JSON file
        with open("workflow_responses.json", "w") as f:
            json.dump(workflow_responses, f, indent=2)
    
    except Exception as e:
        # Handle any exceptions that occur in the main function
        print(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    # Execute the workflow with sequential compaction and default response
    main("workflow.json", compact_sequentially=True, one_shot=False)