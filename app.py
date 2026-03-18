import streamlit as st
from PIL import Image
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components

# ====================== YOUR ORIGINAL CONFIG & CSS ======================
st.set_page_config(page_title="Kenz Quest • مهمة الكنز", layout="wide", page_icon="🧞")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Kaushan+Script&display=swap');
@keyframes gentleGlow {0% {text-shadow: 0 0 50px rgba(255,255,255,0.2);} 50% {text-shadow: 0 0 100px rgba(255,255,255,0.5);} 100% {text-shadow: 0 0 50px rgba(255,255,255,0.2);}}
.stApp {background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url('https://images.unsplash.com/photo-1531230689007-0b32d7a7c33e') no-repeat center center fixed; background-size: cover;}
.big-title {font-family: 'Kaushan Script', cursive !important; font-size: 5rem !important; text-align: center !important; background: linear-gradient(to right, #e31e24 40%, #ffffff 50%, #006400 60%) !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;}
.tag-subtitle {font-size: clamp(1.5rem, 5vw, 3rem); font-weight: 800; text-align: center; color: white !important; text-shadow: 2px 2px 15px rgba(0,0,0,1);}
.stButton > button {background-color: rgba(255, 255, 255, 0.05); color: white !important; border-radius: 15px; border: 3px solid #e31e24; font-size: 1.3rem; padding: 18px 25px;}
.stButton > button:hover {background-color: #e31e24; transform: scale(1.05);}
</style>
""", unsafe_allow_html=True)

# ====================== SESSION STATE ======================
if "page" not in st.session_state: st.session_state.page = "home"
if "current_stop" not in st.session_state: st.session_state.current_stop = 1
if "stop1_phase" not in st.session_state: st.session_state.stop1_phase = "welcome"
if "score" not in st.session_state: st.session_state.score = 0
if "stop_answers" not in st.session_state: st.session_state.stop_answers = {}

welcome_url = "https://mywebar.com/p/Project_0_ckwoq2vq9l"
riddle_url_stop1 = "https://mywebar.com/p/Project_1_to00xjn24"

# ====================== HOME PAGE (EXACTLY AS YOU HAD) ======================
if st.session_state.page == "home":
    st.markdown('<h1 class="big-title">Kenz Quest - مهمة الكنز</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">Explore Morocco Culturally • اكتشف المغرب</div>', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">🗺️ Click on a region / اضغط على جهة</h3>', unsafe_allow_html=True)
    try:
        image = Image.open("morocco_regions_map.png")
        image = image.resize((700, 500), Image.Resampling.LANCZOS)
    except:
        image = None
    if image is not None:
        map_col, legend_col = st.columns([1.8, 1])
        with map_col:
            if 'streamlit_image_coordinates' in globals():
                click = streamlit_image_coordinates(image, key="morocco_region_map")
                if click:
                    rel_x = click["x"] / image.width
                    rel_y = click["y"] / image.height
                    if 0.47 <= rel_x <= 0.61 and 0.28 <= rel_y <= 0.38:
                        st.session_state.page = "marrakech_safi"
                        st.rerun()
                    else:
                        st.toast("Coming Soon! / قريباً", icon="⏳")
            else:
                st.image(image, use_container_width=True)
        with legend_col:
            st.markdown('<h3 style="text-align:center;">📋 Regions / الجهات</h3>', unsafe_allow_html=True)
            if st.button("**Marrakech-Safi** 🕌", use_container_width=True, type="primary"):
                st.session_state.page = "marrakech_safi"
                st.rerun()

# ====================== MARRAKECH-SAFI MAP (EXACTLY AS YOU HAD) ======================
elif st.session_state.page == "marrakech_safi":
    st.markdown('<h1 class="big-title">Marrakech-Safi</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">📍 مراكش آسفي</div>', unsafe_allow_html=True)
    try:
        image = Image.open("marrakech_safi.png")
        image = image.resize((600, 400), Image.Resampling.LANCZOS)
    except:
        image = None
    if image is not None:
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if 'streamlit_image_coordinates' in globals():
                click = streamlit_image_coordinates(image, key="marrakech-safi")
                if click is not None:
                    rel_x = click["x"] / image.width
                    rel_y = click["y"] / image.height
                    if 0.53 <= rel_x <= 0.62 and 0.41 <= rel_y <= 0.69:
                        st.session_state.page = "adventure"
                        st.session_state.stop1_phase = "welcome"
                        st.rerun()
                    else:
                        st.toast("Coming Soon! / قريباً", icon="⏳")
            else:
                st.image(image, use_container_width=True)
    if st.button("⬅ Back to Regions Map"):
        st.session_state.page = "home"
        st.rerun()

# ====================== ADVENTURE – STOP 1 ONLY (UPDATED AS YOU ASKED) ======================
else:
    current = st.session_state.current_stop
    phase = st.session_state.stop1_phase

    st.progress(current / 7)
    st.markdown(f'<h3 style="text-align: center; color: #e31e24;">🏆 Score: {st.session_state.score} pts</h3>', unsafe_allow_html=True)

    # AR Genie
    col_left, col_mid, col_right = st.columns([1, 4, 1])
    with col_mid:
        st.markdown("### 🧞 The Genie is talking to you...")
        if phase == "welcome":
            current_webar = welcome_url
        else:
            current_webar = riddle_url_stop1
        components.iframe(current_webar, height=700, scrolling=True)

    st.markdown("---")

    # ==================== 1. WELCOME TRAVELER (with cute privacy) ====================
    if phase == "welcome":
        st.markdown('<h1 class="big-title">Welcome Traveler • مرحبًا بك أيها المسافر</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background:rgba(255,255,255,0.1); padding:20px; border-radius:20px; text-align:center;">
        🧞 Hey friend! Just so you know…<br>
        <b>We never keep any photo of your face</b> and we collect <b>zero data</b>. 
        Your adventure stays 100% private and magical ✨
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Let's Start the Adventure • أبدأ المغامرة", type="primary", use_container_width=True):
            st.session_state.stop1_phase = "riddle"
            st.rerun()

    # ==================== 2. RIDDLE PAGE (asked by the WebAR Genie) ====================
    elif phase == "riddle":
        st.markdown("### 🧩 The Genie just whispered the riddle…")
        st.markdown("**Listen carefully to the Genie in the AR box above** and choose your answer below!")

        options = [
            "A) Bab Agnaou", "B) Jemaa el-Fna", "C) Mouassine Square",
            "D) Koutoubia Gardens", "E) Saadian Tombs", "F) Bahia Palace"
        ]

        if "riddle_answer" not in st.session_state.stop_answers:
            st.session_state.stop_answers["riddle_answer"] = None

        cols = st.columns(2)
        for i, opt in enumerate(options):
            with cols[i % 2]:
                if st.button(opt, use_container_width=True, key=f"r{i}"):
                    st.session_state.stop_answers["riddle_answer"] = opt
                    if opt == "B) Jemaa el-Fna":
                        st.session_state.score += 30
                        st.success("🌟 Correct! You found the legendary square!")
                        st.session_state.stop1_phase = "content"
                    else:
                        st.error("Not quite… The Genie says the answer is B) Jemaa el-Fna")
                    st.rerun()

    # ==================== 3. FULL STOP 1 CONTENT (exactly as you described) ====================
    elif phase == "content":
        st.markdown('<h1 class="big-title">Stop 1 • Jemaa el-Fna</h1>', unsafe_allow_html=True)
        st.markdown("### The World’s Oldest Social Media Platform ✨")

        st.info("You are standing in the world's oldest **social media** platform. Before TikTok there was the **Halqa** — storytellers uploading history directly into people’s minds for 1000 years!")

        st.info("In 1985 the entire Medina of Marrakech was listed as UNESCO World Heritage. In 2001 Jemaa el-Fna was proclaimed a **Masterpiece of the Oral and Intangible Heritage of Humanity**.")

        st.info("Music fills the air. Gnaoua rhythms echo. Healers and snake charmers create pure magic every night.")

        st.markdown("### 🎤 Special Guest: Lalla Aïcha Hamdouchia")
        st.info("One of the most powerful voices you can hear here is the legendary Gnaoua singer **Lalla Aïcha Hamdouchia**.")

        if st.button("🧞 Click to hear the Genie tell her story of resistance ✨", use_container_width=True):
            st.markdown("""
            <div style="background:rgba(227,30,36,0.2); padding:20px; border-radius:15px;">
            🧞‍♀️ "Ya traveler! In the 1950s this very square became the beating heart of the Moroccan resistance. 
            People gathered here in secret to sing songs of freedom. Lalla Aïcha Hamdouchia’s voice became a call for unity. 
            This square helped us stay strong until the day our beloved King Mohammed V visited M’Hamid El Ghizlane and the southern provinces 
            (Laâyoune, Smara, Boujdour) in 1958 — forever sealing our sovereignty over the Sahara!"
            </div>
            """, unsafe_allow_html=True)

        st.info("The square is also the starting point of the spiritual protection circle of the **Seven Saints of Marrakech** (Source: Abu al-Abbas al-Sabti).")

        st.markdown("### 🧭 The Next Adventure Awaits…")
        st.info("The caravans trading here came from the deep south. Let’s follow the **Silver Path** to find where the desert meets the city.\n\n**Next Stop: Hassani Silver Filigree Artisan**")

        if st.button("🌟 Continue to the Silver Artisan", type="primary", use_container_width=True):
            st.session_state.current_stop = 2
            st.session_state.stop1_phase = "welcome"  # reset for future stops
            st.rerun()

    # Simple back button
    if st.button("⬅ Back to Marrakech-Safi Map"):
        st.session_state.page = "marrakech_safi"
        st.session_state.stop1_phase = "welcome"
        st.rerun()

st.caption("Kenz Quest • Made with ❤️ for Moroccan heritage & artisans • Hackathon 2026")
