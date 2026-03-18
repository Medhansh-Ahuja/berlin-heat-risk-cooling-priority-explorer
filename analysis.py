from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import osmnx as ox
import pandas as pd
from owslib.wfs import WebFeatureService


# =========================
# Configuration
# =========================

WFS_URL = "https://gdi.berlin.de/services/wfs/ua_klimaanalyse_2022?service=WFS&request=GetCapabilities"
LAYER_NAME = "ua_klimaanalyse_2022:lb_ua_oberfltemp_str_t2m_14h_2022"

DATA_DIR = Path("data")
FIGURES_DIR = Path("figures")

OUTPUT_GEOJSON = DATA_DIR / "berlin_surface_temp_14h.geojson"
GREEN_GEOJSON = DATA_DIR / "berlin_green_areas.geojson"
DISTRICTS_GEOJSON = DATA_DIR / "berlin_districts.geojson"
PRIORITY_GEOJSON = DATA_DIR / "berlin_priority_zones.geojson"

OUTPUT_FIGURE = FIGURES_DIR / "berlin_surface_temperature_map.png"
OVERLAY_FIGURE = FIGURES_DIR / "berlin_heat_green_overlay.png"
BOXPLOT_FIGURE = FIGURES_DIR / "temperature_green_vs_non_green_boxplot.png"
DISTRICT_BAR_FIGURE = FIGURES_DIR / "district_mean_temperature_bar.png"
PRIORITY_MAP_FIGURE = FIGURES_DIR / "cooling_priority_map.png"

DISTRICT_SUMMARY_CSV = DATA_DIR / "district_temperature_summary.csv"
TOP_PRIORITY_CSV = DATA_DIR / "top_cooling_priority_zones.csv"


# =========================
# Utility
# =========================

def ensure_directories():
    DATA_DIR.mkdir(exist_ok=True)
    FIGURES_DIR.mkdir(exist_ok=True)


# =========================
# Temperature data
# =========================

def download_temperature_layer():
    if OUTPUT_GEOJSON.exists():
        print(f"Temperature file already exists: {OUTPUT_GEOJSON}")
        return

    print("Connecting to Berlin WFS service...")
    wfs = WebFeatureService(url=WFS_URL, version="2.0.0")
    print("Connected.")

    print(f"Downloading layer: {LAYER_NAME}")
    response = wfs.getfeature(
        typename=[LAYER_NAME],
        outputFormat="application/json"
    )

    with open(OUTPUT_GEOJSON, "wb") as f:
        f.write(response.read())

    print(f"Saved GeoJSON to: {OUTPUT_GEOJSON}")


def load_temperature_data():
    print("Loading temperature data...")
    gdf = gpd.read_file(OUTPUT_GEOJSON)

    print("\nDataset loaded successfully")
    print("Shape:", gdf.shape)
    print("CRS:", gdf.crs)
    print("\nColumns:")
    print(gdf.columns.tolist())

    print("\nSurface temperature summary (tsurf14h):")
    print(gdf["tsurf14h"].describe())

    return gdf


def plot_temperature_map(gdf):
    print("\nCreating surface temperature heat map...")

    fig, ax = plt.subplots(figsize=(10, 10))

    gdf.plot(
        column="tsurf14h",
        cmap="hot",
        linewidth=0,
        legend=True,
        ax=ax
    )

    ax.set_title("Berlin Surface Temperature at 14:00 (2022)", fontsize=16)
    ax.set_axis_off()

    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURE, dpi=300, bbox_inches="tight")
    plt.show()

    print(f"Saved figure to: {OUTPUT_FIGURE}")


# =========================
# Green-space data
# =========================

