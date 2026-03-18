import streamlit as st
import streamlit.components.v1 as components

# ====================== SESSION STATE INITIALIZATION ======================
if "page" not in st.session_state:
    st.session_state.page = "marrakech_intro"  # Start here after clicking Marrakech
if "marrakech_subpage" not in st.session_state:
    st.session_state.marrakech_subpage = "welcome"
if "riddle_solved" not in st.session_state:
    st.session_state.riddle_solved = False
if "score" not in st.session_state:
    st.session_state.score = 0

# ====================== STYLING  ======================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Kaushan+Script&family=Amiri:wght@400;700&display=swap');

.stApp {
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
                url('https://images.unsplash.com/photo-1596200230881-224419f71c9d?q=80&w=2070')
                no-repeat center center fixed;
    background-size: cover;
    color: white !important;
}

.genie-speech {
    background-color: rgba(255, 255, 255, 0.1);
    border-left: 5px solid #f1c40f;
    padding: 20px;
    border-radius: 10px;
    font-style: italic;
    font-size: 1.2rem;
    margin: 20px 0;
}

.history-card {
    background: rgba(0, 0, 0, 0.6);
    border: 1px solid #e31e24;
    padding: 25px;
    border-radius: 20px;
    margin-bottom: 20px;
}

.privacy-badge {
    text-align: center;
    font-size: 0.8rem;
    color: #00ff88;
    background: rgba(0, 255, 136, 0.1);
    padding: 5px;
    border-radius: 5px;
}

.stButton > button {
    background-color: #e31e24;
    color: white !important;
    border-radius: 50px;
    padding: 10px 30px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(227, 30, 36, 0.6);
}
</style>
""", unsafe_allow_html=True)

# ====================== PAGE 1: WELCOME TRAVELER ======================
if st.session_state.marrakech_subpage == "welcome":
    st.markdown("<h1 style='text-align: center; font-family: \"Kaushan Script\"; font-size: 4rem; color: #f1c40f;'>مرحباً بك أيها المسافر</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Welcome, Traveler!</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        # AR Placeholder: Genie exciting the user
        components.iframe("https://mywebar.com/p/Project_0_ckwoq2vq9l", height=500)
        
        st.markdown("""
        <div class="genie-speech">
        "Ah! A new face in the Red City! I am the Guardian of the Treasure. 
        Are you ready to unlock the secrets of our ancestors? My magic is strong, 
        but your wit must be stronger. Shall we begin our journey through time?"
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="privacy-badge">🔒 Privacy First: We do not store any images of your face or collect personal data.</div>', unsafe_allow_html=True)
        
        if st.button("🚀 Let's Start the Adventure", use_container_width=True):
            st.session_state.marrakech_subpage = "entry_riddle"
            st.rerun()

