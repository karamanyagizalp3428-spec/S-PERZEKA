import streamlit as st
import google.generativeai as genai
import time
import random
import json

# Sayfa ayarlarını v14 PRO olarak güncelliyoruz
st.set_page_config(page_title="SÜPERZEKA v14 PRO", page_icon="🤖", layout="wide")

# 🎨 SİBER VE İSLAMİ TASARIM (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; }
    h1, h2, h3, p, span, label { color: #00ffcc !important; font-family: 'Consolas', monospace !important; }
    input, textarea { background-color: #111111 !important; color: white !important; border: 1px solid #00ffcc !important; font-family: 'Consolas', monospace !important; }
    [data-testid="stSidebar"] { background-color: #0c0c0c !important; border-right: 2px solid #00ffcc; }
    .stButton>button { background-color: #1a1a1a !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; width: 100%; }
    .chat-box { background-color: #111111; border: 1px dashed #00ffcc; padding: 12px; border-radius: 8px; margin-top: 10px; margin-bottom: 10px; }
    .status-panel { background-color: #002211; padding: 10px; border-radius: 5px; border: 1px solid #00ffcc; text-align: center; margin-bottom: 15px; }
    .stImage { border: 2px solid #00ffcc !important; border-radius: 10px; padding: 5px; background-color: #111; }
    </style>
""", unsafe_allow_html=True)

# API Şifre Kontrolü
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("API Anahtarı bulunamadı kanka!")

# --- SİSTEM HAFIZASI (Session State) ---
if "mod" not in st.session_state: st.session_state.mod = "ÖĞRENCİ"
if "hata_sayaci" not in st.session_state: st.session_state.hata_sayaci = 0
if "guvenlik_kilidi" not in st.session_state: st.session_state.guvenlik_kilidi = False
if "pomodoro_saniye" not in st.session_state: st.session_state.pomodoro_saniye = 25 * 60
if "pomodoro_calisiyor" not in st.session_state: st.session_state.pomodoro_calisiyor = False
if "canvas_icerik" not in st.session_state: 
    st.session_state.canvas_icerik = "# Siber Canvas\n\nBuraya ödevini veya kodunu yapıştır kanka!"

# ☁️ BULUT BULUCU LOGİN SİSTEMİ
if "bulut_kullanici" not in st.session_state:
    st.session_state.bulut_kullanici = None
if "bulut_veritabani" not in st.session_state:
    # Sahte bulut veritabanı (İleride API'ye bağlanacak alan kanka)
    st.session_state.bulut_veritabani = {}

# --- VERİ HAVUZLARI ---
gunun_bilgileri = ["Sıfırı Harezmi buldu.", "İlk robotu El-Cezeri yaptı.", "Yazılım Binary (0-1) sistemidir."]
hadis_havuzu = ["“İlim öğrenmek her Müslümana farzdır.”", "“Kolaylaştırınız, zorlaştırmayınız.”"]

# --- SOL PANEL (SIDEBAR) ---
st.sidebar.title("🤖 SÜPERZEKA v14 PRO")

# ☁️ BULUT GİRİŞ PANELİ
st.sidebar.header("☁️ SüperZeka Cloud Girişi")
if not st.session_state.bulut_kullanici:
    kullanici_adi = st.sidebar.text_input("Siber Kullanıcı Adınız:", placeholder="Örn: yagizalp_pro")
    if st.sidebar.button("Bulut Hafızasına Bağlan ⚡"):
        if kullanici_adi:
            st.session_state.bulut_kullanici = kullanici_adi.strip().lower()
            if st.session_state.bulut_kullanici not in st.session_state.bulut_veritabani:
                st.session_state.bulut_veritabani[st.session_state.bulut_kullanici] = []
            st.sidebar.success(f"Bulut aktif: {st.session_state.bulut_kullanici}")
            st.rerun()
else:
    st.sidebar.markdown(f"<div class='status-panel'>☁️ Bulut Oturumu: <b>{st.session_state.bulut_kullanici}</b></div>", unsafe_allow_html=True)
    if st.sidebar.button("Bulut Oturumunu Kapat 🛑"):
        st.session_state.bulut_kullanici = None
        st.rerun()

st.sidebar.markdown(f"<div class='status-panel'>Mevcut Mod: <b>{st.session_state.mod}</b></div>", unsafe_allow_html=True)

# 🔍 SİBER GEÇMİŞ ARAMA MOTORU
st.sidebar.header("🔍 Konuşma Arama")
arama_sorgusu = st.sidebar.text_input("Geçmiş konulardan bir kelime ara:", placeholder="Örn: Git kurulumu...")

# 🔐 MOD DEĞİŞTİRİCİ
st.sidebar.header("🔐 Mod Değiştirici")
if st.session_state.mod == "ÖĞRENCİ":
    sifre = st.sidebar.text_input("Öğretmen Modu Şifresi:", type="password")
    if st.sidebar.button("Öğretmen Moduna Geç 🔑"):
        if sifre == time.strftime("%M"):
            st.session_state.mod = "ÖĞRETMEN"
            st.session_state.hata_sayaci = 0
            st.rerun()
        else:
            st.session_state.hata_sayaci += 1
            st.sidebar.error(f"Hatalı! ({st.session_state.hata_sayaci}/3)")
            if st.session_state.hata_sayaci >= 3: st.session_state.guvenlik_kilidi = True; st.rerun()
else:
    if st.sidebar.button("Öğrenci Moduna Dön 🎒"):
        st.session_state.mod = "ÖĞRENCİ"
        st.rerun()

st.sidebar.markdown("---")
if st.sidebar.button("Sohbet Geçmişini Temizle 🗑️"):
    if st.session_state.bulut_kullanici:
        st.session_state.bulut_veritabani[st.session_state.bulut_kullanici] = []
    st.rerun()

# --- ANA EKRAN ---
if st.session_state.guvenlik_kilidi: st.error("🚨 SİSTEM KİLİTLENDİ!"); st.stop()

st.image("sz_logo.png", use_container_width=True)
st.code(f"""
[SİSTEM LOGU] v14 PRO | Bulut Durumu: {"AKTİF" if st.session_state.bulut_kullanici else "ÇEVRİMDIŞI"}
🕋 Hadis: {random.choice(hadis_havuzu)}
""", language="text")

with st.expander("💡 Günün Bilgileri", expanded=True):
    for bilgi in gunun_bilgileri: st.markdown(f"- {bilgi}")

st.markdown("---")

# 🖼 *ÇİFT EKRAN*
sol, sag = st.columns([1, 1])

with sol:
    st.subheader("📝 Canvas")
    st.session_state.canvas_icerik = st.text_area("Çalışma Alanı:", value=st.session_state.canvas_icerik, height=400)

with sag:
    st.subheader("🧠 Siber Sorgu Ekranı")
    
    with st.form(key="sorgu_formu", clear_on_submit=True):
        u_input = st.text_input("SüperZeka'ya bir komut gönder kanka:", placeholder="Mesajını yaz ve Enter'a bas...")
        submit_button = st.form_submit_button(label="Sorgula / Çalıştır 🚀")
        
    # Kullanıcı adını alıyoruz, giriş yapmadıysa 'misafir' yapıyoruz kanka
    aktif_user = st.session_state.bulut_kullanici if st.session_state.bulut_kullanici else "misafir"
    if aktif_user not in st.session_state.bulut_veritabani:
        st.session_state.bulut_veritabani[aktif_user] = []

    if submit_button and u_input:
        with st.spinner("🧠 Sentezleniyor..."):
            try:
                gecmis_listesi = st.session_state.bulut_veritabani[aktif_user]
                gecmis = "\n".join([f"Kullanıcı: {q}\nSüperZeka: {a}" for q, a in gecmis_listesi[-3:]])
                
                talimat = (
                    f"Sen SÜPERZEKA v14 PRO'sun. Mimarin Yağızalp KARAMAN. Müslüman bir asistansın. "
                    f"Canvas İçeriği: {st.session_state.canvas_icerik}\nGeçmiş: {gecmis}\n"
                )
                if st.session_state.mod == "ÖĞRENCİ":
                    talimat += "Selamun aleyküm kanka diyerek başla. Doğrudan cevap verme, konuyu anlat ve '💡 Siber İpucu' ver. Samimi ol."
                else:
                    talimat += "ÖĞRETMEN modundasin. Selamsız, doğrudan, profesyonel tam cevap ver."

                model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=talimat)
                res = model.generate_content(u_input)
                
                # ☁️ BULUT SİSTEMİNE KAYIT ATILIYOR!
                st.session_state.bulut_veritabani[aktif_user].append((u_input, res.text))
                st.rerun()
            except Exception as e: st.error(f"Bağlantı Hatası: {e}")

    # 📜 BULUTTAN GELEN SOHBET AKIŞI
    user_gecmis = st.session_state.bulut_veritabani[aktif_user]
    if user_gecmis:
        st.markdown("---")
        if arama_sorgusu:
            st.write(f"🔍 **'{arama_sorgusu}' İçeren Bulut Kayıtları:**")
            for q, a in reversed(user_gecmis):
                if arama_sorgusu.lower() in q.lower() or arama_sorgusu.lower() in a.lower():
                    st.markdown(f"<div class='chat-box'>👤 <b>Sen:</b> {q}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='chat-box' style='border-color:#00ffcc;'>🤖 <b>SÜPERZEKA:</b> {a}</div>", unsafe_allow_html=True)
        else:
            st.write("💬 **Bulut Sohbet Akışı:**")
            for q, a in reversed(user_gecmis):
                st.markdown(f"<div class='chat-box'>👤 <b>Sen:</b> {q}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='chat-box' style='border-color:#00ffcc;'>🤖 <b>SÜPERZEKA:</b> {a}</div>", unsafe_allow_html=True)