def download_green_space_data(target_crs):
    if GREEN_GEOJSON.exists():
        print(f"Green-space file already exists: {GREEN_GEOJSON}")
        return

    print("\nDownloading Berlin green-space data from OpenStreetMap...")

    place = "Berlin, Germany"
    tags = {
        "leisure": ["park", "garden"],
        "landuse": ["forest", "grass", "recreation_ground", "allotments"],
        "natural": ["wood", "grassland", "heath", "scrub"]
    }

    green = ox.features_from_place(place, tags=tags)

    print("Raw green-space shape:", green.shape)
    print("\nGreen-space geometry types:")
    print(green.geometry.geom_type.value_counts())

    green = green.reset_index(drop=True)
    green = green[green.geometry.notnull()].copy()
    green = green[green.geometry.geom_type.isin(["Polygon", "MultiPolygon"])].copy()

    green = green.to_crs(target_crs)
    green = green[["geometry"]].copy()
    green["green_id"] = range(len(green))

    green.to_file(GREEN_GEOJSON, driver="GeoJSON")
    print(f"Saved green-space data to: {GREEN_GEOJSON}")


def load_green_space_data(target_crs):
    print("\nLoading green-space data...")
    green = gpd.read_file(GREEN_GEOJSON)

    if green.crs != target_crs:
        green = green.to_crs(target_crs)

    print("Green-space shape:", green.shape)
    print("Green-space CRS:", green.crs)

    return green


def plot_heat_green_overlay(temp_gdf, green_gdf):
    print("\nCreating overlay map...")

    fig, ax = plt.subplots(figsize=(10, 10))

    temp_gdf.plot(
        column="tsurf14h",
        cmap="hot",
        linewidth=0,
        legend=True,
        ax=ax,
        alpha=0.85
    )

    green_gdf.plot(
        ax=ax,
        color="green",
        alpha=0.35,
        edgecolor="none"
    )

    ax.set_title("Berlin Heat Map with Green Spaces Overlay", fontsize=16)
    ax.set_axis_off()

    plt.tight_layout()
    plt.savefig(OVERLAY_FIGURE, dpi=300, bbox_inches="tight")
    plt.show()

    print(f"Saved figure to: {OVERLAY_FIGURE}")


# =========================
# District data
# =========================

def download_berlin_districts(target_crs):
    if DISTRICTS_GEOJSON.exists():
        print(f"District file already exists: {DISTRICTS_GEOJSON}")
        return

    print("\nDownloading Berlin district boundaries...")

    district_names = [
        "Mitte",
        "Friedrichshain-Kreuzberg",
        "Pankow",
        "Charlottenburg-Wilmersdorf",
        "Spandau",
        "Steglitz-Zehlendorf",
        "Tempelhof-Schöneberg",
        "Neukölln",
        "Treptow-Köpenick",
        "Marzahn-Hellersdorf",
        "Lichtenberg",
        "Reinickendorf",
    ]

    district_frames = []

    for district in district_names:
        query = f"{district}, Berlin, Germany"
        print(f"  - {query}")
        district_gdf = ox.geocode_to_gdf(query)
        district_gdf = district_gdf[["geometry"]].copy()
        district_gdf["district"] = district
        district_frames.append(district_gdf)

    districts = gpd.GeoDataFrame(
        pd.concat(district_frames, ignore_index=True),
        crs="EPSG:4326"
    ).to_crs(target_crs)

    districts.to_file(DISTRICTS_GEOJSON, driver="GeoJSON")
    print(f"Saved district boundaries to: {DISTRICTS_GEOJSON}")


def load_berlin_districts(target_crs):
    print("\nLoading district boundaries...")
    districts = gpd.read_file(DISTRICTS_GEOJSON)

    if districts.crs != target_crs:
        districts = districts.to_crs(target_crs)

    print("Districts shape:", districts.shape)
    print("Districts CRS:", districts.crs)

    return districts


# =========================
# Analysis preparation
# =========================

def build_analysis_dataset(temp_gdf, green_gdf, districts_gdf):
    print("\nBuilding analysis dataset...")

    analysis_gdf = temp_gdf.copy()
    analysis_gdf["zone_id"] = range(1, len(analysis_gdf) + 1)

    temp_points = temp_gdf.copy()
    temp_points["geometry"] = temp_points.geometry.centroid

    # Green / non-green
    green_union = green_gdf.dissolve()
    green_join = gpd.sjoin(
        temp_points[["tsurf14h", "geometry"]],
        green_union[["geometry"]],
        how="left",
        predicate="within"
    ).sort_index()

    analysis_gdf["area_type"] = (
        green_join["index_right"]
        .notna()
        .map({True: "Green area", False: "Non-green area"})
        .reindex(analysis_gdf.index)
        .values
    )

    # District
    district_join = gpd.sjoin(
        temp_points[["tsurf14h", "geometry"]],
        districts_gdf[["district", "geometry"]],
        how="left",
        predicate="within"
    ).sort_index()

    analysis_gdf["district"] = district_join["district"].reindex(analysis_gdf.index).values

    print("Analysis dataset ready.")
    return analysis_gdf


