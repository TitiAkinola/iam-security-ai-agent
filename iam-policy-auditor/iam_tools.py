from iam_checker import audit_policy 
import io
import sys
from contextlib import redirect_stdout

def ai_audit_tool(file_path: str) -> str:
    """
    Scans an IAM policy file for security risks like '*' or Admin access.
    Use this when the user wants to audit, check, or scan a JSON policy.
    
    Args:
        file_path (str): The path to the JSON policy file.
    """
    # Create a string buffer to hold the text
    f = io.StringIO()
    
    try:
        # Redirect the 'print' statements from audit_policy into our buffer 'f'
        with redirect_stdout(f):
            audit_policy(file_path)
        
        # Get the captured text as a string
        output = f.getvalue()
        #print(f"DEBUG: Tool captured {len(output)} characters.")
        return output if output.strip() else "Audit completed, but no risks were detected."
    
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found. Please check the path."
    except Exception as e:
        return f"An error occurred during the tool execution: {str(e)}"