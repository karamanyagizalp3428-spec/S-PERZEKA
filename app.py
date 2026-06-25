import streamlit as st
import google.generativeai as genai
import time
import random

# Sayfa ayarları
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

# API Ayarları
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("API Anahtarı bulunamadı kanka!")

# --- SİSTEM HAFIZASI ---
if "mod" not in st.session_state: st.session_state.mod = "ÖĞRENCİ"
if "canvas_icerik" not in st.session_state: st.session_state.canvas_icerik = "# Siber Canvas\n\nBuraya ödevini veya kodunu yapıştır kanka!"
if "bulut_kullanici" not in st.session_state: st.session_state.bulut_kullanici = None
if "bulut_veritabani" not in st.session_state: st.session_state.bulut_veritabani = {}

# --- BİLGİ HAVUZLARI ---
gunun_bilgileri = ["🤖 Yapay zeka, 1956'da Dartmouth Konferansı ile doğmuştur.", "🌐 İnternet, ARPANET ile gelişti.", "🧠 İnsan beyni saniyede trilyonlarca işlem yapar."]
hadis_havuzu = ["“İlim öğrenmek her Müslümana farzdır.”", "“Kolaylaştırınız, zorlaştırmayınız.”", "“En hayırlınız, ahlakı en güzel olanınızdır.”"]

# --- SIDEBAR ---
st.sidebar.title("🤖 SÜPERZEKA v20 PRO")
if not st.session_state.bulut_kullanici:
    kullanici = st.sidebar.text_input("Siber Kullanıcı Adınız:")
    if st.sidebar.button("Bulut'a Bağlan ⚡") and kullanici:
        st.session_state.bulut_kullanici = kullanici.strip().lower()
        st.rerun()
else:
    st.sidebar.markdown(f"<div class='status-panel'>☁️ Oturum: <b>{st.session_state.bulut_kullanici}</b></div>", unsafe_allow_html=True)
    if st.sidebar.button("Oturumu Kapat 🛑"): st.session_state.bulut_kullanici = None; st.rerun()

if st.sidebar.button("Mod Değiştir 🔄"): 
    st.session_state.mod = "ÖĞRETMEN" if st.session_state.mod == "ÖĞRENCİ" else "ÖĞRENCİ"
    st.rerun()

# --- ANA EKRAN ---
st.markdown("<div class='logo-kutusu'><h1>🧠 [ SÜPERZEKA v20 PRO ] 🧠</h1><p>Mimar: Yağızalp KARAMAN</p></div>", unsafe_allow_html=True)

col_l, col_r = st.columns(2)
with col_l:
    st.markdown(f"<div class='bilgi-paneli'><h3>💡 Günün Bilgisi</h3>{random.choice(gunun_bilgileri)}</div>", unsafe_allow_html=True)
with col_r:
    st.markdown(f"<div class='bilgi-paneli'><h3>🕋 Hadis-i Şerif</h3>{random.choice(hadis_havuzu)}</div>", unsafe_allow_html=True)

# Çift Ekran: Canvas ve Sorgu
sol, sag = st.columns(2)
with sol:
    st.subheader("📝 Canvas")
    st.session_state.canvas_icerik = st.text_area("Çalışma Alanı:", value=st.session_state.canvas_icerik, height=400)

with sag:
    st.subheader("🧠 Siber Sorgu Ekranı")
    u_input = st.text_input("Komut gönder:")
    
    if st.button("Sorgula / Çalıştır 🚀") and u_input:
        with st.spinner("Sentezleniyor..."):
            # ÖĞRENCİ MODU KURALI: ASLA CEVAP VERME, İPUCU VER
            if st.session_state.mod == "ÖĞRENCİ":
                talimat = ("Sen SÜPERZEKA v20 PRO'sun. Öğrenci modundasın. GÖREVİN: "
                           "ASLA DOĞRUDAN CEVABI VERME. Öğrencinin konuyu anlaması için ona "
                           "yönlendirici ipuçları ve sorular sor. Cevabı asla açıklama. "
                           "Cevabını '💡 Siber İpucu: [Yönlendirici Bilgi]' ile bitir.")
            else:
                talimat = ("Sen SÜPERZEKA v20 PRO'sun. Öğretmen modundasın. "
                           "Profesyonel, teknik ve doğrudan cevap ver.")
            
            try:
                model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=talimat)
                res = model.generate_content(f"Canvas İçeriği: {st.session_state.canvas_icerik}\nSoru: {u_input}")
                
                user = st.session_state.bulut_kullanici or "misafir"
                if user not in st.session_state.bulut_veritabani: st.session_state.bulut_veritabani[user] = []
                st.session_state.bulut_veritabani[user].append((u_input, res.text))
                st.rerun()
            except Exception as e: st.error(f"Sistem Hatası: {e}")

    # Geçmişi listele
    user = st.session_state.bulut_kullanici or "misafir"
    for q, a in reversed(st.session_state.bulut_veritabani.get(user, [])):
        st.markdown(f"<div class='chat-box'>👤 <b>Sen:</b> {q}<br><br>🤖 <b>SüperZeka:</b> {a}</div>", unsafe_allow_html=True)
