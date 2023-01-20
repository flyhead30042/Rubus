import os
import folium
import folium.plugins as plugins
import streamlit as st
from streamlit_folium import st_folium, folium_static
import rubus
from rubus import search_place
from geopandas import GeoDataFrame


st.set_page_config(page_title="Dual Map", page_icon="🎈", layout="wide", initial_sidebar_state="expanded")
st.write(
    """
    Dual Map  
    """
)

m = plugins.DualMap(location=[25.13891,121.58833],
           zoom_start=14, tiles=None)
r = rubus.load_config(os.path.join(rubus.CONFIGURATIONS_DIR, "resource.yaml"))
options = [tls["name"] for tls in r["TileLayers"] if not tls["overlay"]]

def get_tilelayer(name:str) -> folium.raster_layers.TileLayer:
    idx = options.index(name)
    tls = r["TileLayers"][idx]
    layer = folium.raster_layers.TileLayer(
        tiles=tls["tiles"],
        name=tls["name"],
        max_zoom=tls["max_zoom"],
        subdomains=tls["subdomains"],
        overlay=tls["overlay"],
        control=tls["control"],
        attr=tls["attr"],
    )
    return layer

def add_feature_to_tilelayer():
    plugins.Fullscreen(
        position='topleft',
        title='Expand me',
        title_cancel='Exit me',
        force_separate_button=True
    ).add_to(m.m1)
    plugins.Fullscreen(
        position='topleft',
        title='Expand me',
        title_cancel='Exit me',
        force_separate_button=True
    ).add_to(m.m2)

    plugins.MeasureControl(position='topleft',).add_to(m.m1)
    plugins.MeasureControl(position='topleft',).add_to(m.m2)

with st.container():
    c1, c2 = st.columns(2, gap="small")
    option_left = c1.selectbox("-- Left Map --", options=options, index=0)
    option_right = c2.selectbox("-- Right Map --", options=options, index=1)

    if option_left:
        get_tilelayer(option_left).add_to(m.m1)
    if option_right:
        get_tilelayer(option_right).add_to(m.m2)

    add_feature_to_tilelayer()

# Search place
with st.sidebar:
    q = st.text_input("Search Place ", key=search_place)
    if q:
        gdf:GeoDataFrame = search_place.nominatim(q)
        options = gdf["display_name"].to_list()
        options.insert(0, "----")
        place:str = st.sidebar.radio(
            "Select the place", options=options, index=0)

        if place and not place.startswith("----"):
            selected = gdf.loc[gdf["display_name"] == place].iloc[0]
            p = (selected.geometry.y,selected.geometry.x)
            m.m1.location = p
            folium.Marker( p, tooltip=selected["display_name"],
                       popup=f"<b>{selected.display_name}</b><br>" +
                             f"<li>座標:{selected.geometry.x, selected.geometry.y}</li>",
                       icon=folium.Icon(color="red", icon="info-sign")).add_to(m.m1)
            m.m2.location = p
            folium.Marker( p, tooltip=selected["display_name"],
                       popup=f"<b>{selected.display_name}</b><br>" +
                             f"<li>座標:{selected.geometry.x, selected.geometry.y}</li>",
                       icon=folium.Icon(color="red", icon="info-sign")).add_to(m.m2)


st_data = st_folium(m, width=1050, height=500)

