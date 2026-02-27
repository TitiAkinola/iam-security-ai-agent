import json

def run_waste_audit(file_path):
    print(f"--- 🛡️ Starting FinOps Audit for {file_path} ---")
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        total_potential_savings = 0
        
        for item in data['resources']:
            # Logic 1: Find unattached storage
            if item['type'] == 'storage' and item['status'] == 'available':
                print(f"⚠️ WASTE: Unattached Disk {item['id']} is costing ${item['monthly_cost']}/mo")
                total_potential_savings += item['monthly_cost']
            
            # Logic 2: Find Load Balancers with no traffic
            if item['type'] == 'load_balancer' and item['active_targets'] == 0:
                print(f"⚠️ WASTE: Idle Load Balancer {item['id']} is costing ${item['monthly_cost']}/mo")
                total_potential_savings += item['monthly_cost']

        print(f"\n💰 TOTAL PROJECTED SAVINGS: ${total_potential_savings}/month")
        
    except FileNotFoundError:
        print("❌ Error: Inventory file not found.")

if __name__ == "__main__":
    run_waste_audit('cloud_inventory.json')
