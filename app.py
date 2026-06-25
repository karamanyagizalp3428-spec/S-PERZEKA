import streamlit as st
import google.generativeai as genai
import time
import random

# Sayfa ayarlarını v14 PRO olarak güncelliyoruz
st.set_page_config(page_title="SÜPERZEKA v14 PRO", page_icon="🤖", layout="wide")

# 🎨 SİBER VE İSLAMİ TASARIM (CSS) - Kutuları ve yazıların hizasını sabitliyoruz
st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; }
    h1, h2, h3, p, span, label { color: #00ffcc !important; font-family: 'Consolas', monospace !important; }
    input, textarea { background-color: #111111 !important; color: white !important; border: 1px solid #00ffcc !important; font-family: 'Consolas', monospace !important; }
    [data-testid="stSidebar"] { background-color: #0c0c0c !important; border-right: 2px solid #00ffcc; }
    .stButton>button { background-color: #1a1a1a !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; width: 100%; }
    .chat-box { background-color: #111111; border: 1px dashed #00ffcc; padding: 12px; border-radius: 8px; margin-top: 10px; margin-bottom: 10px; }
    .status-panel { background-color: #002211; padding: 10px; border-radius: 5px; border: 1px solid #00ffcc; text-align: center; margin-bottom: 15px; }
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
if "sohbet_gecmisi" not in st.session_state: st.session_state.sohbet_gecmisi = []
if "canvas_icerik" not in st.session_state: 
    st.session_state.canvas_icerik = "# Siber Canvas\n\nBuraya ödevini veya kodunu yapıştır kanka!"

# --- VERİ HAVUZLARI ---
gunun_bilgileri = ["Sıfırı Harezmi buldu.", "İlk robotu El-Cezeri yaptı.", "Yazılım Binary (0-1) sistemidir."]
hadis_havuzu = ["“İlim öğrenmek her Müslümana farzdır.”", "“Kolaylaştırınız, zorlaştırmayınız.”", "“En hayırlınız ahlakı güzel olandır.”"]

# --- SOL PANEL (SIDEBAR) ---
st.sidebar.title("🤖 SÜPERZEKA v14 PRO")
st.sidebar.markdown(f"<div class='status-panel'>Mevcut Mod: <b>{st.session_state.mod}</b></div>", unsafe_allow_html=True)

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
# 🗑️ SOHBETİ SIFIRLAMA BUTONU
if st.sidebar.button("Sohbet Geçmişini Temizle 🗑️"):
    st.session_state.sohbet_gecmisi = []
    st.rerun()

# --- ANA EKRAN ---
if st.session_state.guvenlik_kilidi:
    st.error("🚨 SİSTEM KİLİTLENDİ!"); st.stop()

st.code(f"""
[SİSTEM LOGU] v14 PRO | Mod: {st.session_state.mod}
💡 Bilgi: {random.choice(gunun_bilgileri)}
🕋 Hadis: {random.choice(hadis_havuzu)}
""", language="text")

st.markdown("---")

# 🖼️ ÇİFT EKRAN (CANVAS & CHAT)
sol, sag = st.columns([1, 1])

with sol:
    st.subheader("📝 Canvas")
    st.session_state.canvas_icerik = st.text_area("Çalışma Alanı:", value=st.session_state.canvas_icerik, height=400)

with sag:
    st.subheader("🧠 Siber Sorgu Ekranı")
    
    # Form kullanarak Enter tuşuna basıldığında sayfanın saçmalamasını tamamen engelliyoruz kanka!
    with st.form(key="sorgu_formu", clear_on_submit=True):
        u_input = st.text_input("SüperZeka'ya bir komut gönder kanka:", placeholder="Mesajını yaz ve Enter'a bas...")
        submit_button = st.form_submit_button(label="Sorgula / Çalıştır 🚀")
        
    if submit_button and u_input:
        with st.spinner("🧠 Sentezleniyor..."):
            try:
                gecmis = "\n".join([f"Kullanıcı: {q}\nSüperZeka: {a}" for q, a in st.session_state.sohbet_gecmisi[-3:]])
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
                
                # Hafızaya ekle
                st.session_state.sohbet_gecmisi.append((u_input, res.text))
                st.rerun() # Görüntünün anlık ve temiz yenilenmesi için tetikleme
            except Exception as e: 
                st.error(f"Bağlantı Hatası: {e}")

    # 📜 DÜZGÜN AKAN SOHBET GEÇMİŞİ
    if st.session_state.sohbet_gecmisi:
        st.markdown("---")
        st.write("💬 **Sohbet Akışı (Son Mesajlar Üstte):**")
        for q, a in reversed(st.session_state.sohbet_gecmisi):
            st.markdown(f"<div class='chat-box'>👤 <b>Sen:</b> {q}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='chat-box' style='border-color:#00ffcc;'>🤖 <b>SÜPERZEKA:</b> {a}</div>", unsafe_allow_html=True)
