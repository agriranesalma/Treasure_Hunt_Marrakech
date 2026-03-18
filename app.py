import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import base64

# ====================== CONFIG & STYLING ======================
st.set_page_config(page_title="كنز المغرب • Trésor Marocain", layout="wide", page_icon="🕌")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Kaushan+Script&family=Amiri:wght@400;700&display=swap');

.stApp {
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
                url('https://images.unsplash.com/photo-1531230689007-0b32d7a7c33e?q=80&w=2070&auto=format&fit=crop')
                no-repeat center center fixed;
    background-size: cover;
    color: white !important;
}

.big-title {
    font-family: 'Kaushan Script', cursive !important;
    font-size: clamp(3rem, 8vw, 5rem);
    font-weight: 900;
    text-align: center;
    background: linear-gradient(to right, #e31e24, #ffffff, #006400);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px;
}

.tag-subtitle {
    font-size: 1.5rem;
    text-align: center;
    color: #f1c40f !important;
    margin-bottom: 2rem;
}

.history-box {
    background-color: rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 15px;
    border-left: 5px solid #e31e24;
    margin: 15px 0;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    border: 2px solid #e31e24;
    background-color: transparent;
    color: white;
    transition: 0.3s;
}

.stButton > button:hover {
    background-color: #e31e24;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ====================== SESSION STATE ======================
if "current_stop" not in st.session_state:
    st.session_state.current_stop = 1
if "score" not in st.session_state:
    st.session_state.score = 0
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "quiz_solved" not in st.session_state:
    st.session_state.quiz_solved = False

# ====================== DATA & CONTENT ======================
STOPS = {
    1: {
        "title": "Jemaa el-Fna: The Stage of Legends",
        "riddle": "I am a place where the sun sets but the voices never sleep. I have no ceiling, yet I hold a thousand stories. Where am I?",
        "history": "In 2001, UNESCO declared this square a 'Masterpiece of the Oral and Intangible Heritage of Humanity'. It has been the pulse of Marrakech since the 11th century (Source: UNESCO)",
        "cool_fact": "Look up! The square's layout has remained largely unchanged for nearly 1,000 years, serving as a 'Halqa' (storytelling circle) that preserves history through speech rather than books.",
        "cultural_snippet": "🎶 *'Allah Allah Moulana'* — This Gnawa chant often echoes here, calling for peace and spiritual healing. It is a fusion of Sub-Saharan rhythms and Moroccan poetry.",
        "quiz": "Which Almoravid leader founded Marrakech and this square?",
        "options": ["A) Yusuf ibn Tashfin", "B) Ahmed al-Mansur", "C) Moulay Ismail"],
        "correct": "A) Yusuf ibn Tashfin"
    },
    2: {
        "title": "The Sahara Soul: Hassani Artisanat",
        "history": "To understand the Sahara, we remember the 1958 visit of SM Mohammed V to M'Hamid El Ghizlane, where the bond between the throne and the Sahrawi tribes was forever sealed. (Source: Moroccan National Archives)",
        "memory": "We also celebrate the 50th Anniversary of the evacuation of the last foreign soldier from our southern provinces. A moment of true sovereignty!",
        "artisanat": "Discover the 'Filali' leather and Hassani silver. Sahrawi jewelry is more than decoration; each symbol is a map of the stars used for desert navigation.",
        "poetry": "🌵 *Hassani Poesie (Gaf):* 'The sands do not forget the footsteps of the Green March; they still glow with the spirit of three hundred thousand hearts.'",
        "quiz": "In what year did the Green March (La Marche Verte) take place?",
        "options": ["A) 1965", "B) 1975", "C) 1985"],
        "correct": "B) 1975"
    },
    3: {
        "title": "The Mint Tea Break: Tales & Tea",
        "history": "Did you know Moroccan tea culture actually boomed in the 1850s because of the Crimean War? British merchants were stuck with extra tea and sold it to Moroccan ports! (Source: 'A History of Tea in Morocco')",
        "fun_fact": "In the souks, the height from which the tea is poured shows the respect for the guest. The higher the pour, the more 'mousse' (bubbles), and the warmer the welcome.",
        "joke": "Why did the Moroccan man bring a loaf of bread to the cinema? Because he heard it was a 'Jam-packed' movie!",
        "quiz": "What is the nickname for Moroccan mint tea?",
        "options": ["A) Berber Coffee", "B) Whiskey Marocain", "C) Red Gold"],
        "correct": "B) Whiskey Marocain"
    },
    4: {
        "title": "Saadian Tombs: The Golden Dynasty",
        "history": "Hidden for centuries until 1917, these tombs hold the remains of the Saadian dynasty. The 'Chamber of Twelve Columns' is made of Italian Carrara marble. (Source: Ministry of Culture)",
        "quiz": "Look at the walls. What is the name of this hand-cut geometric tile mosaic?",
        "options": ["A) Tadelakt", "B) Zellige", "C) Gebs"],
        "correct": "B) Zellige"
    },
    5: {
        "title": "Zellige Workshop",
        "learning": "Now you see it, now you make it! Zellige is a mathematical art form where every piece is hand-chipped using a special hammer called a 'Manquach'.",
        "task": "Traveler! Visit the artisan and ask: 'How many pieces make a single star?'",
        "quiz": "Which city is the historic capital of Zellige production in Morocco?",
        "options": ["A) Casablanca", "B) Fès", "C) Agadir"],
        "correct": "B) Fès"
    },
    6: {
        "title": "The Tanjia Experience",
        "learning": "The Tanjia Marrakchia is known as the 'Bachelor's Dish'. Historically, souk workers would fill a clay pot with meat and spices and leave it in the 'Fernatchi' (the oven heating the public bath) to slow-cook for 6 hours.",
        "quiz": "What is the essential citrus ingredient in a traditional Tanjia?",
        "options": ["A) Fresh Orange", "B) Preserved Lemon", "C) Sweet Lime"],
        "correct": "B) Preserved Lemon"
    },
    7: {
        "title": "Koutoubia & Berber Calligraphy",
        "history": "Built by the Almohad Caliphate, its minaret served as a blueprint for the Giralda in Seville. The three golden copper balls at the top are said to represent the three elements: Water, Earth, and Fire. (Source: Al-Andalus architectural records)",
        "berber_fact": "The Almohads were a Berber (Amazigh) dynasty. Today, you will learn to write your name in 'Tifinagh', the ancient script of the Sahara.",
        "quiz": "The Koutoubia minaret is exactly 77 meters tall. True or False?",
        "options": ["A) True", "B) False"],
        "correct": "A) True"
    },
    8: {
        "title": "Bahia Palace: The Radiant",
        "learning": "Bahia means 'The Beautiful'. It was built in the late 19th century by Grand Vizier Si Moussa. It has 160 rooms but not a single kitchen—because the food was brought in from the nearby Dar Si Said!",
        "quiz": "The palace architecture was designed to capture: ",
        "options": ["A) Sunlight", "B) The Breeze", "C) Rainwater"],
        "correct": "B) The Breeze"
    },
    9: {
        "title": "The Final Treasure: Pottery & Honor",
        "learning": "You have traveled through centuries. Your final stop is the Pottery Workshop, where the clay of the earth meets the fire of our history.",
        "bonus": "Enter your name to claim your Royal Traveler Certificate!"
    }
}

# ====================== MAIN LOGIC ======================
st.markdown('<h1 class="big-title">Kenz Quest</h1>', unsafe_allow_html=True)
st.markdown('<div class="tag-subtitle">Discover the Soul of Morocco</div>', unsafe_allow_html=True)

curr = st.session_state.current_stop
data = STOPS[curr]

# Progress Bar
st.progress(curr / len(STOPS))
st.write(f"📍 Current Stop: **{data['title']}** | 🏆 Score: **{st.session_state.score}**")

# Stop Content
col1, col2 = st.columns([2, 1])

with col1:
    st.header(data['title'])
    
    if "riddle" in data:
        st.markdown(f"**🧞 The Genie's Riddle:** *{data['riddle']}*")
    
    if "history" in data:
        st.markdown(f'<div class="history-box"><b>📜 National Memory:</b><br>{data["history"]}</div>', unsafe_allow_html=True)
        
    if "cultural_snippet" in data:
        st.info(data["cultural_snippet"])
        
    if "memory" in data:
        st.warning(data["memory"])
        
    if "artisanat" in data:
        st.success(f"🎨 **Artisan Secret:** {data['artisanat']}")

    if "poetry" in data:
        st.markdown(f"✍️ **Poetry:** {data['poetry']}")

    if "joke" in data:
        st.markdown(f"😂 **Wait, one more thing:** {data['joke']}")

with col2:
    if "quiz" in data:
        st.subheader("🧩 The Challenge")
        choice = st.radio(data["quiz"], data["options"], key=f"quiz_{curr}")
        if st.button("Check Answer"):
            if choice == data["correct"]:
                st.success("Correct! +20 Points")
                st.session_state.score += 20
                st.session_state.quiz_solved = True
            else:
                st.error("Not quite! Try thinking about the history we just shared.")

# Final Stop Logic
if curr == 9:
    st.session_state.user_name = st.text_input("Enter your full name for the certificate:", placeholder="e.g. Amina Al-Fassi")
    if st.session_state.user_name:
        cert_text = f"""
        **************************************************
        * KENZ QUEST HONORARY SCROLL           *
        **************************************************
        
        This certifies that the Great Traveler:
        {st.session_state.user_name.upper()}
        
        Has successfully navigated the 9 Gates of 
        Marrakech, mastered the history of the 
        Sahara, and honored the artisans of Morocco.
        
        Points Earned: {st.session_state.score}
        Date: March 2026
        
        **************************************************
        """
        st.download_button("📜 Download Your Treasure Map Certificate", cert_text, file_name="Kenz_Quest_Certificate.txt")
        st.balloons()

# Navigation
st.markdown("---")
n_col1, n_col2, n_col3 = st.columns([1, 2, 1])
with n_col1:
    if curr > 1:
        if st.button("⬅ Previous Stop"):
            st.session_state.current_stop -= 1
            st.rerun()
with n_col3:
    if curr < len(STOPS):
        if st.button("Next Stop →"):
            st.session_state.current_stop += 1
            st.rerun()
