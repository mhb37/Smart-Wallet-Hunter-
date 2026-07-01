from collections import defaultdict

from discovery.solana_rpc import get_recent_signatures, get_transaction
from discovery.wallet_extractor import extract_wallets_from_transaction, filter_wallets


# =========================
# MEMORY (IMPORTANT V6)
# =========================

WALLET_STATS = defaultdict(int)
SEED_WALLETS = [
    "So11111111111111111111111111111111111111112"
]


def _update_memory(wallets):

    for w in wallets:
        WALLET_STATS[w] += 1


def _filter_recurrent(wallets):

    """
    Garde uniquement les wallets déjà vus au moins 2 fois
    => réduit MASSIVEMENT le bruit
    """

    filtered = []

    for w in wallets:
        if WALLET_STATS[w] >= 2:
            filtered.append(w)

    return filtered


def discover_wallet_candidates():

    all_wallets = set()

    # =========================
    # DYNAMIC SEEDS (IMPORTANT)
    # =========================
    dynamic_seeds = list(set(SEED_WALLETS) | set(list(WALLET_STATS.keys())))

    # limite anti explosion
    dynamic_seeds = dynamic_seeds[:20]

    for seed in dynamic_seeds:

        try:
            signatures = get_recent_signatures(seed, limit=8)
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
    # UPDATE MEMORY
    # =========================
    _update_memory(all_wallets)

    # =========================
    # FILTER RECURRING SIGNAL
    # =========================
    final_wallets = _filter_recurrent(all_wallets)

    # fallback sécurité : si trop strict, on renvoie brut
    if len(final_wallets) < 3:
        return list(all_wallets)

    return list(final_wallets)