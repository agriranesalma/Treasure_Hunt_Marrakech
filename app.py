import streamlit as st
from PIL import Image
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components

try:
    from streamlit_image_coordinates import streamlit_image_coordinates
except ImportError:
    streamlit_image_coordinates = None

st.set_page_config(page_title="كنز المغرب • Trésor Marocain", layout="wide", page_icon="🕌")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Kaushan+Script&display=swap');

@keyframes gentleGlow {
    0% { text-shadow: 0 0 50px rgba(255,255,255,0.2); }
    50% { text-shadow: 0 0 100px rgba(255,255,255,0.5); }
    100% { text-shadow: 0 0 50px rgba(255,255,255,0.2); }
}

.stApp {
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
                url('https://images.unsplash.com/photo-1531230689007-0b32d7a7c33e?q=80&w=2070&auto=format&fit=crop')
                no-repeat center center fixed;
    background-size: cover;
    color: white !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

.main .block-container {
    padding-top: 0rem !important;
    padding-left: 3% !important;
    padding-right: 3% !important;
    max-width: 95% !important;
}

.big-title {
    font-family: 'Kaushan Script', cursive !important;
    font-size: 5rem !important; 
    font-weight: 900 !important;
    text-align: center !important;
    background: linear-gradient(to right, #e31e24 40%, #ffffff 50%, #006400 60%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    display: block !important;
    width: 100% !important;
    line-height: 1.2 !important;
    margin-bottom: 0px !important;
    padding-bottom: 0px !important;
    -webkit-text-stroke: 4px rgba(255,255,255,0.1);
}

.tag-subtitle {
    font-size: clamp(1.5rem, 5vw, 3rem);
    font-weight: 800;
    text-align: center;
    color: white !important;
    text-shadow: 2px 2px 15px rgba(0,0,0,1);
    margin-top: 4rem !important;
    margin-bottom: 4rem;
    letter-spacing: 2px;
}

.section-header {
    text-align: center;
    margin-bottom: 2rem;
    font-size: 1.5rem;
}

[data-testid="stImageCoordinates"] img,
img[src*="streamlit_image_coordinates"] {
    max-width: 100% !important;
    height: auto !important;
    display: block;
    margin: 0 auto;
    border-radius: 30px;
    box-shadow: 0 30px 60px rgba(0,0,0,0.6);
}

.stButton > button {
    background-color: rgba(255, 255, 255, 0.05);
    color: white !important;
    border-radius: 15px;
    border: 3px solid #e31e24;
    font-size: 1.3rem;
    padding: 18px 25px;
    backdrop-filter: blur(15px);
    transition: all 0.4s ease;
}

.stButton > button:hover {
    background-color: #e31e24;
    transform: scale(1.05);
    box-shadow: 0 20px 40px rgba(227,30,36,0.5);
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
if "stop_answers" not in st.session_state:
    st.session_state.stop_answers = {}
if "stop1_phase" not in st.session_state:
    st.session_state.stop1_phase = "intro"
welcome_url = "https://mywebar.com/p/Project_0_ckwoq2vq9l"
riddle_url = "https://mywebar.com/p/Project_1_to00xjn24"
# ====================== STOP DATA (add more stops here later) ======================
stops_data = {
    1: {
        "riddle_options": [
            "A) Bab Agnaou",
            "B) Jemaa el-Fna",
            "C) Mouassine Square",
            "D) Koutoubia Gardens"
        ],
        "correct_riddle": "B) Jemaa el-Fna",
        "learning": """Jemaa el-Fna is the heart of Marrakech’s medina. For over 800 years, people have gathered here for storytelling circles (halqa), musicians, and entertainers. In fact, in 2001 UNESCO declared Jemaa el-Fna a “Masterpiece of the Oral and Intangible Heritage of Humanity” because of its living traditions. At dusk, dozens of food stalls and performers appear – changing the atmosphere completely.""",
        "mini_question": "Look around the square: one drink is sold from many orange juice stalls. What fruit is used for the famous orange juice here?",
        "mini_options": [
            "A) Pomegranate",
            "B) Orange",
            "C) Lemon",
            "D) Peach"
        ],
        "correct_mini": "B) Orange",
        "mini_explanation": "Marrakech’s Jemaa el-Fna is famous for its fresh orange juice stalls."
    }
    # Example for stop 2 :
    # 2: { "riddle_options": [...], "correct_riddle": "...", ... }
}
if st.session_state.page == "home":
    st.markdown('<h1 class="big-title">Kenz Quest     -      مهمة الكنز</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">Explore Morocco Culturally • اكتشف المغرب</div>', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">🗺️ Click on a region / اضغط على جهة</h3>', unsafe_allow_html=True)

    try:
        image = Image.open("morocco_regions_map.png")
        target_w = 700
        w, h = image.size
        ratio = target_w / float(w)
        new_h = int(h * ratio)
        image = image.resize((target_w, new_h), Image.Resampling.LANCZOS)
    except:
        image = None

    if image is not None:
        map_col, legend_col = st.columns([1.8, 1])

        with map_col:
            if streamlit_image_coordinates is not None:
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
                    st.markdown(f'<div style="background:{color}; width:18px; height:18px; border-radius:50%; margin-top:16px;"></div>', unsafe_allow_html=True)
                with btn_col:
                    if st.button(name, key=f"btn_{num}", use_container_width=True):
                        if name == "Marrakech-Safi":
                            st.session_state.page = "marrakech_safi"
                            st.rerun()
                        else:
                            st.toast("Coming Soon! / قريباً", icon="⏳")
# ====================== MARRAKECH-SAFI MAP ======================
elif st.session_state.page == "marrakech_safi":
    st.markdown('<h1 class="big-title">Marrakech-Safi</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">📍 مراكش آسفي</div>', unsafe_allow_html=True)

    try:
        image = Image.open("marrakech_safi.png")
        target_w = 600
        w, h = image.size
        ratio = target_w / float(w)
        new_h = int(h * ratio)
        image = image.resize((target_w, new_h), Image.Resampling.LANCZOS)
    except Exception as e:
        st.error(f"Error loading image: {e}")
        image = None

    if image is not None:
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if streamlit_image_coordinates is not None:
                click = streamlit_image_coordinates(image, key="marrakech-safi")
                if click is not None:
                    rel_x = click["x"] / image.width
                    rel_y = click["y"] / image.height
                    if 0.53 <= rel_x <= 0.62 and 0.41 <= rel_y <= 0.69:
                        st.session_state.page = "marrakech"
                        st.rerun()
                    else:
                        st.toast("Coming Soon! / قريباً", icon="⏳")
            else:
                st.image(image, use_container_width=True)

    if st.button("⬅ Back to Regions Map"):
        st.session_state.page = "home"
        st.rerun()
# ====================== ADVENTURE PAGE ======================
else: 
    current = st.session_state.current_stop
    phase = st.session_state.stop1_phase if current == 1 else "puzzle"
    
    if current == 1 and phase == "intro":
        st.markdown('<h1 class="big-title">Stop 1 – Welcome</h1>', unsafe_allow_html=True)
        st.markdown('<div class="tag-subtitle">🧞 مرحبًا بك أيها المسافر • Welcome Traveler</div>', unsafe_allow_html=True)
    else:
        st.markdown('<h1 class="big-title">Stop 1 – Jemaa el-Fna Puzzle</h1>', unsafe_allow_html=True)
        st.markdown('<div class="tag-subtitle">🕌 المحطة الأولى • اللغز</div>', unsafe_allow_html=True)

    if st.button("⬅ Back to Marrakech-Safi Map"):
        st.session_state.page = "marrakech_safi"
        st.session_state.stop1_phase = "intro"   # reset for next time
        st.rerun()

    total_stops = 7
    st.progress(current / total_stops)
    st.markdown(f'<h3 style="text-align: center; color: #e31e24;">🏆 Score: {st.session_state.score} pts</h3>', unsafe_allow_html=True)

    # ==================== AR IFRAME – switches automatically between the two links ====================
    col_left, col_mid, col_right = st.columns([1, 4, 1])
    with col_mid:
        st.markdown("### 🧞 Scan the AR Treasure")
        if current == 1 and phase == "intro":
            current_webar_url = welcome_url          # ← Intro page
        else:
            current_webar_url = riddle_url           # ← Puzzle page (different link!)
        components.iframe(current_webar_url, height=700, scrolling=True)

    st.markdown("---")

    # ==================== PAGE 1: INTRO (welcome + Let's Start) ====================
    if current == 1 and phase == "intro":
        st.info("The Genie is happy for your arrival .click the button below to go to start **the adventure**.")
        st.info("يسعد الجني بقدومك. اضغط على الزر أدناه لبدء رحلتك في المغامرة.")
        if st.button("🚀 Let's Start – أبدأ المغامرة", type="primary", use_container_width=True):
            st.session_state.stop1_phase = "puzzle"
            st.rerun()

    # ==================== PAGE 2: PUZZLE (different WebAR link + clickable answers) ====================
    elif current == 1 and phase == "puzzle" and current in stops_data:
        stop = stops_data[1]

        if 1 not in st.session_state.stop_answers:
            st.session_state.stop_answers[1] = {"riddle": None, "mini": None, "riddle_scored": False, "mini_scored": False}
        answers = st.session_state.stop_answers[1]

        st.subheader("🧩 Click your answer to the AR puzzle")
        if answers["riddle"] is None:
            c1, c2 = st.columns(2)
            for i, opt in enumerate(stop["riddle_options"]):
                with (c1 if i % 2 == 0 else c2):
                    if st.button(opt, use_container_width=True, key=f"r1_{i}"):
                        answers["riddle"] = opt
                        if opt == stop["correct_riddle"] and not answers["riddle_scored"]:
                            answers["riddle_scored"] = True
                            st.session_state.score += 25
                        st.rerun()
        else:
            if answers["riddle"] == stop["correct_riddle"]:
                st.success(f"✅ Correct! The legendary place is **{stop['correct_riddle']}**")
            else:
                st.error(f"❌ You chose {answers['riddle']}. The correct answer is {stop['correct_riddle']}")
                if st.button("🔄 Try Riddle Again"): answers["riddle"] = None; st.rerun()
            st.markdown("**📖 Learning Moment**"); st.info(stop["learning"])

        if answers["riddle"] is not None:
            st.subheader("🔍 Mini-Challenge: Observation")
            st.write(stop["mini_question"])
            if answers["mini"] is None:
                c1, c2 = st.columns(2)
                for i, opt in enumerate(stop["mini_options"]):
                    with (c1 if i % 2 == 0 else c2):
                        if st.button(opt, use_container_width=True, key=f"m1_{i}"):
                            answers["mini"] = opt
                            if opt == stop["correct_mini"] and not answers["mini_scored"]:
                                answers["mini_scored"] = True
                                st.session_state.score += 15
                            st.rerun()
            else:
                if answers["mini"] == stop["correct_mini"]:
                    st.success(f"✅ Yes! {stop['mini_explanation']}")
                else:
                    st.error(f"❌ Not quite. The answer is {stop['correct_mini']}")
                    if st.button("🔄 Try Mini Again"): answers["mini"] = None; st.rerun()

    elif current > 1:
        st.info("Stops 2–7 coming soon – same structure (one AR link per stop).")

    st.markdown("---")

    # Navigation
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
    with btn_col1:
        if current > 1 and st.button("← Previous", use_container_width=True):
            st.session_state.current_stop -= 1
            if current == 2: st.session_state.stop1_phase = "puzzle"  # stay on puzzle when going back
            st.rerun()
    with btn_col2:
        st.markdown(f"**Stop {current} / {total_stops}**", unsafe_allow_html=True)
    with btn_col3:
        if current < total_stops:
            if st.button("Next →", type="primary", use_container_width=True):
                st.session_state.current_stop += 1
                if st.session_state.current_stop not in st.session_state.unlocked_stops:
                    st.session_state.unlocked_stops.append(st.session_state.current_stop)
                st.rerun()
        else:
            st.success("🎉 Congratulations! You completed the Marrakech-Safi Treasure Hunt!")
