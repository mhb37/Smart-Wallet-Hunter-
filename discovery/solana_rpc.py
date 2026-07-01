import requests

SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"


def get_recent_signatures(address, limit=10):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [address, {"limit": limit}]
    }

    response = requests.post(SOLANA_RPC_URL, json=payload)
    data = response.json()

    return data.get("result", [])


def get_transaction(signature):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [
            signature,
            {
                "encoding": "jsonParsed",
                "maxSupportedTransactionVersion": 0
            }
        ]
    }

    response = requests.post(SOLANA_RPC_URL, json=payload)
    data = response.json()

    return data.get("result")