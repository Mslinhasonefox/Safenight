import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# 页面配置
st.set_page_config(page_title="Safenight - Population", layout="wide")

# 中心点与亮色底图
CENTER = [22.284, 114.137]
TILES  = "cartodb positron"

# 加载人口密度地图
def population_map():
    roads = gpd.read_file("zip://safenight/HKU_ROUTE_MEAN_PopDen.zip!HKU_ROUTE_MEAN_PopDen/HKU_ROUTE_MEAN_PopDen.shp")
    m = folium.Map(location=CENTER, zoom_start=15, tiles=TILES)
    for _, r in roads.iterrows():
        folium.GeoJson(
            r.geometry,
            style_function=lambda f: {"color": "darkred", "weight": 3},
            popup=folium.Popup(f"Population density: {r['MEAN']}", max_width=300)
        ).add_to(m)
    return m

# 页面标题
st.markdown(
    "<h1 style='text-align: center; color: black;'>Safenight - Population Density Map</h1>",
    unsafe_allow_html=True
)

# 地图展示
st_folium(population_map(), height=700)
