import streamlit as st
import google.generativeai as genai
import time
import random
from PIL import Image

# SAYFA AYARLARI
st.set_page_config(page_title="SÜPERZEKA v20 PRO", page_icon="🤖", layout="wide")

# ESTETİK CSS - ZİFİRİ KARANLIK SİBER TEMA
st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; }
    h1, h2, h3, b, p { color: #00ffcc !important; font-family: 'Consolas', monospace !important; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { 
        background-color: #111 !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; 
    }
    .chat-box { border: 1px dashed #00ffcc; padding: 15px; margin: 10px 0; background: #0c0c0c; border-radius: 10px; }
    .logo-kutusu { border: 2px solid #00ffcc; padding: 20px; border-radius: 10px; text-align: center; background: #0c0c0c; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# OTURUM (HAFIZA)
if "mod" not in st.session_state: st.session_state.mod = "ÖĞRENCİ"
if "hata_sayisi" not in st.session_state: st.session_state.hata_sayisi = 0
if "gecmis" not in st.session_state: st.session_state.gecmis = []
if "pomodoro_basladi" not in st.session_state: st.session_state.pomodoro_basladi = False

# SIDEBAR: LOGO VE SİBER ÜS
try:
    st.sidebar.image("logo.png", use_column_width=True)
except:
    st.sidebar.error("Logo bulunamadı.")

st.sidebar.title("🔐 SİBER ÜS")

# ÖĞRETMEN MODU ŞİFRE SİSTEMİ (DAKİKA ŞİFRESİ)
dakika_sifre = time.strftime("%M")
if st.session_state.mod == "ÖĞRENCİ":
    girilen_sifre = st.sidebar.text_input("Öğretmen Girişi:", type="password")
    if st.sidebar.button("Modu Yükselt 🔑"):
        if girilen_sifre == dakika_sifre:
            st.session_state.mod = "ÖĞRETMEN"
            st.rerun()
        else:
            st.session_state.hata_sayisi += 1
            if st.session_state.hata_sayisi >= 3:
                st.sidebar.warning("❌ DELİL KAYDEDİLDİ: Yaramaz öğrenci tespiti!")
else:
    if st.sidebar.button("Öğrenci Moduna Dön 🎒"): st.session_state.mod = "ÖĞRENCİ"; st.rerun()

# ANA EKRAN
st.markdown("<div class='logo-kutusu'><h1>🧠 [ SÜPERZEKA v20 PRO ] 🧠</h1></div>", unsafe_allow_html=True)

# PANORAMA (BİLGİ & HADİS)
c1, c2 = st.columns(2)
with c1: st.info(f"🌟 **Günün Bilgisi:** {random.choice(['AI verimliliktir.', 'Kodlamak sanattır.'])}")
with c2: st.info(f"🕋 **Hadis:** {random.choice(['İlim öğrenmek farzdır.', 'Kolaylaştırın.'])}")

# CANVAS VE POMODORO
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("📝 Canvas")
    st.session_state.canvas = st.text_area("Düzenleme:", value=st.session_state.get("canvas", ""), height=250)
with col2:
    st.subheader("⏱️ Odak")
    if not st.session_state.pomodoro_basladi:
        if st.button("Pomodoro'yu Başlat"): st.session_state.pomodoro_basladi = True; st.rerun()
    else:
        st.metric("Kalan Süre", "25:00")
        if st.button("Mola"): st.session_state.pomodoro_basladi = False; st.rerun()

# SİBER SORGU
st.subheader("🧠 Siber Sorgu")
u_input = st.text_input("Komut:", key="input")
if st.button("Sorgula 🚀") and u_input:
    talimat = ("İpucu ver, cevap verme." if st.session_state.mod == "ÖĞRENCİ" else "Konuyu detaylı anlat ve cevabı ver.")
    st.session_state.gecmis.append((u_input, f"[SİSTEM: {st.session_state.mod} MODU] Yanıt hazırlanıyor..."))
    st.rerun()

for q, a in reversed(st.session_state.gecmis):
    st.markdown(f"<div class='chat-box'>👤 {q}<br>🤖 {a}</div>", unsafe_allow_html=True)
