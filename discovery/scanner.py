from discovery.solana_rpc import get_recent_signatures, get_transaction
from discovery.wallet_extractor import extract_wallets_from_transaction, filter_wallets


SEED_WALLETS = [
    "So11111111111111111111111111111111111111112"
]

EXPLORED = set()


def discover_wallet_candidates():

    all_wallets = set()

    # 🔥 dynamic seeds = seeds + anciens wallets
    dynamic_seeds = list(set(SEED_WALLETS) | EXPLORED)

    for seed in dynamic_seeds[:20]:  # limite pour éviter explosion

        try:
            signatures = get_recent_signatures(seed, limit=5)
        except:
            continue

        for tx in signatures:

            sig = tx.get("signature")
            if not sig:
                continue

            full_tx = get_transaction(sig)

            wallets = extract_wallets_from_transaction(full_tx)
            wallets = filter_wallets(wallets)

            for w in wallets:
                all_wallets.add(w)
                EXPLORED.add(w)  # 🔥 clé du système

    return list(all_wallets)