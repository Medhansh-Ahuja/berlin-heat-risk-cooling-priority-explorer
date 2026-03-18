from pathlib import Path
from html import escape
import json
import urllib.request

import folium
import geopandas as gpd
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium


# =========================
# Page setup
# =========================

st.set_page_config(
    page_title="Berlin Heat Risk & Cooling Priority Explorer",
    page_icon="🌡️",
    layout="wide"
)

CUSTOM_CSS = """
<style>
.stApp {
    background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.hero-card {
    background: linear-gradient(135deg, #111827 0%, #1f2937 45%, #7c2d12 100%);
    color: white;
    padding: 1.6rem 1.8rem;
    border-radius: 24px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.14);
    margin-bottom: 1rem;
}

.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 0.4rem;
}

.hero-subtitle {
    font-size: 1.05rem;
    opacity: 0.92;
    line-height: 1.5;
}

.pill-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 1rem;
}

.pill {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.18);
    padding: 0.45rem 0.8rem;
    border-radius: 999px;
    font-size: 0.9rem;
}

.metric-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 1rem 1rem 0.8rem 1rem;
    box-shadow: 0 8px 18px rgba(15,23,42,0.05);
    min-height: 110px;
}

.metric-label {
    color: #6b7280;
    font-size: 0.9rem;
    margin-bottom: 0.35rem;
}

.metric-value {
    color: #111827;
    font-size: 2rem;
    font-weight: 800;
    line-height: 1.1;
}

.metric-sub {
    color: #9ca3af;
    font-size: 0.84rem;
    margin-top: 0.3rem;
}

.insight-box {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 1rem;
    box-shadow: 0 8px 18px rgba(15,23,42,0.04);
    margin-bottom: 0.8rem;
}

.insight-title {
    font-size: 1rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 0.35rem;
}

.insight-text {
    color: #4b5563;
    font-size: 0.95rem;
    line-height: 1.5;
}

.legend-row {
    display: flex;
    align-items: center;
    margin-bottom: 0.35rem;
}

.legend-color {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    display: inline-block;
    margin-right: 8px;
    border: 1px solid #d1d5db;
}

.filter-banner {
    background: linear-gradient(90deg, #fff7ed 0%, #ffedd5 100%);
    border: 1px solid #fdba74;
    border-radius: 18px;
    padding: 0.9rem 1rem;
    margin-bottom: 1rem;
    color: #9a3412;
    font-weight: 600;
}

.recommend-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #e5e7eb;
    border-left: 6px solid #f97316;
    border-radius: 18px;
    padding: 1rem;
    box-shadow: 0 8px 18px rgba(15,23,42,0.04);
}

.subsection-title {
    font-size: 1.2rem;
    font-weight: 800;
    color: #111827;
    margin-bottom: 0.6rem;
}

.weather-shell {
    background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 55%, #38bdf8 100%);
    padding: 1.2rem;
    border-radius: 22px;
    box-shadow: 0 18px 35px rgba(29,78,216,0.22);
    margin-bottom: 1rem;
    color: white;
    overflow: hidden;
}

.weather-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 1rem;
}

.weather-title {
    color: white;
    font-size: 1rem;
    font-weight: 700;
    line-height: 1.2;
}

.weather-caption {
    color: rgba(255,255,255,0.78);
    font-size: 0.85rem;
    margin-top: 0.2rem;
}

.weather-updated {
    color: rgba(255,255,255,0.82);
    font-size: 0.8rem;
    text-align: right;
    white-space: nowrap;
}

.weather-body {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 1rem;
}

.weather-left {
    flex: 0 0 auto;
}

.weather-icon {
    font-size: 4rem;
    line-height: 1;
}

.weather-right {
    flex: 1;
    min-width: 0;
}

.weather-main {
    color: white;
    font-size: 3rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.25rem;
}

.weather-desc {
    color: rgba(255,255,255,0.92);
    font-size: 1rem;
}

.weather-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
}

.weather-stat {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 16px;
    padding: 0.85rem 0.95rem;
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
}

.weather-stat-label {
    color: rgba(255,255,255,0.8);
    font-size: 0.82rem;
    margin-bottom: 0.25rem;
}

.weather-stat-value {
    color: white;
    font-size: 1.8rem;
    font-weight: 700;
    line-height: 1.1;
    word-break: break-word;
}

[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.88);
    border-right: 1px solid #e5e7eb;
}

@media (max-width: 900px) {
    .weather-header {
        flex-direction: column;
        align-items: flex-start;
    }

    .weather-updated {
        text-align: left;
        white-space: normal;
    }

    .weather-body {
        flex-direction: column;
        align-items: flex-start;
    }

    .weather-grid {
        grid-template-columns: 1fr;
    }

    .weather-main {
        font-size: 2.5rem;
    }
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =========================
# Helpers
# =========================

def html_block(html: str) -> None:
    st.markdown(html.strip(), unsafe_allow_html=True)


# =========================
# File paths
# =========================

DATA_DIR = Path("data")
FIGURES_DIR = Path("figures")

PRIORITY_GEOJSON = DATA_DIR / "berlin_priority_zones.geojson"
GREEN_GEOJSON = DATA_DIR / "berlin_green_areas.geojson"
DISTRICT_SUMMARY_CSV = DATA_DIR / "district_temperature_summary.csv"
TOP_PRIORITY_CSV = DATA_DIR / "top_cooling_priority_zones.csv"

HEATMAP_FIGURE = FIGURES_DIR / "berlin_surface_temperature_map.png"
OVERLAY_FIGURE = FIGURES_DIR / "berlin_heat_green_overlay.png"
BOXPLOT_FIGURE = FIGURES_DIR / "temperature_green_vs_non_green_boxplot.png"
DISTRICT_BAR_FIGURE = FIGURES_DIR / "district_mean_temperature_bar.png"
PRIORITY_MAP_FIGURE = FIGURES_DIR / "cooling_priority_map.png"


# =========================
# Berlin weather config
# =========================

BERLIN_LAT = 52.52
BERLIN_LON = 13.405


# =========================
# Data loaders
# =========================

@st.cache_data
def load_priority_data():
    gdf = gpd.read_file(PRIORITY_GEOJSON)
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
    gdf = gdf.copy()
    gdf["tsurf14h"] = pd.to_numeric(gdf["tsurf14h"], errors="coerce")
    gdf["priority_score"] = pd.to_numeric(gdf["priority_score"], errors="coerce")
    gdf["geometry"] = gdf.geometry.simplify(0.00005, preserve_topology=True)
    return gdf


@st.cache_data
def load_green_data():
    gdf = gpd.read_file(GREEN_GEOJSON)
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
    gdf = gdf.copy()
    gdf["geometry"] = gdf.geometry.simplify(0.00005, preserve_topology=True)
    return gdf


@st.cache_data
def load_district_summary():
    df = pd.read_csv(DISTRICT_SUMMARY_CSV)
    return df.sort_values("mean", ascending=False).reset_index(drop=True)


@st.cache_data
def load_top_priority():
    return pd.read_csv(TOP_PRIORITY_CSV)


@st.cache_data(ttl=900)
def load_live_weather():
    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={BERLIN_LAT}"
        f"&longitude={BERLIN_LON}"
        "&current=temperature_2m,apparent_temperature,relative_humidity_2m,"
        "wind_speed_10m,weather_code,precipitation,is_day"
        "&timezone=auto"
    )
    try:
        with urllib.request.urlopen(weather_url, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data.get("current", {})
    except Exception:
        return {}


def weather_code_label(code: int) -> str:
    mapping = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with hail",
    }
    return mapping.get(code, "Unknown")


def weather_code_icon(code, is_day) -> str:
    if code is None:
        return "🌤️"
    code = int(code)
    if code == 0:
        return "☀️" if is_day == 1 else "🌙"
    if code in [1, 2]:
        return "🌤️" if is_day == 1 else "☁️"
    if code == 3:
        return "☁️"
    if code in [45, 48]:
        return "🌫️"
    if code in [51, 53, 55, 56, 57]:
        return "🌦️"
    if code in [61, 63, 65, 66, 67, 80, 81, 82]:
        return "🌧️"
    if code in [71, 73, 75, 77, 85, 86]:
        return "❄️"
    if code in [95, 96, 99]:
        return "⛈️"
    return "🌡️"


def safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


# =========================
# Load project data
# =========================

priority_gdf = load_priority_data()
green_gdf = load_green_data()
district_df = load_district_summary()
top_priority_df = load_top_priority()
current_weather = load_live_weather()


# =========================
# Sidebar
# =========================

st.sidebar.title("Controls")

district_options = ["All"] + sorted(
    [d for d in priority_gdf["district"].dropna().unique().tolist()]
)
selected_district = st.sidebar.selectbox("District", district_options)

priority_options = ["All", "Very High", "High", "Medium", "Low"]
selected_priority = st.sidebar.selectbox("Priority class", priority_options)

show_green = st.sidebar.checkbox("Show green spaces", value=True)

if st.sidebar.button("Refresh live weather"):
    load_live_weather.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Tip: use filters to focus the map and shortlist intervention zones.")


# =========================
# Filtering
# =========================

filtered_gdf = priority_gdf.copy()

if selected_district != "All":
    filtered_gdf = filtered_gdf[filtered_gdf["district"] == selected_district]

if selected_priority != "All":
    filtered_gdf = filtered_gdf[filtered_gdf["priority_class"] == selected_priority]


# =========================
# KPIs
# =========================

avg_temp = filtered_gdf["tsurf14h"].mean()
very_high_count = (filtered_gdf["priority_class"] == "Very High").sum()
high_count = (filtered_gdf["priority_class"] == "High").sum()

green_mean = priority_gdf.loc[
    priority_gdf["area_type"] == "Green area", "tsurf14h"
].mean()
nongreen_mean = priority_gdf.loc[
    priority_gdf["area_type"] == "Non-green area", "tsurf14h"
].mean()
cooling_difference = nongreen_mean - green_mean

hottest_district = district_df.iloc[0]["district"]
hottest_mean = district_df.iloc[0]["mean"]
coolest_district = district_df.iloc[-1]["district"]
coolest_mean = district_df.iloc[-1]["mean"]


# =========================
# Hero
# =========================

hero_html = (
    '<div class="hero-card">'
    '<div class="hero-title">🌡️ Berlin Heat Risk & Cooling Priority Explorer</div>'
    '<div class="hero-subtitle">'
    'A portfolio-grade urban climate dashboard combining official Berlin surface-temperature data, '
    'green-space overlays, hotspot prioritization, and live weather context.'
    '</div>'
    '<div class="pill-row">'
    '<div class="pill">Official Berlin climate data</div>'
    '<div class="pill">Geospatial analytics</div>'
    '<div class="pill">Cooling priority zoning</div>'
    '<div class="pill">Interactive decision-support app</div>'
    '</div>'
    '</div>'
)
html_block(hero_html)


# =========================
# Top metrics
# =========================

m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    html_block(
        f'<div class="metric-card">'
        f'<div class="metric-label">Filtered zones</div>'
        f'<div class="metric-value">{len(filtered_gdf):,}</div>'
        f'<div class="metric-sub">Current selection</div>'
        f'</div>'
    )

with m2:
    val = "N/A" if pd.isna(avg_temp) else f"{avg_temp:.2f}°C"
    html_block(
        f'<div class="metric-card">'
        f'<div class="metric-label">Avg. surface temp</div>'
        f'<div class="metric-value">{val}</div>'
        f'<div class="metric-sub">Filtered zones</div>'
        f'</div>'
    )

with m3:
    html_block(
        f'<div class="metric-card">'
        f'<div class="metric-label">Very High priority</div>'
        f'<div class="metric-value">{very_high_count:,}</div>'
        f'<div class="metric-sub">Critical zones</div>'
        f'</div>'
    )

with m4:
    html_block(
        f'<div class="metric-card">'
        f'<div class="metric-label">High priority</div>'
        f'<div class="metric-value">{high_count:,}</div>'
        f'<div class="metric-sub">Intervention candidates</div>'
        f'</div>'
    )

with m5:
    html_block(
        f'<div class="metric-card">'
        f'<div class="metric-label">Cooling association</div>'
        f'<div class="metric-value">{cooling_difference:.2f}°C</div>'
        f'<div class="metric-sub">Green vs non-green</div>'
        f'</div>'
    )

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)


# =========================
# Map helpers
# =========================

def priority_color(priority_class):
    if priority_class == "Very High":
        return "#d7301f"
    if priority_class == "High":
        return "#fc8d59"
    if priority_class == "Medium":
        return "#fdd49e"
    return "#bdbdbd"


def build_map(priority_layer, green_layer=None):
    center = [52.52, 13.405]
    m = folium.Map(location=center, zoom_start=10, tiles="CartoDB positron")

    if green_layer is not None:
        folium.GeoJson(
            green_layer,
            name="Green spaces",
            style_function=lambda _: {
                "fillColor": "#31a354",
                "color": "#31a354",
                "weight": 0,
                "fillOpacity": 0.15,
            },
        ).add_to(m)

    folium.GeoJson(
        priority_layer,
        name="Priority zones",
        style_function=lambda feature: {
            "fillColor": priority_color(feature["properties"]["priority_class"]),
            "color": "black",
            "weight": 0.12,
            "fillOpacity": 0.78,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=[
                "zone_id",
                "district",
                "tsurf14h",
                "area_type",
                "priority_class",
                "suggested_intervention",
            ],
            aliases=[
                "Zone ID",
                "District",
                "Surface temp (°C)",
                "Area type",
                "Priority",
                "Suggested intervention",
            ],
            localize=True,
            sticky=False,
        ),
    ).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)
    return m


# =========================
# Tabs
# =========================

tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview", "Map Explorer", "Priority Tables", "Figures"]
)

with tab1:
    left, right = st.columns([1.1, 0.9])

    with left:
        html_block("<div class='subsection-title'>Project summary</div>")

        html_block(
            '<div class="insight-box">'
            '<div class="insight-title">Research question</div>'
            '<div class="insight-text">'
            'Where are Berlin’s urban heat hotspots, and which non-green hot zones should be prioritized for cooling interventions?'
            '</div>'
            '</div>'
        )

        html_block(
            '<div class="insight-box">'
            '<div class="insight-title">Data</div>'
            '<div class="insight-text">'
            '• Official Berlin Climate Analysis 2022 surface-temperature layer<br>'
            '• OpenStreetMap green-space polygons<br>'
            '• Berlin district boundaries'
            '</div>'
            '</div>'
        )

        html_block(
            '<div class="insight-box">'
            '<div class="insight-title">Method</div>'
            '<div class="insight-text">'
            'Descriptive geospatial analysis, overlay analysis, district aggregation, '
            'and hotspot prioritization for cooling interventions.'
            '</div>'
            '</div>'
        )

        html_block("<div class='subsection-title'>Key insights</div>")

        html_block(
            '<div class="insight-box">'
            '<div class="insight-title">What the analysis shows</div>'
            '<div class="insight-text">'
            f'• Green areas are about <b>{cooling_difference:.2f}°C cooler</b> on average.<br>'
            f'• The hottest district in this analysis is <b>{escape(str(hottest_district))}</b> ({hottest_mean:.2f}°C).<br>'
            f'• The coolest district is <b>{escape(str(coolest_district))}</b> ({coolest_mean:.2f}°C).<br>'
            '• Non-green hot zones are highlighted as cooling priorities for intervention planning.'
            '</div>'
            '</div>'
        )

        html_block("<div class='subsection-title'>Priority legend</div>")

        html_block(
            '<div class="insight-box">'
            '<div class="legend-row"><span class="legend-color" style="background:#d7301f;"></span>Very High priority</div>'
            '<div class="legend-row"><span class="legend-color" style="background:#fc8d59;"></span>High priority</div>'
            '<div class="legend-row"><span class="legend-color" style="background:#fdd49e;"></span>Medium priority</div>'
            '<div class="legend-row"><span class="legend-color" style="background:#31a354;"></span>Green space overlay</div>'
            '</div>'
        )

    with right:
        html_block("<div class='subsection-title'>Live Berlin weather</div>")

        weather_temp = safe_float(current_weather.get("temperature_2m"))
        apparent_temp = safe_float(current_weather.get("apparent_temperature"))
        humidity = current_weather.get("relative_humidity_2m", "N/A")
        wind = current_weather.get("wind_speed_10m", "N/A")
        precip = current_weather.get("precipitation", "N/A")
        weather_code = current_weather.get("weather_code")
        is_day = current_weather.get("is_day")
        weather_desc = weather_code_label(int(weather_code)) if weather_code is not None else "Unknown"
        weather_icon = weather_code_icon(weather_code, is_day)
        weather_time = current_weather.get("time", "N/A")

        weather_html = (
            '<div class="weather-shell">'
            '<div class="weather-header">'
            '<div>'
            '<div class="weather-title">Berlin • Live context</div>'
            '<div class="weather-caption">Current weather conditions</div>'
            '</div>'
            f'<div class="weather-updated">Updated: {escape(str(weather_time))}</div>'
            '</div>'
            '<div class="weather-body">'
            '<div class="weather-left">'
            f'<div class="weather-icon">{escape(str(weather_icon))}</div>'
            '</div>'
            '<div class="weather-right">'
            f'<div class="weather-main">{weather_temp:.1f}°C</div>'
            f'<div class="weather-desc">{escape(str(weather_desc))}</div>'
            '</div>'
            '</div>'
            '<div class="weather-grid">'
            '<div class="weather-stat">'
            '<div class="weather-stat-label">Feels like</div>'
            f'<div class="weather-stat-value">{apparent_temp:.1f}°C</div>'
            '</div>'
            '<div class="weather-stat">'
            '<div class="weather-stat-label">Wind</div>'
            f'<div class="weather-stat-value">{escape(str(wind))} km/h</div>'
            '</div>'
            '<div class="weather-stat">'
            '<div class="weather-stat-label">Humidity</div>'
            f'<div class="weather-stat-value">{escape(str(humidity))}%</div>'
            '</div>'
            '<div class="weather-stat">'
            '<div class="weather-stat-label">Precipitation</div>'
            f'<div class="weather-stat-value">{escape(str(precip))} mm</div>'
            '</div>'
            '</div>'
            '</div>'
        )
        html_block(weather_html)

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        html_block("<div class='subsection-title'>Downloads</div>")
        d1, d2 = st.columns(2)
        with d1:
            st.download_button(
                label="District summary CSV",
                data=DISTRICT_SUMMARY_CSV.read_bytes(),
                file_name="district_temperature_summary.csv",
                mime="text/csv"
            )
        with d2:
            st.download_button(
                label="Priority zones CSV",
                data=TOP_PRIORITY_CSV.read_bytes(),
                file_name="top_cooling_priority_zones.csv",
                mime="text/csv"
            )

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        recommendation_text = "Tree planting + shaded public space"
        if selected_priority == "Very High":
            recommendation_text = "Street trees + shade structures + cool roofs"
        elif selected_priority == "High":
            recommendation_text = "Tree planting + shaded public space"
        elif selected_priority == "Medium":
            recommendation_text = "Pocket parks + permeable surfaces"

        html_block("<div class='subsection-title'>Recommended intervention focus</div>")

        html_block(
            '<div class="recommend-card">'
            f'<b>Suggested action:</b> {escape(recommendation_text)}<br><br>'
            '<span style="color:#6b7280; font-size:0.88rem;">'
            'This recommendation is based on the current priority filter and the hotspot ranking logic used in the project.'
            '</span>'
            '</div>'
        )

with tab2:
    banner_district = selected_district if selected_district != "All" else "all districts"
    banner_priority = selected_priority if selected_priority != "All" else "all priority classes"

    html_block(
        '<div class="filter-banner">'
        f'Showing <b>{escape(str(banner_priority))}</b> zones in '
        f'<b>{escape(str(banner_district))}</b> • {len(filtered_gdf):,} matching zones'
        '</div>'
    )

    if filtered_gdf.empty:
        st.warning("No zones match the selected filters.")
    else:
        map_green = green_gdf if show_green else None
        folium_map = build_map(filtered_gdf, map_green)
        st_folium(folium_map, width=1200, height=650)

        c1, c2 = st.columns([1.15, 1])

        with c1:
            html_block("<div class='subsection-title'>Filtered summary</div>")
            summary_df = (
                filtered_gdf.groupby(["priority_class", "area_type"])["tsurf14h"]
                .agg(["count", "mean"])
                .reset_index()
            )
            st.dataframe(summary_df, use_container_width=True)

        with c2:
            html_block("<div class='subsection-title'>Top 5 filtered priority zones</div>")
            top_filtered = (
                filtered_gdf.sort_values(["priority_score", "tsurf14h"], ascending=False)
                .loc[:, ["zone_id", "district", "tsurf14h", "priority_class", "suggested_intervention"]]
                .head(5)
            )
            st.dataframe(top_filtered, use_container_width=True)

with tab3:
    html_block("<div class='subsection-title'>Top cooling priority zones</div>")

    display_df = top_priority_df.copy()
    if selected_district != "All":
        display_df = display_df[display_df["district"] == selected_district]
    if selected_priority != "All":
        display_df = display_df[display_df["priority_class"] == selected_priority]

    st.dataframe(display_df, use_container_width=True)

    html_block("<div class='subsection-title'>District temperature ranking</div>")
    district_display = district_df.copy()
    if selected_district != "All":
        district_display = district_display[district_display["district"] == selected_district]
    st.dataframe(district_display, use_container_width=True)

    hottest = district_df.head(5).copy()
    coolest = district_df.tail(5).sort_values("mean", ascending=True).copy()

    t1, t2 = st.columns(2)
    with t1:
        html_block("<div class='subsection-title'>Hottest districts</div>")
        st.table(hottest[["district", "mean", "median", "max"]])

    with t2:
        html_block("<div class='subsection-title'>Coolest districts</div>")
        st.table(coolest[["district", "mean", "median", "max"]])

with tab4:
    html_block("<div class='subsection-title'>Saved figures</div>")

    f1, f2 = st.columns(2)
    with f1:
        st.image(str(HEATMAP_FIGURE), caption="Berlin surface temperature map")
    with f2:
        st.image(str(OVERLAY_FIGURE), caption="Heat map with green-space overlay")

    f3, f4 = st.columns(2)
    with f3:
        st.image(str(BOXPLOT_FIGURE), caption="Green vs non-green comparison")
    with f4:
        st.image(str(DISTRICT_BAR_FIGURE), caption="District mean temperature ranking")

    st.image(str(PRIORITY_MAP_FIGURE), caption="Cooling priority map")

st.markdown("---")
st.markdown(
    """
    **Portfolio framing:** This project combines official climate data, geospatial analytics, live weather context, and an interactive decision-support interface to identify Berlin heat hotspots and prioritize urban cooling interventions.
    """
)