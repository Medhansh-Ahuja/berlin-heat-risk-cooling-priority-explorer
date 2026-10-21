# Berlin Heat Risk & Cooling Priority Explorer

A geospatial urban-climate decision-support project that identifies heat hotspots in Berlin and prioritizes non-green hot zones for cooling interventions.

## Project overview

Berlin Heat Risk & Cooling Priority Explorer is designed as more than a heat map.  
It is a spatial decision-support tool that combines official Berlin surface-temperature data, green-space polygons, and district boundaries to:

- map urban heat patterns across Berlin
- compare green vs non-green areas
- summarize district-level heat differences
- identify non-green hot zones for cooling intervention prioritization
- present the results in an interactive Streamlit dashboard

This project sits at the intersection of **geospatial analysis, urban climate analytics, planning-oriented insight, and dashboard delivery**.

---

## Project goal

The goal of the project is to support urban heat-risk understanding and intervention targeting by translating geospatial heat data into a practical prioritization workflow.

Instead of only visualizing heat, the project highlights where cooling interventions may deserve greater attention.

---

## Key questions

This project was built to answer questions such as:

- Where are the hottest surface-temperature zones in Berlin?
- Are green areas cooler than non-green areas?
- How does heat exposure vary across Berlin districts?
- Which non-green hot zones should be prioritized for cooling interventions?

---

## Data sources

The project uses the following spatial data sources:

- **Berlin Climate Analysis 2022 surface-temperature layer**
- **OpenStreetMap green-space polygons**
- **Berlin district boundaries**

These datasets are combined through geospatial processing and overlay analysis to produce both descriptive and prioritization-focused outputs.

---

## Methodology

The analysis pipeline includes:

1. **Geospatial data loading and preprocessing**
   - load temperature, green-space, and district boundary layers
   - clean and align spatial datasets
   - prepare spatial outputs for analysis and visualization

2. **Surface temperature mapping**
   - map the Berlin temperature layer
   - identify urban heat patterns spatially

3. **Green vs non-green comparison**
   - overlay temperature data with green-space polygons
   - compare temperature distributions between green and non-green areas

4. **District-level aggregation**
   - aggregate temperature values by Berlin district
   - calculate district-level mean heat exposure

5. **Cooling priority classification**
   - identify hot, non-green zones
   - classify these zones as higher cooling-intervention priorities

6. **Dashboard development**
   - package the outputs into a Streamlit interface
   - enable interactive exploration of maps, KPIs, figures, and priority tables

---

## Key results

### Green vs non-green comparison
- **Mean temperature in green areas:** 30.66°C
- **Mean temperature in non-green areas:** 31.68°C
- **Difference:** green areas were **1.02°C cooler on average**

### District-level findings
- **Mitte** is the hottest district, with a mean surface temperature of **33.0°C** at 14:00
- **Steglitz-Zehlendorf** is the coolest, at **30.2°C**, a gap of about **2.8°C** between districts
- District aggregation reveals differences that are not visible in city-wide averages alone

### Cooling-priority findings
- **3,242 of 33,887 zones** (about 10%) are classified as **Very High** priority
- The largest numbers of Very High zones are in Marzahn-Hellersdorf, Treptow-Köpenick and Pankow
- Non-green hot zones emerge as the strongest cooling-intervention priorities, which turns the project from descriptive visualization into a planning-oriented workflow

---

## Outputs generated

The project produces:

- Berlin surface temperature map
- Heat map with green-space overlay
- Green vs non-green boxplot
- District mean temperature bar chart
- Cooling priority map
- Top cooling priority zones CSV
- District temperature summary CSV
- Interactive Streamlit dashboard

---

## Streamlit app features

The Streamlit dashboard includes:

- KPI cards
- district filter
- priority-class filter
- interactive cooling priority map
- priority tables
- figures tab
- Berlin weather context
- overview tab with insights and recommendations

This makes the project usable as an exploratory dashboard rather than only a static analysis notebook or script output.

---

## Repository structure

```text
berlin-heat-risk-cooling-priority-explorer/
├── app.py                 # Streamlit dashboard
├── analysis.py            # data download, processing, figures and priority zones
├── requirements.txt
├── data/                  # processed outputs used by the dashboard
├── figures/               # static maps and charts
└── presentation/          # project slides (PDF)
```

---

## How to run

```bash
git clone https://github.com/Medhansh-Ahuja/berlin-heat-risk-cooling-priority-explorer.git
cd berlin-heat-risk-cooling-priority-explorer
pip install -r requirements.txt

# Launch the dashboard (uses the processed files in data/)
streamlit run app.py

# Optional: rebuild the analysis from source data
python analysis.py
```

`analysis.py` downloads the raw surface-temperature layer from the Berlin WFS service when it is not present locally. The processed GeoJSON files in `data/` are slightly simplified (0.5 m tolerance) to keep the repository small; this has no visible effect on the maps.

---

## Presentation

A short slide deck summarising the project: [Berlin_Heat_Risk_Explorer_Presentation.pdf](presentation/Berlin_Heat_Risk_Explorer_Presentation.pdf)

---

## Limitations and next steps

- The priority score is currently driven by **surface temperature (hazard)**, with green areas down-weighted. A fuller heat-risk model would also include **exposure** (population density) and **vulnerability** (e.g. share of residents aged 65+).
- Surface temperature at 14:00 is not the same as the air temperature people experience; night-time heat would add another important dimension.
- Some zones on district borders are not assigned to a district and appear without a district label.
