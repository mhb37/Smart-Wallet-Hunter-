from collections import Counter

from discovery.solana_rpc import get_recent_signatures, get_transaction
from discovery.wallet_extractor import extract_wallets_from_transaction, filter_wallets


# =========================
# MEMORY
# =========================
SEEN = Counter()

SEED_WALLETS = [
    "So11111111111111111111111111111111111111112"
]


# =========================
# FILTER (léger)
# =========================
def recurrence_filter(wallets):

    result = []

    for w in wallets:
        SEEN[w] += 1

        if SEEN[w] >= 2:
            result.append(w)

    return result


# =========================
# DEBUG SCANNER
# =========================
def discover_wallet_candidates():

    print("\n===== SCANNER DEBUG START =====")

    current_seeds = set(SEED_WALLETS)
    all_discovered = set()

    for seed in list(current_seeds):

        print(f"\n[DEBUG] SEED: {seed}")

        # =========================
        # 1. GET SIGNATURES
        # =========================
        try:
            signatures = get_recent_signatures(seed, limit=10)
            print(f"[DEBUG] signatures raw type={type(signatures)}")

        except Exception as e:
            print(f"[ERROR] get_recent_signatures failed: {e}")
            continue

        if not signatures:
            print("[DEBUG] NO signatures returned")
            continue

        print(f"[DEBUG] signatures count={len(signatures)}")

        # =========================
        # 2. LOOP TX
        # =========================
        for i, tx in enumerate(signatures[:10]):

            sig = tx.get("signature") if isinstance(tx, dict) else None

            print(f"\n[DEBUG] TX #{i} sig={sig}")

            if not sig:
                print("[DEBUG] missing signature")
                continue

            # =========================
            # 3. GET FULL TX
            # =========================
            try:
                full_tx = get_transaction(sig)
            except Exception as e:
                print(f"[ERROR] get_transaction failed: {e}")
                continue

            if not full_tx:
                print("[DEBUG] empty transaction")
                continue

            print("[DEBUG] tx loaded OK")

            # =========================
            # 4. EXTRACT WALLETS
            # =========================
            try:
                wallets = extract_wallets_from_transaction(full_tx)
                print(f"[DEBUG] wallets raw: {wallets}")

            except Exception as e:
                print(f"[ERROR] extract_wallets failed: {e}")
                continue

            if not wallets:
                print("[DEBUG] no wallets extracted")
                continue

            # =========================
            # 5. FILTER
            # =========================
            try:
                wallets = filter_wallets(wallets)
                print(f"[DEBUG] wallets after filter: {wallets}")

            except Exception as e:
                print(f"[ERROR] filter_wallets failed: {e}")
                continue

            for w in wallets:
                all_discovered.add(w)

    # =========================
    # FINAL FILTER
    # =========================
    wallets = recurrence_filter(list(all_discovered))

    print("\n===== SCANNER DEBUG END =====")
    print(f"[DEBUG] total discovered wallets={len(all_discovered)}")
    print(f"[DEBUG] final wallets={len(wallets)}")

    if len(wallets) < 2:
        print("[DEBUG] NOT ENOUGH DATA → returning empty")
        return []

    return wallets