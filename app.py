import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components
try:
    from streamlit_image_coordinates import streamlit_image_coordinates
except ImportError:
    streamlit_image_coordinates = None
# ===================== CONFIG + BACKGROUND =====================
st.set_page_config(page_title="كنز المغرب • Trésor Marocain", layout="wide", page_icon="🕌")

st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1531230689007-0b32d7a7c33e?q=80&w=2070&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
.big-title {font-size: 3.2rem; font-weight: bold; color: #c8102e; text-align: center; text-shadow: 2px 2px 8px rgba(0,0,0,0.3);}
.clue-box {background: #f4f0e8; padding: 25px; border-radius: 15px; border: 4px solid #c8102e; margin: 15px 0;}
.success {color: #006400; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# ===================== SESSION STATE =====================
if "page" not in st.session_state:
    st.session_state.page = "home"
if "hunt_started" not in st.session_state:
    st.session_state.hunt_started = False
    st.session_state.current_stop = 1
    st.session_state.unlocked_stops = [1]
    st.session_state.score = 0
    st.session_state.vr_unlocked = False

# ===================== HOME PAGE - 2 COLUMNS =====================
if st.session_state.page == "home":

    st.markdown('<h1 class="big-title">🇲🇦 كنز المغرب • Trésor Marocain</h1>', unsafe_allow_html=True)
    st.markdown("**Explore Morocco culturally • Découvrez le Maroc culturellement • اكتشف المغرب ثقافياً**")

    col_map, col_about = st.columns([1.6, 1])

    with col_map:
        with col_map:
            st.markdown("### 🗺️ Click on a region / اضغط على جهة")

        try:
            image_path = "morocco_regions_map.png"
            image = Image.open(image_path)
            image = image.resize((700, 500)) 
        except FileNotFoundError:
            st.error("File 'morocco_regions_map.png' not found in repo root.")
            st.info("Please commit and push the image file to GitHub.")
            image = None
        except Exception as e:
            st.error(f"Error loading image: {str(e)}")
            image = None

        if image is not None:
            if streamlit_image_coordinates is not None:
                click = streamlit_image_coordinates(
                    image,
                    key="morocco_region_map"
                )

                if click is not None:
                    x = click["x"]
                    y = click["y"]
                    st.caption(f"Debug: clicked at x={x:.0f}, y={y:.0f}") 

                  
                    if 180 <= x <= 280 and 90 <= y <= 180:
                        st.session_state.page = "marrakech"
                        st.rerun()
                    else:
                        st.warning("Coming Soon / Bientôt disponible / قريباً")
            else:
                st.warning("Interactive map unavailable (package not installed). Use buttons below instead.")
                st.image(image, use_container_width=True)
    with col_about:
        st.markdown("### ℹ️ About the Adventure / عن المغامرة")
        st.write("""
        **Moroccan Cultural Treasure Hunt**  
        **Chasse au Trésor Culturel Marocaine**  
        **مغامرة البحث عن الكنز الثقافي المغربي**

        Follow clues across Marrakech-Safi, discover historical sites,  
        cultural stories, and partner cafés/shops.

        Solve puzzles → get secret codes → win prizes (including VR!).

        Hackathon prototype – only Marrakech-Safi is active.
        """)




st.markdown("### 🗺️ Click on a region / اضغط على جهة")

        try:
            image_path = "marrakech_safi.png"
            image = Image.open(image_path)
            image = image.resize((700, 500)) 
        except FileNotFoundError:
            st.error("File 'marrakech_safi.png' not found in repo root.")
            st.info("Please commit and push the image file to GitHub.")
            image = None
        except Exception as e:
            st.error(f"Error loading image: {str(e)}")
            image = None

        if image is not None:
            if streamlit_image_coordinates is not None:
                click = streamlit_image_coordinates(
                    image,
                    key="morocco_region_map"
                )

                if click is not None:
                    x = click["x"]
                    y = click["y"]
                    st.caption(f"Debug: clicked at x={x:.0f}, y={y:.0f}") 

                  
                    if 180 <= x <= 280 and 90 <= y <= 180:
                        st.session_state.page = "marrakech"
                        st.rerun()
                    else:
                        st.warning("Coming Soon / Bientôt disponible / قريباً")
            else:
                st.warning("Interactive map unavailable (package not installed). Use buttons below instead.")
                st.image(image, use_container_width=True)
# MARRAKECH TREASURE HUNT 
"""else:
    st.markdown('<h1 class="big-title">🕌 مغامرة مراكش-آسفي • Marrakech-Safi Treasure Hunt</h1>', unsafe_allow_html=True)
    st.caption("7 étapes • Suivez les indices sur le terrain")

    if st.button("⬅ Back to Map / العودة إلى الخريطة"):
        st.session_state.page = "home"
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

    # === CLUES & PUZZLES ( i will add this later, im tired and i will sleep)
    stop = st.session_state.current_stop
    clues = { ... } """

