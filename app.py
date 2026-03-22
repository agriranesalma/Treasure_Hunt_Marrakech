import streamlit as st
from PIL import Image
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
    st.session_state.stop1_phase = "welcome"
if "quiz_unlocked" not in st.session_state:
    st.session_state.quiz_unlocked = {}
if "pottery_code_entered" not in st.session_state:
    st.session_state.pottery_code_entered = False
if "quiz_correct_count" not in st.session_state:
    st.session_state.quiz_correct_count = {i: 0 for i in range(1, 10)}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = {}

# ---------------- CONSTANTS ----------------
welcome_url = "https://mywebar.com/p/Project_0_ckwoq2vq9l"
riddle_url_stop1 = "https://mywebar.com/p/Project_1_to00xjn24"
PARTNER_ACCESS_CODE = "KENZQUEST2026"
stop_titles = {
    1: "Gueliz",
    2: "Jemaa el-Fna — The Open-Air Theater",
    3: "Silver jewlery Workshop",
    4: "☕ Partner Café Stop",
    5: "🏛️ Saadian Tombs",
    6: "🏺 Zellige Artisan Workshop",
    7: "🍲 Moroccan Cuisine Class",
    8: "🕌 Koutoubia Mosque",
    9: "🏛️ Bahia Palace",
    10: "🏺 Pottery / Souk"
}

# ---------------- STOPS DATA ----------------
stops_data = {
    1: {
        "title": "Jemaa el-Fna — The Open-Air Theater",
        "riddle": "🧞 the genie will give you the first riddle, pick the correct answer",
        "riddle_options": ["A) Koutoubia Gardens", "B) Bab Agnaou", "C) Jemaa el-Fna", "D) Mouassine Square", "E) Bahia Palace", "F) Saadian Tombs"],
        "correct_riddle": "C) Jemaa el-Fna",
        "hook": "You are standing in the world’s oldest social media platform. Before TikTok, there was the Halqa. For centuries, storytellers, musicians, poets, healers, acrobats, and performers used this square to upload memory into people’s minds.",
        "unesco": "In 1985, the Medina of Marrakech was inscribed as a World Heritage Site, and in 2001 Jemaa el-Fna was proclaimed a Masterpiece of the Oral and Intangible Heritage of Humanity.",
        "atmosphere": "By day, the square lives through orange juice stalls, spices, street games, and movement. By night, it turns into a glowing stage of drums, Gnaoua rhythms, storytellers, herbalists, and crowd-formed circles of wonder.",
        "national_memory": "But this square is not only a place of stories and music — it is also a place of memory. Jemaa el-Fnaa isn't just a marketplace; it is and have been a heartbeat. In the 1950s, while the world watched the performers, a secret spirit of resistance was brewing right here. This energy eventually flowed south, echoing the legendary moment when King Mohammed V stood in the sands of M’Hamid El Ghizlane to reclaim the desert’s soul.",
        "legend": "The Circle of Protection in Marrakech refers to the spiritual, cultural, and symbolic efforts to safeguard the city, primarily embodied by the Seven Saints (Sabatou Rijal) pilgrimage tradition. These seven holy figures are believed to provide divine protection (baraka) to the city, fostering a spiritual atmosphere. ",
        "transition": "And just like these stories and traditions, the life of this square did not begin here. The merchants, the music, the knowledge — all traveled from far beyond the city walls, some coming all the way from the far south of the country, lets get to know a little about the hassanie culture. In the vast silence of the dunes, the voice became the greatest treasure. To understand the heart of the Sahara, you must listen to the poetry that flows like the desert wind, rhythmic, deep, and timeless.",
        "next_stop_label": "Hassani Silver Filigree Artisan",
        "next_stop_intro": "The next stop is a Hassani Silver Filigree artisan..."
    }
}

