import logging

import requests


logger = logging.getLogger(__name__)


SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"

# Jupiter
TARGET_PROGRAM = "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4"


def fetch_transactions(limit=25):

    signatures = get_recent_signatures(
        TARGET_PROGRAM,
        limit
    )

    return [
        tx["signature"]
        for tx in signatures
        if "signature" in tx
    ]


def get_recent_signatures(address, limit=25):

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [
            address,
            {
                "limit": limit
            }
        ]
    }

    try:

        response = requests.post(
            SOLANA_RPC_URL,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        return data.get("result", [])

    except Exception as e:

        logger.exception(
            "get_recent_signatures failed: %s",
            e
        )

        return []


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

    try:

        response = requests.post(
            SOLANA_RPC_URL,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        return data.get("result")

    except Exception as e:

        logger.exception(
            "get_transaction failed: %s",
            e
        )

        return None