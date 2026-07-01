def extract_wallets_from_transaction(tx):

    wallets = set()

    if not tx:
        return wallets

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

    result = []

    blacklist = {
        "So11111111111111111111111111111111111111112",
        "11111111111111111111111111111111"
    }

    for w in wallets:

        if not isinstance(w, str):
            continue

        if len(w) < 32:
            continue

        if w in blacklist:
            continue

        result.append(w)

    return result


def load_tx(signature):

    from discovery.solana_rpc import load_tx as rpc_load

    tx = rpc_load(signature)

    if not tx:
        return None

    wallets = extract_wallets_from_transaction(tx)

    wallets = filter_wallets(wallets)

    return {
        "wallets": wallets
    }