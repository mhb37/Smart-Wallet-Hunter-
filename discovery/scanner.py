from collections import Counter

from discovery.solana_rpc import get_recent_signatures, get_transaction
from discovery.wallet_extractor import extract_wallets_from_transaction, filter_wallets


# =========================
# MEMORY (runtime only)
# =========================
SEEN = Counter()

# seeds init (point de départ réseau)
SEED_WALLETS = [
    "So11111111111111111111111111111111111111112"
]


# =========================
# FILTER RÉCURRENCE (léger, pas destructif)
# =========================
def recurrence_filter(wallets):

    result = []

    for w in wallets:
        SEEN[w] += 1

        # seuil équilibré (IMPORTANT)
        if SEEN[w] >= 2:
            result.append(w)

    return result


# =========================
# MULTI-HOP DISCOVERY ENGINE (FIX IMPORTANT)
# =========================
def discover_wallet_candidates():

    current_seeds = set(SEED_WALLETS)
    all_discovered = set()

    # 🔁 MULTI-HOP EXPLORATION (clé du fix)
    for _ in range(2):  # depth = 2

        next_seeds = set()

        for seed in list(current_seeds):

            try:
                signatures = get_recent_signatures(seed, limit=10)
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
                    all_discovered.add(w)
                    next_seeds.add(w)

        # propagation vers la couche suivante
        current_seeds = next_seeds

        # stop si rien ne progresse
        if not current_seeds:
            break

    # =========================
    # FINAL FILTER
    # =========================
    wallets = recurrence_filter(list(all_discovered))

    # sécurité anti bruit
    if len(wallets) < 2:
        return []

    return wallets