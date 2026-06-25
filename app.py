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
if "sohbet_gecmisi" not in st.session_state: st.session_state.sohbet_gecmisi = []
if "canvas_icerik" not in st.session_state: st.session_state.canvas_icerik = "# Siber Canvas\n\nBuraya ödevini veya kodunu yapıştır kanka!"
if "bulut_kullanici" not in st.session_state: st.session_state.bulut_kullanici = None
if "bulut_veritabani" not in st.session_state: st.session_state.bulut_veritabani = {}

# --- GÜNCELLENMİŞ BİLGİ HAVUZU ---
gunun_bilgileri = [
    "🤖 YAPAY ZEKANIN TEMELLERİ: 1956 Dartmouth Konferansı'ndan günümüze, makinelerin öğrenme ve problem çözme yeteneği her geçen gün devrimsel bir şekilde artıyor.",
    "🌐 İNTERNET TARİHİ: 1960'lardaki ARPANET'ten günümüzün global World Wide Web ağına, bilgiye erişim artık ışık hızında.",
    "🧠 BEYNİMİZİN SIRLARI: 86 milyar nöronluk biyolojik işlemcimiz, evrendeki en gelişmiş ve hala tam çözülememiş sistemdir.",
    "🌌 UZAYIN DERİNLİKLERİ: 13.8 milyar yıllık evrenimiz, keşfedilmeyi bekleyen milyarlarca galaksi ve gizemle dolu.",
    "💾 BİLGİSAYAR EVRİMİ: Odanın yarısını kaplayan ENIAC'tan cebimizdeki süper güçlere kadar, teknoloji dünyayı değiştirdi."
]
hadis_havuzu = ["“İlim öğrenmek her Müslümana farzdır.”", "“Kolaylaştırınız, zorlaştırmayınız.”", "“En hayırlınız, ahlakı en güzel olandır.”"]

# --- SOL PANEL (SIDEBAR) ---
st.sidebar.title("🤖 SÜPERZEKA v20 PRO")
st.sidebar.header("☁️ SüperZeka Cloud Girişi")

if not st.session_state.bulut_kullanici:
    kullanici_adi = st.sidebar.text_input("Siber Kullanıcı Adınız:", placeholder="Örn: yagizalp_pro")
    if st.sidebar.button("Bulut Hafızasına Bağlan ⚡"):
        if kullanici_adi:
            st.session_state.bulut_kullanici = kullanici_adi.strip().lower()
            if st.session_state.bulut_kullanici not in st.session_state.bulut_veritabani:
                st.session_state.bulut_veritabani[st.session_state.bulut_kullanici] = []
            st.rerun()
else:
    st.sidebar.markdown(f"<div class='status-panel'>☁️ Bulut Oturumu: <b>{st.session_state.bulut_kullanici}</b></div>", unsafe_allow_html=True)
    if st.sidebar.button("Bulut Oturumunu Kapat 🛑"):
        st.session_state.bulut_kullanici = None
        st.rerun()

st.sidebar.markdown(f"<div class='status-panel'>Mevcut Mod: <b>{st.session_state.mod}</b></div>", unsafe_allow_html=True)
arama_sorgusu = st.sidebar.text_input("🔍 Geçmiş konulardan bir kelime ara:", placeholder="Örn: Git...")

# Mod Değiştirici
st.sidebar.header("🔐 Mod Değiştirici")
if st.session_state.mod == "ÖĞRENCİ":
    sifre = st.sidebar.text_input("Öğretmen Modu Şifresi:", type="password")
    if st.sidebar.button("Öğretmen Moduna Geç 🔑"):
        if sifre == time.strftime("%M"):
            st.session_state.mod = "ÖĞRETMEN"
            st.rerun()
        else:
            st.session_state.hata_sayaci += 1
            st.sidebar.error(f"Hatalı! ({st.session_state.hata_sayaci}/3)")
            if st.session_state.hata_sayaci >= 3: st.session_state.guvenlik_kilidi = True; st.rerun()
else:
    if st.sidebar.button("Öğrenci Moduna Dön 🎒"):
        st.session_state.mod = "ÖĞRENCİ"
        st.rerun()

# --- ANA EKRAN ---
if st.session_state.guvenlik_kilidi: st.error("🚨 SİSTEM KİLİTLENDİ!"); st.stop()

st.markdown("""
    <div class='logo-kutusu'>
        <h1 style='font-size: 35px; margin: 0; padding: 5px;'>🧠 [ SÜPERZEKA v20 PRO ] 🧠</h1>
        <p style='color: #00ffcc !important; margin-top: 10px; font-size: 14px;'>⚡ Mimar: Yağızalp Karaman | Siber Yapay Zeka Üssü ⚡</p>
    </div>
""", unsafe_allow_html=True)

st.code(f"""
[SİSTEM LOGU] v20 PRO | Bulut Durumu: {"AKTİF" if st.session_state.bulut_kullanici else "ÇEVRİMDIŞI"}
🕋 Hadis: {random.choice(hadis_havuzu)}
""", language="text")

# BİLGİ PANELİ
st.markdown(f"""
    <div class='bilgi-paneli'>
        <h3 style='margin: 0; padding-bottom: 8px; border-bottom: 1px dashed #00ffcc;'>💡 Günün Harika Bilgisi</h3>
        <p style='margin-top: 12px;'>{random.choice(gunun_bilgileri)}</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")
sol, sag = st.columns([1, 1])

with sol:
    st.subheader("📝 Canvas")
    st.session_state.canvas_icerik = st.text_area("Çalışma Alanı:", value=st.session_state.canvas_icerik, height=400)

with sag:
    st.subheader("🧠 Siber Sorgu Ekranı")
    with st.form(key="sorgu_formu", clear_on_submit=True):
        u_input = st.text_input("SüperZeka'ya bir komut gönder kanka:", placeholder="Mesajını yaz...")
        submit_button = st.form_submit_button(label="Sorgula / Çalıştır 🚀")
        
    aktif_user = st.session_state.bulut_kullanici if st.session_state.bulut_kullanici else "misafir"
    if aktif_user not in st.session_state.bulut_veritabani: st.session_state.bulut_veritabani[aktif_user] = []

    if submit_button and u_input:
        with st.spinner("🧠 Sentezleniyor..."):
            try:
                gecmis_listesi = st.session_state.bulut_veritabani[aktif_user]
                gecmis = "\n".join([f"Kullanıcı: {q}\nSüperZeka: {a}" for q, a in gecmis_listesi[-3:]])
                talimat = f"Sen SÜPERZEKA v20 PRO'sun. Mimarin Yağızalp KARAMAN. {st.session_state.mod} modundasın."
                
                model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=talimat)
                res = model.generate_content(u_input)
                st.session_state.bulut_veritabani[aktif_user].append((u_input, res.text))
                st.rerun()
            except Exception as e: st.error(f"Bağlantı Hatası: {e}")

    user_gecmis = st.session_state.bulut_veritabani[aktif_user]
    for q, a in reversed(user_gecmis):
        st.markdown(f"<div class='chat-box'>👤 <b>Sen:</b> {q}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-box' style='border-color:#00ffcc;'>🤖 <b>SÜPERZEKA:</b> {a}</div>", unsafe_allow_html=True)
