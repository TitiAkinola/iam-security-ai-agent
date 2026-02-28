🛡️ GCP AI-Powered IAM Security Auditor
An automated Security Agent designed to bridge the gap between Gemini 3 Flash reasoning and local Python security tools to audit Google Cloud IAM policy bindings.

🚀 Key Features
Agentic Execution Loop: Utilizes a manual function-calling loop where the AI autonomously identifies the need for a security scan and triggers a local Python "bridge" (iam_tools.py) to parse GCP JSON exports.

Rate Limit Resilience: Implements recursive retry logic to handle 429 RESOURCE_EXHAUSTED errors gracefully, ensuring 100% completion even on free-tier API quotas.

Senior SRE Analysis: Beyond simple flag-based scanning, the agent identifies GCP Basic Roles (Owner/Editor) that violate security best practices and suggests granular Predefined Roles.

Professional CLI UI: Built with the Rich library to provide real-time status spinners, timestamped audit trails, and formatted analysis panels.

🛠️ Updated Technical Stack
Core Engine: Gemini 3 Flash (Preview).

Reasoning: Optimized for low-latency, high-frequency "Agentic Loops" required for real-time cloud auditing.

Tooling: Python 3.12, google-genai SDK, and the Rich terminal library.

⚡ Why Gemini 3 Flash?
As a Google Cloud TSE, I chose Gemini 3 Flash for its superior performance in automated SRE workflows:

Reduced Latency: Near-instant response times allow for real-time terminal feedback, essential for interactive security tools.

Function Calling Efficiency: The model excels at identifying exactly when to trigger the ai_audit_tool without conversational overhead.

Scalability: Designed for high-volume, repetitive tasks like scanning thousands of IAM bindings across a complex Google Cloud Organization.

📖 How It Works
Input: The user provides a GCP IAM policy export (e.g., policy_sample.json).

Reasoning: The AI analyzes the request and decides to call the ai_audit_tool.

Execution: A local Python script executes a security audit on the bindings and captures the output.

Feedback: The raw audit data is fed back to the AI for final reasoning and risk assessment.

Output: A formatted "Senior Google Cloud SRE Analysis" is displayed in the terminal.

🏗️ Technical Challenges & Solutions
The 429 "Quota" Wall: Initial runs hit API rate limits. I implemented Recursive Retry Logic that detects 429 errors and automatically triggers a "cool down" period before resuming the audit.

The "None" Rendering Bug: Extracting text from multi-part AI responses (which include function call data) often resulted in empty UI panels. I engineered a Text Extraction Filter to isolate specific text parts before rendering the final report.

Environment Isolation: Utilized a Python Virtual Environment (.venv) to ensure project portability and prevent version conflicts with system-level packages.

🛡️ GCP Remediation Example
Detected Risk: role: "roles/owner" assigned to a Service Account.

SRE Recommendation: Move to a Predefined Role (e.g., roles/compute.admin or roles/storage.objectAdmin) to restrict permissions to only the necessary resources within the project.

