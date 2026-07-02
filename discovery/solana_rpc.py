import os
import requests
import logging


logger = logging.getLogger(__name__)


SOLANA_RPC_URL = os.getenv(
    "SOLANA_RPC_URL",
    "https://api.mainnet-beta.solana.com"
)


TARGET_WALLETS = [
    "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4",
]


def get_recent_signatures(address, limit=20):

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

    response = requests.post(
        SOLANA_RPC_URL,
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return data.get("result", [])


def fetch_transactions(limit=20):

    signatures = []

    for address in TARGET_WALLETS:

        try:

            result = get_recent_signatures(
                address,
                limit
            )

            signatures.extend(
                x["signature"]
                for x in result
            )

        except Exception as e:

            logger.exception(e)

    return list(dict.fromkeys(signatures))


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
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return data.get("result")