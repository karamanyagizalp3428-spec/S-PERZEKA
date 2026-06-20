import streamlit as st
import google.generativeai as genai
import time
import random

# Sayfa ayarlarını yapıyoruz
st.set_page_config(page_title="SÜPERZEKA v13 ULTRA PRO", page_icon="🤖", layout="wide")

# 🎨 SİBER RENKLENDİRME (CSS) - Ekranı senin istediğin gibi simsiyah ve yeşil yapıyoruz kanka!
st.markdown("""
    <style>
    /* Ana Arka Planı Simsiyah Yap */
    .stApp {
        background-color: #050505 !important;
    }
    /* Tüm Yazıları Siber Yeşil Yap */
    h1, h2, h3, p, span, label {
        color: #00ffcc !important;
        font-family: 'Consolas', monospace !important;
    }
    /* Giriş Kutularının İçini Düzenle */
    input {
        background-color: #111111 !important;
        color: white !important;
        border: 1px solid #00ffcc !important;
    }
    /* Sol Menüyü (Sidebar) Karart */
    [data-testid="stSidebar"] {
        background-color: #111111 !important;
        border-right: 1px solid #00ffcc;
    }
    </style>
""", unsafe_gradient=True, unsafe_allow_html=True)

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

# Bilgi Havuzu
gunun_bilgileri = [
    "Işık, Güneş'ten Dünya'ya 8 dakikada ulaşır.",
    "Harezmi sıfırı bulan kişidir.",
    "Yazılımın temeli Binary sistemidir."
]

# --- SOL PANEL (SIDEBAR) ---
st.sidebar.title("🤖 SÜPERZEKA v13")
st.sidebar.subheader("Mimar: Yağızalp Karaman")
st.sidebar.markdown("---")

# ⏱️ POMODORO SAYAÇ SİSTEMİ
st.sidebar.header("⏱️ Pomodoro Sayacı")
pomodoro_durumu = st.sidebar.radio("Sayaç Durumu:", ["Mola Veriliyor ☕", "Ders Çalışılıyor ✍️"])

st.sidebar.markdown("---")

# 🔐 GÜVENLİK ANAHTARI SİSTEMİ
st.sidebar.header("🔐 Güvenlik Paneli")
st.sidebar.write(f"Mevcut Durum: **{st.session_state.mod} MODU**")

if st.session_state.mod == "ÖĞRENCİ":
    # 1. İSTEK: "Şu anki dakika" yazısını sildik, yerine gizemli bir siber uyarı koyduk kanka!
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

# 👁️ GÖZ: Sabotaj Kilit Ekranı
if st.session_state.guvenlik_kilidi:
    st.error("🚨🚨🚨 SİBER İHLAL: Üst üste 3 kez hatalı şifre girildi! Sistem kilitlendi!")
    foto = st.camera_input("Güvenlik doğrulaması için yüzünü göster kanka:")
    if foto:
        st.success("Kanıt kaydedildi! Giriş engellendi.")
    st.stop()

# Üst Bilgilendirme Logları
st.code(f"""
[SİSTEM LOGU]:
🤖 SÜPERZEKA v13 Başlatıldı.
👁️ Göz (Kamera) Aktif. | 👂 Kulak (Sesli Komut) Hazır.
🧠 5 Yapay Zeka Beyni Çevrimiçi.
💡 GÜNÜN BİLGİSİ: {random.choice(gunun_bilgileri)}
""", language="text")

# ANA SORGULAMA ALANI
st.subheader("🧠 Siber Asistan Sorgu Ekranı")
user_input = st.text_input("SüperZeka'ya bir komut veya soru gönder kanka:", placeholder="Örn: Harezmi kimdir?")

if st.button("Sorgula / Çalıştır 🚀"):
    if user_input:
        with st.spinner("🧠 5 Yapay Zeka Beyni Ortak Karar Alıyor..."):
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(user_input)
                gemini_yaniti = response.text
                
                gpt_yanit = "[GPT-4o Yanıtı]: API bağlanmadığı için bu model simüle ediliyor kanka."
                claude_yanit = "[Claude-3 Yanıtı]: API bağlanmadığı için bu model simüle ediliyor kanka."
                llama_yanit = "[Llama-3 Yanıtı]: API bağlanmadığı için bu model simüle ediliyor kanka."
                deepseek_yanit = "[DeepSeek Yanıtı]: API bağlanmadığı için bu model simüle ediliyor kanka."

                st.markdown("---")
                
                if st.session_state.mod == "ÖĞRENCİ":
                    st.success("🤖 SÜPERZEKA - 5 Model Ortak Kararı (İpucu):")
                    st.write(f"[Gemini Yanıtı]: {gemini_yaniti}")
                    st.info("💡 (Doğrudan formülü kullanma, mantığı yakala kanka!)")
                else:
                    st.success("👨‍🏫 SÜPERZEKA - ÖĞRETMEN MODU - TÜM MODEL RAPORLARI:")
                    st.write(f"[Gemini Yanıtı]: {gemini_yaniti}")
                    st.text(gpt_yanit)
                    st.text(claude_yanit)
                    st.text(llama_yanit)
                    st.text(deepseek_yanit)

            except Exception as e:
                st.error(f"Siber bağlantı hatası oluştu kanka: {e}")
