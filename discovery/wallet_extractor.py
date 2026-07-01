SYSTEM_WALLETS = {
    # System
    "11111111111111111111111111111111",
    "ComputeBudget111111111111111111111111111111",

    # SPL Token
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
    "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb",

    # Associated Token Account
    "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL",

    # Memo
    "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr",

    # Wrapped SOL
    "So11111111111111111111111111111111111111112",

    # Jupiter
    "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4",
    "D8cy77BBepLMngZx6ZukaTff5hCt1HrWyKk3Hnd9oitf",

    # Jito
    "jitodontfront1111111111111111JustUseJupiter",

    # Sysvars
    "SysvarRecentB1ockHashes11111111111111111111",
    "Sysvar1nstructions1111111111111111111111111",
    "SysvarC1ock11111111111111111111111111111111",
}


def is_system_wallet(pubkey: str) -> bool:

    if pubkey in SYSTEM_WALLETS:
        return True

    # Autres comptes système Solana
    if pubkey.startswith("Sysvar"):
        return True

    return False


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

            if is_system_wallet(pubkey):
                continue

            wallets.append(pubkey)

    except Exception as e:
        print(f"wallet extraction error: {e}")

    # Supprime les doublons tout en conservant l'ordre
    return list(dict.fromkeys(wallets))