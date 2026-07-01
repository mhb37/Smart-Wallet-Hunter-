from discovery.solana_rpc import get_transaction


BLACKLIST = {
    "11111111111111111111111111111111",
    "So11111111111111111111111111111111111111112",
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
    "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL",
    "ComputeBudget111111111111111111111111111111",
    "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb",
}


def load_tx(signature):

    tx = get_transaction(signature)

    if not tx:
        return None

    wallets = extract_wallets_from_transaction(tx)

    wallets = filter_wallets(wallets)

    return {
        "wallets": wallets
    }


def extract_wallets_from_transaction(tx):

    wallets = set()

    try:

        accounts = tx["transaction"]["message"]["accountKeys"]

        for acc in accounts:

            if isinstance(acc, dict):

                pubkey = acc.get("pubkey")

                if pubkey:
                    wallets.add(pubkey)

            elif isinstance(acc, str):

                wallets.add(acc)

    except Exception:
        pass

    return wallets


def filter_wallets(wallets):

    result = []

    for w in wallets:

        if not w:
            continue

        if len(w) < 32:
            continue

        if w in BLACKLIST:
            continue

        if "111111111111" in w:
            continue

        result.append(w)

    return result