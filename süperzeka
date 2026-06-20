import threading
import asyncio
import tkinter as tk
from tkinter import scrolledtext, simpledialog
import cv2
import pyttsx3
import time
import random
import sqlite3
from google import genai
import speech_recognition as sr  # 🎙️ YENİ: Ses tanıma kütüphanesi eklendi


# =====================================================
# SÜPERZEKA v13 ULTRA PRO - FINAL (CYBERNETIC EDITION)
# Mimar: Yağızalp Karaman
# =====================================================

class SuperZekaV13Pro:
    def __init__(self, root):
        self.root = root
        self.root.title("SÜPERZEKA v13 ULTRA PRO - Siber Asistan")
        self.root.geometry("950x750")
        self.root.configure(bg="#050505")

        # 1. BELLEK (SQLite Veritabanı Kurulumu)
        self.conn = sqlite3.connect("superzeka_v13.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS cyber_logs (sender TEXT, message TEXT, zaman TIMESTAMP)")

        # YAPAY ZEKA API KURULUMU
        # UYARI: Kendi API anahtarını aşağıdaki tırnakların içine yapıştır!
        self.ai_client = genai.Client(api_key="")

        # Sistem Değişkenleri
        self.mod = "ÖĞRENCİ"
        self.hata_sayaci = 0
        self.timer_running = False
        self.remaining_time = 25 * 60

        # Bilgi Havuzu
        self.gunun_bilgileri = [
            "Işık, Güneş'ten Dünya'ya 8 dakikada ulaşır.",
            "Harezmi sıfırı bulan kişidir.",
            "Yazılımın temeli Binary sistemidir."
        ]

        # Arayüzü Başlat
        self.setup_ui()
        self.write("SİSTEM",
                   f"🤖 SÜPERZEKA v13 Başlatıldı.\n👁️ Göz (Kamera) Aktif.\n👂 Kulak (Mikrofon) Aktif.\n🧠 5 Yapay Zeka Beyni Çevrimiçi.\n💾 Veritabanı Bağlandı.\n💡 GÜNÜN BİLGİSİ: {random.choice(self.gunun_bilgileri)}")

    def setup_ui(self):
        # Üst Panel (Öğrenci için Pomodoro Sayacı)
        self.top_frame = tk.Frame(self.root, bg="#111111", height=50)
        self.top_frame.pack(fill="x", padx=20, pady=5)

        self.timer_label = tk.Label(self.top_frame, text="⏱️ Pomodoro: 25:00", bg="#111111", fg="#ffcc00",
                                    font=("Consolas", 12, "bold"))
        self.timer_label.pack(side="left", padx=10, pady=5)

        self.timer_btn = tk.Button(self.top_frame, text="Başlat", bg="#222222", fg="white", command=self.toggle_timer,
                                   bd=0, padx=10)
        self.timer_btn.pack(side="left", padx=5)

        # Mikrofon (Sesli Komut) Butonu - GERÇEK KULAK ÖZELLİĞİ
        self.mic_btn = tk.Button(self.top_frame, text="👂 Dinle (Sesli Komut)", bg="#0055ff", fg="white",
                                 command=self.listen_voice, bd=0, padx=10)
        self.mic_btn.pack(side="right", padx=10)

        # 1. ÖNCE GİRİŞ KUTUSUNU EN ALTA SABİTLE
        self.input_field = tk.Entry(self.root, bg="#111111", fg="white", font=("Arial", 14), bd=1, relief="solid",
                                    insertbackground="white")
        self.input_field.pack(side="bottom", fill="x", padx=20, pady=20, ipady=8)
        self.input_field.bind("<Return>", lambda e: self.process_query())
        self.input_field.focus_set()

        # 2. SONRA MESAJLAŞMA EKRANINI KALAN BOŞLUĞA YAY
        self.chat_area = scrolledtext.ScrolledText(self.root, bg="#050505", fg="#00ffcc", font=("Consolas", 11), bd=0)
        self.chat_area.pack(side="top", expand=True, fill="both", padx=20, pady=10)

    # 👂 KULAK: GERÇEK Sesli Komut Dinleme Sistemi
    def listen_voice(self):
        self.write("SİSTEM", "🎙️ Kulak aktif... Konuşmanı bekliyorum kanka...")
        self.speak("Seni dinliyorum.")

        def real_listen():
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                try:
                    # Ortamdaki cızırtıyı ve arka plan gürültüsünü temizle
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)

                    # Sesi dinle (En fazla 5 saniye ses gelmesini bekler)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

                    self.root.after(0, lambda: self.write("SİSTEM", "⏳ Ses işleniyor..."))

                    # Google'ın ücretsiz ses tanıma motoruyla sesi Türkçe metne çevir
                    text = recognizer.recognize_google(audio, language="tr-TR")

                    # Söylenen metni arayüzdeki giriş kutusuna yazdır ve enter'a basılmış gibi gönder
                    self.root.after(0, lambda: (
                        self.input_field.delete(0, tk.END),
                        self.input_field.insert(0, text),
                        self.process_query()
                    ))

                except sr.WaitTimeoutError:
                    self.root.after(0, lambda: self.write("SİSTEM", "⚠️ Ses duyamadım, dinleme iptal edildi."))
                except sr.UnknownValueError:
                    self.root.after(0,
                                    lambda: self.write("SİSTEM", "⚠️ Ne dediğini tam anlayamadım, tekrar dener misin?"))
                except sr.RequestError:
                    self.root.after(0, lambda: self.write("SİSTEM", "⚠️ İnternet veya ses servisi bağlantı hatası!"))

        # Arayüz donmasın diye dinleme işlemini arka planda başlat
        threading.Thread(target=real_listen, daemon=True).start()

    # ⏱️ POMODORO SAYAÇ SİSTEMİ
    def toggle_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.timer_btn.config(text="Durdur")
            self.update_timer()
        else:
            self.timer_running = False
            self.timer_btn.config(text="Başlat")

    def update_timer(self):
        if self.timer_running and self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"⏱️ Ders: {mins:02d}:{secs:02d}")
            self.remaining_time -= 1
            self.root.after(1000, self.update_timer)
        elif self.remaining_time == 0:
            self.timer_running = False
            self.timer_label.config(text="⏱️ Süre Bitti!")
            self.speak("Harika çalıştın! Mola zamanı.")

    # 💾 VERİTABANI YAZICI VE EKRAN GÜNCELLEME
    def write(self, sender, text):
        self.chat_area.insert(tk.END, f"[{sender}]: {text}\n\n")
        self.chat_area.see(tk.END)
        self.cursor.execute("INSERT INTO cyber_logs VALUES (?, ?, ?)", (sender, text, time.ctime()))
        self.conn.commit()

    # 👄 AĞIZ: Sesli Yanıt Sistemi
    def speak(self, text):
        def run_speech():
            try:
                eng = pyttsx3.init()
                eng.say(text)
                eng.runAndWait()
            except:
                pass

        threading.Thread(target=run_speech, daemon=True).start()

    # 🧠 ASYNCIO TABANLI 5 YAPAY ZEKA BEYNİ
    async def call_ai_models(self, prompt):
        async def mock_ai_request(model_name, delay):
            await asyncio.sleep(delay)
            return f"[{model_name} Yanıtı]: API bağlanmadığı için bu model simüle ediliyor."

        async def real_gemini_request(prompt_text):
            try:
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: self.ai_client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt_text
                    )
                )
                return f"[Gemini Yanıtı]: {response.text}"
            except Exception as e:
                return f"[Gemini Yanıtı]: ⚠️ API Bağlantı Hatası: {e}"

        tasks = [
            real_gemini_request(prompt),
            mock_ai_request("GPT-4o", 0.7),
            mock_ai_request("Claude-3", 0.4),
            mock_ai_request("Llama-3", 0.6),
            mock_ai_request("DeepSeek", 0.3)
        ]

        cevaplar = await asyncio.gather(*tasks)
        return cevaplar

    def process_query(self):
        q = self.input_field.get().strip()
        if not q: return
        self.input_field.delete(0, tk.END)

        if "ŞİFRE" in q.upper():
            self.check_password()
            return

        self.write("KULLANICI", q)

        def run_async_ai():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            cevaplar = loop.run_until_complete(self.call_ai_models(q))

            if self.mod == "ÖĞRENCİ":
                final_cevap = f"🧠 5 Model Ortak Kararı (İpucu):\n{cevaplar[0]} (Doğrudan formülü kullanma, mantığı yakala kanka!)"
            else:
                final_cevap = f"🧠 ÖĞRETMEN MODU - TÜM MODEL RAPORLARI:\n" + "\n".join(cevaplar)

            self.root.after(0, lambda: (self.write("SÜPERZEKA", final_cevap), self.speak("Cevap hazır.")))

        threading.Thread(target=run_async_ai, daemon=True).start()

    # 🔐 GÜVENLİK ANAHTARI SİSTEMİ
    def check_password(self):
        if simpledialog.askstring("GÜVENLİK", "Sistem Anahtarı (Dakika):") == time.strftime("%M"):
            self.mod = "ÖĞRETMEN"
            self.timer_running = False
            self.top_frame.pack_forget()
            self.write("GÜVENLİK", "Erişim Onaylandı: ÖĞRETMEN MODU SİSTEMİ AKTİF.")
            self.speak("Öğretmen modu aktif edildi.")
        else:
            self.hata_sayaci += 1
            if self.hata_sayaci >= 3:
                self.trigger_security()
            else:
                self.write("GÜVENLİK", f"Hatalı şifre! ({self.hata_sayaci}/3)")
                self.speak("Hatalı şifre.")

    # 👁️ GÖZ: Kamera Sabotaj Koruma Sistemi
    def trigger_security(self):
        self.write("GÜVENLİK", "⚠️ SİBER İHLAL: Kanıt kaydediliyor, kamera devrede!")
        self.speak("Sistem ihlali. Fotoğrafınız kaydediliyor.")
        try:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite("intrusion_evidence.jpg", frame)
                self.write("GÜVENLİK",
                           "⚠️ İHLAL KANITI: 'intrusion_evidence.jpg' olarak başarıyla veritabanı dizinine kilitlendi!")
            cap.release()
        except:
            self.write("GÜVENLİK", "⚠️ HATA: Göz donanımına (Kameraya) erişilemedi!")


if __name__ == "__main__":
    root = tk.Tk()
    app = SuperZekaV13Pro(root)
    root.mainloop()
