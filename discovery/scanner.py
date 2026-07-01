from collections import Counter

from discovery.solana_rpc import get_recent_signatures, get_transaction
from discovery.wallet_extractor import extract_wallets_from_transaction, filter_wallets


# =========================
# MEMORY GLOBAL (PERSISTANT RUNTIME)
# =========================
SEEN = Counter()


SEED_WALLETS = [
    "So11111111111111111111111111111111111111112"
]


def strong_filter(wallets):

    filtered = []

    for w in wallets:
        SEEN[w] += 1

        # 🔥 on force récurrence forte
        if SEEN[w] >= 3:
            filtered.append(w)

    return filtered


def discover_wallet_candidates():

    all_wallets = set()

    seeds = list(set(SEED_WALLETS) | set(SEEN.keys()))
    seeds = seeds[:15]  # anti explosion

    for seed in seeds:

        try:
            signatures = get_recent_signatures(seed, limit=5)
        except Exception:
            continue

        for tx in signatures:

            sig = tx.get("signature")
            if not sig:
                continue

            try:
                full_tx = get_transaction(sig)
            except Exception:
                continue

            wallets = extract_wallets_from_transaction(full_tx)
            wallets = filter_wallets(wallets)

            for w in wallets:
                all_wallets.add(w)

    # =========================
    # FILTER FINAL (IMPORTANT)
    # =========================
    wallets = strong_filter(list(all_wallets))

    if len(wallets) < 2:
        return []

    return wallets