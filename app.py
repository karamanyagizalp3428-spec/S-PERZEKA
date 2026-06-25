import streamlit as st
import google.generativeai as genai
import time
import random

# Sayfa ayarlarını v20 PRO olarak güncelledik
st.set_page_config(page_title="SÜPERZEKA v20 PRO", page_icon="🤖", layout="wide")

# 🎨 SİBER RENK DÜZELTME MERKEZİ (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; }
    h1, h2, h3, h4, h5, h6, p, span, label, li, div, b, strong { color: #00ffcc !important; font-family: 'Consolas', monospace !important; }
    input, textarea { background-color: #111111 !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; font-family: 'Consolas', monospace !important; }
    [data-testid="stSidebar"] { background-color: #0c0c0c !important; border-right: 2px solid #00ffcc; }
    [data-testid="stSidebar"] * { color: #00ffcc !important; font-family: 'Consolas', monospace !important; }
    .stButton>button { background-color: #1a1a1a !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; width: 100%; }
    .stButton>button:hover { background-color: #00ffcc !important; color: #050505 !important; }
    .chat-box { background-color: #111111; border: 1px dashed #00ffcc; padding: 12px; border-radius: 8px; margin-top: 10px; margin-bottom: 10px; color: #00ffcc !important; }
    .status-panel { background-color: #002211 !important; padding: 10px; border-radius: 5px; border: 1px solid #00ffcc; text-align: center; margin-bottom: 15px; }
    .logo-kutusu { background-color: #111; border: 2px solid #00ffcc; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 15px; }
    .bilgi-paneli { background-color: #050505 !important; border: 1px solid #00ffcc; padding: 15px; border-radius: 8px; margin-top: 15px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# API Şifre Kontrolü
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("API Anahtarı bulunamadı kanka!")

# --- SİSTEM HAFIZASI ---
if "mod" not in st.session_state: st.session_state.mod = "ÖĞRENCİ"
if "hata_sayaci" not in st.session_state: st.session_state.hata_sayaci = 0
if "guvenlik_kilidi" not in st.session_state: st.session_state.guvenlik_kilidi = False
if "canvas_icerik" not in st.session_state: st.session_state.canvas_icerik = "# Siber Canvas\n\nBuraya ödevini veya kodunu yapıştır kanka!"
if "bulut_kullanici" not in st.session_state: st.session_state.bulut_kullanici = None
if "bulut_veritabani" not in st.session_state: st.session_state.bulut_veritabani = {}

# --- BİLGİ HAVUZLARI ---
gunun_bilgileri = [
    "🤖 YAPAY ZEKANIN TEMELLERİ: 1956'da başladı, bugün her yerde!",
    "🌐 İNTERNET: ARPANET'ten günümüze ışık hızında bilgi.",
    "🧠 BEYİN: Evrendeki en karmaşık biyolojik işlemci.",
    "💾 EVRİM: ENIAC'tan cebimizdeki süper bilgisayarlara."
]
hadis_havuzu = ["“İlim öğrenmek her Müslümana farzdır.”", "“Kolaylaştırınız, zorlaştırmayınız.”"]

# --- SOL PANEL (SIDEBAR) ---
st.sidebar.title("🤖 SÜPERZEKA v20 PRO")
st.sidebar.header("☁️ SüperZeka Cloud")
if not st.session_state.bulut_kullanici:
    kullanici_adi = st.sidebar.text_input("Siber Kullanıcı Adı:")
    if st.sidebar.button("Bağlan ⚡"):
        st.session_state.bulut_kullanici = kullanici_adi.strip().lower()
        st.rerun()
else:
    st.sidebar.markdown(f"<div class='status-panel'>☁️ Oturum: <b>{st.session_state.bulut_kullanici}</b></div>", unsafe_allow_html=True)
    if st.sidebar.button("Oturumu Kapat 🛑"):
        st.session_state.bulut_kullanici = None
        st.rerun()

# Mod Değiştirici
st.sidebar.header("🔐 Mod Değiştirici")
if st.session_state.mod == "ÖĞRENCİ":
    sifre = st.sidebar.text_input("Şifre:", type="password")
    if st.sidebar.button("Öğretmen Moduna Geç 🔑"):
        if sifre == time.strftime("%M"): st.session_state.mod = "ÖĞRETMEN"; st.rerun()
else:
    if st.sidebar.button("Öğrenci Moduna Dön 🎒"): st.session_state.mod = "ÖĞRENCİ"; st.rerun()

# --- ANA EKRAN ---
st.markdown("<div class='logo-kutusu'><h1>🧠 [ SÜPERZEKA v20 PRO ] 🧠</h1><p>Mimar: Yağızalp Karaman</p></div>", unsafe_allow_html=True)

# 🖼️ ÇİFT EKRAN
sol, sag = st.columns([1, 1])
with sol:
    st.subheader("📝 Canvas")
    st.session_state.canvas_icerik = st.text_area("Çalışma Alanı:", value=st.session_state.canvas_icerik, height=400)

with sag:
    st.subheader("🧠 Siber Sorgu")
    u_input = st.text_input("Komut gönder:")
    if st.button("Çalıştır 🚀") and u_input:
        talimat = (
            "Sen SÜPERZEKA v20 PRO'sun. Kullanıcı ÖĞRENCİ modunda: Selamun aleyküm kanka diyerek başla, "
            "samimi anlat ve '💡 Siber İpucu' ver. ÖĞRETMEN modunda: Profesyonel, doğrudan cevap ver."
        )
        model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=talimat)
        res = model.generate_content(u_input)
        if st.session_state.bulut_kullanici:
            st.session_state.bulut_veritabani.setdefault(st.session_state.bulut_kullanici, []).append((u_input, res.text))
        st.rerun()

    # Sohbet Geçmişi
    gecmis = st.session_state.bulut_veritabani.get(st.session_state.bulut_kullanici, []) if st.session_state.bulut_kullanici else []
    for q, a in reversed(gecmis):
        st.markdown(f"<div class='chat-box'>👤 <b>Sen:</b> {q}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-box' style='border-color:#00ffcc;'>🤖 <b>SüperZeka:</b> {a}</div>", unsafe_allow_html=True)