# =========================
# Quantitative comparison
# =========================

def analyze_green_vs_non_green(analysis_gdf):
    print("\nAnalyzing temperature in green vs non-green areas...")

    summary = analysis_gdf.groupby("area_type")["tsurf14h"].agg(
        ["count", "mean", "median", "min", "max"]
    )
    print("\nTemperature summary by area type:")
    print(summary)

    return summary


def plot_green_vs_non_green_boxplot(analysis_gdf):
    print("\nCreating boxplot...")

    plot_df = analysis_gdf[["area_type", "tsurf14h"]].dropna().copy()

    green_values = plot_df.loc[plot_df["area_type"] == "Green area", "tsurf14h"]
    nongreen_values = plot_df.loc[plot_df["area_type"] == "Non-green area", "tsurf14h"]

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.boxplot([green_values, nongreen_values], tick_labels=["Green area", "Non-green area"])
    ax.set_title("Surface Temperature: Green vs Non-Green Areas", fontsize=14)
    ax.set_ylabel("Surface Temperature at 14:00")
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(BOXPLOT_FIGURE, dpi=300, bbox_inches="tight")
    plt.show()

    print(f"Saved figure to: {BOXPLOT_FIGURE}")


def analyze_temperature_by_district(analysis_gdf):
    print("\nAnalyzing temperature by district...")

    summary = (
        analysis_gdf.groupby("district")["tsurf14h"]
        .agg(["count", "mean", "median", "min", "max"])
        .sort_values("mean", ascending=False)
    )

    summary.to_csv(DISTRICT_SUMMARY_CSV)

    print("\nDistrict temperature summary:")
    print(summary)

    return summary


def plot_district_temperature_bar(summary):
    print("\nCreating district mean temperature bar chart...")

    fig, ax = plt.subplots(figsize=(10, 6))

    summary["mean"].sort_values().plot(kind="barh", ax=ax)

    ax.set_title("Mean Surface Temperature by Berlin District", fontsize=14)
    ax.set_xlabel("Mean Surface Temperature at 14:00")
    ax.set_ylabel("District")
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(DISTRICT_BAR_FIGURE, dpi=300, bbox_inches="tight")
    plt.show()

    print(f"Saved figure to: {DISTRICT_BAR_FIGURE}")


# =========================
# Priority zones
# =========================

def assign_priority_class(temp_value, q60, q75, q90, area_type):
    if area_type == "Green area":
        return "Low"

    if temp_value >= q90:
        return "Very High"
    if temp_value >= q75:
        return "High"
    if temp_value >= q60:
        return "Medium"
    return "Low"


def suggest_intervention(priority_class):
    if priority_class == "Very High":
        return "Street trees + shade structures + cool roofs"
    if priority_class == "High":
        return "Tree planting + shaded public space"
    if priority_class == "Medium":
        return "Pocket parks + permeable surfaces"
    return "Monitor / maintain existing cooling assets"


def create_priority_zones(analysis_gdf):
    print("\nCreating cooling priority zones...")

    q60 = analysis_gdf["tsurf14h"].quantile(0.60)
    q75 = analysis_gdf["tsurf14h"].quantile(0.75)
    q90 = analysis_gdf["tsurf14h"].quantile(0.90)

    priority_gdf = analysis_gdf.copy()

    priority_gdf["priority_class"] = priority_gdf.apply(
        lambda row: assign_priority_class(
            temp_value=row["tsurf14h"],
            q60=q60,
            q75=q75,
            q90=q90,
            area_type=row["area_type"]
        ),
        axis=1
    )

    priority_gdf["temp_percentile"] = priority_gdf["tsurf14h"].rank(pct=True) * 100
    priority_gdf["priority_score"] = priority_gdf["temp_percentile"]

    priority_gdf.loc[priority_gdf["area_type"] == "Green area", "priority_score"] *= 0.25

    priority_gdf["suggested_intervention"] = priority_gdf["priority_class"].map(suggest_intervention)

    export_cols = [
        "zone_id",
        "district",
        "tsurf14h",
        "area_type",
        "priority_class",
        "priority_score",
        "suggested_intervention",
        "geometry",
    ]
    priority_gdf[export_cols].to_file(PRIORITY_GEOJSON, driver="GeoJSON")

    print(f"Saved priority zones to: {PRIORITY_GEOJSON}")
    return priority_gdf


