from discovery.solana_rpc import get_transaction


def load_tx(signature):

    tx = get_transaction(signature)

    if not tx:
        return None

    wallets = extract_wallets_from_transaction(tx)

    wallets = filter_wallets(wallets)

    return {
        "wallets": list(wallets)
    }


def extract_wallets_from_transaction(tx):

    wallets = set()

    try:

        accounts = (
            tx["transaction"]["message"]
            .get("accountKeys", [])
        )

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

    banned = {
        "So11111111111111111111111111111111111111112",
        "11111111111111111111111111111111"
    }

    filtered = []

    for w in wallets:

        if not w:
            continue

        if len(w) < 32:
            continue

        if w in banned:
            continue

        filtered.append(w)

    return filtered