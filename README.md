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
- Heat exposure varies across Berlin districts
- District aggregation reveals differences that are not visible in city-wide averages alone

### Cooling-priority findings
- Non-green hot zones emerge as the strongest cooling-intervention priorities
- The prioritization layer turns the project from descriptive visualization into a planning-oriented workflow

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
├── app.py
├── analysis.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
├── figures/
└── slides/