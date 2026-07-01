from discovery.scanner import discover_wallet_candidates


def discover_wallets_job():

    wallets = discover_wallet_candidates()

    print(f"{len(wallets)} candidats détectés")