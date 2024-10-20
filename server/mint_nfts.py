import requests

# Replace with the appropriate URL for your agent's REST endpoint
url = 'http://localhost:8000/mint_nft'  # The default port for uagents REST is 8000

# List of URLs for minting NFTs
data = {
    'urls': [
        'https://example.com/nft1',
        'https://example.com/nft2'
    ]
}

# Send POST request
response = requests.post(url, json=data)

# Print the response from the server
print(response.text)