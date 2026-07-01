from collections import defaultdict

from discovery.solana_rpc import get_recent_signatures, get_transaction
from discovery.wallet_extractor import extract_wallets_from_transaction


# =========================
# CONFIG
# =========================
SEED_WALLETS = [
    "So11111111111111111111111111111111111111112"
]


# =========================
# STATS MEMORY (runtime only)
# =========================
WALLET_STATS = defaultdict(lambda: {
    "appear": 0
})


# =========================
# NO FILTER (SAFE MODE)
# =========================
def recurrence_filter(wallets):
    """
    ⚠️ SAFE MODE:
    Aucun filtrage destructeur ici.
    """
    return list(wallets)


# =========================
# MAIN SCANNER
# =========================
def discover_wallet_candidates():

    print("\n===== SCANNER START =====")

    all_wallets = set()

    for seed in SEED_WALLETS:

        print(f"\n[DEBUG] SEED = {seed}")

        # =========================
        # 1. GET SIGNATURES
        # =========================
        try:
            signatures = get_recent_signatures(seed, limit=10)
        except Exception as e:
            print(f"[ERROR] get_recent_signatures: {e}")
            continue

        if not signatures:
            print("[DEBUG] NO signatures returned")
            continue

        print(f"[DEBUG] signatures count = {len(signatures)}")

        # =========================
        # 2. PROCESS TX
        # =========================
        for i, tx in enumerate(signatures):

            sig = tx.get("signature") if isinstance(tx, dict) else None

            print(f"\n[DEBUG] TX #{i} sig = {sig}")

            if not sig:
                continue

            # =========================
            # 3. GET TX
            # =========================
            try:
                full_tx = get_transaction(sig)
            except Exception as e:
                print(f"[ERROR] get_transaction: {e}")
                continue

            if not full_tx:
                print("[DEBUG] empty tx")
                continue

            print("[DEBUG] tx loaded OK")

            # =========================
            # 4. EXTRACT WALLETS
            # =========================
            try:
                wallets = extract_wallets_from_transaction(full_tx)
            except Exception as e:
                print(f"[ERROR] extract_wallets: {e}")
                continue

            if not wallets:
                print("[DEBUG] no wallets extracted")
                continue

            print(f"[DEBUG] wallets raw = {wallets}")

            # =========================
            # 5. FILTER (DISABLED SAFE)
            # =========================
            wallets = recurrence_filter(wallets)

            print(f"[DEBUG] wallets after filter = {wallets}")

            # =========================
            # 6. STORE GLOBAL SET (IMPORTANT FIX)
            # =========================
            for w in wallets:
                all_wallets.add(w)
                WALLET_STATS[w]["appear"] += 1

    # =========================
    # FINAL DEBUG (CRITICAL FIX AREA)
    # =========================
    print("\n===== FINAL DEBUG =====")
    print(f"[DEBUG] discovered wallets = {len(all_wallets)}")
    print(f"[DEBUG] sample = {list(all_wallets)[:5]}")

    final_wallets = list(all_wallets)

    # =========================
    # SAFETY RETURN (NO EMPTY RESET BUG)
    # =========================
    if len(final_wallets) == 0:
        print("[DEBUG] EMPTY RESULT - CHECK RPC OR EXTRACTION")
        return []

    print(f"[DEBUG] FINAL OUTPUT = {len(final_wallets)} wallets")

    return final_wallets