import streamlit as st
from PIL import Image
import folium
from streamlit_folium import st_folium

try:
    from streamlit_image_coordinates import streamlit_image_coordinates
except ImportError:
    streamlit_image_coordinates = None

st.set_page_config(page_title="كنز المغرب • Trésor Marocain", layout="wide", page_icon="🕌")

st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1531230689007-0b32d7a7c33e?q=80&w=2070&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
.stApp::after {
    content: "";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(255, 255, 255, 0.88);
    z-index: -1;
    pointer-events: none;
}

html, body, [data-testid="stAppViewContainer"], .stApp, .block-container, .main {
    overflow-x: hidden !important;
    max-width: 100vw !important;
    padding-left: 5% !important;
    padding-right: 5% !important;
    margin: 0 !important;
}

div.row-widget.stHorizontal, .stColumns {
    margin: 0 !important;
    padding: 0 !important;
    gap: 2rem !important;
}

[data-testid="stImageCoordinates"] img,
img[src*="streamlit_image_coordinates"] {
    max-width: 100% !important;
    height: auto !important;
    display: block;
    margin: 0 auto;
    border-radius: 15px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.big-title {
    font-size: clamp(2rem, 8vw, 3.5rem);
    font-weight: bold;
    color: #c8102e;
    text-align: center;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    margin-bottom: 1rem;
}

.section-header {
    text-align: center;
    color: #1a1a1a;
    margin-top: 1rem;
    width: 100%;
}

.stButton > button {
    background-color: #f8f8f8;
    color: #1a1a1a;
    border-radius: 12px;
    border: 3px solid #c8102e;
    font-size: 1.05rem;
    padding: 12px 10px;
    box-shadow: 0 4px 8px rgba(200,16,46,0.15);
    transition: all 0.2s;
}
.stButton > button:hover {
    background-color: #ffebee;
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"
if "hunt_started" not in st.session_state:
    st.session_state.hunt_started = False
    st.session_state.current_stop = 1
    st.session_state.unlocked_stops = [1]
    st.session_state.score = 0
    st.session_state.vr_unlocked = False

if st.session_state.page == "home":
    st.markdown('<h1 class="big-title">🇲🇦 كنز المغرب • Trésor Marocain</h1>', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><b>Explore Morocco culturally • Découvrez le Maroc culturellement • اكتشف المغرب ثقافياً</b></div>', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">🗺️ Click on a region / اضغط على جهة</h3>', unsafe_allow_html=True)

    try:
        image = Image.open("morocco_regions_map.png")
        target_w = 600  
        w, h = image.size
        ratio = target_w / float(w)
        new_h = int(h * ratio)
        image = image.resize((target_w, new_h), Image.Resampling.LANCZOS)
    except FileNotFoundError:
        st.error("File 'morocco_regions_map.png' not found.")
        image = None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        image = None

    if image is not None:
        map_col, legend_col = st.columns([1.2, 1]) 

        with map_col:
            if streamlit_image_coordinates is not None:
                click = streamlit_image_coordinates(image, key="morocco_region_map")
                if click is not None:
                    rel_x = click["x"] / image.width
                    rel_y = click["y"] / image.height
                    if 0.28 <= rel_x <= 0.52 and 0.42 <= rel_y <= 0.68:
                        st.session_state.page = "marrakech_safi"
                        st.rerun()
                    else:
                        st.warning("Coming Soon / Bientôt disponible / قريباً")
            else:
                st.image(image, use_container_width=True)

        with legend_col:
            st.markdown('<h3 style="text-align:center;">📋 Regions / الجهات</h3>', unsafe_allow_html=True)
            regions = [
                ("01", "Tanger-Tétouan-Al Hoceïma", "#26C6C0"),
                ("02", "Oriental", "#FF9F00"),
                ("03", "Fès-Meknès", "#34C76F"),
                ("04", "Rabat-Salé-Kénitra", "#E03E3E"),
                ("05", "Béni Mellal-Khénifra", "#2C5F7A"),
                ("06", "Casablanca-Settat", "#7A8A9C"),
                ("07", "Marrakech-Safi", "#FF9F00"),
                ("08", "Drâa-Tafilalet", "#5EB8FF"),
                ("09", "Souss-Massa", "#00C9A0"),
                ("10", "Guelmim-Oued Noun", "#FFCB4E"),
                ("11", "Laâyoune-Sakia El Hamra", "#9B59B5"),
                ("12", "Eddakhla-Oued Ed-dahab", "#1E9BFF"),
            ]
            for num, name, color in regions:
                dot_col, btn_col = st.columns([0.15, 0.85])
                with dot_col:
                    st.markdown(f'<div style="background:{color}; width:20px; height:20px; border-radius:50%; margin-top:12px;"></div>', unsafe_allow_html=True)
                with btn_col:
                    if st.button(name, key=f"btn_{num}", use_container_width=True):
                        if name == "Marrakech-Safi":
                            st.session_state.page = "marrakech_safi"
                            st.rerun()
                        else:
                            st.warning("Coming Soon / Bientôt disponible / قريباً")

elif st.session_state.page == "marrakech_safi":
    st.markdown('<h1 class="big-title">📍 Marrakech-Safi • مراكش آسفي</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">🗺️ Click on a province / اضغط على إقليم</h3>', unsafe_allow_html=True)

    try:
        image = Image.open("marrakech_safi.png")
        target_w = 500
        w, h = image.size
        ratio = target_w / float(w)
        new_h = int(h * ratio)
        image = image.resize((target_w, new_h), Image.Resampling.LANCZOS)
    except Exception:
        image = None

    if image is not None:
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if streamlit_image_coordinates is not None:
                click = streamlit_image_coordinates(image, key="marrakech-safi")
                if click is not None:
                    rel_x = click["x"] / image.width
                    rel_y = click["y"] / image.height
                    if 0.25 <= rel_x <= 0.55 and 0.35 <= rel_y <= 0.65:
                        st.session_state.page = "marrakech"
                        st.rerun()
                    else:
                        st.warning("Coming Soon")
            else:
                st.image(image, use_container_width=True)

    if st.button("⬅ Back to Regions Map"):
        st.session_state.page = "home"
        st.rerun()

else:
    st.markdown('<h1 class="big-title">🕌 مغامرة مراكش • Marrakech Treasure Hunt</h1>', unsafe_allow_html=True)
    if st.button("⬅ Back to Map"):
        st.session_state.page = "marrakech_safi"
        st.rerun()
    progress = (len(st.session_state.unlocked_stops) / 7)
    st.progress(progress)
    st.write(f"**Étape {st.session_state.current_stop}/7** | **نقاط : {st.session_state.score}**")
    m = folium.Map(location=[31.63, -7.99], zoom_start=12, tiles="CartoDB positron")
    st_folium(m, width=1200, height=500)
