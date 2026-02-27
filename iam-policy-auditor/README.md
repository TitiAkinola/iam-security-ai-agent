AI-Powered IAM Security Auditor
An automated Security Agent that bridges the gap between Gemini 2.0 Flash reasoning and local Python security tools to audit AWS IAM policies.

🚀 Key Features
Agentic Execution Loop: Utilizes a manual function-calling loop where the AI autonomously identifies the need for a security scan and triggers a local Python "bridge" (iam_tools.py).

Rate Limit Resilience: Implements recursive retry logic to handle 429 RESOURCE_EXHAUSTED errors gracefully, ensuring 100% completion even on free-tier API quotas.

Senior SRE Analysis: Beyond simple flag-based scanning, the agent provides a high-level summary of risks (like wildcard permissions) and suggests "Least Privilege" remediations.

Professional CLI UI: Built with the Rich library to provide real-time status spinners, timestamped audit trails, and formatted analysis panels.

🛠️ Tech Stack
Language: Python 3.12+

AI Model: Google Gemini-3-flash-preview

Libraries: google-genai, rich

Infrastructure: AWS IAM Policy structure

📖 How It Works
Input: The user provides an IAM policy file (e.g., policy_sample.json).

Reasoning: The AI analyzes the request and decides to call the ai_audit_tool.

Execution: A local Python script executes a security audit on the file and captures the output.

Feedback: The raw audit data is fed back to the AI for final reasoning.

Output: A formatted "Senior SRE Analysis" is displayed in the terminal.

🛡️ Remediation Example
Detected Risk: Action: "*" on Resource: "*" (Administrative Wildcard).

SRE Recommendation: Move to a scoped policy allowing only specific actions (e.g., s3:GetObject) on specific resources.
