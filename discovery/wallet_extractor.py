SYSTEM_WALLETS = {
    # System
    "11111111111111111111111111111111",
    "ComputeBudget111111111111111111111111111111",

    # SPL Token
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
    "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb",

    # ATA
    "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL",

    # Memo
    "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr",

    # Wrapped SOL
    "So11111111111111111111111111111111111111112",

    # Jupiter
    "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4",
    "D8cy77BBepLMngZx6ZukaTff5hCt1HrWyKk3Hnd9oitf",
}


BANNED_PREFIXES = (
    "jit",
    "jito",
    "J1to",
    "goon",
    "pAMM",
    "pfee",
)


def is_system_wallet(pubkey: str) -> bool:

    if pubkey in SYSTEM_WALLETS:
        return True

    if pubkey.startswith("Sysvar"):
        return True

    for prefix in BANNED_PREFIXES:
        if pubkey.startswith(prefix):
            return True

    return False


def extract_wallets_from_transaction(tx):

    wallets = []

    if not tx:
        return wallets

    try:

        message = tx["transaction"]["message"]

        for acc in message.get("accountKeys", []):

            if isinstance(acc, dict):
                pubkey = acc.get("pubkey")
            else:
                pubkey = acc

            if not pubkey:
                continue

            if len(pubkey) < 32:
                continue

            if pubkey.endswith("pump"):
                continue

            if is_system_wallet(pubkey):
                continue

            wallets.append(pubkey)

    except Exception as e:
        print(f"wallet extraction error: {e}")

    return list(dict.fromkeys(wallets))