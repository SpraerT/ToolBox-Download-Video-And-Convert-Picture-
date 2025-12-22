import streamlit as st
import yt_dlp
import os
import time
from PIL import Image
import shutil

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ultimate Toolbox", page_icon="🧰", layout="centered")

# --- İNDİRME KLASÖRÜ ---
DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# --- RICK ROLL ---
def rick_roll_yap():
    st.error("⚠️ SİSTEM HACKLENDİ! KAÇIN!")
    time.sleep(1)
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ", autoplay=True)

# --- YAN MENÜ ---
with st.sidebar:
    st.title("🧰 MENÜ")
    secim = st.radio("Araç Seç:", ["YouTube İndirici", "Resim Dönüştürücü"])
    st.markdown("---")
    st.caption("v24.0 Debug Edition")
    if st.button("⚠️ KIRMIZI BUTON", type="primary"):
        rick_roll_yap()

# ==========================================
# 1. YOUTUBE İNDİRİCİ
# ==========================================
if secim == "YouTube İndirici":
    st.title("🎬 YouTube İndirici")
    
    url = st.text_input("Video Linki:")
    col1, col2 = st.columns(2)
    with col1: fmt = st.radio("Biçim:", ("MP4 (Video)", "MP3 (Ses)"))

    if st.button("İndir 🚀", use_container_width=True):
        if not url:
            st.warning("Link girmeyi unuttun!")
        elif "dQw4w9WgXcQ" in url:
            rick_roll_yap()
        else:
            try:
                # Klasörü temizle
                for f in os.listdir(DOWNLOAD_DIR):
                    try: os.remove(os.path.join(DOWNLOAD_DIR, f))
                    except: pass

                with st.status("İşleniyor... (Lütfen bekleyin)", expanded=True) as status:
                    st.write("🔍 Video bilgileri alınıyor...")
                    
                    ydl_opts = {
                        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
                        'quiet': True,
                        'no_warnings': True,
                        'restrictfilenames': True, # Türkçe karakter sorununu çözer
                    }
                    
                    if fmt.startswith("MP3"):
                        st.write("🎵 Sese dönüştürülüyor (FFmpeg)...")
                        ydl_opts.update({
                            'format': 'bestaudio/best',
                            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]
                        })
                    else:
                        st.write("🎥 Video birleştiriliyor...")
                        ydl_opts.update({'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'})

                    # İndirme İşlemi
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        dosya_adi = ydl.prepare_filename(info)
                        if fmt.startswith("MP3"): 
                            dosya_adi = os.path.splitext(dosya_adi)[0] + ".mp3"
                    
                    status.update(label="✅ İşlem Başarılı!", state="complete", expanded=False)

                # İNDİRME BUTONU
                dosya_ismi = os.path.basename(dosya_adi)
                with open(dosya_adi, "rb") as file:
                    st.download_button(
                        label=f"📥 {dosya_ismi} İNDİR",
                        data=file,
                        file_name=dosya_ismi,
                        mime="audio/mpeg" if fmt.startswith("MP3") else "video/mp4",
                        use_container_width=True
                    )
                st.balloons()

            except Exception as e:
                st.error("❌ BİR HATA OLUŞTU!")
                st.code(f"Hata Detayı: {e}")
                st.warning("Eğer hata 'ffprobe' veya 'ffmpeg' içeriyorsa, sistemde FFmpeg yüklü değildir.")
                if os.name == 'posix': # Linux/Mac uyarısı
                    st.info("Çözüm: Terminale 'sudo apt install ffmpeg' yaz.")

# ==========================================
# 2. RESİM DÖNÜŞTÜRÜCÜ
# ==========================================
elif secim == "Resim Dönüştürücü":
    st.title("🖼️ Resim Dönüştürücü")
    up_file = st.file_uploader("Resim", type=['png', 'jpg', 'webp', 'bmp'])
    
    if up_file:
        img = Image.open(up_file)
        st.image(img, width=200)
        target = st.selectbox("Format", ["JPEG", "PNG", "PDF", "ICO"])
        
        if st.button("Dönüştür"):
            try:
                if target in ["JPEG", "PDF"] and img.mode == "RGBA":
                    bg = Image.new("RGB", img.size, (255,255,255))
                    bg.paste(img, mask=img.split()[3])
                    img = bg
                
                path = os.path.join(DOWNLOAD_DIR, f"resim.{target.lower()}")
                img.save(path, format=target)
                
                with open(path, "rb") as f:
                    st.download_button("📥 İNDİR", f, file_name=f"resim.{target.lower()}")
                st.success("Tamam!")
            except Exception as e: st.error(f"Hata: {e}")

