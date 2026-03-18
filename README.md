# Berlin Heat Risk & Cooling Priority Explorer

An urban-climate decision-support project that identifies heat hotspots in Berlin and prioritizes non-green hot zones for cooling interventions.

## Project overview

This project combines official Berlin surface-temperature data, green-space data from OpenStreetMap, district boundaries, and a Streamlit dashboard to explore urban heat patterns and support intervention planning.

## Research question

Where are Berlin’s urban heat hotspots, and which non-green hot zones should be prioritized for cooling interventions?

## Data sources

- Berlin Climate Analysis 2022 surface-temperature layer
- OpenStreetMap green-space polygons
- Berlin district boundaries

## Method

The project uses descriptive geospatial analysis to:

1. map surface temperature across Berlin
2. overlay green-space polygons
3. compare temperatures in green vs non-green areas
4. aggregate temperature by district
5. classify and rank cooling priority zones
6. present the results in an interactive Streamlit app

## Key findings

- Green areas are about **1.02°C cooler** on average than non-green areas.
- Heat exposure is not evenly distributed across Berlin districts.
- Non-green hot zones can be ranked as cooling priorities for interventions such as tree planting, shaded public spaces, cool roofs, and permeable surfaces.

## Outputs

### Static outputs
- Berlin surface temperature map
- Heat + green-space overlay map
- Green vs non-green temperature boxplot
- District temperature ranking bar chart
- Cooling priority map

### Interactive output
- Streamlit dashboard with filters, live weather context, priority tables, and map exploration

## Files

- `analysis.py` — main geospatial analysis workflow
- `app.py` — Streamlit dashboard
- `data/` — processed geospatial outputs and CSVs
- `figures/` — exported maps and plots
- `slides/` — presentation materials

## Run locally

### 1. Create and activate environment
```bash
python3 -m venv .venv
source .venv/bin/activate