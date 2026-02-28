import os
from google import genai

# Initialize the client (uses your GEMINI_API_KEY environment variable)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

print(f"{'MODEL NAME':<40} | {'SUPPORTED METHODS'}")
print("-" * 70)

# Iterate through all models available to your specific API Key
for m in client.models.list():
    # Filter for models that support 'generateContent' (the method used for Chat/Agents)
    if "generateContent" in m.supported_actions:
        # We join the supported actions into a readable string
        methods = ", ".join(m.supported_actions)
        print(f"{m.name:<40} | {methods}")