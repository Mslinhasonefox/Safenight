import streamlit as st
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
import streamlit.components.v1 as components

# --------------------------
# 页面设置 & 顶部样式
# --------------------------
st.set_page_config(layout="wide", page_title="Safenight 夜间道路安全地图")
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .title {
        font-size: 40px;
        font-weight: bold;
        color: white;
        padding: 20px;
        text-align: center;
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        border-radius: 5px;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<div class="title">Safenight: 夜间道路安全交互地图展示</div>', unsafe_allow_html=True)

# --------------------------
# 创建四个 Tab 页
# --------------------------
tab1, tab2, tab3, tab4 = st.tabs(["🟧 人口密度路段", "🟨 路灯分布图", "🟦 CCTV图层", "🟩 安全评分总图"])

# --------------------------
# Tab 1 - 人口密度路段
# --------------------------
with tab1:
    st.subheader("人口密度道路分布")
    with st.spinner("加载人口密度图层..."):
        roads = gpd.read_file("data/HKU_ROUTE_MEAN_PopDen.shp")
        m1 = folium.Map(location=[22.284, 114.137], zoom_start=15, tiles="cartodb dark_matter")
        for _, row in roads.iterrows():
            folium.GeoJson(
                row.geometry,
                style_function=lambda f: {"color": "orange", "weight": 3},
                tooltip=f"人口密度：{row['MEAN']}"
            ).add_to(m1)
        components.html(m1._repr_html_(), height=700, scrolling=False)

# --------------------------
# Tab 2 - 路灯图层
# --------------------------
with tab2:
    st.subheader("路灯类型与安全评分")
    with st.spinner("加载路灯数据..."):
        lamps = gpd.read_file("data/Lamppost_HKU.shp")
        m2 = folium.Map(location=[22.284, 114.137], zoom_start=15, tiles="cartodb dark_matter")
        cluster = MarkerCluster().add_to(m2)
        for _, row in lamps.iterrows():
            folium.Marker(
                location=[row.geometry.y, row.geometry.x],
                popup=f"类型：{row['Lamp_Type']}<br>得分：{row['Safety_Score']}",
                icon=folium.Icon(color='lightgray', icon='lightbulb', prefix='fa')
            ).add_to(cluster)
        components.html(m2._repr_html_(), height=700, scrolling=False)

# --------------------------
# Tab 3 - CCTV 图层
# --------------------------
with tab3:
    st.subheader("CCTV 监控分布")
    with st.spinner("加载 CCTV 图层..."):
        cctv = gpd.read_file("data/CCTV_all_fc.shp")
        m3 = folium.Map(location=[22.284, 114.137], zoom_start=15, tiles="cartodb dark_matter")
        for _, row in cctv.iterrows():
            folium.CircleMarker(
                location=[row.geometry.y, row.geometry.x],
                radius=3,
                color='cyan',
                fill=True,
                fill_opacity=0.6
            ).add_to(m3)
        components.html(m3._repr_html_(), height=700, scrolling=False)

# --------------------------
# Tab 4 - 安全评分总图
# --------------------------
with tab4:
    st.subheader("整合安全评分图层")
    with st.spinner("加载评分数据..."):
        scored = gpd.read_file("data/roads_scored_new.geojson")
        m4 = folium.Map(location=[22.284, 114.137], zoom_start=15, tiles="cartodb dark_matter")
        for _, row in scored.iterrows():
            popup_text = (
                f"<b>总安全分：</b>{row['total_safety_score']}<br>"
                f"<b>灯光得分：</b>{row['lamp_score']}<br>"
                f"<b>CCTV 得分：</b>{row['cctv_score']}<br>"
                f"<b>人口密度得分：</b>{row['pop_score']}"
            )
            folium.GeoJson(
                row.geometry,
                style_function=lambda f: {"color": "limegreen", "weight": 4, "opacity": 0.7},
                tooltip=popup_text
            ).add_to(m4)
        components.html(m4._repr_html_(), height=700, scrolling=False)