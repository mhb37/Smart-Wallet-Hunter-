import requests


SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"

SEED_ADDRESS = "So11111111111111111111111111111111111111112"


def fetch_transactions(limit=10):

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [
            SEED_ADDRESS,
            {
                "limit": limit
            }
        ]
    }

    r = requests.post(
        SOLANA_RPC_URL,
        json=payload,
        timeout=20
    )

    data = r.json()

    signatures = data.get("result", [])

    return [
        x["signature"]
        for x in signatures
    ]


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

    r = requests.post(
        SOLANA_RPC_URL,
        json=payload,
        timeout=20
    )

    data = r.json()

    return data.get("result")