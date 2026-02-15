import time
from datetime import datetime, timezone
from elasticsearch import Elasticsearch

# --- CONFIGURATION ---
# 1. Get ENDPOINT_URL from the Elastic Cloud Console
# 2. Create an API Key in Stack Management > API Keys
ENDPOINT_URL = [REDACTED]

API_KEY = [REDACTED]

# Connect to Elastic
es = Elasticsearch(hosts=[ENDPOINT_URL],api_key=API_KEY)

def inject_mvp_logs():
    index_name = "logs-incident-mvp"
    print(f"🚀 Starting log injection into {index_name}...")
    
    for i in range(12):
        doc = {
            "@timestamp": datetime.now(timezone.utc).isoformat(),
            "service": {"name": "payment-api"},
            "log": {"level": "ERROR"},
            "http": {
                "response": {"status_code": 500},
                "request": {"method": "POST", "path": "/v1/charge"}
            },
            "error": {
                "message": "ConnectionPoolTimeoutException: Timeout waiting for connection from createConnection",
                "stack_trace": "org.postgresql.util.PSQLException: Cannot connect to server...",
                "type": "database"
            },
            "message": "Failed to process payment request due to downstream timeout"
        }
        
        try:
            es.index(index=index_name, document=doc)
            print(f"✅ Injected log {i+1}/12")
        except Exception as e:
            print(f"❌ Failed to inject log: {e}")
        
        time.sleep(0.2) # Slight delay to simulate real-time traffic

if __name__ == "__main__":
    inject_mvp_logs()
