import streamlit as st
from PIL import Image
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components

try:
    from streamlit_image_coordinates import streamlit_image_coordinates
except ImportError:
    streamlit_image_coordinates = None
# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="كنز المغرب • Trésor Marocain",
    layout="wide",
    page_icon="🗺️"
)

# ---------------- THEME / CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Kaushan+Script&display=swap');

.stApp {
    background: linear-gradient(rgba(0,0,0,0.84), rgba(0,0,0,0.84)),
                url('https://images.unsplash.com/photo-1531230689007-0b32d7a7c33e?q=80&w=2070&auto=format&fit=crop')
                no-repeat center center fixed;
    background-size: cover;
    color: white !important;
}

[data-testid="stHeader"] { background: transparent !important; }

.main .block-container {
    padding-top: 0.5rem !important;
    padding-left: 3% !important;
    padding-right: 3% !important;
    max-width: 95% !important;
}

.big-title {
    font-family: 'Kaushan Script', cursive !important;
    font-size: clamp(2.8rem, 7vw, 5rem) !important;
    font-weight: 900 !important;
    text-align: center !important;
    background: linear-gradient(to right, #e31e24 40%, #ffffff 50%, #006400 60%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    display: block !important;
    width: 100% !important;
    line-height: 1.15 !important;
    margin-bottom: 0.2rem !important;
}

.tag-subtitle {
    font-size: clamp(1.2rem, 3.5vw, 2.2rem);
    font-weight: 800;
    text-align: center;
    color: white !important;
    text-shadow: 2px 2px 15px rgba(0,0,0,1);
    margin-top: 0.4rem !important;
    margin-bottom: 1.4rem !important;
    letter-spacing: 1px;
}

.magic-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,215,0,0.22);
    border-radius: 24px;
    padding: 1.1rem 1.2rem;
    box-shadow: 0 18px 50px rgba(0,0,0,0.35);
    backdrop-filter: blur(12px);
    margin: 0.6rem 0;
}

.magic-card h3, .magic-card h4, .magic-card p, .magic-card li {
    color: white !important;
}

