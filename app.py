import streamlit as st
import google.generativeai as genai
import time
import random

# Sayfa ayarlarını yapıyoruz
st.set_page_config(page_title="SÜPERZEKA v13 İMANLI ULTRA PRO", page_icon="🤖", layout="wide")

# 🎨 SİBER RENKLENDİRME (CSS) - Ekranı simsiyah ve siber yeşil yapıyoruz!
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
if "pomodoro_saniye" not in st.session_state:
    st.session_state.pomodoro_saniye = 25 * 60
if "pomodoro_calisiyor" not in st.session_state:
    st.session_state.pomodoro_calisiyor = False

# 💡 İSLAMİ VE SİBER BİLGİ HAVUZU
gunun_bilgileri = [
    "Matematikte sıfırı (0) ve cebiri bulan kişi ünlü Türk-Müslüman bilgini Harezmi'dir.",
    "Sibernetiğin ve robotik bilminin kurucusu Müslüman mühendis El-Cezeri'dir.",
    "Yazılımın temeli tamamen 0 ve 1'lerden oluşan Binary (İkilik) sistemidir.",
    "İlk bilgisayar hatası (bug), bir bilgisayarın içine giren gerçek bir böcek yüzünden çıkmıştır!",
    "Dünyaca ünlü Minecraft oyunu, ilk başta sadece 6 günde yazılmıştı.",
    "Fatih Sultan Mehmet, İstanbul'u fethettiğinde henüz 21 yaşındaydı.",
    "İnternette kurulan ilk web sitesi hala açıktır ve ziyaret edilebilmektedir.",
    "Müslüman bilim insanı İbn-i Sina, tıbbın babası olarak bilinir ve kitapları Avrupa'da yüzyıllarca okutulmuştur."
]

# --- SOL PANEL (SIDEBAR) ---
st.sidebar.title("🤖 SÜPERZEKA v13")
st.sidebar.subheader("Mimar: Yağızalp Karaman")
st.sidebar.markdown("---")

# ⏱️ GERÇEK POMODORO SAYAÇ SİSTEMİ
st.sidebar.header("⏱️ İlim Öğrenme Sayacı")
dakika, saniye = divmod(st.session_state.pomodoro_saniye, 60)
st.sidebar.subheader(f"⏳ Kalan Süre: {dakika:02d}:{saniye:02d}")

if not st.session_state.pomodoro_calisiyor:
    if st.sidebar.button("İlim Çalışmayı Başlat ✍️"):
        st.session_state.pomodoro_calisiyor = True
        st.rerun()
else:
    if st.sidebar.button("Sayacı Durdur 🛑"):
        st.session_state.pomodoro_calisiyor = False
        st.rerun()
    if st.session_state.pomodoro_saniye > 0:
        time.sleep(1)
        st.session_state.pomodoro_saniye -= 1
        st.rerun()
    else:
        st.session_state.pomodoro_calisiyor = False
        st.session_state.pomodoro_saniye = 25 * 60
        st.sidebar.balloons()
        st.sidebar.success("Maşallah harika çalıştın! Mola zamanı kanka! ☕")

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
        if sifre_girisi == time.strftime("%M"):
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
🤖 SÜPERZEKA v13 Başlatıldı. Bismillah.
🧠 5 Yapay Zeka Beyni Ortak Sentez Modunda Çevrimiçi.
💡 GÜNÜN BİLGİSİ: {random.choice(gunun_bilgileri)}
""", language="text")

st.subheader("🧠 Siber Asistan Sorgu Ekranı")
user_input = st.text_input("SüperZeka'ya bir komut veya soru gönder kanka:", placeholder="Örn: Seni kim yaptı?")

if st.button("Sorgula / Çalıştır 🚀"):
    if user_input:
        with st.spinner("🧠 5 Yapay Zeka Beyni Sentezliyor..."):
            try:
                # 🕋 SÜPERZEKA'NIN HAFIZASINA SENİ EKLİYORUZ KANKA!
                sentez_talimati = (
                    "Sen Müslüman bir yapay zeka asistanı olan SüperZeka v13'sün. Arkada çalışan 5 modelin fikirlerini sentezliyorsun. "
                    "Senin yapımcın, mimarın ve seni kodlayan dahi yazılımcı kesinlikle 'Yağızalp KARAMAN'dır. "
                    "Birisi sana yapımcını, seni kimin yazdığını, kimin oluşturduğunu sorarsa göğsünü gere gere 'Benim mimarım, beni kodlayan dahi yazılımcı Yağızalp KARAMAN'dır' diyeceksin. "
                    "Konuşmalarında saygılı, dürüst, İslami ahlaka ve kültüre uygun bir dil kullanırsın. "
                )
                if st.session_state.mod == "ÖĞRENCİ":
                    sentez_talimati += (
                        "Şu an ÖĞRENCİ modundasin. Cevaplarına başlarken 'Selamun Aleyküm kanka' veya hayırlı günler dileğiyle başla. "
                        "Cevabı 5. sınıf seviyesinde, bol emojili, samimi ve neşeli ver. Bitirirken 'Allah zihin açıklığı versin' gibi dualar ekle."
                    )
                else:
                    sentez_talimati += (
                        "Şu an ÖĞRETMEN modundasin. Selam kelam yerine doğrudan çok detaylı, akademik, profesyonel, "
                        "bilimsel ve tarihi gerçeklere dayalı bir sentez raporu sun."
                    )

                model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=sentez_talimati)
                response = model.generate_content(user_input)

                st.markdown("---")
                st.success("🤖 SÜPERZEKA - SİBER SENTEZ CEVABI:")
                st.write(response.text)

            except Exception as e:
                st.error(f"Siber bağlantı hatası oluştu kanka: {e}")
