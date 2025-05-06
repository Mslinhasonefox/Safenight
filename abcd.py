import streamlit as st
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# --- 页面与自定义 CSS -------------------------------------------------
st.set_page_config("Safenight", layout="wide")
st.markdown("""
<style>
body   {background:#1c2431;}
h1     {text-align:center;color:#f4f6fa;margin:20px 0 40px;font-size:56px;}
.stButton>button              {width:100%;height:150px;font-size:20px;
                               font-weight:600;border:none;border-radius:14px;box-shadow:3px 3px 8px #0004;}
#pop   {background:#3b82f6;color:#fff;}          /* 蓝 */
#lamp  {background:#eab308;color:#000;}          /* 琥珀 */
#cctv  {background:#22c55e;color:#fff;}          /* 绿 */
#score {background:#ef4444;color:#fff;}          /* 红 */
.stButton>button:hover         {filter:brightness(1.15);}
</style>
""", unsafe_allow_html=True)
st.markdown("<h1>Safenight</h1>", unsafe_allow_html=True)

CENTER=[22.284,114.137]; TILES="cartodbdark_matter"

# --- 四张地图函数 ------------------------------------------------------
def population_map():
    roads=gpd.read_file("zip://safenight/HKU_ROUTE_MEAN_PopDen.zip!HKU_ROUTE_MEAN_PopDen/HKU_ROUTE_MEAN_PopDen.shp")
    m=folium.Map(location=CENTER,zoom_start=15,tiles=TILES)
    for _,r in roads.iterrows():
        folium.GeoJson(r.geometry,
           style_function=lambda f:{"color":"orange","weight":3},
           tooltip=f"Population density: {r['MEAN']}").add_to(m)
    return m

def lamp_map():
    lamps=gpd.read_file("zip://safenight/Lamppost_HKU.zip!Lamppost_HKU/Lamppost_HKU.shp")
    m=folium.Map(location=CENTER,zoom_start=15,tiles=TILES)
    cluster=MarkerCluster().add_to(m)
    for _,r in lamps.iterrows():
        folium.Marker([r.geometry.y,r.geometry.x],
            popup=f"Lamp type: {r['Lamp_Type']}<br>Score: {r['Safety_Score']}",
            icon=folium.Icon(color="lightgray",icon="lightbulb",prefix="fa")).add_to(cluster)
    return m

def cctv_map():
    cams=gpd.read_file("zip://safenight/cctv.zip!CCTV_all_fc/CCTV_all_fc.shp")
    m=folium.Map(location=CENTER,zoom_start=15,tiles=TILES)
    for _,r in cams.iterrows():
        folium.CircleMarker([r.geometry.y,r.geometry.x],radius=3,
            color="#00e5ff",fill=True,fill_opacity=.8).add_to(m)
    return m

def score_map():
    gdf=gpd.read_file("safenight/roads_scored_new.geojson")
    m=folium.Map(location=CENTER,zoom_start=15,tiles=TILES)
    for _,r in gdf.iterrows():
        folium.GeoJson(r.geometry,
           style_function=lambda f:{"color":"#10b981","weight":4,"opacity":.7},
           tooltip=(f"<b>Total:</b> {r['total_safety_score']}<br>"
                    f"<b>Lamp:</b> {r['lamp_score']}<br>"
                    f"<b>CCTV:</b> {r['cctv_score']}<br>"
                    f"<b>Pop:</b> {r['pop_score']}")).add_to(m)
    return m

# --- 四个彩色按钮 ------------------------------------------------------
col1,col2=st.columns(2,gap="large")
if col1.button("Population‑density roads", key="pop"):   st_folium(population_map(),height=650)
if col2.button("Lamp posts",               key="lamp"):  st_folium(lamp_map(),       height=650)
if col1.button("CCTV layer",               key="cctv"):  st_folium(cctv_map(),       height=650)
if col2.button("Safety score map",         key="score"): st_folium(score_map(),      height=650)

if not any(st.session_state.get(k) for k in ("pop","lamp","cctv","score")):
    st.info("Click one of the four cards above to display its interactive map.")