.stButton > button {
    background-color: rgba(255, 255, 255, 0.05);
    color: white !important;
    border-radius: 14px;
    border: 2px solid #e31e24;
    font-size: 1.05rem;
    padding: 0.9rem 1rem;
    transition: all 0.25s ease;
}
.stButton > button:hover {
    background-color: #e31e24;
    transform: translateY(-1px);
    box-shadow: 0 18px 30px rgba(227,30,36,0.35);
}
.stTextInput input {
    border-radius: 12px !important;
}
.notice {
    background: rgba(0,200,83,0.12);
    border: 1px solid rgba(0,200,83,0.28);
    border-radius: 18px;
    padding: 0.9rem 1rem;
    margin: 0.7rem 0;
}
.small-center {
    text-align:center;
    opacity:0.95;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "current_stop" not in st.session_state:
    st.session_state.current_stop = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "stop_answers" not in st.session_state:
    st.session_state.stop_answers = {}

if "stop1_phase" not in st.session_state:
    st.session_state.stop1_phase = "welcome"   # welcome -> riddle -> story -> code_gate

if "hunt_started" not in st.session_state:
    st.session_state.hunt_started = False

# ---------------- CONSTANTS ----------------
welcome_url = "https://mywebar.com/p/Project_0_ckwoq2vq9l"
riddle_url_stop1 = "https://mywebar.com/p/Project_1_to00xjn24"

# One reusable code for all partner businesses in the hackathon
PARTNER_ACCESS_CODE = "KENZQUEST2026"

# ---------------- STOP 1 CONTENT ----------------
stops_data = {
    1: {
        "title": "Jemaa el-Fna — The Open-Air Theater",
        "riddle": "I am a stage without a curtain, a book without pages, and a kitchen that never sleeps. I change my face when the sun sets, but my voice has remained the same for 800 years. Where am I?",
        "riddle_options": [
            "A) Koutoubia Gardens",
            "B) Bab Agnaou",
            "C) Jemaa el-Fna",
            "D) Mouassine Square",
            "E) Bahia Palace",
            "F) Saadian Tombs"
        ],
        "correct_riddle": "C) Jemaa el-Fna",
        "hook": "You are standing in the world’s oldest social media platform. Before TikTok, there was the Halqa. For centuries, storytellers, musicians, poets, healers, acrobats, and performers used this square to upload memory into people’s minds.",
        "unesco": "In 1985, the Medina of Marrakech was inscribed as a World Heritage Site, and in 2001 Jemaa el-Fna was proclaimed a Masterpiece of the Oral and Intangible Heritage of Humanity.",
        "atmosphere": "By day, the square lives through orange juice stalls, spices, street games, and movement. By night, it turns into a glowing stage of drums, Gnaoua rhythms, storytellers, herbalists, and crowd-formed circles of wonder.",
        "gnawa": "Among the sounds that make the square unforgettable is Gnaoua music: hypnotic, spiritual, and rooted in deep memory. In your story world, one of the songs can salute Lalla Aïcha Hamdouchia as a symbol of dignity, courage, and resistance carried through oral tradition.",
        "genie_speech": (
            "Listen carefully, traveler. This square has never been silent when Morocco needed its voice. "
            "In the 1950s, under the weight of the Protectorate, places like this helped carry the pulse of resistance, "
            "union, and national awareness. Songs, gatherings, and shared memory kept the Moroccan spirit standing tall. "
            "A square can be a theater—but it can also be a shield."
        ),
        "national_memory": (
            "This moment also connects to national memory: the 68th anniversary of HM King Mohammed V’s historic visit "
            "to M’Hamid El Ghizlane and the southern provinces, as well as the commemoration of the last foreign soldier’s "
            "departure from the Moroccan Sahara. These milestones speak to sovereignty, continuity, and territorial unity."
        ),
        "legend": (
            "And there is a circle of protection around Marrakech: the Seven Saints. "
            "Rooted in the tradition associated with Abu al-Abbas al-Sabti, this spiritual journey helped shape the city’s memory, "
            "identity, and blessing."
        ),
        "transition": (
            "The caravans trading here came from the deep south. Let’s follow the Silver Path to find where the desert meets the city."
        ),
        "next_stop": "Hassani Silver Filigree Artisanat",
        "next_stop_label": "Hassani Silver Filigree Artisanat",
        "next_stop_intro": "The next stop is a Hassani Silver Filigree artisanat, where the treasure changes from stories to craft."
    }
}

# ---------------- HELPERS ----------------
def render_webar(url, height=680):
    components.iframe(url, height=height, scrolling=True)

def init_answer_state(stop_num):
    if stop_num not in st.session_state.stop_answers:
        st.session_state.stop_answers[stop_num] = {
            "riddle": None,
            "unlocked": False
        }

def show_welcome_page():
    st.markdown('<h1 class="big-title">Welcome Traveler • مرحبًا بك أيها المسافر</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">🧞 The Genie is waiting for you</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("""
        <div class="magic-card">
            <h3>🌟 Your journey begins here</h3>
            <p>The Genie is excited to guide you through Morocco’s living memory. She is asking:</p>
            <p><strong>“Are you ready for the journey?”</strong></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="notice">
            <strong>Privacy notice:</strong> We do not store images of your face; no data is collected.
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Start the Adventure", type="primary", use_container_width=True):
            st.session_state.stop1_phase = "riddle"
            st.rerun()

    with col2:
        st.markdown("### 🪄 WebAR Genie")
        render_webar(welcome_url, height=620)

def show_entry_riddle():
    stop = stops_data[1]
    init_answer_state(1)
    answers = st.session_state.stop_answers[1]

    st.markdown('<h1 class="big-title">🧩 The First Riddle</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">Solve the mystery to reveal the first stop</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"""
        <div class="magic-card">
            <h3>Riddle</h3>
            <p style="font-size:1.15rem; line-height:1.8;">{stop["riddle"]}</p>
        </div>
        """, unsafe_allow_html=True)

        if answers["riddle"] is None:
            st.subheader("Choose one answer")
            cols = st.columns(2)
            for i, opt in enumerate(stop["riddle_options"]):
                with cols[i % 2]:
                    if st.button(opt, key=f"stop1_riddle_{i}", use_container_width=True):
                        answers["riddle"] = opt
                        if opt == stop["correct_riddle"]:
                            st.session_state.score += 25
                            answers["unlocked"] = True
                        st.rerun()
        else:
            if answers["riddle"] == stop["correct_riddle"]:
                st.success("✅ Correct! You found the place.")
                st.session_state.stop1_phase = "story"
                st.rerun()
            else:
                st.error("❌ Not this one. Try again.")
                if st.button("🔄 Try again", key="retry_stop1_riddle"):
                    answers["riddle"] = None
                    st.rerun()

    with col2:
        st.markdown("### 🧞 The Genie watches the square")
        render_webar(riddle_url_stop1, height=620)

def show_stop1_story():
    stop = stops_data[1]

    st.markdown(f'<h1 class="big-title">{stop["title"]}</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">✨ A square of memory, music, and resistance</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="magic-card">
        <h3>⭐ Hook</h3>
        <p>{stop["hook"]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="magic-card">
        <h3>🏛️ UNESCO Memory</h3>
        <p>{stop["unesco"]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="magic-card">
        <h3>🎶 What you hear in the square</h3>
        <p>{stop["atmosphere"]}</p>
        <p>{stop["gnawa"]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="magic-card">
        <h3>🧞 The Genie’s speech</h3>
        <p>{stop["genie_speech"]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="magic-card">
        <h3>🇲🇦 National memory</h3>
        <p>{stop["national_memory"]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="magic-card">
        <h3>🔱 The Legend of the Seven Saints</h3>
        <p>{stop["legend"]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="magic-card">
        <h3>🛤️ Transition</h3>
        <p>{stop["transition"]}</p>
        <p><strong>Next stop:</strong> {stop["next_stop_intro"]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.info("✨ To continue, use the partner code at the next artisan stop.")

def show_partner_code_gate(next_label, next_stop_num):
    st.markdown('<h2 class="big-title">🔐 Silver Path Gate</h2>', unsafe_allow_html=True)
    st.markdown(f'<div class="tag-subtitle">Unlock the next treasure: {next_label}</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="magic-card">
        <p>Enter the shared hackathon code to open the next stop.</p>
    </div>
    """, unsafe_allow_html=True)

    code = st.text_input("Enter code", placeholder="e.g. KENZQUEST2026", key=f"code_gate_{next_stop_num}")
    if st.button("Unlock next stop", key=f"unlock_{next_stop_num}", type="primary"):
        if code.strip() == PARTNER_ACCESS_CODE:
            st.session_state.current_stop = next_stop_num
            st.session_state.stop1_phase = "welcome"  # reset for future revisits
            st.session_state.score += 10
            st.success("✅ Unlocked!")
            st.rerun()
        else:
            st.error("❌ Incorrect code. Try again.")

# ---------------- ROUTING ----------------
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
                ("01", "Tanger-Tétouan-Al Hoceïma", "#06b6ad"),
                ("02", "Oriental", "#e9711d"),
                ("03", "Fès-Meknès", "#2e8b58"),
                ("04", "Rabat-Salé-Kénitra", "#d7292a"),
                ("05", "Béni Mellal-Khénifra", "#404064"),
                ("06", "Casablanca-Settat", "#656474"),
                ("07", "Marrakech-Safi", "#db8e3d"),
                ("08", "Drâa-Tafilalet", "#82a0dc"),
                ("09", "Souss-Massa", "#79c779"),
                ("10", "Guelmim-Oued Noun", "#c9ab34"),
                ("11", "Laâyoune-Sakia El Hamra", "#8d3267"),
                ("12", "Eddakhla-Oued Ed-dahab", "#51aadc"),
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

else:
    current = st.session_state.current_stop
    total_stops = 7

    st.markdown(f'<h3 style="text-align:center;">🏆 Score: {st.session_state.score} pts</h3>', unsafe_allow_html=True)
    st.progress(current / total_stops)

    if current == 1:
        phase = st.session_state.stop1_phase
        if phase == "welcome":
            show_welcome_page()
        elif phase == "riddle":
            show_entry_riddle()
        elif phase == "story":
            show_stop1_story()
            st.markdown("---")
            if st.button("Continue to the Silver Path →", type="primary", use_container_width=True):
                st.session_state.current_stop = 2
                st.rerun()

            # Optional: if you want the code gate right after the story
            st.markdown("### 🔐 Partner business gate")
            show_partner_code_gate(
                next_label=stops_data[1]["next_stop_label"],
                next_stop_num=2
            )

    else:
        st.success(f"Stop {current} page goes here.")

    st.markdown("---")
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if current > 1 and st.button("← Previous", use_container_width=True):
            st.session_state.current_stop -= 1
            st.rerun()
    with c2:
        st.markdown(f"<p style='text-align:center;'><strong>Stop {current} / {total_stops}</strong></p>", unsafe_allow_html=True)
    with c3:
        if current < total_stops and st.button("Next →", type="primary", use_container_width=True):
            st.session_state.current_stop += 1
            st.rerun()
