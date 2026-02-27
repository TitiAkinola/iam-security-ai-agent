import requests

def check_website(url):
    """
    Pings a URL and returns whether it is Up or Down.
    """
    try:
        # We set a 5-second timeout to prevent the script from hanging
        response = requests.get(url, timeout=5)
        
        # HTTP status codes 200-299 are considered 'Up'
        if 200 <= response.status_code < 300:
            print(f"✅ UP: {url} (Status: {response.status_code})")
        else:
            print(f"⚠️ DOWN: {url} (Status: {response.status_code})")
            
    except requests.exceptions.RequestException as e:
        # Handles connection errors, DNS failures, or timeouts
        print(f"❌ DOWN: {url} (Error: {e})")

if __name__ == "__main__":
    # Test with a few URLs
    sites = ["https://www.google.com", "https://httpstat.us/404", "https://thisisafakesite123.com"]
    
    print("--- Starting API Health Check ---")
    for site in sites:
        check_website(site)