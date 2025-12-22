import streamlit as st
import yt_dlp
import os
import time
from PIL import Image
import shutil

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ultimate Toolbox", page_icon="🧰", layout="centered")

# --- GEÇİCİ İNDİRME KLASÖRÜ (Sunucu için) ---
DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# --- RICK ROLL FONKSİYONU ---
def rick_roll_yap():
    st.error("⚠️ UYARI: KRİTİK HATA TESPİT EDİLDİ!")
    time.sleep(1)
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ", autoplay=True)
    st.toast("🕺 NEVER GONNA GIVE YOU UP!")

# --- YAN MENÜ ---
with st.sidebar:
    st.title("🧰 MENÜ")
    secim = st.radio("Araç Seç:", ["YouTube İndirici", "Resim Dönüştürücü"])
    st.markdown("---")
    
    # RICK ROLL BUTONU (Gizli Silah)
    st.write("🔧 **Admin Paneli**")
    if st.button("⚠️ SİSTEMİ SIFIRLA (SAKIN BASMA)", type="primary"):
        rick_roll_yap()

# ==========================================
# 1. YOUTUBE İNDİRİCİ (Yayınlamaya Uygun)
# ==========================================
if secim == "YouTube İndirici":
    st.title("🎬 YouTube İndirici")
    st.caption("Videoları sunucuda işler ve sana indirme linki verir.")
    
    url = st.text_input("Video Linki:")
    col1, col2 = st.columns(2)
    with col1: fmt = st.radio("Biçim:", ("MP4 (Video)", "MP3 (Ses)"))

    if st.button("Hazırla 🚀", use_container_width=True):
        if not url:
            st.warning("Lütfen bir link gir.")
        # RICK ROLL LİNK KONTROLÜ
        elif "dQw4w9WgXcQ" in url:
            rick_roll_yap()
        else:
            try:
                with st.spinner('Sunucuda işleniyor... Bu işlem videonun uzunluğuna göre sürebilir.'):
                    # Önceki dosyaları temizle (Sunucu şişmesin)
                    for f in os.listdir(DOWNLOAD_DIR):
                        os.remove(os.path.join(DOWNLOAD_DIR, f))

                    # İndirme Ayarları
                    ydl_opts = {
                        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
                        'quiet': True,
                        'no_warnings': True,
                    }
                    
                    if fmt.startswith("MP3"):
                        ydl_opts.update({
                            'format': 'bestaudio/best',
                            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]
                        })
                    else:
                        ydl_opts.update({'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'})

                    # İndirmeyi Başlat
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        dosya_adi = ydl.prepare_filename(info)
                        if fmt.startswith("MP3"): 
                            dosya_adi = os.path.splitext(dosya_adi)[0] + ".mp3"

                    # İNDİRME BUTONU OLUŞTUR
                    dosya_ismi = os.path.basename(dosya_adi)
                    with open(dosya_adi, "rb") as file:
                        btn = st.download_button(
                            label=f"📥 {dosya_ismi} İNDİR",
                            data=file,
                            file_name=dosya_ismi,
                            mime="audio/mpeg" if fmt.startswith("MP3") else "video/mp4",
                            use_container_width=True
                        )
                    st.success("Video hazır! Yukarıdaki butona basarak cihazına indir.")

            except Exception as e:
                st.error("Bir hata oluştu. Linki kontrol et.")

# ==========================================
# 2. RESİM DÖNÜŞTÜRÜCÜ (Yayınlamaya Uygun)
# ==========================================
elif secim == "Resim Dönüştürücü":
    st.title("🖼️ Resim Dönüştürücü")
    
    up_file = st.file_uploader("Resim Yükle", type=['png', 'jpg', 'webp', 'bmp', 'tiff'])
    
    if up_file:
        img = Image.open(up_file)
        st.image(img, width=200)
        
        target_fmt = st.selectbox("Hedef Format", ["JPEG", "PNG", "PDF", "ICO", "WEBP"])
        
        if st.button("Dönüştür 🔄", use_container_width=True):
            try:
                # RGB Dönüşümü (PNG -> JPG/PDF hatası olmaması için)
                if target_fmt in ["JPEG", "PDF"] and img.mode == "RGBA":
                    bg = Image.new("RGB", img.size, (255,255,255))
                    bg.paste(img, mask=img.split()[3])
                    img = bg
                
                # Geçici kaydet
                save_path = os.path.join(DOWNLOAD_DIR, f"converted_image.{target_fmt.lower()}")
                img.save(save_path, format=target_fmt)
                
                # İndirme Butonu
                with open(save_path, "rb") as file:
                    st.download_button(
                        label="📥 RESMİ İNDİR",
                        data=file,
                        file_name=f"yeni_resim.{target_fmt.lower()}",
                        mime=f"image/{target_fmt.lower()}",
                        use_container_width=True
                    )
                st.success("Dönüştürme başarılı!")
            except Exception as e:
                st.error(f"Hata: {e}")

st.markdown("---")
st.caption("🚀 Ultimate Toolbox | v1.0 Release")