# ---------------- QUIZZES DATA (Bab Agnaou quiz completely removed) ----------------
quizzes_data = {
    1: { 
        "general": [
            {"q": "Which 1975 peaceful march saw 350,000 Moroccans walk into the Sahara to assert national sovereignty?", "options": ["Green March", "Independence Walk", "Desert Caravan", "Atlas March"], "correct": "Green March"},
            {"q": "During World War II, Mohammed V famously refused to apply the Vichy government's laws. Who was he protecting?", "options": ["The Moroccan Jewish community", "The French settlers", "The British soldiers", "The Spanish merchants"], "correct": "The Moroccan Jewish community"}
        ],
        "detailed": [
            {"q": "Look at the official 'UNESCO World Heritage' plaque located near the square's entrance—what is the first word of the second line?", "correct": "masterpiece"},
            {"q": "Find the nearest official Horse Carriage (Caleche) station. Look at the carriage license plates—what color is the background of the plate?", "correct": "green"}
        ]
    },
    2: { 
        "general": [
            {"q": "Which Moroccan city is so famous for filmmaking that it has hosted Gladiator, Game of Thrones, and The Mummy?", "options": ["Ouarzazate", "Casablanca", "Agadir", "Tangier"], "correct": "Ouarzazate"},
            {"q": "Morocco was the very first country in the world to recognize the independence of which country in 1777?", "options": ["USA", "France", "Russia", "China"], "correct": "USA"}
        ],
        "detailed": [
            {"q": "In Moroccan tea culture, why is the tea traditionally poured from a great height into the glass?", "correct": "to create foam"},
            {"q": "Moroccan 'Atay' is a blend of three essential ingredients: Green tea, fresh mint, and what else?", "correct": "sugar"}
        ]
    },
    4: { 
        "general": [
            {"q": "The Saadian dynasty is famous for the 'Battle of the Three Kings'—which European power did they defeat in 1578?", "options": ["Portugal", "England", "Italy", "Ottoman Empire"], "correct": "Portugal"},
            {"q": "In 1600, Sultan Ahmed al-Mansur sent a high-level diplomatic embassy to London. Which famous English Queen did he form a strategic alliance with to challenge the Spanish Empire?", "options": ["Queen Mary I", "Queen Victoria", "Queen Elizabeth I", "Queen Anne"], "correct": "Queen Elizabeth I"}
        ],
        "detailed": [
            {"q": "Look at the pillars—how many large marble columns are supporting the central dome?", "correct": "12"},
            {"q": "Look closely at the zellige floor patterns—what is the dominant color of the tiles surrounding the royal graves?", "correct": "green"}
        ]
    },
    5: { 
        "general": [
            {"q": "Morocco is the only country in Africa that has coastline on which two major bodies of water?", "options": ["The Mediterranean Sea and the Atlantic Ocean", "The Red Sea and the Indian Ocean", "The Dead Sea and the Black Sea", "The Atlantic Ocean and the Nile River"], "correct": "The Mediterranean Sea and the Atlantic Ocean"},
            {"q": "Morocco is home to one of the best places in the world to find 'Space Rocks' (Meteorites). Why are they so much easier to find in the Moroccan Sahara than anywhere else?", "options": ["Dark rocks stand out against light sand", "Natural magnetic pull of the Atlas Mountains", "Higher frequency of meteor strikes in North Africa", "The dry climate prevents the rocks from eroding"], "correct": "Dark rocks stand out against light sand"}
        ],
        "detailed": [
            {"q": "Watch the artisan for a moment. He is using a 'Manquach' (hammer). Is the head of the hammer rectangular or pointed at both ends?", "correct": "pointed at both ends"},
            {"q": "Pick up a discarded tile scrap from the floor. Touch the 'back' (non-glazed side). What color is the raw, unbaked clay?", "correct": "grey"}
        ]
    },
    6: { 
        "general": [
            {"q": "What is the name of the famous Moroccan spice blend that can contain over 30 ingredients?", "options": ["Ras el Hanout", "Harissa", "Chermoula", "Kamoun"], "correct": "Ras el Hanout"},
            {"q": "Morocco is one of the world's largest exporters of which 'red gold' spice grown in Taliouine?", "options": ["Saffron", "Paprika", "Cinnamon", "Cayenne"], "correct": "Saffron"}
        ],
        "detailed": [
            {"q": "Look at the large display plates (Taws) in the shop. What animal is on it", "correct": "Peacock"},
            {"q": "What is the name of the traditional clay oven used to slow-cook meat dishes like Tangia?", "correct": "Farnatchi"}
        ]
    },
    7: { 
        "general": [
            {"q": "Which famous tower in Seville, Spain, is considered the 'twin sister' of the Koutoubia minaret?", "options": ["Giralda", "Torre del Oro", "Alhambra", "Belem Tower"], "correct": "Giralda"},
            {"q": "How many golden copper orbs are stacked on the spire of the Koutoubia minaret?", "options": ["4", "3", "5", "1"], "correct": "4"}
        ],
        "detailed": [
            {"q": "Stand on the side of the tower facing the gardens. Look at the upper windows. What is the shape of the stone arch above the window: Pointed, Horseshoe, or Scalloped?", "correct": "scalloped"},
            {"q": "Look at the ruins of the 'old' mosque foundation next to the tower. Are the remaining column stumps circular or square?", "correct": "square"}
        ]
    },
    8: { 
        "general": [
            {"q": "The Bahia Palace was built to be the greatest palace of its time. What does 'Bahia' translate to?", "options": ["The Brilliance", "The Secret", "The Fortress", "The Garden"], "correct": "The Brilliance"},
            {"q": "Which powerful Grand Vizier, who effectively ruled Morocco as a regent, lived here?", "options": ["Ba Ahmed", "Thami El Glaoui", "Lyautey", "Moulay Ismael"], "correct": "Ba Ahmed"}
        ],
        "detailed": [
            {"q": "Walk into the massive Court of Honor (the huge open marble floor). Count the number of small fountains embedded in the floor of this specific courtyard.", "correct": "2"},
            {"q": "Look up at the ceilings around you—what material and style are the carved ceilings made of?", "correct": "cedar wood"}
        ]
    },
    9: { 
        "general": [
            {"q": "In Moroccan pottery, After shaping a pot on the wheel, what is the usual next step before drying?","options": ["Covering the pot with cloth to preserve moisture", "Painting intricate designs with glaze", "Stacking the pots in the sun immediately", "Trimming the base to refine its shape"], "correct": "Trimming the base to refine its shape"},
            {"q": "Traditional Moroccan pottery is typically dried in what?", "options": ["Wood-fired ovens", "Open-air courtyards","Ceramic kilns"], "correct": "Open-air courtyards"}
        ],
        "detailed": [
            {"q": "The blue pottery of Fez gets its iconic color from which mineral?", "correct": "Cobalt"},
            {"q": "Touch the edge of a 'raw' (unpainted) tagine pot. Whats is the texture like?", "correct": "sandy"}
        ]
    }
}

# ---------------- HELPERS ----------------
def render_webar(url, height=680):
    components.iframe(url, height=height, scrolling=True)

