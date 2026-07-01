from discovery.solana_rpc import get_recent_signatures, get_transaction
from discovery.wallet_extractor import (
    extract_wallets_from_transaction,
    filter_wallets
)


SEED_WALLETS = [
    "So11111111111111111111111111111111111111112"
]


def discover_wallet_candidates():

    all_wallets = set()

    for seed in SEED_WALLETS:

        signatures = get_recent_signatures(seed, limit=5)

        for tx in signatures:

            signature = tx.get("signature")
            if not signature:
                continue

            full_tx = get_transaction(signature)

            wallets = extract_wallets_from_transaction(full_tx)
            wallets = filter_wallets(wallets)

            all_wallets.update(wallets)

    return list(all_wallets)