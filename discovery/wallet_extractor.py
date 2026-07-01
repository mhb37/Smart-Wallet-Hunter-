import logging

logger = logging.getLogger(__name__)


# programmes Solana à exclure
EXCLUDED_WALLETS = {
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
    "ComputeBudget111111111111111111111111111111",
    "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL",
    "11111111111111111111111111111111",
    "SysvarRent111111111111111111111111111111111",
}


def extract_wallets_from_transaction(tx: dict) -> set[str]:
    """
    Extrait uniquement les wallets utiles (signers + accounts)
    """
    wallets = set()

    if not tx:
        return wallets

    try:
        message = tx.get("transaction", {}).get("message", {})
        accounts = message.get("accountKeys", [])

        for acc in accounts:

            # format jsonParsed
            if isinstance(acc, dict):
                pubkey = acc.get("pubkey")
                signer = acc.get("signer", False)

                if pubkey and signer and pubkey not in EXCLUDED_WALLETS:
                    wallets.add(pubkey)

            # format string
            elif isinstance(acc, str):
                if acc not in EXCLUDED_WALLETS:
                    wallets.add(acc)

    except Exception as e:
        logger.debug("wallet extractor error: %s", e)

    return wallets


def filter_wallets(wallets: set[str]) -> list[str]:
    """
    Nettoyage final
    """
    cleaned = set()

    for w in wallets:
        if not w:
            continue

        if not isinstance(w, str):
            continue

        if len(w) < 32:
            continue

        if "111111" in w:
            continue

        if w in EXCLUDED_WALLETS:
            continue

        cleaned.add(w)

    return list(cleaned)


def load_tx(tx):
    """
    Wrapper simple utilisé par scanner.py
    """
    return {
        "wallets": list(extract_wallets_from_transaction(tx))
    }