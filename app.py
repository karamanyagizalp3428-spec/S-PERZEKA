import streamlit as st
import google.generativeai as genai
import time
import random

# Sayfa ayarlarını siber temaya uygun yapıyoruz kanka
st.set_page_config(page_title="SÜPERZEKA v13 ULTRA PRO", page_icon="🤖", layout="wide")

# API Şifre Kontrolü
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("API Anahtarı bulunamadı kanka!")

# SİSTEM HAFIZASI (Session State) - Sitenin durumları unutmaması için
if "mod" not in st.session_state:
    st.session_state.mod = "ÖĞRENCİ"
if "hata_sayaci" not in st.session_state:
    st.session_state.hata_sayaci = 0
if "guvenlik_kilidi" not in st.session_state:
    st.session_state.guvenlik_kilidi = False

# Bilgi Havuzu (Senin kodundaki gunun_bilgileri)
gunun_bilgileri = [
    "Işık, Güneş'ten Dünya'ya 8 dakikada ulaşır.",
    "Harezmi sıfırı bulan kişidir.",
    "Yazılımın temeli Binary sistemidir."
]

# --- SOL PANEL (SIDEBAR) ---
st.sidebar.title("🤖 SÜPERZEKA v13 ULTRA PRO")
st.sidebar.subheader("Mimar: Yağızalp Karaman")
st.sidebar.markdown("---")

# ⏱️ POMODORO SAYAÇ SİSTEMİ
st.sidebar.header("⏱️ Pomodoro Sayacı")
pomodoro_durumu = st.sidebar.radio("Sayaç Durumu:", ["Mola Veriliyor ☕", "Ders Çalışılıyor ✍️"])
if pomodoro_durumu == "Ders Çalışılıyor ✍️":
    st.sidebar.warning("⏱️ Ders: 25 Dakika Başladı! Odaklan kanka!")
else:
    st.sidebar.success("☕ Harika çalıştın! Mola zamanı.")

st.sidebar.markdown("---")

# 🔐 GÜVENLİK ANAHTARI SİSTEMİ (Dakika Şifresi)
st.sidebar.header("🔐 Güvenlik Paneli")
st.sidebar.write(f"Mevcut Durum: **{st.session_state.mod} MODU**")

if st.session_state.mod == "ÖĞRENCİ":
    sifre_girisi = st.sidebar.text_input("Sistem Anahtarını Gir (Şu anki Dakika):", type="password")
    if st.sidebar.button("Erişim İste 🔑"):
        # Senin yazdığın o meşhur dakika kontrolü!
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
    st.warning("👁️ GÖZ (Kamera) Devrede! Sabotajcının fotoğrafı sisteme kilitlendi.")
    # Web kamerası üzerinden fotoğraf çekme özelliği kanka!
    foto = st.camera_input("Güvenlik doğrulaması için yüzünü göster kanka:")
    if foto:
        st.success("Kanıt kaydedildi! Giriş engellendi.")
    st.stop()

# Üst Bilgilendirme Logları
st.code(f"""
[SİSTEM LOGU]:
🤖 SÜPERZEKA v13 Başlatıldı.
👁️ Göz (Kamera) Aktif. | 👂 Kulak (Sesli Komut) Hazır.
🧠 5 Yapay Zeka Beyni Çevrimiçi (Gemini, GPT-4o, Claude, Llama, DeepSeek).
💡 GÜNÜN BİLGİSİ: {random.choice(gunun_bilgileri)}
""")

# 🎙️ KULAK: Ses Tanıma Özelliği (Web uyumlu)
st.subheader("🎙️ Sesli Komut (Kulak)")
ses_aktif = st.checkbox("Kulak (Mikrofon) Açılsın mı kanka?")
sesli_yazi = ""
if ses_aktif:
    st.info("Tarayıcının mikrofon iznini onayladıktan sonra konuşabilirsin kanka.")
    ses_dosyasi = st.audio_input("Mikrofona konuş ve kaydet butonuna bas kanka:")
    if ses_dosyasi:
        sesli_yazi = " (Not: Sesli komut başarıyla algılandı!)"

# ANA SORGULAMA ALANI
st.subheader("🧠 Siber Asistan Sorgu Ekranı")
user_input = st.text_input("SüperZeka'ya bir komut veya soru gönder kanka:", placeholder="Örn: Harezmi kimdir?")

if st.button("Sorgula / Çalıştır 🚀") or sesli_yazi:
    if user_input:
        with st.spinner("🧠 5 Yapay Zeka Beyni Ortak Karar Alıyor..."):
            try:
                # Gerçek Gemini Motoru
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(user_input)
                gemini_yaniti = response.text
                
                # Senin kodundaki o simüle edilen (mock) diğer 4 modelin yanıtları kanka!
                gpt_yanit = "[GPT-4o Yanıtı]: API bağlanmadığı için bu model simüle ediliyor kanka."
                claude_yanit = "[Claude-3 Yanıtı]: API bağlanmadığı için bu model simüle ediliyor kanka."
                llama_yanit = "[Llama-3 Yanıtı]: API bağlanmadığı için bu model simüle ediliyor kanka."
                deepseek_yanit = "[DeepSeek Yanıtı]: API bağlanmadığı için bu model simüle ediliyor kanka."

                st.markdown("---")
                
                # Seçilen moda göre ekrana yazdırma mantığı (Senin yazdığın sistemin aynısı!)
                if st.session_state.mod == "ÖĞRENCİ":
                    st.success("🤖 SÜPERZEKA - 5 Model Ortak Kararı (İpucu):")
                    st.write(f"[Gemini Yanıtı]: {gemini_yaniti}")
                    st.info("💡 (Doğrudan formülü kullanma, mantığı yakala kanka!)")
                else:
                    # Öğretmen modu seçildiyse tüm modelleri alt alta döker!
                    st.success("👨‍🏫 SÜPERZEKA - ÖĞRETMEN MODU - TÜM MODEL RAPORLARI:")
                    st.write(f"[Gemini Yanıtı]: {gemini_yaniti}")
                    st.text(gpt_yanit)
                    st.text(claude_yanit)
                    st.text(llama_yanit)
                    st.text(deepseek_yanit)

            except Exception as e:
                st.error(f"Siber bağlantı hatası oluştu kanka: {e}")
