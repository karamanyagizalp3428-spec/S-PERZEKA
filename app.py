import streamlit as st
import google.generativeai as genai
import random

st.set_page_config(page_title="SÜPERZEKA v20 PRO", page_icon="🤖", layout="wide")

# CSS (Siber Stil)
st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; }
    h1, h2, p, div { color: #00ffcc !important; font-family: 'Consolas', monospace !important; }
    .chat-box { background-color: #111; border: 1px dashed #00ffcc; padding: 10px; border-radius: 8px; margin: 10px 0; }
    .bilgi-paneli { background-color: #050505; border: 1px solid #00ffcc; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# Session State
if "mod" not in st.session_state: st.session_state.mod = "ÖĞRENCİ"
if "gecmis" not in st.session_state: st.session_state.gecmis = []

# Bilgiler
gunun_bilgileri = ["Yapay zeka 1956'da doğdu.", "İnternet ARPANET ile başladı.", "Beyin 86 milyar nörondur."]
hadis_havuzu = ["İlim öğrenmek farzdır.", "Kolaylaştırınız, zorlaştırmayınız."]

# Arayüz
st.markdown("<h1>🧠 SÜPERZEKA v20 PRO 🧠</h1>", unsafe_allow_html=True)

# Bilgi ve Hadis
st.markdown(f"""
    <div class='bilgi-paneli'>
        <p>💡 <b>Bilgi:</b> {random.choice(gunun_bilgileri)}</p>
        <p>🕋 <b>Hadis:</b> {random.choice(hadis_havuzu)}</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🤖 MOD KONTROL")
if st.sidebar.button("Mod Değiştir"):
    st.session_state.mod = "ÖĞRETMEN" if st.session_state.mod == "ÖĞRENCİ" else "ÖĞRENCİ"
    st.rerun()

# Sorgu
u_input = st.text_input("Komut gönder:")
if st.button("Sorgula 🚀") and u_input:
    # Talimat
    if st.session_state.mod == "ÖĞRENCİ":
        talimat = "Sen bir eğitmensin. Asla cevabı söyleme. Sadece ipucu ver ve öğrencinin bulmasını sağla. '💡 Siber İpucu: ...' ile bitir."
    else:
        talimat = "Sen bir öğretmensin. Sorunun cevabını doğrudan, teknik ve profesyonel ver."
    
    model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=talimat)
    res = model.generate_content(u_input)
    st.session_state.gecmis.append((u_input, res.text))
    st.rerun()

# Geçmiş
for q, a in reversed(st.session_state.gecmis):
    st.markdown(f"<div class='chat-box'>👤 <b>Sen:</b> {q}<br><br>🤖 <b>SÜPERZEKA:</b> {a}</div>", unsafe_allow_html=True)