# ====================== PAGE 2: ENTRY RIDDLE ======================
elif st.session_state.marrakech_subpage == "entry_riddle":
    st.markdown("<h2 style='text-align: center;'>The Gatekeeper's Challenge</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        # AR Placeholder: Riddle box
        components.iframe("https://mywebar.com/p/Project_1_to00xjn24", height=400)
        
        st.markdown("### Solve the riddle to enter:")
        st.info("I am a stage without a curtain, a book without pages, and a kitchen that never sleeps. I change my face when the sun sets, but my voice has remained the same for 800 years. Where am I?")
        
        options = ["A) Bahia Palace", "B) Majorelle Garden", "C) Jemaa el-Fna", "D) Koutoubia Mosque"]
        choice = st.radio("Your Answer:", options, index=None)
        
        if st.button("Submit Answer"):
            if choice == "C) Jemaa el-Fna":
                st.success("Correct! The pulse of Marrakech awaits you.")
                st.session_state.score += 50
                st.session_state.marrakech_subpage = "stop_1_content"
                st.rerun()
            elif choice is not None:
                st.error("The Genie shakes his head... Try again!")

# ====================== PAGE 3: STOP 1 - JEMAA EL-FNA ======================
elif st.session_state.marrakech_subpage == "stop_1_content":
    st.markdown("<h1 style='text-align: center; color: #e31e24;'>Stop 1: Jemaa el-Fna</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; opacity: 0.8;'>The Open-Air Theater of Humanity</h4>", unsafe_allow_html=True)

    # Historical "Hook"
    st.markdown("""
    <div class="history-card">
    <h3>📱 The World's Oldest 'Social Media'</h3>
    <p>You are standing in a place where people have 'uploaded' history into minds for 1,000 years. Before TikTok, there was the <b>Halqa</b> (storytelling circle). 
    In 1985, UNESCO recognized the entire Medina of Marrakech as a World Heritage site, and in 2001, this very square was proclaimed a 
    <b>Masterpiece of the Oral and Intangible Heritage of Humanity</b>.</p>
    </div>
    """, unsafe_allow_html=True)

    # Cultural Features
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### ✨ What Makes it Amazing?")
        st.write("- **The Halqa:** Storytellers spinning legends.")
        st.write("- **Gnaoua Musicians:** Healers of the soul through rhythm.")
        st.write("- **The Henna Artists:** Painting identity on skin.")
        st.write("- **The Night Kitchen:** A feast for all senses.")
    with c2:
        st.markdown("### 🎶 Soul of the Square: Gnaoua")
        st.write("Listen closely... the sound of the *Krakebs* (iron castanets) is the heartbeat of the Sahara. One of their most famous songs honors **Lalla Aïcha Hamdouchia**.")

    # Resistance & National Memory
    st.markdown("---")
    st.markdown("### 🧞 The Genie Whispers: A Hero's Tale")
    st.markdown("""
    <div class="genie-speech">
    "Look at the banners! We remember <b>Aïcha Hamdouchia</b>, the anti-colonial fighter. She represents more than just a name; 
    she is the spirit of Moroccan resistance! In the 1950s, this square wasn't just for fun—it was the secret center of 
    Moroccan union against foreign occupation. The storytellers used their tales to hide messages of freedom!"
    </div>
    """, unsafe_allow_html=True)

    # Green March & Royal Visit
    st.markdown("""
    <div class="history-card" style="border-left: 5px solid #006400;">
    <h3>🇲🇦 National Sovereignty</h3>
    <p>The square stands as a witness to our unity. We celebrate the anniversary of the <b>historic visit of HM King Mohammed V 
    to M’Hamid El Ghizlane</b> and the provinces of Laâyoune, Smara, and Boujdour. This was a founding moment of our national 
    sovereignty, showing the unbreakable bond between the Throne and the People. It reminds us of the <b>Green March</b> and 
    the anniversary of the evacuation of the last foreign soldier from the Moroccan Sahara.</p>
    </div>
    """, unsafe_allow_html=True)

    # The Seven Saints Legend
    st.markdown("### 🏮 The Legend of the Seven Saints")
    st.info("Source: 'The Seven Saints of Marrakesh' by Abu al-Abbas al-Sabti. Since the 17th century, a spiritual circle of seven protectors has guarded this city. This square is the starting point of that sacred circle.")

    # Link to Stop 2
    st.markdown("---")
    st.markdown("<h3 style='text-align: center; color: #f1c40f;'>🧭 Clue to Stop 2</h3>", unsafe_allow_html=True)
    st.success("The caravans that once traded in this square didn’t start here; they came from the deep south. Let’s follow the **'Silver Path'** to find where the desert meets the city. Our next stop is a master of **Hassani Silver Filigree**!")
    
    if st.button("Proceed to Stop 2: The Silver Artisan"):
        st.session_state.current_stop = 2
        st.session_state.marrakech_subpage = "stop_2" # I would build this next
        st.rerun()

# Navigation Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div class="privacy-badge">No face data is collected. Your journey is private.</div>', unsafe_allow_html=True)
