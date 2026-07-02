import logging
import os
import requests

logger = logging.getLogger(__name__)


SOLANA_RPC_URL = os.getenv(
    "SOLANA_RPC_URL",
    "https://api.mainnet-beta.solana.com"
)


TARGET_PROGRAMS = [
    # Jupiter
    "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4",

    # Raydium AMM
    "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8",

    # Raydium CLMM
    "CAMMCzo5YL8w4VFF8KVHrK22GGUQhJ6cA7Y7xqHY2k",

    # Pump.fun
    "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P",

    # Meteora
    "LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo",
]


session = requests.Session()


def rpc_call(method, params):

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params,
    }

    response = session.post(
        SOLANA_RPC_URL,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("error"):
        raise Exception(data["error"])

    return data["result"]


def get_recent_signatures(address, limit=20):

    return rpc_call(
        "getSignaturesForAddress",
        [
            address,
            {
                "limit": limit
            }
        ]
    )


def fetch_transactions(limit_per_program=20):

    signatures = []

    seen = set()

    for program in TARGET_PROGRAMS:

        try:

            txs = get_recent_signatures(
                program,
                limit_per_program
            )

            logger.info(
                "%s -> %s signatures",
                program,
                len(txs)
            )

            for tx in txs:

                sig = tx["signature"]

                if sig in seen:
                    continue

                seen.add(sig)
                signatures.append(sig)

        except Exception as e:

            logger.exception(
                "RPC error on %s: %s",
                program,
                e
            )

    logger.info(
        "TOTAL signatures collected = %s",
        len(signatures)
    )

    return signatures


def get_transaction(signature):

    try:

        return rpc_call(
            "getTransaction",
            [
                signature,
                {
                    "encoding": "jsonParsed",
                    "maxSupportedTransactionVersion": 0,
                }
            ]
        )

    except Exception as e:

        logger.exception(
            "transaction error %s : %s",
            signature,
            e
        )

        return None