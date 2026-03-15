import streamlit as st
from PIL import Image
import requests

import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components
from streamlit_image_coordinates import streamlit_image_coordinates

# CONFIG + BACKGROUND 
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

# SESSION STATE 
if "page" not in st.session_state:
    st.session_state.page = "home"
if "hunt_started" not in st.session_state:
    st.session_state.hunt_started = False
    st.session_state.current_stop = 1
    st.session_state.unlocked_stops = [1]
    st.session_state.score = 0
    st.session_state.vr_unlocked = False

# HOME PAGE - 2 COLUMNS
if st.session_state.page == "home":

    st.markdown('<h1 class="big-title">🇲🇦 كنز المغرب • Trésor Marocain</h1>', unsafe_allow_html=True)
    st.markdown("**Explore Morocco culturally • Découvrez le Maroc culturellement • اكتشف المغرب ثقافياً**")

    col_map, col_about = st.columns([1.6, 1])

    with col_map:
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
elif st.session_state.page == "marrakech":
    st.markdown('<h1 class="big-title">🕌 مغامرة مراكش-آسفي • Marrakech-Safi Treasure Hunt</h1>', unsafe_allow_html=True)
    st.caption("7 étapes • Suivez les indices sur le terrain")

    if st.button("⬅ Back to Map / العودة إلى الخريطة"):
        st.session_state.page = "home"
        st.rerun()

    # Progress bar
    progress = (len(st.session_state.unlocked_stops) / 7) * 100
    st.progress(progress / 100)
    st.write(f"**Étape {st.session_state.current_stop}/7** | **نقاط : {st.session_state.score}**")

    # Interactive treasure map
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

    # CLUES & PUZZLES bilingual =====================
    stop = st.session_state.current_stop

    clues = {
        1: ("Allez à la place Jamaâ el-Fnaâ, cœur battant de Marrakech.\nاذهبوا إلى ساحة جامع الفنا، قلب مراكش النابض.",
            "Qu'est-ce qui rend Jamaâ el-Fnaâ célèbre dans le monde entier ?\nما الذي يجعل جامع الفنا مشهوراً في العالم أجمع؟",
            ["Les conteurs et charmeurs de serpents", "Les restaurants et spectacles", "Les deux ! C'est un théâtre vivant !"]),
        2: ("Direction les Tombeaux Saadiens.\nتوجهوا إلى قبور السعديين.",
            "Qui a construit les Tombeaux Saadiens au XVIe siècle ?\nمن بنى قبور السعديين في القرن السادس عشر؟",
            ["La dynastie Saadienne", "Les Almoravides", "Les Alaouites"]),
        3: ("Prochaine étape : Mosquée Koutoubia.\nالخطوة التالية: مسجد الكتبية.",
            "Quel est le nom de la mosquée la plus emblématique de Marrakech ?\nما اسم أشهر مسجد في مراكش؟",
            ["Koutoubia", "Hassan II", "Tinmel"]),
        4: ("Rendez-vous au Palais Bahia.\nاذهبوا إلى قصر الباهية.",
            "Le Palais Bahia a été construit pour qui ?\nلمن بني قصر الباهية؟",
            ["Le grand vizir Si Moussa et son fils", "Le roi Mohammed VI", "Les Saadiens"]),
        5: ("Pause au Café du Jardin Majorelle (partenaire).\nاستراحة في مقهى حديقة ماجوريل (شريك).",
            "Entrez le code secret que le serveur vous a donné :\nأدخلوا الكود السري الذي أعطاكم إياه النادل"),
        6: ("Question culturelle sur Casablanca :\nسؤال ثقافي عن الدار البيضاء",
            "Quelle est la plus grande mosquée d'Afrique ?\nما هي أكبر مسجد في أفريقيا؟",
            None),
        7: ("Dernier stop : Atelier de Poterie à Safi (partenaire).\nالمحطة الأخيرة: ورشة الخزف في آسفي (شريك).",
            "Entrez le code spécial du potier :\nأدخلوا الكود الخاص من الحرفي"),
    }

    clue_fr_ar, question_fr_ar, options = clues[stop]
    st.markdown(f'<div class="clue-box"><b>Indice {stop} / تلميح {stop} :</b><br>{clue_fr_ar}<br><br><b>{question_fr_ar}</b></div>', unsafe_allow_html=True)

    # Puzzle logic
    if stop in [1,2,3,4]:
        answer = st.radio("Votre réponse / إجابتك", options, key=f"q{stop}")
        if st.button("Vérifier / تحقق", key=f"check{stop}"):
            correct = (stop == 1 and "deux" in answer.lower()) or \
                      (stop == 2 and "Saadienne" in answer) or \
                      (stop == 3 and "Koutoubia" in answer) or \
                      (stop == 4 and "Si Moussa" in answer)
            if correct:
                st.success("✅ Correct ! +10 points • صحيح !")
                st.session_state.score += 10
                if stop + 1 not in st.session_state.unlocked_stops:
                    st.session_state.unlocked_stops.append(stop + 1)
                st.session_state.current_stop += 1
                st.rerun()
            else:
                st.error("Réessayez • حاول مرة أخرى")

    elif stop in [5, 7]:
        code = st.text_input("Code secret / الكود السري", key=f"code{stop}")
        if st.button("Valider / تحقق", key=f"val{stop}"):
            correct_code = "JARDIN2026" if stop == 5 else "POTTERIE2026"
            if code.upper() == correct_code:
                st.success("🎉 Code accepté ! Souvenir + remise spéciale offerte par le partenaire.")
                st.session_state.score += 15
                if stop + 1 not in st.session_state.unlocked_stops:
                    st.session_state.unlocked_stops.append(stop + 1)
                st.session_state.current_stop += 1
                st.rerun()
            else:
                st.error("Code incorrect • الكود خاطئ")

    elif stop == 6:
        ans = st.text_input("Réponse / الجواب (écrivez exactement « Hassan II » ou « حسن الثاني »)")
        if st.button("Vérifier / تحقق"):
            if "hassan" in ans.lower() or "حسن" in ans:
                st.success("🏆 Bravo ! Vous avez gagné l'expérience VR de la Mosquée Hassan II !")
                st.session_state.score += 20
                st.session_state.vr_unlocked = True

                st.markdown("### 🎁 Votre prix VR interactif")
                components.iframe(
                    src="https://app.vectary.com/p/6oYpA0nJ5tLgtdBGp03cSH",
                    width="100%",
                    height=600,
                    scrolling=False
                )
                st.write("**Interagissez** : faites glisser pour tourner, molette pour zoomer, AR sur mobile !")

                if 7 not in st.session_state.unlocked_stops:
                    st.session_state.unlocked_stops.append(7)
                if st.button("Continuer vers l'étape 7 / الاستمرار إلى المرحلة 7"):
                    st.session_state.current_stop = 7
                    st.rerun()
            else:
                st.error("Ce n'est pas la bonne mosquée • ليس المسجد الصحيح")

    # Win screen
    if st.session_state.current_stop > 7:
        st.balloons()
        st.markdown("## 🎉 Félicitations ! Vous avez terminé le trésor de Marrakech-Safi !\n## مبروك ! لقد أنهيتم كنز مراكش-آسفي")
        if st.button("Recommencer / ابدأوا من جديد"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Étape précédente / الخطوة السابقة") and st.session_state.current_stop > 1:
            st.session_state.current_stop -= 1
            st.rerun()
    with col2:
        if st.button("Retour à l'accueil / العودة للصفحة الرئيسية"):
            st.session_state.page = "home"
            st.rerun()
