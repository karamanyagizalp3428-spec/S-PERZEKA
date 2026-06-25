import streamlit as st
import google.generativeai as genai
import time
import random

# --- SİSTEM AYARLARI ---
st.set_page_config(page_title="SÜPERZEKA v20 PRO", page_icon="🤖", layout="wide")

# --- CSS ZENGİNLİĞİ (TÜM TASARIM) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; }
    h1, h2, h3, h4, h5, h6, p, span, label, li, div, b, strong { color: #00ffcc !important; font-family: 'Consolas', monospace !important; }
    input, textarea { background-color: #111111 !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; font-family: 'Consolas', monospace !important; }
    [data-testid="stSidebar"] { background-color: #0c0c0c !important; border-right: 2px solid #00ffcc; }
    .stButton>button { background-color: #1a1a1a !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; width: 100%; }
    .chat-box { background-color: #111111; border: 1px dashed #00ffcc; padding: 12px; border-radius: 8px; margin-top: 10px; margin-bottom: 10px; color: #00ffcc !important; }
    .logo-kutusu { background-color: #111; border: 2px solid #00ffcc; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 15px; }
    .bilgi-paneli { background-color: #050505 !important; border: 1px solid #00ffcc; padding: 15px; border-radius: 8px; margin-top: 15px; }
    .status-panel { background-color: #002211 !important; padding: 10px; border-radius: 5px; border: 1px solid #00ffcc; text-align: center; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- SİSTEM HAFIZASI ---
if "mod" not in st.session_state: st.session_state.mod = "ÖĞRENCİ"
if "hata_sayaci" not in st.session_state: st.session_state.hata_sayaci = 0
if "canvas" not in st.session_state: st.session_state.canvas = "# Siber Canvas\n\nBuraya ödevini veya kodunu yapıştır kanka!"
if "bulut_user" not in st.session_state: st.session_state.bulut_user = None
if "gecmis" not in st.session_state: st.session_state.gecmis = {}

# --- BİLGİ VE HADİS VERİTABANI ---
gunun_bilgileri = ["🤖 Yapay Zeka 1956 Dartmouth Konferansı'ndan günümüze evrildi.", "🌐 İnternet, 1960'lardaki ARPANET'ten devasa bir ağa dönüştü.", "🧠 İnsan beyni 86 milyar nöronla evrenin en karmaşık yapısıdır."]
hadis_havuzu = ["“İlim öğrenmek her Müslümana farzdır.”", "“Kolaylaştırınız, zorlaştırmayınız.”", "“En hayırlınız, ahlakı en güzel olandır.”"]

# --- SIDEBAR (SİBER ÜS KONTROL) ---
st.sidebar.title("🤖 SÜPERZEKA v20 PRO")
st.sidebar.header("☁️ SüperZeka Cloud")
if not st.session_state.bulut_user:
    user = st.sidebar.text_input("Siber Kullanıcı Adınız:")
    if st.sidebar.button("Bulut Hafızasına Bağlan ⚡"):
        st.session_state.bulut_user = user.strip().lower()
        st.rerun()
else:
    st.sidebar.markdown(f"<div class='status-panel'>☁️ Oturum: <b>{st.session_state.bulut_user}</b></div>", unsafe_allow_html=True)
    if st.sidebar.button("Oturumu Kapat 🛑"): st.session_state.bulut_user = None; st.rerun()

st.sidebar.header("🔐 Mod Değiştirici")
if st.session_state.mod == "ÖĞRENCİ":
    sifre = st.sidebar.text_input("Şifre (Dakika):", type="password")
    if st.sidebar.button("Öğretmen Moduna Geç 🔑"):
        if sifre == time.strftime("%M"): st.session_state.mod = "ÖĞRETMEN"; st.rerun()
else:
    if st.sidebar.button("Öğrenci Moduna Dön 🎒"): st.session_state.mod = "ÖĞRENCİ"; st.rerun()

# --- ANA EKRAN ---
st.markdown("<div class='logo-kutusu'><h1>🧠 [ SÜPERZEKA v20 PRO ] 🧠</h1><p>Mimar: Yağızalp KARAMAN | Siber Üs</p></div>", unsafe_allow_html=True)

st.code(f"[SİSTEM LOGU] v20 PRO | Bulut: {'AKTİF' if st.session_state.bulut_user else 'OFF'}", language="text")

col_l, col_r = st.columns(2)
with col_l:
    st.markdown(f"<div class='bilgi-paneli'><h3>💡 Günün Bilgisi</h3>{random.choice(gunun_bilgileri)}</div>", unsafe_allow_html=True)
with col_r:
    st.markdown(f"<div class='bilgi-paneli'><h3>🕋 Hadis-i Şerif</h3>{random.choice(hadis_havuzu)}</div>", unsafe_allow_html=True)

st.markdown("---")

sol, sag = st.columns([1, 1])
with sol:
    st.subheader("📝 Canvas")
    st.session_state.canvas = st.text_area("Çalışma Alanı:", value=st.session_state.canvas, height=350)
with sag:
    st.subheader("🧠 Siber Sorgu Ekranı")
    u_input = st.text_input("Komut gönder:")
    if st.button("Sorgula 🚀") and u_input:
        talimat = ("Öğrenci modundasın: ASLA CEVABI VERME, yönlendirici sorular sor, '💡 Siber İpucu' ver." if st.session_state.mod == "ÖĞRENCİ" 
                   else "Öğretmen modundasın: Profesyonel, teknik, ciddi ve doğrudan cevap ver.")
        
        try:
            model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=talimat)
            res = model.generate_content(f"Canvas: {st.session_state.canvas}\nSoru: {u_input}")
            user = st.session_state.bulut_user or "misafir"
            st.session_state.gecmis.setdefault(user, []).append((u_input, res.text))
            st.rerun()
        except Exception as e: st.error(f"Sistem Hatası: {e}")

    user = st.session_state.bulut_user or "misafir"
    for q, a in reversed(st.session_state.gecmis.get(user, [])):
        st.markdown(f"<div class='chat-box'>👤 <b>Sen:</b> {q}<br><br>🤖 <b>SüperZeka:</b> {a}</div>", unsafe_allow_html=True)
