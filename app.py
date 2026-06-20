import streamlit as st
import google.generativeai as genai

# Şifreyi kontrol ediyoruz
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("API Anahtarı bulunamadı kanka!")

# Sitenin görüntüsü
st.title("🤖 S-PERZEKA Yapay Zeka Asistanı")
st.write("İlk Canlı Projem! Sorunu yaz, cevaplasın.")

user_input = st.text_input("Yapay zekaya bir şey sor:")

if st.button("Soruyu Gönder 🚀"):
    if user_input:
        with st.spinner("Düşünüyorum..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(user_input)
                st.success("🤖 Cevap:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Hata oldu: {e}")
