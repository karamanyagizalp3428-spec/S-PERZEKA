import streamlit as st
import google.generativeai as genai
import random

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="SÜPERZEKA v20 PRO", page_icon="🤖", layout="wide")

# --- SİBER CSS (TASARIM VE PANEL GÜÇLENDİRME) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; }
    h1, h2, h3, p, div, b { color: #00ffcc !important; font-family: 'Consolas', monospace !important; }
    .chat-box { background-color: #111; border: 1px dashed #00ffcc; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
    .logo-kutusu { background-color: #111; border: 2px solid #00ffcc; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px; }
    .bilgi-paneli { background-color: #001a1a; border: 1px solid #00ffcc; padding: 20px; border-radius: 12px; margin-bottom: 20px; }
    .stButton>button { background-color: #1a1a1a; color: #00ffcc; border: 1px solid #00ffcc; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- SİSTEM HAFIZASI ---
if "mod" not in st.session_state: st.session_state.mod = "ÖĞRENCİ"
if "gecmis" not in st.session_state: st.session_state.gecmis = []

# --- BİLGİ VE HADİS VERİTABANI ---
gunun_bilgileri = [
    "🤖 Yapay zeka, 1956 yılındaki Dartmouth Konferansı ile resmen doğmuştur.",
    "🌐 World Wide Web, 1989 yılında Tim Berners-Lee tarafından icat edilmiştir.",
    "🧠 İnsan beyni, saniyede trilyonlarca işlemi aynı anda yapabilen biyolojik bir süper bilgisayardır.",
    "🚀 İlk yapay uydu Sputnik 1, 1957 yılında uzaya fırlatılmıştır."
]
hadis_havuzu = [
    "“İlim öğrenmek her Müslümana farzdır.”",
    "“Kolaylaştırınız, zorlaştırmayınız; müjdeleyiniz, nefret ettirmeyiniz.”",
    "“En hayırlınız, ahlakı en güzel olanınızdır.”",
    "“Hiçbiriniz, kendisi için istediğini mümin kardeşi için istemedikçe (tam) iman etmiş olmaz.”"
]

# --- ARAYÜZ (LOGO + PANEL) ---
st.markdown("<div class='logo-kutusu'><h1>🧠 SÜPERZEKA v20 PRO 🧠</h1><p>Mimar: Yağızalp KARAMAN | Siber Üs Aktif</p></div>", unsafe_allow_html=True)

# GÜNÜN BİLGİSİ VE HADİSİ ŞERİF PANELİ
col_l, col_r = st.columns([1, 1])

with col_l:
    st.markdown(f"""
        <div class='bilgi-paneli'>
            <h3>💡 GÜNÜN BİLGİSİ</h3>
            <p>{random.choice(gunun_bilgileri)}</p>
        </div>
    """, unsafe_allow_html=True)

with col_r:
    st.markdown(f"""
        <div class='bilgi-paneli'>
            <h3>🕋 HADİS-İ ŞERİF</h3>
            <p>{random.choice(hadis_havuzu)}</p>
        </div>
    """, unsafe_allow_html=True)

# --- MOD KONTROL VE SORGULAR ---
st.sidebar.title("🤖 MOD KONTROL")
st.sidebar.markdown(f"**Aktif Mod:** `{st.session_state.mod}`")
if st.sidebar.button("Modu Değiştir"):
    st.session_state.mod = "ÖĞRETMEN" if st.session_state.mod == "ÖĞRENCİ" else "ÖĞRENCİ"
    st.rerun()

st.subheader("🧠 Siber Sorgu Ekranı")
u_input = st.text_input("Komutunu gir kanka:")

if st.button("Sorgula / Çalıştır 🚀") and u_input:
    # TALİMAT MANTIĞI
    if st.session_state.mod == "ÖĞRENCİ":
        talimat = "Sen SÜPERZEKA v20 PRO'sun. Kullanıcı ÖĞRENCİ modunda. ASLA DOĞRUDAN CEVABI VERME. Öğrencinin kendisinin bulması için yol göster, ipuçları ver. Espri yapma. Cevabını '💡 Siber İpucu: [Yönlendirici Bilgi]' ile bitir."
    else:
        talimat = "Sen SÜPERZEKA v20 PRO'sun. ÖĞRETMEN modundasın. Teknik, ciddi, doğrudan ve profesyonel cevap ver. Cevabı söylemekten çekinme."
    
    # AI ÇALIŞTIRMA
    try:
        model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=talimat)
        res = model.generate_content(u_input)
        st.session_state.gecmis.append((u_input, res.text))
        st.rerun()
    except Exception as e:
        st.error(f"Sistem Hatası: {e}")

# --- SOHBET AKIŞI ---
for q, a in reversed(st.session_state.gecmis):
    st.markdown(f"<div class='chat-box'>👤 <b>Sen:</b> {q}<br><br>🤖 <b>SÜPERZEKA:</b> {a}</div>", unsafe_allow_html=True)
