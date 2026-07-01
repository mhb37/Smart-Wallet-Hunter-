import logging
import requests

logger = logging.getLogger(__name__)

SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"

SESSION = requests.Session()


def rpc_call(method, params):
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }

        response = SESSION.post(
            SOLANA_RPC_URL,
            json=payload,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        if "error" in data:
            logger.error(
                "[RPC ERROR] %s -> %s",
                method,
                data["error"]
            )
            return None

        return data.get("result")

    except Exception as e:
        logger.exception(
            "[RPC FAILED] %s",
            method
        )
        return None


def get_recent_signatures(address, limit=10):
    result = rpc_call(
        "getSignaturesForAddress",
        [
            address,
            {"limit": limit}
        ]
    )

    if not result:
        return []

    logger.info(
        "[DEBUG] signatures count=%s",
        len(result)
    )

    return result


def get_transaction(signature):
    result = rpc_call(
        "getTransaction",
        [
            signature,
            {
                "encoding": "jsonParsed",
                "maxSupportedTransactionVersion": 0
            }
        ]
    )

    if result:
        logger.info("[DEBUG] tx loaded OK")
    else:
        logger.warning(
            "[DEBUG] empty transaction %s",
            signature
        )

    return result