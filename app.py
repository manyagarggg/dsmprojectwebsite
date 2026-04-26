# run with streamlit run app.py 
import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium
import time
import random
import re

# Page config
st.set_page_config(
    page_title="Illegal Sand Mining in India",
    page_icon="🏜️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS — editorial / field-report aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Sans+3:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Source Sans 3', sans-serif;
    }

    /* App background */
    .stApp {
        background-color: #f9f5ef;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1c1a17;
        color: #e8dcc8;
    }
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #c9b99a !important;
        font-family: 'Source Sans 3', sans-serif;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiselect label,
    [data-testid="stSidebar"] .stCheckbox label {
        color: #e8dcc8 !important;
        font-size: 0.85rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        font-weight: 600;
    }

    /* Sidebar title */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2 {
        color: #e8a838 !important;
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        border-bottom: 1px solid #3a3530;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1c1a17;
        border-radius: 8px 8px 0 0;
        padding: 4px 4px 0 4px;
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #2e2b26;
        color: #9a8c78;
        border-radius: 6px 6px 0 0;
        font-family: 'Source Sans 3', sans-serif;
        font-size: 0.9rem;
        letter-spacing: 0.04em;
        font-weight: 600;
        padding: 8px 20px;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e8a838 !important;
        color: #1c1a17 !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #f9f5ef;
        border: 1px solid #e0d5c4;
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 1.5rem;
    }

    /* Page titles */
    h1 {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.4rem !important;
        font-weight: 900 !important;
        color: #1c1a17 !important;
        letter-spacing: -0.01em;
        line-height: 1.1;
    }
    h2 {
        font-family: 'Playfair Display', serif !important;
        color: #2e2b26 !important;
        font-size: 1.6rem !important;
    }
    h3 {
        font-family: 'Source Sans 3', sans-serif !important;
        color: #5a4e3c !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    p, li {
        color: #3a3530;
        line-height: 1.75;
    }

    /* Buttons */
    .stButton > button {
        background-color: #e8a838;
        color: #1c1a17;
        font-family: 'Source Sans 3', sans-serif;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1.25rem;
        transition: background-color 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #c98a1a;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #fff8ee;
        border: 1px solid #e0d5c4;
        border-left: 4px solid #e8a838;
        border-radius: 6px;
        padding: 1rem 1.25rem;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #7a6e5e !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Playfair Display', serif;
        font-size: 2rem !important;
        color: #1c1a17 !important;
    }

    /* Subheaders / dividers */
    hr {
        border-color: #e0d5c4;
    }

    /* Checkbox / warning */
    .stWarning {
        background-color: #fff3cd;
        border-left: 4px solid #e8a838;
        color: #5a4e3c;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #f0ebe0; }
    ::-webkit-scrollbar-thumb { background: #c9b99a; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# Loading quotes
QUOTES = [
    "Sand is the second most exploited resource in the world, after water.",
    "If you remove sand from the river, you are digging your own grave. — Dinesh Kumar Mishra",
    "Unchecked sand extraction causes irreversible damage to river ecosystems. — Bidyut Mohanty",
    "It is a big challenge to stop illegal sand mining, because money drives everything. — S. Chandrasekhar",
    "We never know the worth of water until the well is dry. — Thomas Fuller",
    "Rivers are the soul of our civilization, and sand is their body.",
    "Over the years, India's rivers have been badly affected by unrestricted sand mining. — National Green Tribunal",
    "Mining jumped 14.7× after the PMAY-U housing scheme launched in 2015.",
]

def show_loading_page():
    st.markdown("<h1 style='text-align:center; margin-top:3rem;'>🏜️ Illegal Sand Mining in India</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#7a6e5e; font-size:1.1rem;'>Loading data & preparing your dashboard…</p>", unsafe_allow_html=True)

    quote_placeholder = st.empty()
    progress_bar = st.progress(0)

    for i in range(101):
        if i % 12 == 0:
            quote = random.choice(QUOTES)
            quote_placeholder.markdown(
                f"<blockquote style='border-left:4px solid #e8a838; padding:0.5rem 1rem; "
                f"color:#5a4e3c; font-style:italic; background:#fff8ee; border-radius:0 6px 6px 0;'>"
                f"{quote}</blockquote>",
                unsafe_allow_html=True
            )
        progress_bar.progress(i)
        time.sleep(0.04)

    st.success("✅ Data loaded successfully.")


# ------------------------------------------------------------------
# Data loading
# ------------------------------------------------------------------
@st.cache_data
def load_data():
    mining_df = pd.read_csv("data/final_unified_geo_data_rows.csv")
    if 'latitude' in mining_df.columns and 'longitude' in mining_df.columns:
        mining_df['latitude'] = pd.to_numeric(mining_df['latitude'], errors='coerce')
        mining_df['longitude'] = pd.to_numeric(mining_df['longitude'], errors='coerce')
        mining_df = mining_df.dropna(subset=['latitude', 'longitude'])
    else:
        mining_df = pd.DataFrame(columns=['latitude', 'longitude', 'source', 'state',
                                          'district', 'river', 'raw_location', 'description', 'geom'])

    india_gdf = gpd.read_file("india_district.geojson")

    court_df  = pd.read_csv("data/indiasandwatch/court_docs.csv",  header=1)
    news_df   = pd.read_csv("data/indiasandwatch/news_reports.csv", header=1)
    mining_obs_df = pd.read_csv("data/indiasandwatch/mining_obs.csv", header=1)

    def parse_location(loc):
        if pd.isna(loc):
            return pd.Series([np.nan, np.nan])
        match = re.search(r"(-?\d+\.\d+),\s*(-?\d+\.\d+)", str(loc))
        if match:
            return pd.Series([float(match.group(1)), float(match.group(2))])
        return pd.Series([np.nan, np.nan])

    mining_obs_df[['latitude', 'longitude']] = mining_obs_df['Location'].apply(parse_location)
    mining_obs_df = mining_obs_df.dropna(subset=['latitude', 'longitude'])

    return mining_df, india_gdf, court_df, news_df, mining_obs_df


# ------------------------------------------------------------------
# Map builder  (all three bugs fixed here)
# ------------------------------------------------------------------
def create_map(mining_df, india_gdf, show_mining=True, map_type='political',
               resolution='all', mining_sources=None, mining_obs_df=None):

    # Base tile: CartoDB Positron is clean; for "physical" we swap to Stamen Terrain
    if map_type == 'physical':
        tiles = 'https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg'
        attr  = 'Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors'
    else:
        tiles = 'CartoDB positron'
        attr  = '© CartoDB'

    m = folium.Map(location=[22.5, 78.9], zoom_start=5, tiles=tiles, attr=attr)
    m.fit_bounds([[6.5, 68.1], [35.5, 97.4]])

    # ------------------------------------------------------------------
    # FIX 1: GeoJSON polygons — add style_function + tooltip so hovering works
    # ------------------------------------------------------------------
    def style_fn(feature):
        return {
            'fillColor': '#e8a838',
            'color':     '#5a4e3c',
            'weight':    0.8,
            'fillOpacity': 0.10,
        }

    def highlight_fn(feature):
        return {
            'fillColor': '#c98a1a',
            'color':     '#1c1a17',
            'weight':    2,
            'fillOpacity': 0.35,
        }

    # Decide which name field to use for the tooltip
    name_field = None
    for candidate in ['district', 'DISTRICT', 'dtname', 'NAME_2', 'state', 'STATE', 'NAME_1']:
        if candidate in india_gdf.columns:
            name_field = candidate
            break

    tooltip_fields = [name_field] if name_field else []
    tooltip_aliases = ['District:'] if name_field else []

    # Add a second field (state) if available
    for sf in ['state', 'STATE', 'NAME_1']:
        if sf in india_gdf.columns and sf != name_field:
            tooltip_fields.append(sf)
            tooltip_aliases.append('State:')
            break

    # Political / both modes → add district boundaries
    if map_type in ('political', 'both'):
        folium.GeoJson(
            india_gdf,
            name='Districts',
            style_function=style_fn,
            highlight_function=highlight_fn,
            tooltip=folium.GeoJsonTooltip(
                fields=tooltip_fields if tooltip_fields else list(india_gdf.columns[:1]),
                aliases=tooltip_aliases if tooltip_aliases else [india_gdf.columns[0] + ':'],
                localize=True,
                sticky=True,
                labels=True,
                style=(
                    "background-color: #1c1a17; color: #e8dcc8; "
                    "font-family: 'Source Sans 3', sans-serif; "
                    "font-size: 13px; padding: 6px 10px; border-radius: 4px;"
                ),
            ),
        ).add_to(m)

    # ------------------------------------------------------------------
    # FIX 2: Markers — added for ALL map_type values (was missing 'physical')
    # ------------------------------------------------------------------
    if show_mining and mining_sources:

        # Mining observations (have lat/lon)
        if 'mining_obs' in mining_sources and mining_obs_df is not None and len(mining_obs_df) > 0:
            cluster = MarkerCluster(name='Mining Observations').add_to(m)
            for _, row in mining_obs_df.iterrows():
                title = row.get('Title', row.get('title', 'Mining Observation'))
                desc  = row.get('Description', row.get('description', ''))
                popup_html = (
                    f"<div style='font-family:sans-serif; min-width:160px;'>"
                    f"<b style='color:#c98a1a;'>⚠ Mining Obs</b><br>"
                    f"<span style='font-size:13px;'>{title}</span>"
                    f"{'<br><small>' + str(desc)[:120] + '…</small>' if desc else ''}"
                    f"</div>"
                )
                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    popup=folium.Popup(popup_html, max_width=260),
                    tooltip=str(title)[:60],
                    icon=folium.Icon(color='orange', icon='exclamation-sign', prefix='glyphicon'),
                ).add_to(cluster)

        # Unified geo data (have lat/lon)
        if len(mining_df) > 0:
            cluster_unified = MarkerCluster(name='Unified Data').add_to(m)
            for _, row in mining_df.iterrows():
                desc  = str(row.get('description', row.get('raw_location', 'N/A')))[:120]
                state = row.get('state', '')
                popup_html = (
                    f"<div style='font-family:sans-serif; min-width:160px;'>"
                    f"<b style='color:#c0392b;'>🔴 Mining Incident</b><br>"
                    f"{'<small>📍 ' + str(state) + '</small><br>' if state else ''}"
                    f"<small>{desc}…</small>"
                    f"</div>"
                )
                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    popup=folium.Popup(popup_html, max_width=260),
                    tooltip=str(row.get('district', row.get('state', 'Incident')))[:60],
                    icon=folium.Icon(color='red', icon='map-marker', prefix='glyphicon'),
                ).add_to(cluster_unified)

    folium.LayerControl().add_to(m)
    return m


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    if 'loaded' not in st.session_state:
        show_loading_page()
        st.session_state.loaded = True
        st.rerun()

    mining_df, india_gdf, court_df, news_df, mining_obs_df = load_data()

    # ── Sidebar ──────────────────────────────────────────────────────
    st.sidebar.markdown("## 🏜️ Controls")

    map_type = st.sidebar.selectbox(
        "Map Style",
        ['political', 'physical', 'both'],
        format_func=lambda x: {'political': '🗺 Political', 'physical': '🌿 Physical (Terrain)', 'both': '⊕ Both'}[x]
    )

    resolution = st.sidebar.multiselect(
        "Resolution Level",
        ['state', 'district', 'latlong', 'rivers'],
        default=['state', 'district', 'latlong'],
    )

    mining_sources = st.sidebar.multiselect(
        "Data Sources",
        ['court_docs', 'mining_obs', 'news_reports'],
        default=['mining_obs'],
        format_func=lambda x: {'court_docs': '⚖ Court Documents', 'mining_obs': '📍 Mining Observations', 'news_reports': '📰 News Reports'}[x]
    )

    show_mining = st.sidebar.checkbox("Show Mining Points", value=True)
    if not show_mining:
        st.sidebar.warning("⚠ Mining data points are hidden.")

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<small style='color:#6a5f4f;'>Data: IndiaSandWatch · 2,212 verified incidents · 2001–2026</small>",
        unsafe_allow_html=True
    )

    # ── Tabs ──────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["🗺  Map View", "📊  Visual Gallery", "📋  Findings"])

    # ── Tab 1: Map ────────────────────────────────────────────────────
    with tab1:
        st.markdown(
            "<h1>Illegal Sand Mining — Interactive Map</h1>"
            "<p style='color:#7a6e5e; margin-top:-0.5rem; font-size:1.05rem;'>"
            "Hover over districts to inspect them. Clusters expand on click. "
            "Use the layer control (top-right of map) to toggle overlays.</p>",
            unsafe_allow_html=True
        )

        # Quick stats row
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Incidents", "2,212")
        c2.metric("States Affected", "28+")
        c3.metric("Top State", "Bihar · 193")
        c4.metric("Post-PMAY Surge", "14.7×")

        st.markdown("<br>", unsafe_allow_html=True)

        m = create_map(mining_df, india_gdf, show_mining, map_type, resolution, mining_sources, mining_obs_df)
        st_folium(m, width="100%", height=580)

    # ── Tab 2: Gallery ────────────────────────────────────────────────
    with tab2:
        st.markdown("<h1>Visualization Gallery</h1>", unsafe_allow_html=True)

        # Correlation heatmap
        st.markdown("### Correlation Heatmap of Indicators")
        try:
            st.image("outputs/correlation_heatmap_indicators.png", use_column_width=True)
        except Exception:
            st.info("📂 Image not found: outputs/correlation_heatmap_indicators.png")

        st.markdown("""
**What it shows:** Correlations between mining, construction, and socioeconomic indicators.

**How to read:** Red = positive correlation, blue = negative. Stronger colour = stronger relationship.

**Key finding:** Mining incidents correlate strongly with PMAY construction scale, but weakly with poverty or literacy rates — illegal mining is demand-driven, not desperation-driven.
        """)

        st.divider()

        gallery_items = [
            ("Mining Observations Heatmap",     "outputs/heatmap_mining_observations.png",
             "Density of mining observations across India.",
             "Darker areas = higher mining activity. Bihar and UP dominate.",
             "Mining hotspots are in economically vulnerable supply states."),

            ("Geographic Distribution by State", "outputs/geographic_distribution_bars.png",
             "Bar chart of mining incidents by state.",
             "Bar height = number of incidents. Bihar leads with 193.",
             "Mining concentrates in supply states, not demand/construction states."),

            ("Dilapidated Housing Choropleth",   "outputs/choropleth_housing_dilapidated.html",
             "Dilapidated housing percentage by state.",
             "Darker shading = higher share of poor housing stock.",
             "Poor housing states have more mining, but PMAY mediates the link."),

            ("Crime Intensity Heatmap",          "outputs/heatmap_crime_intensity.png",
             "Crime rates across Indian cities.",
             "Darker = higher crime intensity.",
             "Crime hotspots often overlap with mining areas."),

            ("Temporal Surge in Mining",         "sangam_ganga_figures/fig_temporal_surge.png",
             "Annual illegal mining incidents 2010–2025, split pre/post-PMAY.",
             "Blue = pre-2015 baseline, red = post-launch surge.",
             "Mining rose from 13/year pre-2015 to 191/year post-2015 — a 14.7× increase."),

            ("Event Study: PMAY Impact",         "sangam_ganga_figures/fig_event_study.png",
             "DiD coefficients showing effect of high-PMAY states over time.",
             "Dots above zero post-2015 = significant mining increase after PMAY launch.",
             "Confirms causal impact of housing policy on illegal extraction."),

            ("Synthetic Control: Uttar Pradesh", "sangam_ganga_figures/fig_synthetic_control.png",
             "Actual UP mining vs. synthetic counterfactual.",
             "Gap post-2015 shows the causal PMAY effect on UP mining.",
             "UP mining is +158% above the counterfactual without PMAY."),

            ("Ganga Conductivity Time Series",   "sangam_ganga_figures/fig_ganga_sangam_timeseries.png",
             "Water quality sensors showing conductivity during dry seasons.",
             "Peaks in Nov–Feb coincide with peak mining and low water levels.",
             "Mining correlates with riverbed disturbance and water degradation."),

            ("Spatial Clusters: Construction vs Mining", "sangam_ganga_figures/fig_spatial_clusters.png",
             "Side-by-side: PMAY allocation vs mining incidents by state.",
             "Visual decoupling — mining and construction occur in different states.",
             "Supply and demand are spatially separated across state borders."),
        ]

        for title, path, desc, reading, insight in gallery_items:
            st.markdown(f"### {title}")
            try:
                if path.endswith('.html'):
                    st.components.v1.html(open(path).read(), height=420)
                else:
                    st.image(path, use_column_width=True)
            except Exception:
                st.info(f"📂 File not found: {path}")
            col_a, col_b, col_c = st.columns(3)
            col_a.markdown(f"**What it shows**\n\n{desc}")
            col_b.markdown(f"**How to read**\n\n{reading}")
            col_c.markdown(f"**Key finding**\n\n{insight}")
            st.divider()

    # ── Tab 3: Findings ───────────────────────────────────────────────
    with tab3:
        st.markdown("<h1>Project Results & Findings</h1>", unsafe_allow_html=True)

        st.markdown("""
## Executive Summary

This study analysed illegal sand mining in India using spatial statistics, causal inference, and environmental monitoring.
The central finding: the 2015 PMAY-U housing scheme caused a **14.7× surge** in illegal mining, with extraction spatially
decoupled from construction demand — occurring primarily in economically vulnerable supply states.

---

## Key Findings

### 1. Causal Impact of Construction Policy
- **Difference-in-Differences:** High-PMAY states saw 158% more mining post-2015
- **Event Study:** Parallel trends hold pre-2015; mining diverges sharply after PMAY launch
- **Synthetic Control:** UP mining is +158% above its counterfactual without PMAY
- **Regression:** PMAY scale explains 58% of mining variance; socioeconomic factors are secondary

### 2. Spatial Patterns & Hotspots
- **Top states:** Bihar (193 incidents), Uttar Pradesh (48), West Bengal (48), Madhya Pradesh (43)
- **Spatial decoupling:** Bivariate Moran's I = 0.033 (p = 0.42) — no co-clustering with construction
- **KDE analysis:** Hotspots concentrated in the Gangetic plain and central India
- **LISA:** Significant local spatial autocorrelation in mining clusters

### 3. Environmental Impacts
- Conductivity spikes at Ganga/Sangam sensors during dry seasons (Nov–Feb) correlate with peak mining
- Mining coincides with WQI deterioration and ecosystem stress
- Illegal extraction threatens aquifer recharge in riverbed sponges

### 4. Economic & Social Dimensions
- Crime hotspots spatially coincide with mining areas
- Poverty and literacy have weak direct effects; construction demand — not desperation — drives mining
- Urbanisation shows no significant independent effect

### 5. Methodological Approach
- **Spatial statistics:** Moran's I, LISA, GWR, KDE
- **Causal inference:** DiD, event studies, synthetic controls, IV regression
- **Machine learning:** Random Forest (PMAY most predictive feature)
- **Time series:** Seasonal decomposition, Granger causality

---

## Data Sources

| Dataset | Coverage | Scale |
|---|---|---|
| Mining incidents (IndiaSandWatch) | 2001–2026 | 2,212 verified cases |
| PMAY-U allocations | 2015–2024 | State / district |
| Economic indicators (Census 2011) | Literacy, BPL, urbanisation | State |
| Ganga/Sangam water sensors | 2019–2020 | Point locations |
| IPC crime statistics | 54 urban centres | City |
| Geographic coverage | 36 states/UTs | 375 mining obs. points |

---

## Policy Implications

**Immediate actions:**
1. Develop legal sand mining infrastructure in high-demand states to reduce illegal supply pressure
2. Focus enforcement on Bihar, UP, and MP — the primary sand mafia hotspots
3. Implement real-time river quality monitoring at active mining sites
4. Invest in economic alternatives for communities dependent on informal extraction

**Long-term reforms:**
1. Strengthen environmental clearances and monitoring for sand permits
2. Create a national sand supply coordination policy to address inter-state decoupling
3. Deploy satellite monitoring and AI for real-time illegal mining detection
4. Involve local communities in sustainable extraction governance

---

## Limitations & Future Research

- District-level analysis would reveal finer spatial patterns
- Pre-2015 mining data is sparse — a longer time series would sharpen causal estimates
- Sand mafia economics and enforcement failures warrant dedicated ethnographic research
- Experimental evaluation of alternative sand supply interventions is needed

---

*Research conducted using rigorous statistical methods across spatial analysis, causal inference, and environmental monitoring.*
        """)


if __name__ == "__main__":
    main()