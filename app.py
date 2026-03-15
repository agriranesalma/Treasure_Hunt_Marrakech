import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components

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
        st.markdown("### 🗺️ Carte des 12 régions / خريطة الـ12 جهة")
        
        st.write("Click on a region to start the adventure.")

        image = Image.open("morocco_regions_map.png")
        image= image.resize((600,400))
        click = streamlit_image_coordinates(image)

        if click is not None:

            x = click["x"]
            y = click["y"]

            # Marrakech coordinates
            if 205 <= x <= 234 and 119 <= y <= 141:
                st.session_state.page = "marrakech"
                st.rerun()

            else:
                st.warning("Coming Soon / Bientôt disponible / قريباً")


        regions = [
            ("Tanger-Tétouan-Al Hoceïma", "طنجة-تطوان-الحسيمة"),
            ("L'Oriental", "الشرق"),
            ("Fès-Meknès", "فاس-مكناس"),
            ("Rabat-Salé-Kénitra", "الرباط-سلا-القنيطرة"),
            ("Béni Mellal-Khénifra", "بني ملال-خنيفرة"),
            ("Casablanca-Settat", "الدار البيضاء-سطات"),
            ("**Marrakech-Safi**", "**مراكش-آسفي**"),
            ("Drâa-Tafilalet", "درعة-تافيلالت"),
            ("Souss-Massa", "سوس-ماسة"),
            ("Guelmim-Oued Noun", "كلميم-واد نون"),
            ("Laâyoune-Sakia El Hamra", "العيون-الساقية الحمراء"),
            ("Dakhla-Oued Ed-Dahab", "الداخلة-وادي الذهب"),
        ]

        cols = st.columns(4)
        for i, (fr, ar) in enumerate(regions):
            with cols[i % 4]:
                if "**Marrakech-Safi**" in fr:
                    if st.button(f"🕌 {fr}\n{ar}", key="marrakech_btn", use_container_width=True, type="primary"):
                        st.session_state.page = "marrakech"
                        st.rerun()
                else:
                    st.button(f"🔒 {fr}\n{ar}", disabled=True, use_container_width=True)

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

# MARRAKECH TREASURE HUNT 
else:
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
    clues = { ... } 

