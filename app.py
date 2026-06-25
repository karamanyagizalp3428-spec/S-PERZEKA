import streamlit as st
import google.generativeai as genai
import time
import random

# Sayfa ayarlarını v14 PRO olarak güncelliyoruz
st.set_page_config(page_title="SÜPERZEKA v14 PRO", page_icon="🤖", layout="wide")

# 🎨 SİBER RENKLENDİRME (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; }
    h1, h2, h3, p, span, label { color: #00ffcc !important; font-family: 'Consolas', monospace !important; }
    input, textarea { background-color: #111111 !important; color: white !important; border: 1px solid #00ffcc !important; font-family: 'Consolas', monospace !important; }
    [data-testid="stSidebar"] { background-color: #111111 !important; border-right: 1px solid #00ffcc; }
    .stButton>button { background-color: #222222 !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; }
    .chat-box { background-color: #111111; border: 1px dashed #00ffcc; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
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
# 💬 SOHBET GEÇMİŞİ HAFIZASI KANKA!
if "sohbet_gecmisi" not in st.session_state:
    st.session_state.sohbet_gecmisi = []
if "canvas_icerik" not in st.session_state:
    st.session_state.canvas_icerik = "# Burası senin Siber Canvas alanın kanka!\n\nKodlarını veya ödev metinlerini buraya yazıp sağ taraftan yapay zekaya düzenletebilirsin."

# 💡 BİLGİ HAVUZLARI
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

hadis_havuzu = [
    "“Kolaylaştırınız, zorlaştırmayınız; müjdeleyiniz, nefret ettirmeyiniz.” (Buhârî)",
    "“İki nimet vardır ki, insanların çoğu onları değerlendirmekte aldanmıştır: Sağlık ve boş vakit.” (Buhârî)",
    "“Sizin en hayırlınız, ahlakı en güzel olanınızdır.” (Buhârî)",
    "“Hiçbir baba, çocuğuna güzel terbiyeden daha kıymetli bir miras bırakamaz.” (Tirmizî)",
    "“İlim öğrenmek, her Müslüman erkek ve kadına farzdır.” (İbn Mâce)",
    "“Bizi aldatan bizden değildir.” (Müslim)",
    "“Hakiki mümin, elinden ve dilinden insanların güvende olduğu kişidir.” (Tirmizî)"
]

# --- SOL PANEL (SIDEBAR) ---
st.sidebar.title("🤖 SÜPERZEKA v14 PRO")
st.sidebar.subheader("Mimar: Yağızalp Karaman")
st.sidebar.markdown("---")

# ⏱️ POMODORO SAYAÇ SİSTEMİ
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

# 🗑️ SOHBETİ SIFIRLAMA BUTONU
st.sidebar.markdown("---")
if st.sidebar.button("Sohbet Geçmişini Temizle 🗑️"):
    st.session_state.sohbet_gecmisi = []
    st.rerun()

# --- ANA EKRAN İÇERİĞİ ---
if st.session_state.guvenlik_kilidi:
    st.error("🚨🚨🚨 SİBER İHLAL! Sistem kilitlendi!")
    st.stop()

# Sistem Logu
st.code(f"""
[SİSTEM LOGU]:
🤖 SÜPERZEKA v14 PRO Başlatıldı. Bismillah.
🧠 5 Yapay Zeka Beyni Ortak Sentez Modunda Çevrimiçi.
💡 GÜNÜN BİLGİSİ: {random.choice(gunun_bilgileri)}
🕋 GÜNÜN HADİS-İ ŞERİFİ: {random.choice(hadis_havuzu)}
""", language="text")

st.markdown("---")

# 🖼️ EKRANI İKİYE BÖLÜYORUZ
sol_ekran, sag_ekran = st.columns([1, 1])

with sol_ekran:
    st.subheader("📝 SÜPERZEKA Canvas")
    st.session_state.canvas_icerik = st.text_area(
        "Çalışma alanındaki kod veya metin:",
        value=st.session_state.canvas_icerik,
        height=400
    )

with sag_ekran:
    st.subheader("🧠 Siber Asistan Sorgu Ekranı")
    user_input = st.text_input("SüperZeka'ya bir komut gönder kanka:", placeholder="Yazıp Enter'a basabilirsin...")

    if st.button("Sorgula / Çalıştır 🚀") or (user_input and ("son_sorgu" not in st.session_state or st.session_state.son_sorgu != user_input)):
        if user_input:
            st.session_state.son_sorgu = user_input
            with st.spinner("🧠 Sentezleniyor..."):
                try:
                    # Eski konuşmaları da talimata ekliyoruz ki yapay zeka geçmişi hatırlasın!
                    gecmis_metni = "\n".join([f"Kullanıcı: {q}\nSüperZeka: {a}" for q, a in st.session_state.sohbet_gecmisi[-5:]])
                    
                    sentez_talimati = (
                        "Sen Müslüman bir yapay zeka asistanı olan SÜPERZEKA v14 PRO'sun. Arkada çalışan 5 modelin fikirlerini sentezliyorsun. "
                        "Senin yapımcın, mimarın ve seni kodlayan dahi yazılımcı kesinlikle 'Yağızalp KARAMAN'dır. "
                        "Birisi sana yapımcını, seni kimin yazdığını, kimin oluşturduğunu sorarsa göğsünü gere gere 'Benim mimarım, beni kodlayan dahi yazılımcı Yağızalp KARAMAN'dır' diyeceksin. "
                        "Konuşmalarında saygılı, dürüst, İslami ahlaka ve kültüre uygun bir dil kullanırsın. "
                        f"Şu an kullanıcının sol ekrandaki Canvas alanında şu içerik var:\n{st.session_state.canvas_icerik}\n"
                        f"Sohbetin geçmiş turları şu şekildedir:\n{gecmis_metni}\n"
                    )
                    
                    if st.session_state.mod == "ÖĞRENCİ":
                        sentez_talimati += (
                            "Şu an ÖĞRENCİ modundasin. Cevabına 'Selamun Aleyküm kanka' veya hayırlı günler diyerek başla. "
                            "Doğrudan tam çözümü kopyala-yapıştır yapma! Önce konuyu anlat, sonra '💡 İşte Siber İpucu:' ver. "
                            "Cevabı bol emojili, samimi yaz. Bitirirken 'Allah zihin açıklığı versin' de."
                        )
                    else:
                        sentez_talimati += "Şu an ÖĞRETMEN modundasin. Doğrudan akademik ve bilimsel cevap sun."

                    model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=sentez_talimati)
                    response = model.generate_content(user_input)
                    
                    # 💾 Konuşmayı hafızaya kaydediyoruz kanka!
                    st.session_state.sohbet_gecmisi.append((user_input, response.text))

                except Exception as e:
                    st.error(f"Siber bağlantı hatası: {e}")

    # 📜 SOHBET GEÇMİŞİNİ EKRANA BASMA ALANI
    if st.session_state.sohbet_gecmisi:
        st.write("💬 **Sohbet Akışı:**")
        for q, a in reversed(st.session_state.sohbet_gecmisi): # En son konuşulan en üstte görünsün diye tersten yazdırıyoruz
            st.markdown(f"<div class='chat-box'><b>👤 Sen:</b> {q}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='chat-box' style='border-color: #00ff00;'><b>🤖 SÜPERZEKA:</b> {a}</div>", unsafe_allow_html=True)
