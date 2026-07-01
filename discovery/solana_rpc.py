import requests


SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"


TARGET_PROGRAM = "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4"


def fetch_transactions(limit=10):

    signatures = get_recent_signatures(
        TARGET_PROGRAM,
        limit
    )

    return [
        tx["signature"]
        for tx in signatures
    ]


def get_recent_signatures(address, limit=10):

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [
            address,
            {"limit": limit}
        ]
    }

    response = requests.post(
        SOLANA_RPC_URL,
        json=payload,
        timeout=30,
    )

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

    response = requests.post(
        SOLANA_RPC_URL,
        json=payload,
        timeout=30,
    )

    data = response.json()

    return data.get("result")