import streamlit as st
import google.generativeai as genai
import time
import random

st.set_page_config(page_title="SÜPERZEKA v20 PRO", page_icon="🤖", layout="wide")

# CSS - BEYAZLIKLARI YOK EDEN FULL SİYAH ZIRH
st.markdown("""
    <style>
    /* Streamlit'in tüm konteynerlerini siyaha boya */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], .main {
        background-color: #050505 !important;
    }
    h1, h2, h3, b, p, div { color: #00ffcc !important; font-family: 'Consolas', monospace !important; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { 
        background-color: #111 !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; 
    }
    .logo-kutusu { border: 2px solid #00ffcc; padding: 20px; border-radius: 10px; text-align: center; background: #0c0c0c; margin-bottom: 20px; }
    .bilgi-paneli { border: 1px solid #00ffcc; padding: 15px; border-radius: 8px; background: #0c0c0c; }
    .chat-box { border: 1px dashed #00ffcc; padding: 10px; margin: 10px 0; background: #111; }
    </style>
""", unsafe_allow_html=True)

# MODEL AYARI
# Anahtarı manuel buraya yazıyorsan config burada:
# genai.configure(api_key="BURAYA_API_ANAHTARINI_YAZ")

# ANA EKRAN
st.markdown("<div class='logo-kutusu'><h1>🧠 [ SÜPERZEKA v20 PRO ] 🧠</h1></div>", unsafe_allow_html=True)

# TEST PANELİ (Sol tarafın siyah olup olmadığını test et)
sol, sag = st.columns(2)
with sol:
    st.markdown("<div class='bilgi-paneli'>Sol Taraf Siyah Olmalı!</div>", unsafe_allow_html=True)
with sag:
    st.markdown("<div class='bilgi-paneli'>Sağ Taraf Siyah Olmalı!</div>", unsafe_allow_html=True)

# SİSTEM SORGU (Garantili Model)
u_input = st.text_input("Komut gönder:")
if st.button("Sorgula"):
    try:
        model = genai.GenerativeModel("gemini-1.0-pro")
        res = model.generate_content(u_input)
        st.write(res.text)
    except Exception as e:
        st.error(f"HATA: {e}")
