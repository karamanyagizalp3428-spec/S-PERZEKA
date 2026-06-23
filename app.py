import streamlit as st
import google.generativeai as genai
import time
import random

# Sayfa ayarlarını yapıyoruz
st.set_page_config(page_title="SÜPERZEKA v13 ULTRA PRO", page_icon="🤖", layout="wide")

# 🎨 SİBER RENKLENDİRME (CSS) - Ekranı simsiyah ve yeşil yapıyoruz kanka!
st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; }
    h1, h2, h3, p, span, label { color: #00ffcc !important; font-family: 'Consolas', monospace !important; }
    input { background-color: #111111 !important; color: white !important; border: 1px solid #00ffcc !important; }
    [data-testid="stSidebar"] { background-color: #111111 !important; border-right: 1px solid #00ffcc; }
    .stButton>button { background-color: #222222 !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; }
    </style>
""", unsafe_allow_html=True)

# API Şifre Kontrolü
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("API Anahtarı bulunamadı kanka!")

# SİSTEM HAFIZASI (Session State)
if "mod" not in st.session_state:
    st.session_state.mod = "ÖĞRENCİ"
if "hata_sayaci" not in st.session_state:
    st.session_state.hata_sayaci = 0
if "guvenlik_kilidi" not in st.session_state:
    st.session_state.guvenlik_kilidi = False
# Pomodoro Zamanı Hafızası
if "pomodoro_saniye" not in st.session_state:
    st.session_state.pomodoro_saniye = 25 * 60
if "pomodoro_calisiyor" not in st.session_state:
    st.session_state.pomodoro_calisiyor = False

# Bilgi Havuzu
gunun_bilgileri = [
    "Işık, Güneş'ten Dünya'ya 8 dakikada ulaşır.",
    "Harezmi sıfırıulan kişidir.",
    "Yazılımın temeli Binary sistemidir."
]

# --- SOL PANEL (SIDEBAR) ---
st.sidebar.title("🤖 SÜPERZEKA v13")
st.sidebar.subheader("Mimar: Yağızalp Karaman")
st.sidebar.markdown("---")

# ⏱️ GERÇEK POMODORO SAYAÇ SİSTEMİ
st.sidebar.header("⏱️ Pomodoro Sayacı")

# Dakika ve Saniye hesaplama
dakika, saniye = divmod(st.session_state.pomodoro_saniye, 60)
st.sidebar.subheader(f"⏳ Kalan Süre: {dakika:02d}:{saniye:02d}")

# Başlat / Durdur Butonları
if not st.session_state.pomodoro_calisiyor:
    if st.sidebar.button("Pomodoro'yu Başlat ⏱️"):
        st.session_state.pomodoro_calisiyor = True
        st.rerun()
else:
    if st.sidebar.button("Sayacı Durdur 🛑"):
        st.session_state.pomodoro_calisiyor = False
        st.rerun()
    
    # Süreyi azalt ve ekranı yenile kanka
    if st.session_state.pomodoro_saniye > 0:
        time.sleep(1)
        st.session_state.pomodoro_saniye -= 1
        st.rerun()
    else:
        st.session_state.pomodoro_calisiyor = False
        st.session_state.pomodoro_saniye = 25 * 60
        st.sidebar.balloons()
        st.sidebar.success("Harika çalıştın! Mola zamanı kanka! ☕")

if st.sidebar.button("Sayacı Sıfırla 🔄"):
    st.session_state.pomodoro_saniye = 25 * 60
    st.session_state.pomodoro_calisiyor = False
    st.rerun()

st.sidebar.markdown("---")

# 🔐 GÜVENLİK ANAHTARI SİSTEMİ
st.sidebar.header("🔐 Güvenlik Paneli")
st.sidebar.write(f"Mevcut Durum: **{st.session_state.mod} MODU**")

if st.session_state.mod == "ÖĞRENCİ":
    sifre_girisi = st.sidebar.text_input("Sistem Güvenlik Anahtarını Girin:", type="password")
    if st.sidebar.button("Erişim İste 🔑"):
        su_anki_dakika = time.strftime("%M")
        if sifre_girisi == su_anki_dakika:
            st.session_state.mod = "ÖĞRETMEN"
            st.sidebar.success("Erişim Onaylandı: ÖĞRETMEN MODU AKTİF.")
            st.rerun()
        else:
            st.session_state.hata_sayaci += 1
            if st.session_state.hata_sayaci >= 3:
                st.session_state.guvenlik_kilidi = True
            st.sidebar.error(f"Hatalı şifre! ({st.session_state.hata_sayaci}/3)")
else:
    if st.sidebar.button("Öğrenci Moduna Dön 🎒"):
        st.session_state.mod = "ÖĞRENCİ"
        st.session_state.hata_sayaci = 0
        st.rerun()

# --- ANA EKRAN İÇERİĞİ ---
if st.session_state.guvenlik_kilidi:
    st.error("🚨🚨🚨 SİBER İHLAL: Üst üste 3 kez hatalı şifre girildi! Sistem kilitlendi!")
    foto = st.camera_input("Güvenlik doğrulaması için yüzünü göster kanka:")
    if foto: st.success("Kanıt kaydedildi! Giriş engellendi.")
    st.stop()

# Sistem Logu
st.code(f"""
[SİSTEM LOGU]:
🤖 SÜPERZEKA v13 Başlatıldı.
🧠 5 Yapay Zeka Beyni Çevrimiçi.
💡 GÜNÜN BİLGİSİ: {random.choice(gunun_bilgileri)}
""", language="text")

st.subheader("🧠 Siber Asistan Sorgu Ekranı")
user_input = st.text_input("SüperZeka'ya bir komut veya soru gönder kanka:", placeholder="Örn: Harezmi kimdir?")

if st.button("Sorgula / Çalıştır 🚀"):
    if user_input:
        with st.spinner("🧠 5 Yapay Zeka Beyni Ortak Karar Alıyor ve Sentezliyor..."):
            try:
                sentez_talimati = (
                    "Sen SüperZeka v13'sün. Arkada çalışan 5 yapay zeka modelinin "
                    "fikirlerini siber bir süzgeçten geçir ve tek bir mükemmel sentez (özet) cevabı sun. "
                )
                if st.session_state.mod == "ÖĞRENCİ":
                    sentez_talimati += "Şu an ÖĞRENCİ modundasin. Sentez cevabını 5. sınıf seviyesinde, eğlenceli ve bol emojili ver."
                else:
                    sentez_talimati += "Şu an ÖĞRETMEN modundasin. Sentez cevabını çok detaylı, profesyonel ve ders notu kıvamında ver."

                model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=sentez_talimati)
                response = model.generate_content(user_input)

                st.markdown("---")
                st.success("🤖 SÜPERZEKA - 5 MODEL ORTAK SENTEZ CEVABI:")
                st.write(response.text)

            except Exception as e:
                st.error(f"Siber bağlantı hatası oluştu kanka: {e}")
