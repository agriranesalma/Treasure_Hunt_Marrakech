import streamlit as st
from PIL import Image
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
[data-testid="stHeader"] { background: transparent !important; }
.main .block-container { padding-top: 0rem !important; padding-left: 3% !important; padding-right: 3% !important; max-width: 95% !important; }
.big-title {
    font-family: 'Kaushan Script', cursive !important;
    font-size: 5rem !important;
    font-weight: 900 !important;
    text-align: center !important;
    background: linear-gradient(to right, #e31e24 40%, #ffffff 50%, #006400 60%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    display: block !important;
    line-height: 1.2 !important;
    margin-bottom: 0px !important;
    -webkit-text-stroke: 4px rgba(255,255,255,0.1);
}
.tag-subtitle {
    font-size: clamp(1.5rem, 5vw, 3rem);
    font-weight: 800;
    text-align: center;
    color: white !important;
    text-shadow: 2px 2px 15px rgba(0,0,0,1);
    margin-top: 2rem !important;
    margin-bottom: 2rem;
    letter-spacing: 2px;
}
.commemoration-banner {
    background: rgba(139, 0, 0, 0.85);
    padding: 15px 30px;
    border-radius: 15px;
    text-align: center;
    font-size: 1.35rem;
    font-weight: 700;
    margin: 20px auto;
    border: 3px solid #006400;
    box-shadow: 0 0 30px rgba(0,100,0,0.6);
}
.gps-tracker {
    display: inline-block;
    background: linear-gradient(90deg, #00c853, #00ff88);
    color: #000;
    padding: 12px 30px;
    border-radius: 50px;
    font-size: 1.25rem;
    font-weight: 700;
    box-shadow: 0 0 25px #00ff88;
    animation: pulse 2s infinite;
    text-align: center;
    margin: 15px auto;
    letter-spacing: 1px;
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
</style>
""", unsafe_allow_html=True)

# ====================== SESSION STATE ======================
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
riddle_url_stop1 = "https://mywebar.com/p/Project_1_to00xjn24"

webar_urls = {
    1: riddle_url_stop1,
    2: "https://mywebar.com/p/stop3-artisanal",          # Hassani Artisanetshop
    3: "https://mywebar.com/p/stop2-cafe-koutoubia",     # Café de France
    4: "https://mywebar.com/p/stop4-fontaine-saadian",   # Saadian Tombs
    5: "https://mywebar.com/p/stop5-bahia-palace",       # Zellige Workshop (replace with your new link)
    6: "https://mywebar.com/p/stop6-food-place",   # Food Workshop (replace with your new link)
    7: "https://mywebar.com/p/stop7-koutoubia",                                 # Koutoubia – replace with your new link
    8: "https://mywebar.com/p/stop8-bahia-palace",                                 # Bahia Palace – replace with your new link
    9: "https://mywebar.com/p/stop9-final-stop"    # Final Pottery
}

# ====================== FULL STOP DATA ======================
stops_data = {
    1: {  # Jemaa el-Fna
        "riddle_options": ["A) Bab Agnaou", "B) Jemaa el-Fna – The Square of Storytellers", "C) Mouassine Square", "D) Koutoubia Gardens"],
        "correct_riddle": "B) Jemaa el-Fna – The Square of Storytellers",
        "learning": """For centuries this square has been the ultimate meeting point where caravans from every corner of Morocco arrived with spices, tales, and dreams. Storytellers still gather circles of people exactly as they did when Berber bards travelled from the south, renewing the oral traditions that UNESCO protects today.""",
        "mini_question": "Look around the square right now: what is the one thing sold from dozens of bright orange stalls that everyone drinks fresh?",
        "mini_options": ["A) Pomegranate juice", "B) Fresh orange juice", "C) Lemon mint", "D) Date milk"],
        "correct_mini": "B) Fresh orange juice",
        "mini_explanation": "Marrakech’s legendary fresh-squeezed orange juice is a daily ritual here!",
        "clue": "The caravans always stopped for a sweet break after long journeys. Follow the scent of mint and sugar to the Hassani treasures at **Ensemble Artisanal**!"
    },
    2: {  # Hassani Artisanat
        "title": "Stop 2 – Hassani Treasures",
        "description": "You’ve arrived at the heart of southern craftsmanship! Hassani artisans are world-famous for their intricate silver jewelry, hand-woven haima tents, and delicate embroidery.",
        "learning": """The Hassani people created poetry and crafts that travelled the same caravan routes you’re following. Their silver pieces shine like stars in the dunes. One ancient Hassani line says the desert wind carries messages of unity across the sands… just like the peaceful Green March of 1975 when hundreds of thousands walked with the Quran and flags to bring the south home forever. In 2026 we celebrate 50 years since the last foreign soldier left — the day Morocco became whole again.""",
        "clue": "After tasting the south’s beauty, it’s time for something sweet and relaxing. Head to the famous café where travelers have rested for over a century: **Café de France**!"
    },
    3: {  # Café de France
        "title": "Stop 3 – Café de France: Mint Tea & Legends",
        "learning": """Café de France opened in 1912 and quickly became the favourite rest stop for explorers and locals. Moroccan tea isn’t just a drink — it’s a ritual: the first glass is bitter like life, the second sweet like love, the third gentle like death. Teens love this: the teapot is poured from high up to create “the crown” of bubbles — basically Moroccan latte art with attitude!""",
        "mini_question": "Why do Moroccans pour tea from so high up?",
        "mini_options": ["A) To cool it faster", "B) To show off", "C) To create bubbles that mean ‘welcome’"],
        "correct_mini": "C) To create bubbles that mean ‘welcome’",
        "mini_explanation": "The bubbles are the sign of hospitality — the higher the pour, the bigger the welcome!",
        "clue": "Feeling refreshed? The next stop hides royal secrets and dazzling walls. Follow the scent of history to the **Saadian Tombs**!"
    },
    4: {  # Saadian Tombs
        "title": "Stop 4 – Saadian Tombs: Hidden Royal Glory",
        "learning": """Built in the late 1500s by Sultan Ahmad al-Mansur, these tombs are pure Moroccan magic: 60 rooms of zellige mosaics, cedar ceilings carved like lace, and marble columns that glow like pearls. The Saadians came from the south and used Sahara gold to create this masterpiece. For 200 years the tombs were completely sealed and forgotten — until 1917 when French pilots spotted them from the sky!""",
        "mini_question": "The lower walls of the Chamber of the Mihrab are covered in colourful geometric tiles. What is the traditional Moroccan name for this mosaic art?",
        "mini_options": ["A) Granite", "B) Zellige", "C) Stained glass", "D) Cedar wood"],
        "correct_mini": "B) Zellige",
        "mini_explanation": "Zellige is hand-cut glazed tiles fitted like a puzzle — the crown jewel of Moroccan design!",
        "clue": "Those shimmering zellige walls were made by master artisans. Your next stop is where you can see them being created live: a traditional **Zellige Workshop** in the medina!"
    },
    5: {  # Zellige Workshop
        "title": "Stop 5 – Zellige Workshop",
        "learning": """Here you watch artisans cut tiny pieces of glazed clay and fit them into perfect patterns — the same technique used in the Saadian Tombs and royal palaces for 500 years. Each tile is a tiny work of art that turns walls into living stories.""",
        "clue": "After the beauty of zellige, it’s time to taste Morocco! Follow the spice trail to a traditional food experience where YOU help prepare lunch."
    },
    6: {  # Moroccan Food Workshop
        "title": "Stop 6 – Traditional Moroccan Lunch Workshop",
        "learning": """You just made your own tajine or couscous! The secret? Slow-cooked spices that travelled the same caravans from the south. Every ingredient tells a story of unity — saffron from the Atlas, cumin from the Sahara routes. Eating together is how Moroccans have always celebrated life.""",
        "clue": "Full and happy? The next treasure towers over the whole city — the iconic **Koutoubia Mosque**!"
    },
    7: {  # Koutoubia
        "title": "Stop 7 – Koutoubia Mosque",
        "learning": """The Koutoubia was founded by the Almoravids — fierce Saharan Berber warriors who built Marrakech itself in 1070. Its 77-metre minaret is the symbol of the city and has guided caravans for 900 years. The golden orbs on top represent the unity of faith and land.""",
        "mini_question": "How many golden orbs sit atop the Koutoubia minaret?",
        "mini_options": ["A) 3", "B) 4", "C) 5", "D) 7"],
        "correct_mini": "C) 5",
        "mini_explanation": "The five orbs are a classic Moroccan architectural detail symbolising balance and unity.",
        "clue": "From the mosque’s shadow, follow the royal path to the breathtaking **Bahia Palace**!"
    },
    8: {  # Bahia Palace
        "title": "Stop 8 – Bahia Palace",
        "learning": """‘Bahia’ means ‘the beautiful’. Built in the 19th century with 160 rooms, stunning gardens, and zellige everywhere, it was designed as a dream of harmony — exactly the unity the caravans always carried between north and south.""",
        "clue": "One last treasure awaits… the pottery workshop where your journey becomes permanent!"
    },
    9: {  # Final Pottery Workshop
        "title": "Stop 9 – Lamsaty Pottery Workshop – The Final Treasure!",
        "special": True,
        "message": "🎉 You completed the Caravan of Unity! You walked the same path as the ancient caravans that kept Morocco connected for centuries.",
        "discount_code": "KENZ2026",
        "certificate_text": """🌟 TREASURE MAP CERTIFICATE 🌟
Kenz Quest – Trésor Marocain
Certificate of the Caravan of Unity

Adventurer: {name}

You have followed the ancient caravan route through:
1. Jemaa el-Fna – Heart of Stories
2. Hassani Artisanat – Southern Silver & Poetry
3. Café de France – Mint Tea & Legends
4. Saadian Tombs – Hidden Royal Glory
5. Zellige Workshop – Living Mosaics
6. Moroccan Lunch – Flavours of Unity
7. Koutoubia – Beacon of the Kingdom
8. Bahia Palace – Dream of Harmony
9. Lamsaty Pottery – Eternal Memory

You are now an official Guardian of Morocco’s Living Memory.
In 2026 we celebrate the 68ᵉ anniversaries and 50 years of full sovereignty — you helped keep that flame alive.

Date: March 2026
Signature of the Genie 🧞‍♂️"""
    }
}

# ====================== HOME PAGE ======================
if st.session_state.page == "home":
    st.markdown('<h1 class="big-title">Kenz Quest - مهمة الكنز</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">Explore Morocco Culturally • اكتشف المغرب</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="commemoration-banner">
        En commémoration du 68ᵉ anniversaire de la visite historique de Feu SM le Roi Mohammed V à M'Hamid El Ghizlane et aux provinces du Sud<br>
        • 68ᵉ anniversaire de la Bataille de Dchira • 50ᵉ anniversaire de la souveraineté retrouvée
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

# ====================== MARRAKECH-SAFI MAP ======================
elif st.session_state.page == "marrakech_safi":
    st.markdown('<h1 class="big-title">Marrakech-Safi</h1>', unsafe_allow_html=True)
    st.markdown('<div class="tag-subtitle">📍 مراكش آسفي • Point de départ de la Mémoire Nationale</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="commemoration-banner" style="font-size:1.1rem; padding:10px 20px;">
        Votre chasse au trésor commence ici – et relie directement Marrakech aux trois grandes commémorations de 2026
    </div>
    """, unsafe_allow_html=True)

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
   
    if current == 1:
        st.markdown('<h1 class="big-title">🧞</h1>', unsafe_allow_html=True)
        st.markdown('<div class="tag-subtitle"> مرحبًا بك أيها المسافر • Welcome Traveler</div>', unsafe_allow_html=True)
    
    if st.button("⬅ Back to Marrakech-Safi Map"):
        st.session_state.page = "marrakech_safi"
        st.session_state.stop1_phase = "intro"
        st.rerun()

    total_stops = 9
    st.progress(current / total_stops)
    st.markdown(f'<h3 style="text-align: center; color: #e31e24;">🏆 Score: {st.session_state.score} pts</h3>', unsafe_allow_html=True)
    st.markdown('<div class="gps-tracker">📍 GPS Tracking Active • تتبع GPS نمط</div>', unsafe_allow_html=True)

    # AR IFRAME
    col_left, col_mid, col_right = st.columns([1, 4, 1])
    with col_mid:
        st.markdown("### 🧞 Scan the AR Treasure")
        if current == 1 and phase == "intro":
            current_webar_url = welcome_url
        else:
            current_webar_url = webar_urls.get(current, riddle_url_stop1)
        components.iframe(current_webar_url, height=700, scrolling=True)

    st.markdown("---")

    # INTRO FOR STOP 1
    if current == 1 and phase == "intro":
        st.info("The Genie is happy for your arrival! Click below to start **the Caravan of Unity** adventure.")
        st.info("يسعد الجني بقدومك ! اضغط على الزر أدناه لبدء رحلتك في المغامرة.")
        if st.button("🚀 Let's Start – أبدأ المغامرة", type="primary", use_container_width=True):
            st.session_state.stop1_phase = "puzzle"
            st.rerun()

    # PUZZLE LOGIC FOR ALL STOPS
    elif current in stops_data:
        stop = stops_data[current]
        if current not in st.session_state.stop_answers:
            st.session_state.stop_answers[current] = {"riddle": None, "mini": None, "riddle_scored": False, "mini_scored": False}
        answers = st.session_state.stop_answers[current]

        if "description" in stop:
            st.markdown("**🛍️ Welcome**")
            st.info(stop["description"])

        if "riddle_options" in stop:
            st.subheader("🧩 Click your answer to the AR puzzle")
            if answers["riddle"] is None:
                c1, c2 = st.columns(2)
                for i, opt in enumerate(stop["riddle_options"]):
                    with (c1 if i % 2 == 0 else c2):
                        if st.button(opt, use_container_width=True, key=f"r{current}_{i}"):
                            answers["riddle"] = opt
                            if opt == stop["correct_riddle"] and not answers["riddle_scored"]:
                                answers["riddle_scored"] = True
                                st.session_state.score += 25
                            st.rerun()
            else:
                if answers["riddle"] == stop["correct_riddle"]:
                    st.success(f"✅ Correct! **{stop['correct_riddle']}**")
                else:
                    st.error(f"❌ The correct answer is {stop['correct_riddle']}")
                    if st.button("🔄 Try Riddle Again", key=f"retry_r{current}"):
                        answers["riddle"] = None
                        st.rerun()
                if "learning" in stop:
                    st.markdown("**📖 Learning Moment**")
                    st.info(stop["learning"])

        if answers.get("riddle") is not None and "mini_question" in stop:
            st.subheader("🔍 Mini-Challenge")
            st.write(stop["mini_question"])
            if answers["mini"] is None:
                c1, c2 = st.columns(2)
                for i, opt in enumerate(stop["mini_options"]):
                    with (c1 if i % 2 == 0 else c2):
                        if st.button(opt, use_container_width=True, key=f"m{current}_{i}"):
                            answers["mini"] = opt
                            if opt == stop["correct_mini"] and not answers["mini_scored"]:
                                answers["mini_scored"] = True
                                st.session_state.score += 15
                            st.rerun()
            else:
                if answers["mini"] == stop["correct_mini"]:
                    st.success(f"✅ Yes! {stop['mini_explanation']}")
                else:
                    st.error(f"❌ The answer is {stop['correct_mini']}")
                    if st.button("🔄 Try Mini Again", key=f"retry_m{current}"):
                        answers["mini"] = None
                        st.rerun()

        if "clue" in stop:
            st.markdown("**🧭 Clue to Next Stop**")
            st.info(stop["clue"])

        # SPECIAL FINAL STOP
        if current == 9 and "special" in stop:
            st.success(stop["message"])
            st.markdown(f"**Your discount code for Lamsaty Workshop:**\n\n**{stop['discount_code']}**")
            st.info("Show this code at the workshop for 20% off your pottery & embroidery class!")

            traveler_name = st.text_input("Enter your name, brave traveler:", placeholder="Your Name")
            if traveler_name:
                cert_text = stop["certificate_text"].replace("{name}", traveler_name)
                if st.button("🎁 Download Your Treasure Map Certificate"):
                    st.download_button(
                        label="📜 Download Certificate (TXT)",
                        data=cert_text,
                        file_name=f"Kenz_Quest_Certificate_{traveler_name}.txt",
                        mime="text/plain"
                    )
                    st.snow()

    else:
        st.info("🌟 More stops coming soon!")

    st.markdown("---")
    # Navigation
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
    with btn_col1:
        if current > 1 and st.button("← Previous", use_container_width=True):
            st.session_state.current_stop -= 1
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
            st.success("🎉 Congratulations! You completed the Marrakech-Safi Treasure Hunt and became a Guardian of the 2026 National Memory!")
