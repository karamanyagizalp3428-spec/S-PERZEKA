import streamlit as st
import time
import random
import os

# SAYFA AYARLARI
st.set_page_config(page_title="SÜPERZEKA v20 PRO", page_icon="🧠", layout="wide")

# CSS: SİBER ESTETİK (SIDEBAR DAHİL TAMAMEN KARANLIK)
st.markdown("""
    <style>
    .stApp, [data-testid="stSidebar"] { background-color: #050505 !important; }
    h1, h2, h3, b, p, label { color: #00ffcc !important; font-family: 'Consolas', monospace !important; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { 
        background-color: #111 !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; 
    }
    .chat-box { border: 1px dashed #00ffcc; padding: 15px; margin: 10px 0; background: #0c0c0c; border-radius: 10px; }
    div.stButton > button { background-color: #0c0c0c !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; }
    </style>
""", unsafe_allow_html=True)

# OTURUM (HAFIZA)
if "mod" not in st.session_state: st.session_state.mod = "ÖĞRENCİ"
if "gecmis" not in st.session_state: st.session_state.gecmis = []

# SÜPER İÇERİK VERİTABANI
bilgiler = ["Kuantum işlemciler, klasiklerin bin yıllık işini saniyede bitirir.", "Nöral ağlar, insan beynindeki sinapsların elektriksel simülasyonudur.", "SüperZeka v20, veri setlerini özyinelemeli olarak işleyebilen bir mimaridir."]
hadisler = ["İlim öğrenmek, kadın ve erkek her Müslümana farzdır.", "Hikmet, müminin yitiğidir; nerede bulursa alır.", "İlim sahibi, uykusunda ibadet edenden daha hayırlıdır."]

# SIDEBAR: LOGO
if os.path.exists("logo.png"): st.sidebar.image("logo.png", use_column_width=True)

# SORGU FONKSİYONU
def sorgula():
    if st.session_state.u_input:
        st.session_state.gecmis.append((st.session_state.u_input, f"[SİSTEM: {st.session_state.mod} - Analiz Başarılı]"))
        st.session_state.u_input = ""

# ANA EKRAN
st.title("🧠 SÜPERZEKA v20 PRO")

# PANORAMA
col_a, col_b = st.columns(2)
with col_a: st.info(f"🌟 **Günün Süper Bilgisi:** {random.choice(bilgiler)}")
with col_b: st.info(f"🕋 **Hadis-i Şerif:** {random.choice(hadisler)}")

# CANVAS VE POMODORO
col1, col2 = st.columns([3, 1])
with col1:
    st.session_state.canvas = st.text_area("📝 Canvas:", value=st.session_state.get("canvas", ""), height=200)
with col2:
    st.metric("⏱️ Odaklanma", "25:00")
    if st.button("Başlat / Mola"): st.rerun()

# ENTER İLE TETİKLENEN SORGU
st.text_input("Komut (Enter'a bas):", key="u_input", on_change=sorgula)

# GEÇMİŞ
for q, a in reversed(st.session_state.gecmis):
    st.markdown(f"<div class='chat-box'>👤 {q}<br>🤖 {a}</div>", unsafe_allow_html=True)
