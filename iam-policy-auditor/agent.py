import os
import sys
import time
from datetime import datetime

# 1. Professional Terminal Imports
from rich.console import Console
from rich.panel import Panel

# 2. AI SDK Imports
from google import genai
from google.genai import types

# 3. Local Tool Import
from iam_tools import ai_audit_tool

# Initialize the Rich Console
console = Console()

def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")

# --- Configuration ---
SYSTEM_INSTRUCTION = """
You are a Senior SRE and Cloud Security Architect specializing in IAM. 
Your goal is to audit IAM policies using the 'ai_audit_tool'.
Explain risks clearly using bullet points and suggest 'Least Privilege' fixes.
"""

# Setup API Key and Client
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    console.print("[bold red]ERROR:[/] GEMINI_API_KEY environment variable not found.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

# 4. Initialize the AI Agent Session
chat = client.chats.create(
    model='gemini-3-flash-preview',
    config=types.GenerateContentConfig(
        tools=[ai_audit_tool],
        tool_config=types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(
                mode='ANY', 
                allowed_function_names=['ai_audit_tool']
            )
        ),
        system_instruction=SYSTEM_INSTRUCTION,
    )
)

# 5. Execution Logic (The SRE Workflow)
def run_audit():
    try:
        console.print(f"[{get_timestamp()}] [bold cyan][INFO][/] Starting SRE Security Agent...")
        
        with console.status("[bold green]Agent is analyzing policy...", spinner="dots"):
            # Step 1: Trigger the audit tool
            response = chat.send_message("Please audit the file 'policy_sample.json'.")

            # --- Agentic Execution Loop ---
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    console.print(f"[{get_timestamp()}] [bold yellow][TOOL][/] AI triggered: {part.function_call.name}")
                    
                    # Step 2: Run the local Python tool
                    audit_result = ai_audit_tool(**part.function_call.args)
                    
                    # Step 3: Feed output back to the model for final analysis
                    response = chat.send_message(
                        message=[
                            types.Part.from_function_response(
                                name=part.function_call.name,
                                response={'result': audit_result}
                            )
                        ]
                    )

        # --- Final Text Extraction Loop ---
        final_analysis = ""
        
        # Step 4: Extract only the text parts from the final response
        if response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.text:
                    final_analysis += part.text
        
        # SRE FAILSAFE: If the response is empty or metadata-only, force a summary
        if not final_analysis.strip():
            console.print(f"[{get_timestamp()}] [bold yellow][INFO][/] Summarizing findings...")
            response = chat.send_message("Based on the tool results, provide your final security report now.")
            # Final attempt to get a clean string
            final_analysis = response.text if response.text else "Analysis complete. Review 'policy_sample.json' for wildcard risks."

        # --- Final Polished Output ---
        console.print(f"[{get_timestamp()}] [bold green][COMPLETE][/] Audit finished.")
        console.rule("[bold white]Senior SRE Analysis[/]")
        
        # We wrap in str() to ensure the Rich Panel always receives valid text
        console.print(Panel(
            str(final_analysis), 
            expand=False, 
            border_style="cyan", 
            title="Security Report", 
            subtitle="IAM Security AI Agent v1.1"
        ))

    except Exception as e:
        if "429" in str(e):
            console.print(f"[{get_timestamp()}] [bold orange3][QUOTA][/] Rate limit hit. Cooling down for 62s...")
            time.sleep(62)
            run_audit() 
        else:
            console.print(f"[bold red]An unexpected error occurred:[/] {e}")

if __name__ == "__main__":
    run_audit()