def export_top_priority_zones(priority_gdf, top_n=20):
    print("\nExporting top cooling priority zones...")

    top_priority = (
        priority_gdf[priority_gdf["priority_class"].isin(["Very High", "High"])]
        .sort_values(["priority_score", "tsurf14h"], ascending=False)
        .loc[:, ["zone_id", "district", "tsurf14h", "area_type", "priority_class", "suggested_intervention"]]
        .head(top_n)
        .copy()
    )

    top_priority["tsurf14h"] = top_priority["tsurf14h"].round(2)
    top_priority.to_csv(TOP_PRIORITY_CSV, index=False)

    print(f"Saved top priority zones to: {TOP_PRIORITY_CSV}")
    print("\nTop priority zones:")
    print(top_priority.head(10))

    return top_priority


def plot_priority_map(priority_gdf, green_gdf):
    print("\nCreating cooling priority map...")

    fig, ax = plt.subplots(figsize=(10, 10))

    green_gdf.plot(ax=ax, color="lightgreen", alpha=0.20, edgecolor="none")

    colors = {
        "Medium": "#fdd49e",
        "High": "#fc8d59",
        "Very High": "#d7301f",
    }

    for priority_class, color in colors.items():
        subset = priority_gdf[priority_gdf["priority_class"] == priority_class]
        if not subset.empty:
            subset.plot(
                ax=ax,
                color=color,
                edgecolor="none",
                alpha=0.85,
                label=priority_class
            )

    ax.set_title("Berlin Cooling Priority Map", fontsize=16)
    ax.set_axis_off()
    ax.legend(title="Priority")

    plt.tight_layout()
    plt.savefig(PRIORITY_MAP_FIGURE, dpi=300, bbox_inches="tight")
    plt.show()

    print(f"Saved figure to: {PRIORITY_MAP_FIGURE}")


# =========================
# Main
# =========================

def main():
    ensure_directories()

    download_temperature_layer()
    temp_gdf = load_temperature_data()
    plot_temperature_map(temp_gdf)

    download_green_space_data(temp_gdf.crs)
    green_gdf = load_green_space_data(temp_gdf.crs)
    plot_heat_green_overlay(temp_gdf, green_gdf)

    download_berlin_districts(temp_gdf.crs)
    districts_gdf = load_berlin_districts(temp_gdf.crs)

    analysis_gdf = build_analysis_dataset(temp_gdf, green_gdf, districts_gdf)

    green_summary = analyze_green_vs_non_green(analysis_gdf)
    plot_green_vs_non_green_boxplot(analysis_gdf)

    district_summary = analyze_temperature_by_district(analysis_gdf)
    plot_district_temperature_bar(district_summary)

    priority_gdf = create_priority_zones(analysis_gdf)
    top_priority = export_top_priority_zones(priority_gdf)
    plot_priority_map(priority_gdf, green_gdf)

    green_mean = green_summary.loc["Green area", "mean"]
    nongreen_mean = green_summary.loc["Non-green area", "mean"]
    cooling_difference = nongreen_mean - green_mean

    print("\nFinished.")
    print("\nKey result:")
    print(green_summary)
    print(f"\nAverage cooling association of green areas: {cooling_difference:.2f}°C")

    print("\nTop 5 districts by mean surface temperature:")
    print(district_summary.head(5))

    print("\nTop 10 cooling priority zones:")
    print(top_priority.head(10))


if __name__ == "__main__":
    main()