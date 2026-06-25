import streamlit as st
import google.generativeai as genai
import time
import random

st.set_page_config(page_title="SÜPERZEKA v20 PRO", page_icon="🤖", layout="wide")

# CSS
st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; }
    h1, h2, h3, h4, h5, h6, p, span, label, li, div, b, strong { color: #00ffcc !important; font-family: 'Consolas', monospace !important; }
    input, textarea { background-color: #111111 !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; }
    .chat-box { background-color: #111; border: 1px dashed #00ffcc; padding: 12px; border-radius: 8px; margin: 10px 0; }
    .logo-kutusu { border: 2px solid #00ffcc; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# HAFIZA
if "mod" not in st.session_state: st.session_state.mod = "ÖĞRENCİ"
if "hata_sayaci" not in st.session_state: st.session_state.hata_sayaci = 0
if "kilitli" not in st.session_state: st.session_state.kilitli = False
if "canvas_icerik" not in st.session_state: st.session_state.canvas_icerik = "# Siber Canvas"
if "gecmis" not in st.session_state: st.session_state.gecmis = []

# SIDEBAR ŞİFRE SİSTEMİ
st.sidebar.title("🔐 SİBER ÜS")
if st.session_state.kilitli:
    st.sidebar.error("🚨 SİSTEM KİLİTLİ: GÜVENLİK İHLALİ!")
    st.sidebar.warning("Delil kaydı başlatıldı... Veriler korumaya alındı.")
else:
    if st.session_state.mod == "ÖĞRENCİ":
        sifre = st.sidebar.text_input("Siber Şifre:", type="password")
        if st.sidebar.button("Öğretmen Moduna Geç 🔑"):
            if sifre == time.strftime("%M"):
                st.session_state.mod = "ÖĞRETMEN"
                st.session_state.hata_sayaci = 0
                st.rerun()
            else:
                st.session_state.hata_sayaci += 1
                st.sidebar.error(f"Hatalı Giriş! ({st.session_state.hata_sayaci}/3)")
                if st.session_state.hata_sayaci >= 3:
                    st.session_state.kilitli = True
                    st.rerun()
    else:
        if st.sidebar.button("Öğrenci Moduna Dön 🎒"):
            st.session_state.mod = "ÖĞRENCİ"
            st.rerun()

# ANA EKRAN
st.markdown(f"""
    <div class='logo-kutusu'>
        <h1>🧠 [ SÜPERZEKA v20 PRO ] 🧠</h1>
        <div style='background:#002211; padding:10px;'>AKTİF MOD: <b>{st.session_state.mod}</b></div>
    </div>
""", unsafe_allow_html=True)

if st.session_state.kilitli:
    st.error("🚨 SİSTEM KİLİTLENDİ! İZİNSİZ ERİŞİM GİRİŞİMİ TESPİT EDİLDİ.")
    st.image("https://media.giphy.com/media/l41lTjJp90YpB5aH6/giphy.gif") # Delil simülasyonu
    st.stop()

# İŞLEM EKRANI
col_l, col_r = st.columns(2)
with col_l:
    st.session_state.canvas_icerik = st.text_area("Canvas:", value=st.session_state.canvas_icerik, height=400)
with col_r:
    with st.form(key='sorgu_form', clear_on_submit=True):
        u_input = st.text_input("Komut gönder (Enter'a bas):")
        submit = st.form_submit_button("Sorgula 🚀")
    
    if (submit or u_input) and u_input:
        talimat = ("Öğrenci modundasın: ASLA CEVABI VERME. İpucu ver, '💡 Siber İpucu' ile bitir." if st.session_state.mod == "ÖĞRENCİ" 
                   else "Öğretmen modundasın: Teknik ve doğrudan cevap ver.")
        try:
            model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=talimat)
            res = model.generate_content(f"Canvas: {st.session_state.canvas_icerik}\nSoru: {u_input}")
            st.session_state.gecmis.append((u_input, res.text))
            st.rerun()
        except: st.error("Bağlantı hatası!")

  # YENİ VE GÜVENLİ KISIM
    if "gecmis" in st.session_state and isinstance(st.session_state.gecmis, list):
        for q, a in reversed(st.session_state.gecmis):
            st.markdown(f"<div class='chat-box'>👤 <b>Sen:</b> {q}<br><br>🤖 <b>SüperZeka:</b> {a}</div>", unsafe_allow_html=True)
