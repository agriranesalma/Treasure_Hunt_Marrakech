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
if "stop4_zellige_correct" not in st.session_state:
    st.session_state.stop4_zellige_correct = False
if "stop4_partner_unlocked" not in st.session_state:
    st.session_state.stop4_partner_unlocked = False
if "koutoubia_quiz_done" not in st.session_state:
    st.session_state.koutoubia_quiz_done = False
if "bahia_quiz_done" not in st.session_state:
    st.session_state.bahia_quiz_done = False
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
    "But this square is not only a place of stories and music — it is also a place of memory. "
    "In the 1950s, as Morocco faced the challenges of the French Protectorate, spaces like this became silent witnesses "
    "to unity, resistance, and the voice of a people determined to reclaim their future. "
    "That same spirit lives on in national milestones, such as the historic visit of His Majesty King Mohammed V to "
    "M’Hamid El Ghizlane and the southern provinces, and the commemoration of the departure of the last foreign soldier "
    "from the Moroccan Sahara. Together, these moments tell one story: a nation standing for its sovereignty, its unity, "
    "and its enduring identity."
),

"legend": (
    "Long before and beyond politics, Marrakech has also been protected in another way. "
    "According to legends, the city is encircled by the spiritual presence of the Seven Saints — a sacred path that has "
    "guided and guarded it since centuries. "
    "Inspired by figures such as Abu al-Abbas al-Sabti, this invisible circle represents faith, protection, and the deep "
    "spiritual roots woven into the soul of the city."
),

"transition": (
    "And just like these stories and traditions, the life of this square did not begin here. "
    "The merchants, the music, the knowledge — all traveled from far beyond the city walls, carried by caravans from the deep south. "
    "Now, it’s your turn to follow that path. Let’s walk the Silver Path, to discover where desert craftsmanship meets the heart of Marrakech."
    )
