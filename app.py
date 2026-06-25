import streamlit as st
import google.generativeai as genai
import time
import random

st.set_page_config(page_title="SÜPERZEKA v20 PRO", page_icon="🤖", layout="wide")

# CSS - FULL DARK SİBER ESTETİK
st.markdown("""
    <style>
    body, .stApp { background-color: #050505 !important; }
    h1, h2, h3, h4, h5, h6, p, span, label, li, div, b, strong { color: #00ffcc !important; font-family: 'Consolas', monospace !important; }
    input, textarea { background-color: #111111 !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; }
    .stButton>button { background-color: #1a1a1a !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; width: 100%; }
    .chat-box { background-color: #111; border: 1px dashed #00ffcc; padding: 12px; border-radius: 8px; margin: 10px 0; }
    .logo-kutusu { border: 2px solid #00ffcc; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 15px; background: #0c0c0c; }
    .bilgi-paneli { border: 1px solid #00ffcc; padding: 15px; border-radius: 8px; background: #0c0c0c; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# HAFIZA YÖNETİMİ
if "mod" not in st.session_state: st.session_state.mod = "ÖĞRENCİ"
if "hata_sayaci" not in st.session_state: st.session_state.hata_sayaci = 0
if "kilitli" not in st.session_state: st.session_state.kilitli = False
if "gecmis" not in st.session_state: st.session_state.gecmis = []
if "canvas" not in st.session_state: st.session_state.canvas = "# Siber Canvas\n\nBuraya ödevini yapıştır kanka!"

# VERİ TABANLARI
bilgiler = ["🤖 AI 1956'da başladı.", "🌐 İnternet devasa bir ağdır.", "🧠 Beyin evrenin merkezidir."]
hadisler = ["“İlim öğrenmek farzdır.”", "“Kolaylaştırınız, zorlaştırmayınız.”", "“Güzel ahlak imandır.”"]

# SIDEBAR - ŞİFRE VE KİLİT
st.sidebar.title("🔐 SİBER ÜS")
if st.session_state.kilitli:
    st.sidebar.error("🚨 SİSTEM KİLİTLİ!")
else:
    if st.session_state.mod == "ÖĞRENCİ":
        sifre = st.sidebar.text_input("Siber Şifre:", type="password")
        if st.sidebar.button("Öğretmen Moduna Geç 🔑"):
            if sifre == time.strftime("%M"): 
                st.session_state.mod = "ÖĞRETMEN"; st.session_state.hata_sayaci = 0; st.rerun()
            else:
                st.session_state.hata_sayaci += 1
                st.sidebar.error(f"Hatalı! ({st.session_state.hata_sayaci}/3)")
                if st.session_state.hata_sayaci >= 3: st.session_state.kilitli = True; st.rerun()
    else:
        if st.sidebar.button("Öğrenci Moduna Dön 🎒"): st.session_state.mod = "ÖĞRENCİ"; st.rerun()

# ANA EKRAN
st.markdown(f"<div class='logo-kutusu'><h1>🧠 [ SÜPERZEKA v20 PRO ] 🧠</h1><div>AKTİF MOD: <b>{st.session_state.mod}</b></div></div>", unsafe_allow_html=True)

if st.session_state.kilitli:
    st.error("🚨 SİSTEM KİLİTLENDİ! GÜVENLİK İHLALİ!"); st.stop()

# BİLGİ VE HADİS PANELİ
c1, c2 = st.columns(2)
with c1: st.markdown(f"<div class='bilgi-paneli'><b>💡 Bilgi:</b> {random.choice(bilgiler)}</div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='bilgi-paneli'><b>🕋 Hadis:</b> {random.choice(hadisler)}</div>", unsafe_allow_html=True)

# CANVAS VE SORGU
col_l, col_r = st.columns(2)
with col_l:
    st.session_state.canvas = st.text_area("Canvas:", value=st.session_state.canvas, height=400)
with col_r:
    with st.form("sorgu_form", clear_on_submit=True):
        u_input = st.text_input("Komut gönder (Enter'a bas):")
        submit = st.form_submit_button("Sorgula 🚀")
    
    if (submit or u_input) and u_input:
        talimat = ("Öğrenci modundasın: ASLA CEVABI VERME. Yönlendirici ipucu ver, '💡 Siber İpucu' ile bitir." if st.session_state.mod == "ÖĞRENCİ" else "Öğretmen modundasın: Teknik ve doğrudan cevap ver.")
        try:
            model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=talimat)
            res = model.generate_content(f"Canvas: {st.session_state.canvas}\nSoru: {u_input}")
            st.session_state.gecmis.append((u_input, res.text))
            st.rerun()
        except Exception as e: st.error(f"Hata: {e}")

    if "gecmis" in st.session_state and isinstance(st.session_state.gecmis, list):
        for q, a in reversed(st.session_state.gecmis):
            st.markdown(f"<div class='chat-box'>👤 <b>Sen:</b> {q}<br><br>🤖 <b>SüperZeka:</b> {a}</div>", unsafe_allow_html=True)
