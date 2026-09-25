# GridSync

## Overview

This repository presents the [PyPSA-Earth](https://github.com/pypsa-meets-earth/pypsa-earth.git) application tailored to Bangladesh, using version 0.3.0 of PyPSA-Earth. The PyPSA-Earth model has been adapted with localized power plant data, cost parameters, and regional demand profiles to develop comprehensive scenarios for the future of the Bangladesh power sector. GridSync extends this foundation to synchronize green hydrogen production and electric vehicle (EV) smart charging with Bangladesh's variable renewable generation, aiming to assist strategic energy planning and policy development by simulating decarbonization pathways alongside sector-coupled flexibility solutions.

## Key Features

- **Localized data**: Integration of official data from the Bangladesh Power Development Board (BPDB), Power Grid Bangladesh PLC (PGCB), and other relevant sources to accurately represent the current energy infrastructure.
- **Scenario analysis**: Development and analysis of multiple future scenarios, including 30% and 40% clean energy targets by 2030 and 2041, respectively, and a decarbonized scenario by 2050.
- **Sector coupling**: Modeling of green hydrogen production and EV smart charging as flexible demand-side resources that absorb variable renewable generation, reducing curtailment and supporting grid stability.
- **Validation**: Model validation using 2019 data to ensure accuracy and reliability, accounting for disruptions in subsequent years due to the COVID-19 pandemic.

## Data Sources

- [Bangladesh Power Development Board (BPDB)](https://bpdb.portal.gov.bd/site/page/c4161d54-5b85-4917-a8d2-68a2d1b26dd4/%E0%A6%AE%E0%A6%BE%E0%A6%B8%E0%A6%BF%E0%A6%95-%E0%A6%AC%E0%A6%BE%E0%A6%B0%E0%A7%8D%E0%A6%B7%E0%A6%BF%E0%A6%95-%E0%A6%AA%E0%A7%8D%E0%A6%B0%E0%A6%A4%E0%A6%BF%E0%A6%AC%E0%A7%87%E0%A6%A6%E0%A6%A8)
- [Power Grid Bangladesh PLC (PGCB)](https://pgcb.gov.bd/)
- IRENA 2019
- EnerData Country Statistics
- Our World in Data

## How to Replicate the Model

1. Follow the installation procedure given in the official [PyPSA-Earth](https://github.com/pypsa-meets-earth/pypsa-earth.git) repository.
2. Use the config files provided in this repository for the different scenarios.
3. Supply custom power plant, cost, and load data as required for your analysis.
4. Set the scenario objectives (e.g., clean energy share, target year, hydrogen/EV coupling assumptions).
5. Read the [PyPSA documentation](https://pypsa.readthedocs.io/en/latest/index.html) for further customization of the model as required.

## Note on Data Files

Large auxiliary datasets (e.g., OSM extracts, land-cover bundles, population and GDP rasters, weather/cutout data) are not tracked in this repository to keep it lightweight. These are automatically retrieved via the PyPSA-Earth `snakemake` workflow rules (e.g., `retrieve_databundle_light`, `build_cutout`) as described in the PyPSA-Earth documentation. Regenerate them locally using the same configuration files provided here.
