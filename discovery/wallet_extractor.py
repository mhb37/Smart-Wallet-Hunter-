import logging

logger = logging.getLogger(__name__)


def load_tx(tx):
    """
    Compatible avec scanner.py
    Reçoit déjà la transaction complète.
    """
    wallets = extract_wallets_from_transaction(tx)
    wallets = filter_wallets(wallets)

    return {
        "wallets": list(wallets)
    }


def extract_wallets_from_transaction(tx):
    wallets = set()

    if not tx:
        return wallets

    try:
        message = tx["transaction"]["message"]
        accounts = message.get("accountKeys", [])

        for acc in accounts:

            # Format jsonParsed
            if isinstance(acc, dict):
                pubkey = acc.get("pubkey")
                signer = acc.get("signer", False)

                if pubkey and signer:
                    wallets.add(pubkey)

            # Format string
            elif isinstance(acc, str):
                wallets.add(acc)

    except Exception as e:
        logger.exception(e)

    return wallets


def filter_wallets(wallets):
    filtered = set()

    for w in wallets:

        if not w:
            continue

        # Taille minimale d'une adresse Solana
        if len(w) < 32:
            continue

        # Élimine les comptes système
        if w.startswith("111111"):
            continue

        filtered.add(w)

    return filtered