,"next_stop_label": "Hassani Silver Filigree Artisan",
"next_stop_intro": "The next stop is a Hassani Silver Filigree artisan, where the treasure changes from stories to craft.",
}}

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
            <p>The Genie is excited to guide you through Morocco’s living memory.</p>
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
    st.markdown('<div class="tag-subtitle">✨ A square of memory, rhythm, and living history</div>', unsafe_allow_html=True)

    # ---------------- HOOK ----------------
    st.markdown(f"""
    <div class="magic-card">
        <h3>⭐ The Living Stage</h3>
        <p>{stop["hook"]}</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- UNESCO ----------------
    st.markdown(f"""
    <div class="magic-card">
        <h3>🏛️ A World Treasure</h3>
        <p>{stop["unesco"]}</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- ATMOSPHERE ----------------
    st.markdown(f"""
    <div class="magic-card">
        <h3>🎭 What surrounds you</h3>
        <p>{stop["atmosphere"]}</p>
        <p><em>You may hear deep rhythms... ancient songs... names carried through generations.</em></p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- HINT TO GENIE ----------------
    st.markdown("""
    <div class="magic-card">
        <h3>🎶 A hidden story in the music</h3>
        <p>
        Some songs in this square are not just music — they are memory.
        Names like <strong>Lalla Aïcha</strong> echo through the rhythms of <strong>Gnawa</strong>.
        But their meaning… is not written here.
        </p>
        <p><strong>Ask the Genie below. She remembers what history did not write.</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- WEBAR GENIE ----------------
    st.markdown("### 🧞 The Genie Speaks")

    genie_stop1_url = "https://mywebar.com/p/Project_2_ncf4wq5286"

    components.iframe(genie_stop1_url, height=700, scrolling=True)

    # ---------------- PRIVACY REMINDER ----------------
    st.markdown("""
    <div class="notice">
        🔒 <strong>Privacy Reminder:</strong> This experience does NOT store your image or any personal data.
    </div>
    """, unsafe_allow_html=True)

    # ---------------- NATIONAL MEMORY ----------------
    st.markdown(f"""
    <div class="magic-card">
        <h3>🇲🇦 Memory & Sovereignty</h3>
        <p>{stop["national_memory"]}</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- LEGEND ----------------
    st.markdown(f"""
    <div class="magic-card">
        <h3>🔱 The Circle of Protection</h3>
        <p>{stop["legend"]}</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- TRANSITION ----------------
    st.markdown(f"""
    <div class="magic-card">
        <h3>🛤️ The Journey Continues</h3>
        <p>{stop["transition"]}</p>
        <p><strong>Next Stop:</strong> {stop.get("next_stop_intro", "Follow the Silver Path to the next hidden treasure.")}</p>
    </div>
    """, unsafe_allow_html=True)
     # ---------------- HASSANI POETRY INTERLUDE ----------------
    st.markdown("""
    <div class="magic-card">
        <h3>🐪 On the road to the South...</h3>
        <p>
        As you walk toward the artisan of silver, remember: the desert does not only trade goods —
        it carries words, rhythm, and poetry.
        </p>
        <p>
        Let me tell you a little about <strong>Hassani poetry</strong>, a poetic tradition from the southern regions of Morocco,
        where language flows like the dunes and memory is passed through verse.
        </p>
        <p><em>Here is a small glimpse of that world:</em></p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### 🎧 Listen to Hassani Poetry")

    st.info("💡 Tip: Use headphones for an immersive experience.")
    st.image(
    "sahara.png",
    caption="The Sahara — where poetry travels with the wind",
    use_container_width=True
    )
    if st.button("🎧 Play the voice of the desert"):
        audio_file = open("hassani_poetry.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")

def show_partner_code_gate(next_label, next_stop_num):
    st.markdown('<h2 class="big-title"> Silver Path Gate</h2>', unsafe_allow_html=True)
    st.markdown(f'<div class="tag-subtitle">Unlock the next treasure: {next_label}</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="magic-card">
        <p>Enter the code given to you by the artisan to open the next stop.</p>
    </div>
    """, unsafe_allow_html=True)

    code = st.text_input("Enter code", placeholder="e.g. KENZQUEST2026", key=f"code_gate_{next_stop_num}")
    if st.button("Unlock next stop", key=f"unlock_{next_stop_num}", type="primary"):
        if code.strip() == PARTNER_ACCESS_CODE:
            st.session_state.current_stop = next_stop_num
            st.session_state.stop1_phase = "welcome"  # reset for future revisits
            st.session_state.score += 10
            st.success("✅ Path Unlocked!")
            st.session_state.current_stop = 2
            st.rerun()
        else:
            st.error("❌ Incorrect code. Try again.")


def show_stop2_cafe():
    st.markdown('<h1 class="big-title">☕ Café Stop — A Moment to Breathe</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">🫖 Pause, sip, and discover Morocco</div>', unsafe_allow_html=True)

    # ---------------- INTRO ----------------
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

    # ---------------- TEA IMAGE ----------------
    st.image(
        "moroccan_tea.jpg",
        caption="Moroccan mint tea — a symbol of hospitality",
        use_container_width=True
    )

    st.info("💡 While you sip your tea… explore these incredible facts about Morocco.")

    # ================== FACT 1 ==================
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

    # IMAGE PLACEHOLDER
    st.image("fact1.jpg", caption="", use_container_width=True)

    # ================== FACT 2 ==================
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

    # ================== FACT 3 ==================
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

    # ================== FACT 4 ==================
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

    # ================== FUN MOMENT ==================
    st.markdown("### 😂 Moroccan Break Time")

    st.markdown("""
    <div class="magic-card">
        <p style="font-size:1.2rem;">
        ليمونا دوزات امتحان، شحال جابت؟  
        <br><strong>عسرة على عسرة 😭</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ================== TRANSITION ==================
    st.markdown("""
    <div class="magic-card">
        <h3>🧭 Ready to continue?</h3>
        <p>
        Your journey continues beyond the café…
        more stories, more craftsmanship, more treasures await.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("➡️ Continue the Journey"):
        st.session_state.current_stop = 3
        st.rerun()

def show_stop3_riddle():
    st.markdown('<h1 class="big-title">🧩 A Royal Secret Awaits</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">Solve to unlock the hidden dynasty</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="magic-card">
            <h3>Riddle</h3>
            <p style="font-size:1.2rem;">
        I am a masterpiece hidden behind high walls, where silence speaks in marble and gold. 
        I was not built for the living, yet I am one of the most visited houses in the Ochre City.
        Twelve columns of stone hold up my ceiling, and intricate tiles tell stories of a golden age. 
        I was kept a secret by time itself until the world looked down from the clouds to find me.
        What am I?
            </p>
        </div>
        """, unsafe_allow_html=True)

    options = [
        "A) Bahia Palace",
        "B) El Badi Palace",
        "C) Saadian Tombs",
        "D) Koutoubia Mosque"
    ]

    if "stop3_answer" not in st.session_state:
        st.session_state.stop3_answer = None

    cols = st.columns(2)

    for i, opt in enumerate(options):
        with cols[i % 2]:
            if st.button(opt, key=f"stop3_{i}", use_container_width=True):
                st.session_state.stop3_answer = opt
                st.rerun()

    if st.session_state.stop3_answer:
        if st.session_state.stop3_answer == "C) Saadian Tombs":
            st.success("✅ Correct! The hidden dynasty reveals itself...")
            st.session_state.current_stop = 4
            st.session_state.score += 20
            st.rerun()
        else:
            st.error("❌ Not quite... try again.")
            if st.button("🔄 Retry"):
                st.session_state.stop3_answer = None
                st.rerun()
def show_stop4_saadian():
    st.markdown('<h1 class="big-title">🏛️ Saadian Tombs</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">✨ A hidden royal necropolis</div>', unsafe_allow_html=True)

    # IMAGE PLACEHOLDER
    st.image("saadian_tombs.jpg", caption="", use_container_width=True)

    # HISTORY
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

    # WONDERS
    st.markdown("""
    <div class="magic-card">
        <h3>💎 What makes it magical?</h3>
        <ul>
            <li>Royal Grandeur: Rare Italian Carrara marble and accents of pure gold commissioned by the "Golden Sultan."</li>
            <li>Artistic Mastery: A symphony of intricate Zellij tilework and hand-carved Muqarnas (honeycomb) plaster.</li>
            <li>The Crown Jewel: The legendary Hall of Twelve Columns—widely considered one of the most stunning architectural monuments in Morocco.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # SECOND IMAGE PLACEHOLDER
    st.image("saadian_inside.jpg", caption="", use_container_width=True)

    # QUIZ TRANSITION
    st.markdown("""
    <div class="magic-card">
        <h3>🔍 Look closely...</h3>
        <p>
        Around you, the lower walls and the floor are covered with intricate geometric patterns.
        This art form is one of Morocco’s most iconic traditions.
        </p>
        <p><strong>Can you name it?</strong></p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("zelige_form"):
        user_answer = st.text_input("Enter your answer:")
        submitted = st.form_submit_button("Submit Answer")
    
        if submitted:
            if user_answer.lower().strip() in ["zellige", "zellij", "zellige tile"]:
                st.success("🎉 Correct! You have the eye of a true explorer.")
                st.session_state.current_stop = 5
                st.session_state.score += 15  # optional reward
                st.rerun()
            else:
                st.error("❌ Not quite... look closer at the patterns around you.")


def show_stop5_zellige_workshop():
    st.markdown('<h1 class="big-title">🏺 Zellige Artisan Workshop</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">Discover the art of Moroccan tiles</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="magic-card">
        <p>
        Welcome to the Zellige workshop! Here you will see how Moroccan artisans craft these intricate geometric tiles by hand.
        Each piece tells a story — centuries of culture and geometry in color.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # IMAGE
    st.image("zellige_workshop.jpg", caption="Handcrafted Zellige Tiles YOU WILL BE MAKING AT THE SHOP", use_container_width=True)

    # OPTIONAL: Partner code gate to go to Stop 6
    code = st.text_input("Enter partner code to continue", placeholder="e.g. KENZQUEST2026", key="code_gate_stop5")
    if st.button("Unlock next stop", key="unlock_stop5"):
        if code.strip() == PARTNER_ACCESS_CODE:
            st.session_state.current_stop = 6  # next stop (Moroccan cuisine)
            st.session_state.score += 10
            st.success("✅ Path unlocked! Onward to Moroccan cuisine class.")
            st.rerun()
        else:
            st.error("❌ Incorrect code. Try again.")
def show_partner_zellige_gate(next_label="Zellige Artisan Workshop", next_stop_num=5):
    st.markdown('<h2 class="big-title">🔐 Artisan Path Gate</h2>', unsafe_allow_html=True)
    st.markdown(f'<div class="tag-subtitle">Unlock the next treasure: {next_label}</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="magic-card">
        <p>To continue your journey, enter the special partner code provided by the artisan workshop.</p>
    </div>
    """, unsafe_allow_html=True)

    code = st.text_input(
        "Enter code here", 
        placeholder=f"e.g. {PARTNER_ACCESS_CODE}", 
        key=f"code_gate_{next_stop_num}"
    )

    if st.button("Unlock next stop", key=f"unlock_{next_stop_num}", type="primary"):
        if code.strip() == PARTNER_ACCESS_CODE:
            st.session_state.current_stop = next_stop_num 
            st.session_state.score += 10
            st.success(f"✅ Path Unlocked! You are now heading to {next_label}.")
            st.session_state.stop5_visited = True
            st.rerun()
        else:
            st.error("❌ Incorrect code. Try again.")
def show_stop6_cuisine():
    st.markdown('<h1 class="big-title">🍲 Moroccan Cuisine Class — Taste & Create</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">👩‍🍳 Cook, savor, and discover Morocco</div>', unsafe_allow_html=True)

    # ---------------- INTRO ----------------
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

    # ---------------- IMAGE ----------------
    st.image(
        "moroccan_cuisine_table.jpg", 
        caption="A Moroccan feast: Couscous, pastilla, harira, and more",
        use_container_width=True
    )

    # ---------------- FUN HISTORY ----------------
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
        Moroccan cuisine blends Arab, Berber, Andalusian, and Mediterranean influences — making it a living history you can taste.
        </p>
        <p><strong>😋 Imagine the aroma of spices filling your kitchen as you cook!</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- MINI TIP ----------------
    st.info("💡 Tip: While imagining your meal, think about the stories every ingredient tells — every spice has a history.")

    # ---------------- KOUTOUBIA QUIZ ----------------
    st.markdown("### 🕌 Final taste-test question")
    
    with st.form("cuisine_to_koutoubia_form"):
        answer = st.text_input(
            "Which monument should you visit next?",
            placeholder="Type the name of the monument"
        )
        submitted = st.form_submit_button("Submit Answer")
    
        if submitted:
            if answer.lower().strip() in ["koutoubia", "koutoubia mosque", "kutubiyya", "kutubiyyah"]:
                st.success("✅ Correct! Your journey continues to Koutoubia.")
                st.session_state.current_stop = 7
                st.session_state.score += 10
                st.rerun()
            else:
                st.error("❌ Not quite — think of Marrakech’s famous landmark with the tall minaret.")
                st.error("❌ Incorrect code. Try again.")
def show_stop7_koutoubia():
    st.markdown('<h1 class="big-title">🕌 Koutoubia Mosque</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">A Marrakech landmark of power, faith, and design</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="magic-card">
        <h3>✨ Why it matters</h3>
        <p>
        The Koutoubia is one of Marrakech’s most famous landmarks and a symbol of the city.
        Its minaret rises 77 meters above the medina and dominates the skyline. UNESCO highlights it as one of the
        major monuments of the Medina of Marrakesh. :contentReference[oaicite:4]{index=4}       <p>
        It was built under the Almohads, a Berber-led movement/dynasty, so in your story you can proudly say:
        this is part of Morocco’s Berber heritage. :contentReference[oaicite:6]{index=6}   </div>
    """, unsafe_allow_html=True)

    st.image(
        "koutoubia.jpg",
        caption="(Add image of Koutoubia here)",
        use_container_width=True
    )

    st.markdown("### 🧩 Mini quiz: look closely at the minaret")

    with st.form("koutoubia_arches_form"):
        arches = st.text_input(
            "How many arches are at the top?",
            placeholder="Type a number"
        )
    
        submitted = st.form_submit_button("Check Answer")
    
        if submitted:
            if arches.strip().lower() in ["4", "four"]:
                st.session_state.koutoubia_quiz_done = True
                st.success("✅ Correct! The topmost tier has four intersecting polylobed arches.")
            else:
                st.error("❌ Not quite — try again.")
    if st.session_state.koutoubia_quiz_done:
    
        st.markdown("""
        <div class="magic-card">
            <h3>🧵 Next stop: Berber Calligraphy</h3>
            <p>
            Now that you have decoded the geometry of Koutoubia, your next treasure leads to the world of
            Berber calligraphy — where letters become art and identity.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
        # ✅ SAFE IMAGE (avoid crash)
        try:
            st.image(
                "berber_calligraphy.jpg",
                caption="Berber calligraphy",
                use_container_width=True
            )
        except:
            st.warning("⚠️ Add 'berber_calligraphy.jpg' to your project.")
    
        st.markdown("### 🔐 Enter the artisan code to continue")
    
        code = st.text_input(
            "Enter artisan code",
            placeholder="e.g. KENZQUEST2026",
            key="code_gate_koutoubia"
        )
    
        if st.button("Unlock next stop", key="unlock_koutoubia"):
            if code.strip() == PARTNER_ACCESS_CODE:
                st.session_state.current_stop = 8
                st.session_state.score += 10
                st.success("✅ Path unlocked!")
                st.rerun()
            else:
                st.error("❌ Incorrect code.")
def show_stop8_bahia():
    st.markdown('<h1 class="big-title">🏛️ Bahia Palace</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">✨ A masterpiece of Moroccan elegance</div>', unsafe_allow_html=True)

    # IMAGE
    try:
        st.image("bahia_palace.jpg", use_container_width=True)
    except:
        st.warning("⚠️ Add bahia_palace.jpg")

    # HISTORY / WOW
    st.markdown("""
    <div class="magic-card">
        <h3>👑 A Palace of Dreams</h3>
        <p>
        Built in the 19th century, Bahia Palace was designed to be the greatest palace of its time.
        Its name means <strong>“Brilliance”</strong>.
        </p>
        <p>
        With over <strong>150 rooms</strong>, peaceful gardens, fountains, and intricate decorations,
        it represents the peak of Moroccan craftsmanship.
        </p>
        <p><strong>🤯 Every ceiling, every tile, every door is handmade.</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # SECOND IMAGE
    try:
        st.image("bahia_inside.jpg", use_container_width=True)
    except:
        pass

    # QUIZ
    st.markdown("### 🧩 Final Palace Challenge")

    with st.form("bahia_quiz"):
        answer = st.text_input(
            "What does 'Bahia' mean?",
            placeholder="Hint: something beautiful..."
        )

        submitted = st.form_submit_button("Submit Answer")

        if submitted:
            if answer.lower().strip() in ["brilliance", "brilliant", "beauty"]:
                st.session_state.bahia_quiz_done = True
                st.success("✅ Correct! You truly understand Moroccan elegance.")
            else:
                st.error("❌ Not quite — think of beauty and brilliance.")

    # NEXT STEP (OUTSIDE FORM)
    if st.session_state.bahia_quiz_done:

        st.markdown("""
        <div class="magic-card">
            <h3>🏺 Final Stop: Moroccan Pottery</h3>
            <p>
            From palaces to clay… your journey now leads to one of Morocco’s oldest crafts:
            pottery. Where earth becomes art.
            </p>
        </div>
        """, unsafe_allow_html=True)

        try:
            st.image("moroccan_pottery.jpg", use_container_width=True)
        except:
            st.warning("⚠️ Add moroccan_pottery.jpg")

        st.markdown("### 🔐 Enter artisan code to finish your journey")

        code = st.text_input(
            "Enter final artisan code",
            placeholder="e.g. KENZQUEST2026",
            key="code_gate_bahia"
        )

        if st.button("Unlock Final Stop"):
            if code.strip() == PARTNER_ACCESS_CODE:
                st.session_state.current_stop = 9
                st.session_state.score += 10
                st.success("🎉 Final path unlocked!")
                st.rerun()
            else:
                st.error("❌ Incorrect code.")
def show_stop9_pottery():
    st.markdown('<h1 class="big-title">🏺 Moroccan Pottery</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">✨ The art of earth and fire</div>', unsafe_allow_html=True)

    try:
        st.image("pottery_workshop.jpg", use_container_width=True)
    except:
        st.warning("⚠️ Add pottery_workshop.jpg")

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

    try:
        st.image("pottery_products.jpg", use_container_width=True)
    except:
        pass

    st.markdown("""
    <div class="magic-card">
        <h3>🎉 Congratulations, Explorer!</h3>
        <p>
        You have completed the Kenz Quest journey through Marrakech.
        From stories and dynasties to crafts and cuisine — you’ve experienced Morocco’s living heritage.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.success(f"🏆 Final Score: {st.session_state.score}")
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
            st.markdown("---")
            # ---------------- ARTISAN EXPERIENCE PREVIEW ----------------
            st.markdown("""
            <div class="magic-card">
                <h2 style="text-align:center;">✨ Your Next Experience</h2>
                <p style="text-align:center; font-size:1.2rem;">
                During your visit to the artisan workshop, you won’t just observe…
                <br><strong>You will create.</strong>
                </p>
                <p style="text-align:center;">
                Guided by a master artisan, you will craft your own piece of
                <strong>Moroccan Sahrawi silver jewelry</strong>,
                inspired by traditions passed down through generations.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # ---------------- JEWELRY IMAGE ----------------
            st.image(
                "sahrawijewlery.png",  # <-- rename your file like this
                caption="A traditional Sahrawi silver piece you will learn to create",
                use_container_width=True
            )
            
            # ---------------- EXTRA IMMERSION ----------------
            st.markdown("""
            <div class="magic-card">
                <p style="text-align:center;">
                Each curve, each engraving, each detail carries the spirit of the desert —
                patience, precision, and identity.
                </p>
                <p style="text-align:center; font-weight:bold;">
                </p>
            </div>
            """, unsafe_allow_html=True)
            # Optional: if I want the code gate right after the story
            st.markdown("### 🔐 Partner business gate")
            show_partner_code_gate(
                next_label=stops_data[1].get("next_stop_label", "Next Hidden Stop"),
                next_stop_num=2
            )

    elif current == 2:
        show_stop2_cafe()
    elif current == 3:
        show_stop3_riddle()
    elif current == 4:
        show_stop4_saadian()
    elif current==5:
        show_stop5_zellige_workshop()
    elif st.session_state.current_stop == 6:
        show_stop6_cuisine()
    elif current == 6:
        show_stop6_cuisine()
    elif current == 7:
        show_stop7_koutoubia()
    elif current == 8:
        show_stop8_bahia()
    elif current==9:
        show_stop9_pottery()
    st.markdown(f"""
        <p style='text-align:center; opacity:0.7;'>
        📍 Step {current} of {total_stops}
        </p>
        """, unsafe_allow_html=True)
