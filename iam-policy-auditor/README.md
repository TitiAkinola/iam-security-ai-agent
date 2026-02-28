![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![AI](https://img.shields.io/badge/Gemini-3--Flash--Preview-9b59b6.svg)


AI-Powered IAM Security Auditor
An automated Security Agent that bridges the gap between Gemini-3-flash-preview reasoning and local Python security tools to audit AWS IAM policies.

🚀 Key Features
Agentic Execution Loop: Utilizes a manual function-calling loop where the AI autonomously identifies the need for a security scan and triggers a local Python "bridge" (iam_tools.py).

Rate Limit Resilience: Implements recursive retry logic to handle 429 RESOURCE_EXHAUSTED errors gracefully, ensuring 100% completion even on free-tier API quotas.

Senior SRE Analysis: Beyond simple flag-based scanning, the agent provides a high-level summary of risks (like wildcard permissions) and suggests "Least Privilege" remediations.

Professional CLI UI: Built with the Rich library to provide real-time status spinners, timestamped audit trails, and formatted analysis panels.

Updated Technical Stack
Core Engine: Gemini 3 Flash (Preview).

Reasoning: Optimized for low-latency, high-frequency "Agentic Loops".

Tooling: Python 3.12, google-genai SDK, and the Rich terminal library.

⚡ Why Gemini 3 Flash?
For a Senior SRE tool, reliability and speed are non-negotiable. I chose Gemini 3 Flash because:

Reduced Latency: It provides the near-instant response times required for real-time terminal feedback and smooth status spinners.

Function Calling Efficiency: The model excels at identifying exactly when to trigger the ai_audit_tool without adding unnecessary conversational overhead.

Computational Scalability: It is designed for high-volume, repetitive tasks like scanning hundreds of IAM policies across a complex cloud environment.

📖 How It Works
Input: The user provides an IAM policy file (e.g., policy_sample.json).

Reasoning: The AI analyzes the request and decides to call the ai_audit_tool.

Execution: A local Python script executes a security audit on the file and captures the output.

Feedback: The raw audit data is fed back to the AI for final reasoning.

Output: A formatted "Senior SRE Analysis" is displayed in the terminal.

🏗️ Technical Challenges & Solutions
Developing an AI agent that interacts with local system files presented specific SRE challenges:

The 429 "Quota" Wall: Initial runs hit API rate limits. I implemented Recursive Retry Logic in agent.py that detects 429 errors and automatically triggers a "cool down" period before resuming the audit.

The "None" Rendering Bug: Extracting text from multi-part AI responses (which include function call data) often resulted in empty UI panels. I engineered a Text Extraction Filter to isolate specific text parts before rendering the final report.

Environment Isolation: To ensure project portability, I utilized a Python Virtual Environment (.venv) to isolate dependencies, preventing version conflicts with system-level packages.

🛡️ Remediation Example
Detected Risk: Action: "*" on Resource: "*" (Administrative Wildcard).

SRE Recommendation: Move to a scoped policy allowing only specific actions (e.g., s3:GetObject) on specific resources.
