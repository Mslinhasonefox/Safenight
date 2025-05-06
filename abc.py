import streamlit as st
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
import streamlit.components.v1 as components

st.set_page_config(page_title="Safenight", layout="wide")
st.markdown(
    """
    <style>
        body {background:#222;}
        .title {font-family:monospace;font-size:60px;
                text-align:center;margin:20px 0 40px;color:#f0f0f0;}
        .card   {display:flex;align-items:center;justify-content:center;
                 border:2px solid #888;border-radius:15px;
                 height:160px;font-size:18px;font-weight:bold;
                 color:#f0f0f0;background:#333;cursor:pointer;
                 box-shadow:3px 3px 8px rgba(0,0,0,.6);}
        .card:hover {border-color:#f0f0f0;box-shadow:5px 5px 12px rgba(0,0,0,.8);}
    </style>
    """, unsafe_allow_html=True
)
st.markdown('<div class="title">Safenight</div>', unsafe_allow_html=True)

CENTER = [22.284, 114.137]
TILES  = "cartodb dark_matter"

def population_map():
    roads = gpd.read_file(
        "zip://safenight/HKU_ROUTE_MEAN_PopDen.zip!HKU_ROUTE_MEAN_PopDen.shp")
    m = folium.Map(location=CENTER, zoom_start=15, tiles=TILES)
    for _, r in roads.iterrows():
        folium.GeoJson(
            r.geometry,
            style_function=lambda f: {"color":"orange","weight":3},
            tooltip=f"Population density: {r['MEAN']}"
        ).add_to(m)
    return m

def lamp_map():
    lamps = gpd.read_file(
        "zip://safenight/Lamppost_HKU.zip!Lamppost_HKU.shp")
    m = folium.Map(location=CENTER, zoom_start=15, tiles=TILES)
    cluster = MarkerCluster().add_to(m)
    for _, r in lamps.iterrows():
        folium.Marker(
            [r.geometry.y, r.geometry.x],
            popup=f"Lamp type: {r['Lamp_Type']}<br>Score: {r['Safety_Score']}",
            icon=folium.Icon(color="white",icon="lightbulb",prefix="fa")
        ).add_to(cluster)
    return m

def cctv_map():
    cams = gpd.read_file(
        "zip://safenight/cctv.zip!CCTV_all_fc.shp")   # ← 若不对只改这里
    m = folium.Map(location=CENTER, zoom_start=15, tiles=TILES)
    for _, r in cams.iterrows():
        folium.CircleMarker(
            [r.geometry.y, r.geometry.x], radius=3,
            color="#00e5ff", fill=True, fill_opacity=.8
        ).add_to(m)
    return m

def score_map():
    scored = gpd.read_file("safenight/roads_scored_new.geojson")
    m = folium.Map(location=CENTER, zoom_start=15, tiles=TILES)
    for _, r in scored.iterrows():
        popup = (f"<b>Total:</b> {r['total_safety_score']}<br>"
                 f"<b>Lamp:</b> {r['lamp_score']}<br>"
                 f"<b>CCTV:</b> {r['cctv_score']}<br>"
                 f"<b>Pop:</b> {r['pop_score']}")
        folium.GeoJson(
            r.geometry,
            style_function=lambda f: {"color":"limegreen","weight":4,"opacity":.7},
            tooltip=popup
        ).add_to(m)
    return m

# ---- 四块矩阵按钮 ----
clicked = st.session_state.get("clicked", None)

cols = st.columns(2, gap="large")
labels = ["Population‑density roads", "Lamp posts",
          "CCTV layer", "Safety score map"]
keys   = ["pop","lamp","cctv","score"]

for i, label in enumerate(labels):
    col = cols[i%2]
    with col:
        if st.markdown(f'<div class="card">{label}</div>',
                       unsafe_allow_html=True) and st.button(" ", key=f"btn{i}"):
            clicked = keys[i]
            st.session_state["clicked"] = clicked

st.markdown("---")

# ---- 根据点击展示地图 ----
if clicked == "pop":
    components.html(population_map()._repr_html_(), height=700, scrolling=False)
elif clicked == "lamp":
    components.html(lamp_map()._repr_html_(), height=700, scrolling=False)
elif clicked == "cctv":
    components.html(cctv_map()._repr_html_(), height=700, scrolling=False)
elif clicked == "score":
    components.html(score_map()._repr_html_(), height=700, scrolling=False)
else:
    st.info("Click one matrix above to open its interactive map.")