from discovery.solana_rpc import get_recent_signatures, get_transaction
from discovery.wallet_extractor import extract_wallets_from_transaction, filter_wallets


SEED_WALLETS = [
    "So11111111111111111111111111111111111111112"
]


def discover_wallet_candidates():

    all_wallets = set()

    for seed in SEED_WALLETS:

        signatures = get_recent_signatures(seed, limit=10)

        for tx in signatures:

            signature = tx.get("signature")
            if not signature:
                continue

            full_tx = get_transaction(signature)

            wallets = extract_wallets_from_transaction(full_tx)
            wallets = filter_wallets(wallets)

            for w in wallets:
                all_wallets.add(w)

                # 🔥 IMPORTANT : re-exploration légère (1 hop)
                try:
                    sub_signatures = get_recent_signatures(w, limit=3)

                    for stx in sub_signatures:
                        sig = stx.get("signature")
                        if not sig:
                            continue

                        sub_tx = get_transaction(sig)

                        sub_wallets = extract_wallets_from_transaction(sub_tx)
                        sub_wallets = filter_wallets(sub_wallets)

                        all_wallets.update(sub_wallets)

                except:
                    pass

    return list(all_wallets)