import streamlit as st
import google.generativeai as genai
import random
import time

st.set_page_config(page_title="SÜPERZEKA v20 PRO", page_icon="🤖", layout="wide")

# SİBER TASARIM
st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; }
    h1, h2, p, div, b { color: #00ffcc !important; font-family: 'Consolas', monospace !important; }
    .chat-box { background-color: #111; border: 1px dashed #00ffcc; padding: 10px; border-radius: 8px; margin: 5px 0; }
    .bilgi-paneli { background-color: #001a1a; border: 1px solid #00ffcc; padding: 15px; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# SİSTEM HAFIZASI
if "mod" not in st.session_state: st.session_state.mod = "ÖĞRENCİ"
if "gecmis" not in st.session_state: st.session_state.gecmis = {}
if "bulut_user" not in st.session_state: st.session_state.bulut_user = None
if "canvas" not in st.session_state: st.session_state.canvas = "# Siber Canvas\nBuraya ödevini yapıştır kanka!"

# ARAYÜZ
st.markdown("<h1>🧠 SÜPERZEKA v20 PRO 🧠</h1>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"<div class='bilgi-paneli'>💡 {random.choice(['Yapay zeka 1956\'da başladı.', 'Beyin 86 milyar nörondur.'])}<br><br>🕋 {random.choice(['İlim öğrenmek farzdır.', 'Kolaylaştırınız, zorlaştırmayınız.'])}</div>", unsafe_allow_html=True)
    
    # BULUT VE GÜVENLİK
    st.sidebar.title("🔐 SİBER ÜS")
    if not st.session_state.bulut_user:
        user = st.sidebar.text_input("Kullanıcı Adı:")
        if st.sidebar.button("Bulut'a Bağlan"): st.session_state.bulut_user = user; st.rerun()
    else:
        st.sidebar.write(f"☁️ Bulut: {st.session_state.bulut_user}")
        if st.sidebar.button("Bağlantıyı Kes"): st.session_state.bulut_user = None; st.rerun()
    
    # ŞİFRE SİSTEMİ
    if st.session_state.mod == "ÖĞRENCİ":
        sifre = st.sidebar.text_input("Şifre (Dakika):", type="password")
        if st.sidebar.button("Öğretmen Moduna Geç"):
            if sifre == time.strftime("%M"): st.session_state.mod = "ÖĞRETMEN"; st.rerun()
    else:
        if st.sidebar.button("Öğrenciye Dön"): st.session_state.mod = "ÖĞRENCİ"; st.rerun()

with col2:
    # CANVAS
    st.subheader("📝 Canvas")
    st.session_state.canvas = st.text_area("Düzenleme Alanı:", value=st.session_state.canvas, height=150)
    
    # SORGU
    u_input = st.text_input("Sorgu:")
    if st.button("Çalıştır 🚀") and u_input:
        talimat = ("Öğrenci modundasın: ASLA CEVABI VERME, yönlendir ve '💡 Siber İpucu' ver." if st.session_state.mod == "ÖĞRENCİ" 
                   else "Öğretmen modundasın: Profesyonel ve doğrudan cevap ver.")
        
        model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=talimat)
        res = model.generate_content(f"Canvas: {st.session_state.canvas}\nSoru: {u_input}")
        
        user = st.session_state.bulut_user or "misafir"
        st.session_state.gecmis.setdefault(user, []).append((u_input, res.text))
        st.rerun()

    # GEÇMİŞ
    user = st.session_state.bulut_user or "misafir"
    for q, a in reversed(st.session_state.gecmis.get(user, [])):
        st.markdown(f"<div class='chat-box'>👤 {q}<br><br>🤖 {a}</div>", unsafe_allow_html=True)
