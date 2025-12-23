import streamlit as st
import yt_dlp
import os
import time
from PIL import Image
import streamlit.components.v1 as components

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ultimate Toolbox & Premium", page_icon="🎁", layout="centered")

# --- İNDİRME KLASÖRÜ ---
DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# --- RICK ROLL FONKSİYONU ---
def rick_roll_yap(mesaj="⚠️ GÜVENLİK İHLALİ TESPİT EDİLDİ!"):
    st.empty()
    st.error(mesaj)
    time.sleep(1)
    st.markdown("### 🕺 RICK ASTLEY TARAFINDAN HACKLENDİNİZ!")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ", autoplay=True)
    st.balloons()

# --- DOOM MOTORU (WEB SÜRÜMÜ) ---
def doom_baslat():
    st.success("👹 DOOM BAŞLATILIYOR...")
    st.caption("ℹ️ Oyun tarayıcıda çalışır. Yüklenmesi 3-5 saniye sürebilir.")
    # GitHub üzerindeki Doom portunu gömüyoruz (En stabil yöntem)
    components.iframe("https://diekmann.github.io/wasm-fdoom/", height=600, scrolling=False)
    st.info("KONTROLLER: Enter=Başlat | Yön Tuşları=Gez | CTRL=Ateş")

# --- YAN MENÜ (TUZAKLI) ---
with st.sidebar:
    st.title("🧰 MENÜ")
    
    # TUZAK 1: GİZLİ FORMAT SEÇENEĞİ
    secim = st.radio("Araç Seç:", ["YouTube İndirici", "Resim Dönüştürücü", "Bitcoin Madencisi (BETA)"])
    
    st.markdown("---")
    
    # TUZAK 2: BEDAVA PREMIUM BUTONU
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e1/Logo_of_YouTube_%282015-2017%29.svg", width=100)
    if st.button("🔥 BEDAVA PREMIUM ÜYELİK AL", type="primary"):
        rick_roll_yap("TEBRİKLER! ÖMÜR BOYU RICK ROLL KAZANDINIZ!")

    st.markdown("---")
    
    # TUZAK 3: VİRÜS TARAMASI
    if st.button("🛡️ Virüs Taraması Yap"):
        with st.status("Taranıyor...", expanded=True) as s:
            time.sleep(1)
            st.write("C:/ taranıyor...")
            time.sleep(1)
            st.error("🚨 1 ADET RICK ASTLEY BULUNDU!")
            s.update(label="HATA!", state="error")
        rick_roll_yap("SİSTEM RICK ASTLEY TARAFINDAN ELE GEÇİRİLDİ!")

