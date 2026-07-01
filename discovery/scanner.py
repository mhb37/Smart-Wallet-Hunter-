from discovery.solana_rpc import get_recent_signatures


SEED_WALLETS = [
    "So11111111111111111111111111111111111111112",  # SOL mint (exemple réseau actif)
]


def discover_wallet_candidates():
    candidates = set()

    for wallet in SEED_WALLETS:
        txs = get_recent_signatures(wallet, limit=5)

        for tx in txs:
            sig = tx.get("signature")
            if sig:
                candidates.add(sig)

    return list(candidates)