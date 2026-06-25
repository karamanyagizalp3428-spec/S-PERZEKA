import streamlit as st
import google.generativeai as genai
import time
import random

# Sayfa ayarları
st.set_page_config(page_title="SÜPERZEKA v20 PRO", page_icon="🤖", layout="wide")

# CSS - HATA RİSKİNİ AZALTAN STİL
st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; }
    h1, h2, h3, p, div, b { color: #00ffcc !important; font-family: 'Consolas', monospace !important; }
    .chat-box { background-color: #111; border: 1px dashed #00ffcc; padding: 12px; border-radius: 8px; margin: 10px 0; }
    .bilgi-paneli { background-color: #001a1a; border: 1px solid #00ffcc; padding: 15px; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# GÜVENLİ BAŞLATMA
if "mod" not in st.session_state: st.session_state.mod = "ÖĞRENCİ"
if "gecmis" not in st.session_state or not isinstance(st.session_state.gecmis, dict): st.session_state.gecmis = {}
if "bulut_user" not in st.session_state: st.session_state.bulut_user = None
if "canvas" not in st.session_state: st.session_state.canvas = "# Siber Canvas\nBuraya ödevini yapıştır kanka!"

# ARAYÜZ
st.markdown("<h1>🧠 SÜPERZEKA v20 PRO 🧠</h1>", unsafe_allow_html=True)
c1, c2 = st.columns([1, 2])

with c1:
    st.markdown(f"<div class='bilgi-paneli'>💡 <b>Bilgi:</b> {random.choice(['Yapay zeka 1956\'da başladı.', 'Beyin 86 milyar nörondur.'])}<br><br>🕋 <b>Hadis:</b> {random.choice(['İlim öğrenmek farzdır.', 'Kolaylaştırınız, zorlaştırmayınız.'])}</div>", unsafe_allow_html=True)
    
    st.sidebar.title("🔐 SİBER ÜS")
    # Bulut Yönetimi
    if not st.session_state.bulut_user:
        user = st.sidebar.text_input("Kullanıcı Adı:")
        if st.sidebar.button("Bulut'a Bağlan"): st.session_state.bulut_user = user; st.rerun()
    else:
        st.sidebar.write(f"☁️ Kullanıcı: {st.session_state.bulut_user}")
        if st.sidebar.button("Bağlantıyı Kes"): st.session_state.bulut_user = None; st.rerun()
    
    # Mod Kontrolü
    if st.session_state.mod == "ÖĞRENCİ":
        sifre = st.sidebar.text_input("Şifre (Dakika):", type="password")
        if st.sidebar.button("Öğretmen Moduna Geç"):
            if sifre == time.strftime("%M"): st.session_state.mod = "ÖĞRETMEN"; st.rerun()
    else:
        if st.sidebar.button("Öğrenciye Dön"): st.session_state.mod = "ÖĞRENCİ"; st.rerun()

with c2:
    st.subheader("📝 Canvas")
    st.session_state.canvas = st.text_area("Düzenleme Alanı:", value=st.session_state.canvas, height=150)
    
    u_input = st.text_input("Sorgu:")
    if st.button("Çalıştır 🚀") and u_input:
        talimat = ("ASLA CEVABI VERME. Yönlendir ve '💡 Siber İpucu' ver." if st.session_state.mod == "ÖĞRENCİ" 
                   else "Doğrudan cevap ver.")
        try:
            model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=talimat)
            res = model.generate_content(f"Canvas: {st.session_state.canvas}\nSoru: {u_input}")
            user_key = st.session_state.bulut_user or "misafir"
            if user_key not in st.session_state.gecmis: st.session_state.gecmis[user_key] = []
            st.session_state.gecmis[user_key].append((u_input, res.text))
            st.rerun()
        except: st.error("Sistem hatası oluştu, tekrar dene.")

    # Hatasız Listeleme
    active_user = st.session_state.bulut_user or "misafir"
    chat_list = st.session_state.gecmis.get(active_user, [])
    for q, a in reversed(chat_list):
        st.markdown(f"<div class='chat-box'>👤 {q}<br><br>🤖 {a}</div>", unsafe_allow_html=True)
