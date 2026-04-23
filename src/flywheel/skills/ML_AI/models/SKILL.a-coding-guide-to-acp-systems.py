import os
import requests
from typing import Dict, List, Optional

class ACPSystem:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.acp.com/v1"

    def validate_api_key(self) -> bool:
        """  Validate the API key by making a request to a dummy endpoint  """
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(f"{self.base_url}/validate", headers=headers)
        return response.status_code == 200

    def fetch_data(self, resource: str) -> Optional[Dict]:
        " Fetch data from the ACP system "
        if not self.validate_api_key():
            raise ValueError("API key is invalid or missing")
        
        url = f"{self.base_url}/{resource}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

    def process_data(self, data: Dict) -> List[Dict]:
        " Process the fetched data "
        # Example processing: filter out some fields
        processed_data = [
            {k: v for k, v in item.items() if k not in ['unwanted_field1', 'unwanted_field2']}
            for item in data['items']
        ]
        return processed_data

# Usage example
if __name__ == "__main__":
    api_key = os.getenv("ACP_API_KEY")
    if not api_key:
        raise ValueError("API key must be provided as an environment variable")

    acp_system = ACPSystem(api_key)
    
    try:
        data = acp_system.fetch_data("data_endpoint")
        processed_data = acp_system.process_data(data)
        print(processed_data)
    except Exception as e:
        print(f"Error: {e}")