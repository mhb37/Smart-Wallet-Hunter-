import logging

from discovery.solana_rpc import fetch_transactions
from discovery.wallet_extractor import load_tx

logger = logging.getLogger(__name__)


def scan_wallets():
    wallets = set()

    try:
        transactions = fetch_transactions()

        logger.info("TX count = %s", len(transactions))

        for tx in transactions:

            data = load_tx(tx)
            raw = data.get("wallets", [])

            if isinstance(raw, str):
                raw = [raw]

            if isinstance(raw, set):
                raw = list(raw)

            for w in raw:
                if isinstance(w, str) and len(w) > 30:
                    wallets.add(w)

        return list(wallets)

    except Exception as e:
        logger.exception(e)
        return []