SYSTEM_WALLETS = {
    "11111111111111111111111111111111",
    "ComputeBudget111111111111111111111111111111",
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
    "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL",
    "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr",
}


def extract_wallets_from_transaction(tx):

    wallets = []

    if not tx:
        return wallets

    try:

        message = tx["transaction"]["message"]

        account_keys = message.get("accountKeys", [])

        for acc in account_keys:

            if isinstance(acc, dict):
                pubkey = acc.get("pubkey")

            elif isinstance(acc, str):
                pubkey = acc

            else:
                continue

            if not pubkey:
                continue

            if len(pubkey) < 32:
                continue

            if pubkey in SYSTEM_WALLETS:
                continue

            wallets.append(pubkey)

    except Exception:
        pass

    return wallets