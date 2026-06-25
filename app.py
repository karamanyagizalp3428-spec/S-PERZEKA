import streamlit as st
import google.generativeai as genai
import time
import random

# Sayfa ayarları
st.set_page_config(page_title="SÜPERZEKA v20 PRO", page_icon="🤖", layout="wide")

# CSS - Siber Tasarım
st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; }
    h1, h2, h3, h4, h5, h6, p, span, label, li, div, b, strong { color: #00ffcc !important; font-family: 'Consolas', monospace !important; }
    input, textarea { background-color: #111111 !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; font-family: 'Consolas', monospace !important; }
    [data-testid="stSidebar"] { background-color: #0c0c0c !important; border-right: 2px solid #00ffcc; }
    .stButton>button { background-color: #1a1a1a !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; width: 100%; }
    .chat-box { background-color: #111111; border: 1px dashed #00ffcc; padding: 12px; border-radius: 8px; margin-top: 10px; margin-bottom: 10px; color: #00ffcc !important; }
    .logo-kutusu { background-color: #111; border: 2px solid #00ffcc; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# API Ayarları
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("API Anahtarı bulunamadı kanka!")

# Session State
if "mod" not in st.session_state: st.session_state.mod = "ÖĞRENCİ"
if "canvas_icerik" not in st.session_state: st.session_state.canvas_icerik = "# Siber Canvas\n\nBuraya ödevini veya kodunu yapıştır kanka!"
if "bulut_veritabani" not in st.session_state: st.session_state.bulut_veritabani = {}

# Bilgiler
gunun_bilgileri = [
    "🤖 YAPAY ZEKANIN TEMELLERİ: 1956 Dartmouth Konferansı'ndan günümüze, makinelerin öğrenme yeteneği devrimsel bir şekilde artıyor.",
    "🌐 İNTERNET TARİHİ: 1960'lardaki ARPANET'ten günümüze, bilgiye erişim artık ışık hızında.",
    "🧠 BEYNİMİZİN SIRLARI: 86 milyar nöronluk biyolojik işlemcimiz, evrendeki en gelişmiş sistemdir.",
    "💾 BİLGİSAYAR EVRİMİ: İlk bilgisayar bir odaydı, şimdi cebimizde süper güçler taşıyoruz."
]

# Arayüz
st.markdown("<div class='logo-kutusu'><h1>🧠 [ SÜPERZEKA v20 PRO ] 🧠</h1><p>⚡ Mimar: Yağızalp Karaman</p></div>", unsafe_allow_html=True)

# Mod Değiştirici (Sidebar)
st.sidebar.title("🤖 SÜPERZEKA v20 PRO")
if st.sidebar.button("Mod Değiştir (Öğrenci/Öğretmen)"):
    st.session_state.mod = "ÖĞRETMEN" if st.session_state.mod == "ÖĞRENCİ" else "ÖĞRENCİ"
    st.rerun()

# Ana Ekran
sol, sag = st.columns([1, 1])
with sol:
    st.subheader("📝 Canvas")
    st.session_state.canvas_icerik = st.text_area("Çalışma Alanı:", value=st.session_state.canvas_icerik, height=400)

with sag:
    st.subheader("🧠 Siber Sorgu Ekranı")
    u_input = st.text_input("SüperZeka'ya komut gönder:")
    if st.button("Sorgula 🚀") and u_input:
        with st.spinner("🧠 Sentezleniyor..."):
            # Talimat Mantığı
            if st.session_state.mod == "ÖĞRENCİ":
                talimat = "Sen SÜPERZEKA v20 PRO'sun. Mimarin Yağızalp KARAMAN. Kullanıcı ÖĞRENCİ modunda. Selamun aleyküm kanka diyerek başla. Konuyu basitçe anlat, samimi ol ve mutlaka '💡 Siber İpucu' ver."
            else:
                talimat = "Sen SÜPERZEKA v20 PRO'sun. Öğretmen modundasın. Selamsız, doğrudan, profesyonel teknik cevap ver."
            
            model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=talimat)
            res = model.generate_content(u_input)
            
            if "misafir" not in st.session_state.bulut_veritabani: st.session_state.bulut_veritabani["misafir"] = []
            st.session_state.bulut_veritabani["misafir"].append((u_input, res.text))
            st.rerun()

    # Sohbet Geçmişi
    for q, a in reversed(st.session_state.bulut_veritabani.get("misafir", [])):
        st.markdown(f"<div class='chat-box'>👤 <b>Sen:</b> {q}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-box' style='border-color:#00ffcc;'>🤖 <b>SÜPERZEKA:</b> {a}</div>", unsafe_allow_html=True)
