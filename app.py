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
    background: rgba(255, 255, 255, 0.68);
    z-index: -1;
    pointer-events: none;
}
.big-title {font-size: 3.2rem; font-weight: bold; color: #c8102e; text-align: center; text-shadow: 2px 2px 8px rgba(0,0,0,0.4);}
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
    transform: scale(1.03);
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

# ===================== REGIONS MAP (HOME) =====================
if st.session_state.page == "home":
    st.markdown('<h1 class="big-title">🇲🇦 كنز المغرب • Trésor Marocain</h1>', unsafe_allow_html=True)
    st.markdown("**Explore Morocco culturally • Découvrez le Maroc culturellement • اكتشف المغرب ثقافياً**")
    st.markdown("### 🗺️ Click on a region / اضغط على جهة")

    try:
        image = Image.open("morocco_regions_map.png")
        target_w = 500
        w, h = image.size
        ratio = target_w / float(w)
        new_h = int(h * ratio)
        image = image.resize((target_w, new_h), Image.Resampling.LANCZOS)
    except FileNotFoundError:
        st.error("File 'morocco_regions_map.png' not found in repo root.")
        st.info("Please commit and push the image file to GitHub.")
        image = None
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        image = None

    if image is not None:
        if streamlit_image_coordinates is not None:
            col1, col2, col3 = st.columns([1, 4, 1])
            with col2:
                click = streamlit_image_coordinates(image, key="morocco_region_map")
            
            if click is not None:
                x = click["x"]
                y = click["y"]
                width = image.width
                height = image.height
                rel_x = x / width
                rel_y = y / height
                st.caption(f"Debug: clicked at x={x:.0f}, y={y:.0f} → **{rel_x:.2f}% , {rel_y:.2f}%**")
                
                if 0.28 <= rel_x <= 0.52 and 0.42 <= rel_y <= 0.68:
                    st.session_state.page = "marrakech_safi"
                    st.rerun()
                else:
                    st.warning("Coming Soon / Bientôt disponible / قريباً")
        else:
            st.warning("Interactive map unavailable (package not installed).")
            st.image(image, use_container_width=True)  

    # ===================== PRETTY COLORED LEGEND + BUTTONS =====================
    st.markdown("### 📋 Tap a region below / اضغط على جهة أدناه")
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
        col_dot, col_btn = st.columns([1, 6])
        with col_dot:
            st.markdown(f'<div style="background:{color}; width:28px; height:28px; border-radius:50%;"></div>', unsafe_allow_html=True)
        with col_btn:
            if st.button(name, key=f"btn_{num}", use_container_width=True):
                if name == "Marrakech-Safi":
                    st.session_state.page = "marrakech_safi"
                    st.rerun()
                else:
                    st.warning("Coming Soon / Bientôt disponible / قريباً")

# ===================== MARRAKECH-SAFI PROVINCES =====================
elif st.session_state.page == "marrakech_safi":
    st.markdown('<h1 class="big-title">📍 Marrakech-Safi • مراكش آسفي</h1>', unsafe_allow_html=True)
    st.markdown("### 🗺️ Click on a province / اضغط على إقليم")

    try:
        image = Image.open("marrakech_safi.png")
        target_w = 500
        w, h = image.size
        ratio = target_w / float(w)
        new_h = int(h * ratio)
        image = image.resize((target_w, new_h), Image.Resampling.LANCZOS)
    except FileNotFoundError:
        st.error("File 'marrakech_safi.png' not found in repo root.")
        st.info("Please commit and push the image file to GitHub.")
        image = None
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        image = None

    if image is not None:
        if streamlit_image_coordinates is not None:
            col1, col2, col3 = st.columns([1, 4, 1])
            with col2:
                click = streamlit_image_coordinates(image, key="marrakech-safi")
            
            if click is not None:
                x = click["x"]
                y = click["y"]
                width = image.width
                height = image.height
                rel_x = x / width
                rel_y = y / height
                st.caption(f"Debug: clicked at x={x:.0f}, y={y:.0f} → **{rel_x:.2f}% , {rel_y:.2f}%**")
                
                if 0.25 <= rel_x <= 0.55 and 0.35 <= rel_y <= 0.65:
                    st.session_state.page = "marrakech"
                    st.rerun()
                else:
                    st.warning("Coming Soon / Bientôt disponible / قريباً")
        else:
            st.warning("Interactive map unavailable (package not installed).")
            st.image(image, use_container_width=True) 

    if st.button("⬅ Back to Regions Map / العودة إلى خريطة الجهات"):
        st.session_state.page = "home"
        st.rerun()

# ===================== MARRAKECH TREASURE HUNT =====================
else:
    st.markdown('<h1 class="big-title">🕌 مغامرة مراكش • Marrakech Treasure Hunt</h1>', unsafe_allow_html=True)
    st.caption("7 étapes • Suivez les indices sur le terrain")
    if st.button("⬅ Back to Marrakech-Safi Map / العودة إلى خريطة مراكش-آسفي"):
        st.session_state.page = "marrakech_safi"
        st.rerun()
    progress = (len(st.session_state.unlocked_stops) / 7) * 100
    st.progress(progress / 100)
    st.write(f"**Étape {st.session_state.current_stop}/7** | **نقاط : {st.session_state.score}**")
    m = folium.Map(location=[31.63, -7.99], zoom_start=12, tiles="CartoDB positron")
    stops_coords = {
        1: (31.6295, -7.9881, "🕌 Jamaâ el-Fnaâ"),
        2: (31.6203, -7.9896, "🪦 Tombeaux Saadiens"),
        3: (31.6289, -7.9894, "🕌 Mosquée Koutoubia"),
        4: (31.6265, -7.9818, "🏰 Palais Bahia"),
        5: (31.6375, -7.9767, "☕ Café Jardin Majorelle"),
        7: (32.299, -9.227, "🏺 Atelier Poterie Safi")
    }
    for stop_num in st.session_state.unlocked_stops:
        if stop_num != 6:
            lat, lon, name = stops_coords[stop_num]
            folium.Marker([lat, lon], popup=name, icon=folium.Icon(color="red", icon="star")).add_to(m)
    if st.session_state.current_stop != 6 and st.session_state.current_stop in stops_coords:
        lat, lon, _ = stops_coords[st.session_state.current_stop]
        folium.Marker([lat, lon], popup="🎯 Vous êtes ici !", icon=folium.Icon(color="green", icon="flag")).add_to(m)
    st_folium(m, width=700, height=400)