def show_quiz_challenge(stop_num):
    st.markdown("---")
    st.markdown('<h2 class="big-title">🧠 Knowledge Challenge</h2>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">2 General + 2 On-Site Detailed • Prove you are here!</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="magic-card">
        <p><strong>General Knowledge</strong> = broad Morocco facts </p>
        <p><strong>Detailed On-Site</strong> = only visible if you are physically at the stop</p>
    </div>
    """, unsafe_allow_html=True)
    data = quizzes_data.get(stop_num, {"general": [], "detailed": []})
    st.markdown("### 📚 General Knowledge Quizzes")
    for i, q in enumerate(data["general"]):
        submitted_key = f"{stop_num}_gen_{i}"
        if submitted_key not in st.session_state.quiz_submitted:
            st.session_state.quiz_submitted[submitted_key] = False
        if not st.session_state.quiz_submitted[submitted_key]:
            st.subheader(f"General {i+1}")
            ans = st.radio(q["q"], q["options"], key=f"gen_{stop_num}_{i}", index=None)
            if st.button(f"Submit General {i+1}", key=f"sub_gen_{stop_num}_{i}"):
                if ans == q["correct"]:
                    st.success("✅ Correct! Great job.")
                    st.session_state.score += 5
                    st.session_state.quiz_submitted[submitted_key] = True
                    st.session_state.quiz_correct_count[stop_num] = st.session_state.quiz_correct_count.get(stop_num, 0) + 1
                    st.rerun()
                else:
                    st.error("❌ Not quite. Try again!")
        else:
            st.subheader(f"General {i+1} ✅")
            st.success("Completed correctly!")
    st.markdown("### 🔍 On-Site Detailed Quizzes (Must be here!)")
    for i, q in enumerate(data["detailed"]):
        submitted_key = f"{stop_num}_det_{i}"
        if submitted_key not in st.session_state.quiz_submitted:
            st.session_state.quiz_submitted[submitted_key] = False
        if not st.session_state.quiz_submitted[submitted_key]:
            st.subheader(f"Detailed {i+1}")
            ans = st.text_input(q["q"], key=f"det_{stop_num}_{i}", placeholder="Type exactly what you see on-site...")
            if st.button(f"Submit Detailed {i+1}", key=f"sub_det_{stop_num}_{i}"):
                user_ans = ans.lower().strip()
                correct_lower = q["correct"].lower().strip()
                if user_ans in [correct_lower, correct_lower + "s"]:
                    st.success("🎉 Perfect! You are really here!")
                    st.session_state.score += 15
                    st.session_state.quiz_submitted[submitted_key] = True
                    st.session_state.quiz_correct_count[stop_num] = st.session_state.quiz_correct_count.get(stop_num, 0) + 1
                    st.rerun()
                else:
                    st.error("❌ Look around carefully — this detail is only visible on-site!")
        else:
            st.subheader(f"Detailed {i+1} ✅")
            st.success("On-site detail verified!")
    correct_count = st.session_state.quiz_correct_count.get(stop_num, 0)
    st.markdown(f"**Progress: {correct_count}/4 correct answers**")
    st.progress(correct_count / 4.0)
    if correct_count >= 4:
        if not st.session_state.quiz_unlocked.get(stop_num, False):
            st.session_state.quiz_unlocked[stop_num] = True
            st.balloons()
            st.success("🎉 All challenges completed! The path to the next treasure is now open.")
    else:
        st.info("Complete all 4 quizzes to unlock the next stop.")

def show_welcome_page():
    st.markdown('<h1 class="big-title">Welcome Traveler • أهلاً بك أيها المسافر</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">🧞 The Genie is waiting for you</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown("""<div class="magic-card"><h3>🌟 Your journey begins here</h3><p>The Genie is excited to guide you through Morocco’s living memory.</p><p><strong>“Are you ready for the journey?”</strong></p></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="notice"><strong>Privacy notice:</strong> We do not store images of your face; no data is collected.</div>""", unsafe_allow_html=True)
        if st.button("🚀 Start the Adventure", type="primary", use_container_width=True):
            st.session_state.stop1_phase = "riddle"
            st.rerun()
    with col2:
        st.markdown("### 🪄 WebAR Genie")
        render_webar(welcome_url, height=620)
def render_location_notice(location_name):
    html = f"""
    <div class="notice" style="text-align:center; font-size:1.1rem;">
        📍 <strong>You are currently at {location_name}</strong><br>
        <small style="font-size:0.75rem; opacity:0.7;">
            tracking only used to unlock next stop and prove physical presence
        </small>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
def show_entry_riddle():
    render_location_notice(stop_titles[1])
    stop = stops_data[1]
    if 1 not in st.session_state.stop_answers:
        st.session_state.stop_answers[1] = {"riddle": None, "unlocked": False}
    answers = st.session_state.stop_answers[1]
    st.markdown('<h1 class="big-title">🧩 The First Riddle</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">Solve the mystery to reveal the first stop</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""<div class="magic-card"><h3>Riddle</h3><p style="font-size:1.15rem; line-height:1.8;">{stop["riddle"]}</p></div>""", unsafe_allow_html=True)
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
        render_webar(riddle_url_stop1, height=620)

def show_stop1_story():
    render_location_notice(stop_titles[2])
    stop = stops_data[1]
    st.markdown(f'<h1 class="big-title">{stop["title"]}</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">✨ A square of memory, rhythm, and living history</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="magic-card"><h3>⭐ The Living Stage</h3><p>{stop["hook"]}</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="magic-card"><h3>🏛️ A World Treasure</h3><p>{stop["unesco"]}</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="magic-card"><h3>🎭 What surrounds you</h3><p>{stop["atmosphere"]}</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="magic-card"><h3>🎶 A hidden story in the music</h3><p>Some songs in this square are not just music — they are memory, they tell us about the moroccan spirit. Names like <strong>Lalla Aïcha kandicha</strong> echo through the rhythms of <strong>Gnawa</strong>.</p></div>""", unsafe_allow_html=True)
    st.text("🧞 Let the genie tell you about her story and what she symbolizes as an anti colonial moroccan legend, enjoy the Gnawa music about her")
    components.iframe("https://mywebar.com/p/Project_2_ncf4wq5286", height=700, scrolling=True)
    st.markdown(f"""<div class="magic-card"><h3>🇲🇦 Memory & Sovereignty</h3><p>{stop["national_memory"]}</p></div>""", unsafe_allow_html=True)
    st.markdown(
    """
    <style>
        .royal-quote-container {
            background: rgba(15, 15, 25, 0.58); /* semi-transparent dark overlay — keeps bg visible */
            backdrop-filter: blur(6px); /* glass-like effect, very subtle */
            -webkit-backdrop-filter: blur(6px);
            border: 1px solid rgba(255, 215, 0, 0.22); /* faint golden border */
            border-radius: 16px;
            padding: 2.2rem 2.4rem;
            margin: 2rem auto;
            max-width: 780px;
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.45);
            position: relative;
            overflow: hidden;
        }
        .royal-quote-container::before {
            content: "";
            position: absolute;
            inset: 0;
            pointer-events: none;
            background: radial-gradient(circle at 30% 20%, rgba(255, 215, 0, 0.07) 0%, transparent 60%);
        }
        .royal-title {
            color: #ffd700;
            font-size: 2.1rem;
            font-weight: 700;
            text-align: center;
            margin: 0 0 1.8rem 0;
            text-shadow:
                0 0 8px rgba(255, 215, 0, 0.7),
                0 0 18px rgba(255, 215, 0, 0.4),
                0 2px 12px rgba(0,0,0,0.6);
            letter-spacing: 1.2px;
            font-family: 'Georgia', 'Times New Roman', serif;
        }
        .arabic-quote {
            font-size: 1.32rem;
            line-height: 2.05;
            color: #f8faff;
            text-align: right;
            direction: rtl;
            margin-bottom: 1.9rem;
            font-family: 'Traditional Arabic', 'Arial', serif;
        }
        .english-quote {
            font-size: 1.18rem;
            line-height: 1.85;
            color: #e0eaff;
            text-align: left;
            direction: ltr;
            font-style: italic;
            padding-top: 1.3rem;
            border-top: 1px solid rgba(255, 215, 0, 0.18);
        }
        .english-quote::before {
            content: "↳ Translation:";
            display: block;
            color: #ffeb3b;
            font-style: normal;
            font-weight: 600;
            margin-bottom: 0.7rem;
            letter-spacing: 0.6px;
        }
    </style>
    <div class="royal-quote-container">
        <div class="royal-title">Iconic Words from His Majesty</div>
        <div class="arabic-quote">
            إن مجيئنا الرمزي إلى هذا المكان ليؤذن بأنه لن يبقى بعده شمال وجنوب إلا في الاصطلاح الجغرافي العادي،
            وسيكون هناك فقط المغرب الموحد.
        </div>
        <div class="english-quote">
            “Our symbolic arrival at this place proclaims that henceforth there shall remain no North and South
            except in the ordinary geographical sense. There will be only one united Morocco.”
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
    st.markdown(f"""<div class="magic-card"><h3>🔱 The Circle of Protection</h3><p>{stop["legend"]}</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="magic-card"><h3>🛤️ The Journey Continues</h3><p>{stop["transition"]}</p></div>""", unsafe_allow_html=True)
    st.markdown("### 🎧 Listen to Hassani Poetry")
    st.info("💡 Tip: Use headphones for an immersive experience.")
    if st.button("🎧 Play the voice of the desert"):
        audio_file = open("hassani_poetry.mp3", "rb")
        st.audio(audio_file.read(), format="audio/mp3")
    st.image("sahara.png", caption="The Sahara — where poetry travels with the wind", use_container_width=True)
    show_quiz_challenge(1)
    if st.session_state.quiz_unlocked.get(1, False):
        show_partner_code_gate(next_label=stops_data[1].get("next_stop_label"), next_stop_num=2)
    else:
        st.warning("🔒 Complete all 4 Knowledge Challenges above to unlock the Silver Path Gate.")

def show_partner_code_gate(next_label, next_stop_num):
    render_location_notice(stop_titles[3])
    st.markdown('<h2 class="big-title"> Silver Path Gate</h2>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div class="magic-card">
        <h2 style="text-align:center;">✨ Your Next Experience</h2>
        <p style="text-align:center; font-size:1.2rem;">
        Lets actually get handsy and learn more about moroccan sahrawi culture.
        You unlocked your visit to the jewlery artisan workshop, you won’t just observe…
        <br><strong>You will create.</strong>
        </p>
        <p style="text-align:center;">
        Guided by a master artisan, you will craft your own piece of
        <strong>Moroccan Sahrawi silver jewelry</strong>,
        inspired by traditions passed down through generations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.image(
        "sahrawijewlery.png",
        caption="A traditional Sahrawi silver piece you will learn to create",
        use_container_width=True
    )
    st.markdown("""
    <div class="magic-card">
        <p style="text-align:center;">
        Each curve, each engraving, each detail carries the spirit of the desert —
        patience, precision, and identity.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">Unlock the next treasure: </div>', unsafe_allow_html=True)
    st.markdown("""<div class="magic-card"><p>Enter the code given to you by the artisan to open the next stop.</p></div>""", unsafe_allow_html=True)
    code = st.text_input("Enter code", placeholder="e.g. KENZQUEST2026", key=f"partner_code_gate_{next_stop_num}")
    if st.button("Unlock next stop", key=f"unlock_btn_{next_stop_num}", type="primary"):
        if code.strip() == PARTNER_ACCESS_CODE:
            st.session_state.current_stop = next_stop_num
            st.session_state.score += 10
            st.success("✅ Path Unlocked!")
            st.rerun()
        else:
            st.error("❌ Incorrect code. Try again.")

def show_stop2_cafe():
    render_location_notice(stop_titles[4])
    st.markdown('<h1 class="big-title">☕ Café Stop — A Moment to Breathe</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">🫖 Pause, sip, and discover Morocco</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="magic-card">
        <h3>🌿 Take a break, traveler</h3>
        <p>
        After your journey through stories and silver, it’s time to slow down.
        Sit, relax, and enjoy a glass of traditional Moroccan tea.
        </p>
        <p><strong>But in Morocco… even a tea break tells stories.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    st.image(
        "moroccan_tea.jpg",
        caption="Moroccan mint tea — a symbol of hospitality",
        use_container_width=True
    )
    st.info("💡 While you sip your tea… explore these incredible facts about Morocco.")
    st.markdown("### 🧬 Fact 1: Origins of Humanity")
    st.markdown("""
    <div class="magic-card">
        <p>
        In 2017, scientists discovered that human remains at <strong>Jebel Irhoud</strong>
        (near Marrakesh) are about <strong>300,000 years old</strong>.
        </p>
        <p>
        This makes them the <strong>oldest known Homo sapiens fossils</strong> ever found —
        meaning Morocco is one of the cradles of humanity.
        </p>
        <p><strong>🤯 Imagine: Humanity may have started right here.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    st.image("fact1.jpg", caption="", use_container_width=True)
    st.markdown("### 🏛️ Fact 2: Ancient Roman City")
    st.markdown("""
    <div class="magic-card">
        <p>
        <strong>Volubilis</strong>, near Meknès, was a major Roman city over 2,000 years ago.
        At its peak, it had temples, a basilica, and massive public buildings.
        </p>
        <p>
        Today, it’s a UNESCO World Heritage site — with real Roman mosaics still intact.
        </p>
        <p><strong>It’s like walking inside Ancient Rome… in Morocco.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    st.image("fact2.jpg", caption="", use_container_width=True)
    st.markdown("### 🎓 Fact 3: The Oldest University")
    st.markdown("""
    <div class="magic-card">
        <p>
        The <strong>University of al-Qarawiyyin</strong> in Fez was founded in 859 AD
        by <strong>Fatima al-Fihri</strong>.
        </p>
        <p>
        It is officially recognized as the <strong>oldest university in the world</strong>.
        </p>
        <p><strong>👩🏻‍💼 A woman founded it over 1,100 years ago.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    st.image("fact3.jpg", caption="", use_container_width=True)
    st.markdown("### 🌍 Fact 4: The Ultimate Traveler")
    st.markdown("""
    <div class="magic-card">
        <p>
        <strong>Ibn Battuta</strong>, from Tangier, traveled over <strong>117,000 km</strong>
        across Africa, Asia, and beyond.
        </p>
        <p>
        His journey lasted nearly 30 years — making him one of the greatest travelers in history.
        </p>
        <p><strong> He traveled further than Marco Polo.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    st.image("fact4.jpg", caption="", use_container_width=True)
    st.markdown("### 😂 Moroccan Break Time")
    st.markdown("""
    <div class="magic-card">
        <p style="font-size:1.2rem;">
        ليمونا دوزات امتحان، شحال جابت؟
        <br><strong>عسرة على عسرة 😭</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    show_quiz_challenge(2)
    if st.session_state.quiz_unlocked.get(2, False):
        if st.button("➡️ Continue the Journey", type="primary", use_container_width=True):
            st.session_state.current_stop = 3   # now goes straight to the Saadian riddle (Bab Agnaou quiz removed)
            st.rerun()
    else:
        st.warning("🔒 Complete all Knowledge Challenges to continue the journey.")

def show_stop3_riddle(): 
    render_location_notice(stop_titles[4])
    st.markdown('<h1 class="big-title">🧩 A Royal Secret Awaits</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">Solve to unlock the hidden dynasty</div>', unsafe_allow_html=True)
    st.markdown("""<div class="magic-card"><h3>Riddle</h3><p style="font-size:1.2rem;">I hold the stories of a royal line,
Hidden for centuries, away from time.
Intricate carvings mark my walls,
Where history whispers through my halls.
Visitors enter to see the past’s embrace,
A secret resting place in Marrakech’s space....</p></div>""", unsafe_allow_html=True)
    options = ["A) Bahia Palace", "B) El Badi Palace", "C) Saadian Tombs", "D) Koutoubia Mosque"]
    if "stop3_answer" not in st.session_state:
        st.session_state.stop3_answer = None
    if st.session_state.stop3_answer is None:
        cols = st.columns(2)
        for i, opt in enumerate(options):
            with cols[i % 2]:
                if st.button(opt, key=f"stop3_{i}", use_container_width=True):
                    st.session_state.stop3_answer = opt
                    st.rerun()
    else:
        if st.session_state.stop3_answer == "C) Saadian Tombs":
            st.success("✅ Correct! The hidden dynasty reveals itself... Continue to the Saadian Tombs!")
            if st.button("➡️ Continue to Saadian Tombs", type="primary", use_container_width=True):
                st.session_state.current_stop = 4
                st.session_state.score += 20
                st.rerun()
        else:
            st.error("❌ Not quite... try again.")
            if st.button("🔄 Retry Riddle", key="retry_stop3"):
                st.session_state.stop3_answer = None
                st.rerun()

def show_stop4_saadian():
    render_location_notice(stop_titles[5])
    st.markdown('<h1 class="big-title">🏛️ Saadian Tombs</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">✨ A hidden royal necropolis</div>', unsafe_allow_html=True)
    st.image("saadian_tombs.jpg", use_container_width=True)
    st.markdown("""
    <div class="magic-card">
        <h3>📜 A Lost Treasure Rediscovered</h3>
        <p>
        Built in the late 16th century by Sultan Ahmed al-Mansur, the Saadian Tombs were a masterpiece of Italian marble and gold leaf.
        </p>
        <p>
        When the Alawite dynasty rose to power, Sultan Moulay Ismail chose to wall off the site rather than destroy it. This was a deep sign of religious respect for the dead, which unintentionally turned the tombs into a perfectly preserved time capsule.
        </p>
        <p>For over 200 years, they remained a hidden sanctuary in the heart of Marrakech—until 1917, when aerial photography finally revealed the "lost" royal treasure from the sky.</p>
    </div>
    """, unsafe_allow_html=True)    
    st.markdown("""
    <div class="magic-card">
        <h3>💎 What makes it magical?</h3>
        <ul>
            <li>Royal Grandeur: Rare Italian Carrara marble and accents of pure gold commissioned by the "Golden Sultan."</li>
            <li>Artistic Mastery: A symphony of intricate Zellij tilework and hand-carved Muqarnas (honeycomb) plaster.</li>
            <li>The Crown Jewel: The famous hall of saadins tombs is considered one of the most stunning architectural monuments in Morocco.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.image("saadian_inside.jpg", use_container_width=True)
    show_quiz_challenge(4)
    if st.session_state.quiz_unlocked.get(4, False):
        if st.button("➡️ Continue to Zellige Workshop", type="primary", use_container_width=True):
            st.session_state.current_stop = 5
            st.rerun()
    else:
        st.warning("🔒 Complete all Knowledge Challenges to continue.")

def show_stop5_zellige_workshop():
    render_location_notice(stop_titles[6])
    st.markdown('<h1 class="big-title">🏺 Zellige Artisan Workshop</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">Discover the art of Moroccan tiles</div>', unsafe_allow_html=True)
    st.markdown("""<div class="magic-card"><p>Welcome to the Zellige workshop! Here you will see how Moroccan artisans craft these intricate geometric tiles by hand.</p></div>""", unsafe_allow_html=True)
    st.image("zellige_workshop.jpg", caption="Handcrafted Zellige Tiles YOU WILL BE MAKING AT THE SHOP", use_container_width=True)
    show_quiz_challenge(5)
    if st.session_state.quiz_unlocked.get(5, False):
        st.markdown('<h3 class="big-title">🔐 Partner Gate</h3>', unsafe_allow_html=True)
        st.markdown("""<div class="magic-card"><p>Enter partner code given to you by the zellige artisan master</p></div>""", unsafe_allow_html=True)
        code = st.text_input("", placeholder="e.g. KENZQUEST2026", key="code_gate_stop5")
        if st.button("Unlock next stop", key="unlock_stop5"):
            if code.strip() == PARTNER_ACCESS_CODE:
                st.session_state.current_stop = 6
                st.session_state.score += 10
                st.success("✅ Path unlocked! Onward to Moroccan cuisine class.")
                st.rerun()
            else:
                st.error("❌ Incorrect code. Try again.")
    else:
        st.warning("🔒 Complete all Knowledge Challenges to access the partner code gate.")

def show_stop6_cuisine():
    render_location_notice(stop_titles[7])
    st.markdown('<h1 class="big-title">🍲 Moroccan Cuisine Class — Taste & Create</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">👩‍🍳 Cook, savor, and discover Morocco</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="magic-card">
        <h3>🌿 Welcome, chef!</h3>
        <p>
        From the bustling markets of Marrakech to the calm kitchens of old medinas,
        Moroccan cuisine is a symphony of flavors. Today, you will get your hands on some iconic dishes —
        starting with <strong>Tangia</strong>, the Marrakech specialty slow-cooked in clay pots, not to be confused with tagine.
        </p>
        <p>
        Surrounding it, a feast unfolds:
        golden <strong>couscous</strong> with vegetables,
        rich <strong>harira</strong> soup,
        crispy <strong>briouates</strong>,
        fresh salads, olives, and perfectly grilled fish.
        </p>
        <p>
        And of course… no Moroccan table is complete without <strong>mint tea</strong>,
        a symbol of hospitality and sharing.
        </p>
        <p><strong>Get ready to cook, taste, and fall in love with Moroccan flavors!</strong></p>
    </div>
    """, unsafe_allow_html=True)
    st.image("moroccan_cuisine_table.jpg", caption="A Moroccan feast: Couscous, tangia, harira, briwat and so much more", use_container_width=True)
    st.markdown("### 📜 Moroccan Culinary Wonders")
    st.markdown("""
    <div class="magic-card">
        <p>
        Did you know? The <strong>tangia</strong> of Marrakech is named after the clay pot it’s cooked in, 
        traditionally slow-cooked in communal ovens. Saffron, preserved lemons, and local spices tell stories 
        of centuries of trade and culture.
        </p>
        <p>
        <strong>Harira</strong> was once the essential soup to break the fast during Ramadan, combining lentils, chickpeas, and tomatoes in a fragrant, hearty meal.
        </p>
        <p>
        Moroccan cuisine blends Arab, Berber, Andalusian, and Mediterranean influences — it's a living history what you are about to taste.
        </p>
    </div>
    """, unsafe_allow_html=True)
    show_quiz_challenge(6)
    if st.session_state.quiz_unlocked.get(6, False):
        st.markdown("---")
        st.markdown('<h3 class="big-title">🔐 Instructor Gate</h3>', unsafe_allow_html=True)
        st.markdown("""<div class="magic-card"><p>Enter the special code given to you by the Moroccan cuisine instructor...</p></div>""", unsafe_allow_html=True)
        code = st.text_input("Enter code from the instructor", placeholder="e.g. KENZQUEST2026", key="cuisine_code_gate")
        if st.button("🚀 Unlock Next Stop", type="primary", use_container_width=True):
            if code.strip() == PARTNER_ACCESS_CODE:
                st.session_state.current_stop = 7
                st.session_state.score += 10
                st.success("✅ Path Unlocked! Onward to the Koutoubia Mosque!")
                st.rerun()
            else:
                st.error("❌ Incorrect code.")
    else:
        st.warning("🔒 Complete all Knowledge Challenges to access the instructor code gate.")

def show_stop7_koutoubia():
    render_location_notice(stop_titles[8])
    st.markdown('<h1 class="big-title">🕌 Koutoubia Mosque</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">A Marrakech landmark of power, faith, and design</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="magic-card">
        <h3>✨ Why it matters</h3>
        <p>
        The Koutoubia is one of Marrakech’s most famous landmarks and a symbol of the city.
        Its minaret rises 77 meters above the medina and dominates the skyline. UNESCO highlights it as one of the
        major monuments of the Medina of Marrakesh. 
        It was built under the Almohads, a Berber-led movement/dynasty
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.image("koutoubia.jpg", use_container_width=True)
    show_quiz_challenge(7)
    st.markdown("""
        <div class="magic-card">
            <h3>🧵 Next stop: Berber Calligraphy</h3>
            <p>
            Now that you know that Koutoubia was built by the Almohad dynasty, a Berber empire. 
            Lets dive deep and learn the intricate Berber calligraphy — where letters become art and identity.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    try:
        st.image(
                "berber_calligraphy.jpg",
                caption="Berber calligraphy",
                use_container_width=True
            )
    except:
        st.warning("⚠️ Add 'berber_calligraphy.jpg' to your project.")
    
    st.markdown("### 🔐 Enter partner code given to you by the calligraphy artisan master")
    
    code = st.text_input(
            "Enter artisan code",
            placeholder="e.g. KENZQUEST2026",
            key="code_gate_koutoubia"
        )
    st.warning("🔒 Complete all Knowledge Challenges to continue.")
    if st.button("Unlock next stop", key="unlock_koutoubia") and st.session_state.quiz_unlocked.get(7, False):
        if code.strip() == PARTNER_ACCESS_CODE:
            st.session_state.current_stop = 8
            st.session_state.score += 10
            st.success("✅ Path unlocked!")
            st.rerun()
        else:
            st.error("❌ Incorrect code.")

def show_stop8_bahia():
    render_location_notice(stop_titles[9])
    st.markdown('<h1 class="big-title">🏛️ Bahia Palace</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">✨ A masterpiece of Moroccan elegance</div>', unsafe_allow_html=True)
    st.image("bahia_palace.jpg", use_container_width=True)
    st.markdown("""
    <div class="magic-card">
        <h3>👑 A Palace of Dreams</h3>
        <p>
        Built in the 19th century, Bahia Palace was designed to be the greatest palace of its time.
        </p>
        <p>
        With over <strong>150 rooms</strong>, peaceful gardens, fountains, and intricate decorations,
        it represents the peak of Moroccan craftsmanship.
        </p>
        <p><strong>🤯 Every ceiling, every tile, every door is handmade.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    st.image("bahia_inside.jpg", use_container_width=True)
    show_quiz_challenge(8)
    if st.session_state.quiz_unlocked.get(8, False):
        if st.button("➡️ Continue to Pottery Shop", type="primary", use_container_width=True):
            st.session_state.current_stop = 9
            st.session_state.score += 5
            st.rerun()
    else:
        st.warning("🔒 Complete all Knowledge Challenges to continue.")

def show_stop9_pottery():
    render_location_notice(stop_titles[10])
    st.markdown('<h1 class="big-title">🏺 Moroccan Pottery</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">✨ The art of earth and fire</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="magic-card">
        <h3>🌍 A Craft from the Earth</h3>
        <p>
        Moroccan pottery dates back thousands of years. Clay from the earth is shaped by hand,
        dried under the sun, and fired in traditional ovens.
        </p>
        <p>
        Each piece is unique — bowls, plates, tagines — all carrying patterns inspired by nature,
        geometry, and culture.
        </p>
        <p><strong>🔥 From earth… to fire… to art.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    st.image("pottery_workshop.jpg", use_container_width=True)
    st.markdown("""
    <div class="magic-card">
        <h3>                        What you will be making and taking home with you</h3>
        <p>
                            Mini moroccan tagines with the mesmerizing colors of your choice 💙💜❤️🩷🩵💚
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.image("pottery_products.jpg", use_container_width=True)
    show_quiz_challenge(9)
    if st.session_state.quiz_unlocked.get(9, False):
        st.markdown("""<div class="magic-card"><h3>🎁 Special Offer</h3><p>Give this code "Legacy_Ladies_2026" to your pottery master to enjoy <strong>40% off</strong></p></div>""", unsafe_allow_html=True)
        if not st.session_state.pottery_code_entered:
            code = st.text_input("Enter the pottery master code", placeholder="e.g. KENZQUEST2026", key="pottery_master_code")
            if st.button("Unlock Certificate", type="primary"):
                if code.strip() == PARTNER_ACCESS_CODE:
                    st.session_state.pottery_code_entered = True
                    st.success("✅ Correct! Your certificate is ready.")
                    st.rerun()
    else:
        st.warning("🔒 Complete all Knowledge Challenges to access the special offer.")
    if st.session_state.quiz_unlocked.get(9, False) and st.session_state.pottery_code_entered:
        user_name = st.text_input("Enter your name for your certificate:")
        if user_name:
            certificate_html = f"""
            <html>
            <head>
                <meta charset="utf-8">
                <title>Kenz Quest Certificate</title>
                <style>
                    body {{
                        font-family: 'Georgia', serif;
                        text-align: center;
                        padding: 60px;
                        margin: 30px;
                        background: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)),
                                    url('https://www.transparenttextures.com/patterns/arabesque.png');
                        border: 15px double #b8860b;
                    }}
                    h1 {{
                        color: #8b0000;
                        font-size: 42px;
                        margin-bottom: 10px;
                    }}
                    h2 {{
                        color: #b8860b;
                        margin-bottom: 30px;
                    }}
                    .name {{
                        font-size: 34px;
                        font-weight: bold;
                        margin: 30px 0;
                        color: #2c2c2c;
                    }}
                    .text {{
                        font-size: 18px;
                        line-height: 1.6;
                        margin: 20px 0;
                    }}
                    .footer {{
                        margin-top: 40px;
                        font-size: 16px;
                        color: #555;
                    }}
                </style>
            </head>
            <body>
    
                <h1>🏆 Certificate of Exploration</h1>
                <h2>Kenz Quest • Trésor Marocain</h2>
    
                <p class="text">This certificate is proudly awarded to</p>
    
                <div class="name">{user_name}</div>
    
                <p class="text">
        The Remarkable Traveler who followed the path of stories, craft, and memory
        across the heart of Morocco.
    </p>
    <p class="text">
        From the living stage of Jemaa el-Fna, to the delicate art of silver filigree,
        from moments of reflection over mint tea to the hidden majesty of the Saadian Tombs,
        you uncovered the layers of a land shaped by history and spirit.
    </p>
    
    <p class="text">
        You traced the geometry of Zellige, tasted the richness of Moroccan cuisine,
        stood before the timeless Koutoubia, wandered through the elegance of Bahia Palace,
        and finally shaped earth into art with your own hands through pottery.
    </p>
    
    <p class="text">
        Through curiosity, creativity, and a true explorer’s heart,
        you did not just visit Morocco —
        <strong>you experienced its soul.</strong>
    </p>
<div class="footer">
    🇲🇦 A journey through Moroccan heritage, craftsmanship, flavor, and architecture 🇲🇦
</div>
            </body>
            </html>
            """
            st.download_button("📄 Download Your Certificate", data=certificate_html.encode("utf-8"), file_name=f"Kenz_Quest_Certificate_{user_name}.html", mime="text/html")

# ---------------- ROUTING ----------------
if st.session_state.page == "home":
    st.markdown('<h1 class="big-title">Kenz Quest - مهمة الكنز</h1>', unsafe_allow_html=True)
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;600&display=swap');
.mini-tagline {
    font-family: 'Dancing Script', cursive;
    font-size: 16px;
    color: #c9a96e;
    text-align: center;
    margin-top: -10px;
}
</style>
<div class="mini-tagline">
Secrets of the past, creativity of the present. • أسرار الماضي، إبداع الحاضر
</div>
""", unsafe_allow_html=True)
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
    st.markdown('<h3 class="section-header">🗺️ Cliquez sur une province / اضغط على عمالة</h3>', unsafe_allow_html=True)
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
    # ---------------- MAIN QUEST ROUTING  ----------------
    current = st.session_state.current_stop
    total_stops = 9   
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
    elif current == 2:
        show_stop2_cafe()
    elif current == 3:
        show_stop3_riddle()   #
    elif current == 4:
        show_stop4_saadian()
    elif current == 5:
        show_stop5_zellige_workshop()
    elif current == 6:
        show_stop6_cuisine()
    elif current == 7:
        show_stop7_koutoubia()
    elif current == 8:
        show_stop8_bahia()
    elif current == 9:
        show_stop9_pottery()
    st.markdown(f"""<p style='text-align:center; opacity:0.7;'>📍 Step {current} of {total_stops}</p>""", unsafe_allow_html=True)
