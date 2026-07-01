import logging

logger = logging.getLogger(__name__)


def scan_wallets():
    wallets = set()

    try:
        transactions = fetch_transactions()

        for tx in transactions:
            data = load_tx(tx)

            raw = data.get("wallets", [])

            if isinstance(raw, set):
                raw = list(raw)

            if isinstance(raw, str):
                raw = [raw]

            cleaned = [
                w for w in raw
                if w and len(w) > 10
            ]

            wallets.update(cleaned)

        return list(wallets)

    except Exception as e:
        logger.exception(e)
        return []


# MOCKS (à remplacer par ton RPC)
def fetch_transactions():
    return []


def load_tx(tx):
    return {"wallets": []}