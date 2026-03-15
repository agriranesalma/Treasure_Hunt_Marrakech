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
@keyframes gentleGlow {
    0% { text-shadow: 0 0 40px rgba(255,255,255,0.3), 0 0 70px rgba(227,30,36,0.2); }
    50% { text-shadow: 0 0 60px rgba(255,255,255,0.5), 0 0 90px rgba(0,100,0,0.3); }
    100% { text-shadow: 0 0 40px rgba(255,255,255,0.3), 0 0 70px rgba(227,30,36,0.2); }
}

.stApp {
    background: linear-gradient(rgba(0,0,0,0.82), rgba(0,0,0,0.82)),
                url('https://images.unsplash.com/photo-1531230689007-0b32d7a7c33e?q=80&w=2070&auto=format&fit=crop')
                no-repeat center center fixed;
    background-size: cover;
    color: white !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

.main .block-container {
    padding-top: 2rem !important;
    padding-left: 5% !important;
    padding-right: 5% !important;
}

.big-title {
    font-size: clamp(3.5rem, 15vw, 11rem);
    font-weight: 900;
    text-align: center;
    background: linear-gradient(to right,
        #e31e24 0%,
        #e31e24 40%,   
        #ffffff 48%,   
        #ffffff 52%,
        #006400 60%,   
        #006400 100%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 8px;
    margin: 0;
    padding: 0;
    line-height: 1;
    animation: gentleGlow 4s infinite ease-in-out;
}

.tag-subtitle {
    font-size: clamp(1.2rem, 3vw, 2.2rem);
    font-weight: 700;
    text-align: center;
    color: #ffffff;
    text-shadow: 0 0 20px rgba(0,0,0,0.9);
    margin: -10px 0 3rem 0;
    letter-spacing: 2px;
}

.section-header {
    text-align: center;
    margin-top: 1rem;
    width: 100%;
    font-weight: 600;
}

[data-testid="stImageCoordinates"] img,
img[src*="streamlit_image_coordinates"] {
    max-width: 100% !important;
    height: auto !important;
    display: block;
    margin: 0 auto;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}

.stButton > button {
    background-color: rgba(255, 255, 255, 0.05);
    color: white !important;
    border-radius: 12px;
    border: 2px solid #e31e24;
    font-size: 1.1rem;
    padding: 12px 15px;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background-color: #e31e24;
    color: white !important;
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(227,30,36,0.5);
}

h1, h2, h3, p, span, label, .stMarkdown {
    color: white !important;
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

if st.session_state.page == "home":
    st.markdown('<h1 class="big-title">Trésor Marocain</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">Explore Morocco Culturally • اكتشف المغرب</div>', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">🗺️ Click on a region / اضغط على جهة</h3>', unsafe_allow_html=True)

    try:
        image = Image.open("morocco_regions_map.png")
        target_w = 650
        w, h = image.size
        ratio = target_w / float(w)
        new_h = int(h * ratio)
        image = image.resize((target_w, new_h), Image.Resampling.LANCZOS)
    except:
        image = None

    if image is not None:
        map_col, legend_col = st.columns([1.5, 1])

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
                dot_col, btn_col = st.columns([0.1, 0.9])
                with dot_col:
                    st.markdown(f'<div style="background:{color}; width:16px; height:16px; border-radius:50%; margin-top:14px;"></div>', unsafe_allow_html=True)
                with btn_col:
                    if st.button(name, key=f"btn_{num}", use_container_width=True):
                        if name == "Marrakech-Safi":
                            st.session_state.page = "marrakech_safi"
                            st.rerun()

elif st.session_state.page == "marrakech_safi":
    st.markdown('<h1 class="big-title">Marrakech</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">📍 مراكش آسفي</div>', unsafe_allow_html=True)

    try:
        image = Image.open("marrakech_safi.png")
        target_w = 500
        w, h = image.size
        ratio = target_w / float(w)
        new_h = int(h * ratio)
        image = image.resize((target_w, new_h), Image.Resampling.LANCZOS)
    except:
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
                st.image(image, use_container_width=True)

    if st.button("⬅ Back to Regions Map"):
        st.session_state.page = "home"
        st.rerun()

else:
    st.markdown('<h1 class="big-title">Adventure</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">🕌 مغامرة مراكش</div>', unsafe_allow_html=True)
    if st.button("⬅ Back"):
        st.session_state.page = "marrakech_safi"
        st.rerun()
    st.progress(len(st.session_state.unlocked_stops) / 7)
    m = folium.Map(location=[31.63, -7.99], zoom_start=12)
    st_folium(m, width=1200, height=500)