# ==========================================
# 1. YOUTUBE İNDİRİCİ (DOOM + TUZAKLI)
# ==========================================
if secim == "YouTube İndirici":
    st.title("🎬 YouTube İndirici")
    st.caption("Linki yapıştır, arkanı yaslan.")
    
    url = st.text_input("Video Linki (veya 'doom' yaz):")
    
    # DOOM KONTROLÜ (Bu kısım tuzağa düşmez, oyunu açar)
    doom_aktif = False
    if url and url.lower().strip() == "doom":
        doom_baslat()
        doom_aktif = True

    # Eğer Doom açık değilse normal arayüzü göster
    if not doom_aktif:
        # TUZAK 4: 8K ULTRA HD SEÇENEĞİ
        col1, col2 = st.columns(2)
        with col1: 
            fmt = st.radio("Kalite Seç:", ("Standart (MP4)", "Sadece Ses (MP3)", "✨ 8K ULTRA HD (Hızlı)"))

        if st.button("İndir 🚀", use_container_width=True):
            # TUZAK 5: BOŞ LİNK KONTROLÜ
            if not url:
                rick_roll_yap("LİNK GİRMEDEN İNDİREMEZSİN ZEKİ ŞEY!")
            
            # TUZAK 6: YASAKLI KELİMELER
            elif any(x in url.lower() for x in ["rick", "hack", "gizli", "secret", "admin"]):
                rick_roll_yap("GİZLİ KODU BULDUN! ÖDÜLÜN BU VİDEO:")
            
            # TUZAK 4 TETİKLEME (8K SEÇİLİRSE)
            elif "8K" in fmt:
                rick_roll_yap("8K İÇİN EKRAN KARTIN YETMEZ AMA BU YETER!")
                
            else:
                # --- GERÇEK İNDİRME KISMI ---
                try:
                    # Klasör temizle
                    for f in os.listdir(DOWNLOAD_DIR):
                        try: os.remove(os.path.join(DOWNLOAD_DIR, f))
                        except: pass

                    with st.status("İşleniyor...", expanded=True) as status:
                        ydl_opts = {
                            'outtmpl': f'{DOWNLOAD_DIR}/%(id)s.%(ext)s',
                            'quiet': True,
                            'no_warnings': True,
                            'nocheckcertificate': True,
                        }
                        
                        # Cookie Kontrolü (GitHub'daki dosya)
                        if os.path.exists("youtube_cookies.txt"):
                            ydl_opts['cookiefile'] = "youtube_cookies.txt"

                        if "MP3" in fmt:
                            st.write("🎵 Ses moduna geçiliyor...")
                            ydl_opts.update({
                                'format': 'bestaudio/best',
                                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]
                            })
                        else:
                            st.write("🎥 Video hazırlanıyor...")
                            ydl_opts.update({'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'})

                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([url])
                        
                        status.update(label="✅ Hazır!", state="complete", expanded=False)

                    dosyalar = os.listdir(DOWNLOAD_DIR)
                    if len(dosyalar) > 0:
                        bulunan_dosya = os.path.join(DOWNLOAD_DIR, dosyalar[0])
                        with open(bulunan_dosya, "rb") as file:
                            st.download_button(
                                label="📥 İNDİRMEK İÇİN BAS",
                                data=file,
                                file_name=dosyalar[0],
                                mime="application/octet-stream",
                                use_container_width=True
                            )
                        st.success("Tebrikler, bu sefer Rick Roll yemedin!")
                    else:
                        st.error("Dosya inemedi. Cookie süresi bitmiş olabilir.")

                except Exception as e:
                    st.error("Hata oluştu! Cookie dosyasını kontrol et.")
                    if "403" in str(e): st.warning("YouTube Erişim Engeli (403).")

# ==========================================
# 2. BITCOIN MADENCİSİ (BÜYÜK TUZAK)
# ==========================================
elif secim == "Bitcoin Madencisi (BETA)":
    st.title("💰 Bedava Bitcoin Kazıcı")
    st.warning("Bu işlem işlemcinizi %100 kullanır!")
    
    if st.button("KAZIMAYA BAŞLA (START MINING)"):
        progress_text = "Bitcoin aranıyor..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.05)
            my_bar.progress(percent_complete + 1, text=f"Bloklar çözülüyor... %{percent_complete}")
        
        rick_roll_yap("BITCOIN YOK AMA RICK ASTLEY VAR!")

# ==========================================
# 3. RESİM DÖNÜŞTÜRÜCÜ
# ==========================================
elif secim == "Resim Dönüştürücü":
    st.title("🖼️ Resim Dönüştürücü")
    up_file = st.file_uploader("Resim Yükle")
    
    if up_file:
        img = Image.open(up_file)
        st.image(img, width=200)
        
        # TUZAK 7: HEDEF FORMAT "GIF"
        target = st.selectbox("Format", ["JPEG", "PNG", "PDF", "ICO", "GIF (Hareketli)"])
        
        if st.button("Dönüştür"):
            if "GIF" in target:
                rick_roll_yap("HAREKETLİ GIF İSTEDİN, AL SANA HAREKET!")
            else:
                try:
                    for f in os.listdir(DOWNLOAD_DIR):
                        try: os.remove(os.path.join(DOWNLOAD_DIR, f))
                        except: pass
                    
                    if target in ["JPEG", "PDF"] and img.mode == "RGBA":
                        bg = Image.new("RGB", img.size, (255,255,255)); bg.paste(img, mask=img.split()[3]); img = bg
                    
                    path = os.path.join(DOWNLOAD_DIR, f"resim.{target.lower()}")
                    img.save(path, format=target)
                    
                    with open(path, "rb") as f:
                        st.download_button("📥 İNDİR", f, file_name=f"resim.{target.lower()}")
                except: st.error("Hata")

# --- ALT BİLGİ TUZAĞI ---
with st.expander("ℹ️ İletişim & Yardım"):
    st.write("Sorun mu yaşıyorsun? Destek ekibimize bağlan:")
    if st.button("📞 Canlı Destek Bağlan"):
        rick_roll_yap("MERHABA BEN DESTEK EKİBİNDEN RICK!")

