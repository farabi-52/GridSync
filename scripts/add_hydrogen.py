# add_hydrogen.py
# Sector coupling: Green H2 for Bangladesh fertilizer plants
# Bus mapping (auto-matched by haversine distance):
#   Chittagong (CUFL)       → BD0 2   (24 km away, lon=92.06, lat=22.38)
#   Ashuganj  (Jamuna Fert) → BD0 1   (35 km away, lon=90.52, lat=23.87)
#   Sylhet    (JFCL)        → BD0 5   (41 km away, lon=91.76, lat=24.54)

import numpy as np
import pandas as pd


def add_h2_sector(n):
    electrolyzer_capex = 500_000
    storage_capex      = 15_000
    electrolyzer_eff   = 0.70
    hb_eff             = 0.85

    regions = {
        "Chittagong": {"bus": "BD0 2",  "h2_demand_mw": 400},
        "Ashuganj":   {"bus": "BD0 1",  "h2_demand_mw": 200},
        "Sylhet":     {"bus": "BD0 5",  "h2_demand_mw": 100},
    }

    for region, cfg in regions.items():
        elec_bus     = cfg["bus"]
        h2_demand_mw = cfg["h2_demand_mw"]
        h2_bus_name  = f"{region} H2"
        nh3_bus_name = f"{region} NH3"

        if "H2" not in n.carriers.index:
            n.add("Carrier", "H2", color="#ff8c00", nice_name="Hydrogen")
        if "NH3" not in n.carriers.index:
            n.add("Carrier", "NH3", color="#6a0dad", nice_name="Ammonia")
        if "H2 electrolysis" not in n.carriers.index:
            n.add("Carrier", "H2 electrolysis", nice_name="Electrolyzer")
        if "NH3 production" not in n.carriers.index:
            n.add("Carrier", "NH3 production", nice_name="Haber-Bosch")

        n.add("Bus", h2_bus_name, carrier="H2",
              x=n.buses.at[elec_bus, "x"],
              y=n.buses.at[elec_bus, "y"])

        n.add("Bus", nh3_bus_name, carrier="NH3",
              x=n.buses.at[elec_bus, "x"],
              y=n.buses.at[elec_bus, "y"])

        n.add("Link",
              f"Electrolyzer {region}",
              bus0=elec_bus,
              bus1=h2_bus_name,
              p_nom_extendable=True,
              p_nom_min=0,
              efficiency=electrolyzer_eff,
              capital_cost=electrolyzer_capex,
              carrier="H2 electrolysis")

        n.add("Store",
              f"H2 storage {region}",
              bus=h2_bus_name,
              e_nom_extendable=True,
              e_cyclic=True,
              e_nom_min=0,
              standing_loss=0.0,
              capital_cost=storage_capex,
              carrier="H2")

        n.add("Link",
              f"NH3 plant {region}",
              bus0=h2_bus_name,
              bus1=nh3_bus_name,
              p_nom=h2_demand_mw / hb_eff,
              p_nom_extendable=False,
              efficiency=hb_eff,
              carrier="NH3 production")

        demand_profile = pd.Series(
            h2_demand_mw * np.ones(len(n.snapshots)),
            index=n.snapshots,
            name=f"NH3 demand {region}"
        )
        n.add("Load",
              f"NH3 demand {region}",
              bus=nh3_bus_name,
              p_set=demand_profile,
              carrier="NH3")

        print(f"[add_hydrogen] Added H2 sector for {region} "
              f"→ bus {elec_bus} | H2 demand: {h2_demand_mw} MW")
    thermal = ["CCGT", "OCGT", "coal", "oil", "nuclear"]
    for carrier in thermal:
        idx = n.generators[n.generators.carrier == carrier].index
        if len(idx) > 0:
            n.generators.loc[idx, "p_nom_extendable"] = False
            n.generators.loc[idx, "p_nom_opt"] = n.generators.loc[idx, "p_nom"]
            print(f"[fix] {carrier}: fixed at {n.generators.loc[idx,'p_nom'].sum():.0f} MW")

# Fix nuclear must-run
    nuc_i = n.generators[n.generators.carrier == "nuclear"].index
    n.generators.loc[nuc_i, "p_min_pu"] = 0.85
    n.generators.loc[nuc_i, "marginal_cost"] = 2.0                