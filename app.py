import streamlit as st
import google.generativeai as genai
import time
import random

st.set_page_config(page_title="SÜPERZEKA v20 PRO", page_icon="🤖", layout="wide")

# CSS - FULL DARK SİBER ESTETİK (Sol tarafın beyazlığını tamamen sildik)
st.markdown("""
    <style>
    /* Arka planı her yerde zifiri karanlık yap */
    .stApp, body, .main, [data-testid="stAppViewContainer"] { background-color: #050505 !important; }
    h1, h2, h3, b, p { color: #00ffcc !important; font-family: 'Consolas', monospace !important; }
    .stTextInput>div>div>input { background-color: #111 !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; }
    .stTextArea>div>div>textarea { background-color: #111 !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; }
    .logo-kutusu { border: 2px solid #00ffcc; padding: 20px; border-radius: 10px; text-align: center; background: #0c0c0c; margin-bottom: 20px; }
    .bilgi-paneli { border: 1px solid #00ffcc; padding: 15px; border-radius: 8px; background: #0c0c0c; }
    .chat-box { border: 1px dashed #00ffcc; padding: 10px; margin: 10px 0; background: #111; }
    </style>
""", unsafe_allow_html=True)

# HAFIZA
if "mod" not in st.session_state: st.session_state.mod = "ÖĞRENCİ"
if "bulut_user" not in st.session_state: st.session_state.bulut_user = None
if "gecmis" not in st.session_state: st.session_state.gecmis = []

# SIDEBAR - BULUT VE ŞİFRE
st.sidebar.title("🔐 SİBER ÜS")
if not st.session_state.bulut_user:
    user = st.sidebar.text_input("Bulut Kullanıcı Adı:")
    if st.sidebar.button("Bulut'a Bağlan ☁️"): st.session_state.bulut_user = user; st.rerun()
else:
    st.sidebar.markdown(f"☁️ **Aktif Bulut:** {st.session_state.bulut_user}")
    if st.sidebar.button("Bulut'tan Çık 🛑"): st.session_state.bulut_user = None; st.rerun()

# ŞİFRE SİSTEMİ (ÖĞRENCİ MODUNDA)
if st.session_state.mod == "ÖĞRENCİ":
    sifre = st.sidebar.text_input("Siber Şifre:", type="password")
    if st.sidebar.button("Öğretmen Moduna Geç 🔑"):
        if sifre == time.strftime("%M"): st.session_state.mod = "ÖĞRETMEN"; st.rerun()
else:
    if st.sidebar.button("Öğrenci Moduna Dön 🎒"): st.session_state.mod = "ÖĞRENCİ"; st.rerun()

# ANA EKRAN
st.markdown(f"<div class='logo-kutusu'><h1>🧠 [ SÜPERZEKA v20 PRO ] 🧠</h1><p>MOD: {st.session_state.mod}</p></div>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1: st.markdown(f"<div class='bilgi-paneli'>💡 <b>Bilgi:</b> {random.choice(['AI devrimdir.', 'Veri güçtür.'])}</div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='bilgi-paneli'>🕋 <b>Hadis:</b> {random.choice(['İlim farzdır.', 'Kolaylaştırın.'])}</div>", unsafe_allow_html=True)

# CANVAS VE SORGU
sol, sag = st.columns(2)
with sol:
    st.subheader("📝 Canvas")
    st.session_state.canvas = st.text_area("Düzenleme:", value=st.session_state.get("canvas", ""), height=300)
with sag:
    st.subheader("🧠 Siber Sorgu")
    u_input = st.text_input("Komut:", key="input")
    if st.button("Sorgula 🚀") and u_input:
        talimat = ("İpucu ver, cevap verme." if st.session_state.mod == "ÖĞRENCİ" else "Direkt cevap ver.")
        try:
            model = genai.GenerativeModel("gemini-1.5-pro") # En garantili model
            res = model.generate_content(f"{talimat} | Soru: {u_input}")
            st.session_state.gecmis.append((u_input, res.text))
            st.rerun()
        except Exception as e: st.error(f"Hata: {e}")

    for q, a in reversed(st.session_state.gecmis):
        st.markdown(f"<div class='chat-box'>👤 {q}<br>🤖 {a}</div>", unsafe_allow_html=True)
