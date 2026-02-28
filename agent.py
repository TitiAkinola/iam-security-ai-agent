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

# 3. Local Tool Import (Assumes iam_tools.py is in the same directory)
from iam_tools import ai_audit_tool

# Initialize the Rich Console
console = Console()

def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")

# --- GCP Configuration ---
SYSTEM_INSTRUCTION = """
You are a Senior Google Cloud SRE and IAM Security Architect. 
Your goal is to audit GCP IAM policy bindings using the 'ai_audit_tool'.
Specifically, identify 'Basic Roles' (roles/owner, roles/editor, roles/viewer) 
assigned to Service Accounts or external identities.
Explain the risks using GCP terminology and suggest moving to 'Predefined Roles' 
to follow the Principle of Least Privilege.
"""

# Setup API Key and Client
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    console.print("[bold red]ERROR:[/] GEMINI_API_KEY environment variable not found.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

# 4. Initialize the AI Agent Session with Gemini 3 Flash
chat = client.chats.create(
    model='models/gemini-3-flash-preview',
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

# 5. Execution Logic (The GCP SRE Workflow)
def run_audit():
    try:
        console.print(f"[{get_timestamp()}] [bold cyan][INFO][/] Starting GCP IAM Security Agent...")
        
        with console.status("[bold green]Agent is analyzing GCP policy bindings...", spinner="dots"):
            # Step 1: Trigger the audit tool for a GCP export file
            response = chat.send_message("Please audit the GCP IAM policy bindings in 'policy_sample.json'.")

            # --- Agentic Execution Loop ---
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    console.print(f"[{get_timestamp()}] [bold yellow][TOOL][/] AI triggered: {part.function_call.name}")
                    
                    # Step 2: Run the local Python tool
                    audit_result = ai_audit_tool(**part.function_call.args)
                    
                    # Step 3: Feed output back to Gemini 3 Flash for final reasoning
                    response = chat.send_message(
                        message=[
                            types.Part.from_function_response(
                                name=part.function_call.name,
                                response={'result': audit_result}
                            )
                        ]
                    )

        # --- Final Text Extraction & Cleaning ---
        final_analysis = ""
        if response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.text:
                    final_analysis += part.text
        
        # SRE FAILSAFE: Ensure the UI box is never empty
        if not final_analysis.strip():
            console.print(f"[{get_timestamp()}] [bold yellow][INFO][/] Synthesizing final report...")
            response = chat.send_message("Based on the tool results, provide your final GCP security report now.")
            final_analysis = response.text if response.text else "Audit complete. Review 'policy_sample.json' for roles/owner risks."

        # --- Final Polished Output ---
        console.print(f"[{get_timestamp()}] [bold green][COMPLETE][/] Audit finished.")
        console.rule("[bold white]Senior Google Cloud SRE Analysis[/]")
        
        console.print(Panel(
            str(final_analysis), 
            expand=False, 
            border_style="cyan", 
            title="GCP Security Report", 
            subtitle="GCP IAM AI Agent v1.2 | Gemini 3 Flash"
        ))

    except Exception as e:
        # Recursive Retry Logic for 429 Quota Limits
        if "429" in str(e):
            console.print(f"[{get_timestamp()}] [bold orange3][QUOTA][/] Rate limit hit. Cooling down for 62s...")
            time.sleep(62)
            run_audit() 
        else:
            console.print(f"[bold red]An unexpected error occurred:[/] {e}")

if __name__ == "__main__":
    run_audit()