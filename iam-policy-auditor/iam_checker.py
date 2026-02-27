import json
import os

def audit_policy(file_path):
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found.")
        return

    with open(file_path, 'r') as file:
        try:
            policy = json.load(file)
            statements = policy.get("Statement", [])
            
            # Ensure statements is a list
            if isinstance(statements, dict):
                statements = [statements]

            admin_found = False
            for stmt in statements:
                action = stmt.get("Action", "")
                effect = stmt.get("Effect", "")

                # Check for administrative wildcards or explicit Admin access
                if effect == "Allow" and (action == "*" or "AdministratorAccess" in str(action)):
                    admin_found = True
                    break
            
            if admin_found:
                print(f"⚠️ SECURITY ALERT: Admin access detected in {file_path}!")
            else:
                print(f"✅ Clean: No broad admin permissions found in {file_path}.")

        except json.JSONDecodeError:
            print(f"❌ Error: Could not parse {file_path}. Ensure it is valid JSON.")

if __name__ == "__main__":
    # Simulate a policy check
    audit_policy("policy_sample.json")
