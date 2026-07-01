import logging

logger = logging.getLogger(__name__)


def load_tx(tx):
    """
    Interface utilisée par scanner.py
    Retourne toujours un dict contenant la clé 'wallets'.
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
        logger.exception(
            "[wallet_extractor] extract failed: %s",
            e
        )

    return wallets


def filter_wallets(wallets):
    filtered = set()

    for wallet in wallets:

        if not wallet:
            continue

        # Taille minimale d'une adresse Solana
        if len(wallet) < 32:
            continue

        # Comptes système
        if wallet.startswith("111111"):
            continue

        # Wrapped SOL
        if wallet == "So11111111111111111111111111111111111111112":
            continue

        filtered.add(wallet)

    return filtered