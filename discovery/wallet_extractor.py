def extract_wallets_from_transaction(tx):
    wallets = set()

    if not tx:
        return wallets

    try:
        message = tx["transaction"]["message"]
        accounts = message.get("accountKeys", [])

        for acc in accounts:

            # format dict (jsonParsed)
            if isinstance(acc, dict):
                pubkey = acc.get("pubkey")
                signer = acc.get("signer", False)

                if pubkey and signer:
                    wallets.add(pubkey)

            # format string
            elif isinstance(acc, str):
                wallets.add(acc)

    except Exception:
        pass

    return wallets


def filter_wallets(wallets):
    filtered = set()

    for w in wallets:

        if not w:
            continue

        # filtre basique
        if len(w) < 32:
            continue

        # adresse système (simplifié)
        if "111111" in w:
            continue

        filtered.add(w)

    return filtered