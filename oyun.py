import streamlit as st
import random
import json
import base64
import os

st.set_page_config(page_title="Krallık Savaşları: Tince'nin Kahramanları", layout="wide", page_icon="⚔️")

# --- GELİŞMİŞ YEREL GÖRSEL YÜKLEME MOTORU ---
def gorsel_yukle(dosya_adi):
    if not dosya_adi:
        return ""
    
    kok_ad = dosya_adi.split('.')[0]
    muhtemel_uzantilar = [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]
    
    bulunan_yol = None
    for uzanti in muhtemel_uzantilar:
        test_yolu = os.path.join("gorseller", kok_ad + uzanti)
        if os.path.exists(test_yolu):
            bulunan_yol = test_yolu
            break
            
    if bulunan_yol:
        try:
            with open(bulunan_yol, "rb") as f:
                data = f.read()
                encoded = base64.b64encode(data).decode()
                ext = bulunan_yol.split('.')[-1].lower()
                if ext == "jpg": ext = "jpeg"
                return f"data:image/{ext};base64,{encoded}"
        except Exception:
            return ""
            
    return ""

# --- KAYIT / YÜKLEME MOTORU ---
def kayit_kodu_olustur():
    veriler = {
        "isim": st.session_state.isim, "sinif": st.session_state.sinif,
        "seviye": st.session_state.seviye, "deneyim": st.session_state.deneyim,
        "altin": st.session_state.altin, "max_hp": st.session_state.max_hp,
        "hp": st.session_state.hp, "guc": st.session_state.guc,
        "ceviklik": st.session_state.ceviklik, "iksir": st.session_state.iksir,
        "odun": st.session_state.odun, "demir": st.session_state.demir,
        "kereste_seviye": st.session_state.kereste_seviye,
        "maden_seviye": st.session_state.maden_seviye,
        "kusandigi_silah": st.session_state.kusandigi_silah,
        "kusandigi_zirh": st.session_state.kusandigi_zirh,
        "silah_bonusu": st.session_state.silah_bonusu,
        "zirh_bonusu": st.session_state.zirh_bonusu,
        "envanter": st.session_state.envanter
    }
    json_str = json.dumps(veriler)
    b64_str = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
    return f"TINCE-{b64_str}"

def kayit_kodu_yukle(kod_str):
    try:
        clean_code = kod_str.strip().replace("TINCE-", "")
        json_str = base64.b64decode(clean_code.encode("utf-8")).decode("utf-8")
        veriler = json.loads(json_str)
        for k, v in veriler.items(): st.session_state[k] = v
        st.session_state.oyun_basladi = True
        st.session_state.konum = "Sığınak"
        st.session_state.secilen_bolge = "Karanlık Orman"
        st.session_state.aktif_olay = None
        st.session_state.savas_loglari = []
        st.session_state.aksiyon_efekti = "⚔️ Hatlar Kuruluyor, Savaşa Hazırlan!"
        return True
    except Exception: return False

# --- DOSYA EŞLEŞTİRMELERİ ---
KAHRAMAN_DOSYALARI = {
    "Savaşçı": "savasci",
    "Okçu": "okcu",
    "Büyücü": "buyucu"
}

CANAVAR_DOSYALARI = {
    "Vahşi Kurt": "kurt",
    "Yaban Domuzu": "domuz",
    "Gölge Haydutu": "haydut",
    "Goblin Savaşçısı": "goblin",
    "Kaya Golemi": "golem",
    "Zehirli Örümcek": "orumcek",
    "İskelet Şövalye": "iskelet",
    "Lanetli Rahip": "rahip",
    "Gölgeler Efendisi": "golge_efendisi",
    "Zindan Muhafızı": "muhafiz",
    "Lav Elementali": "lav_elemental",
    "Kadim Ejderha Ignis": "ejderha"
}

# --- 2D DİYAR HARİTASI ÇİZİM MOTORU ---
def harita_ciz(aktif_konum="Sığınak"):
    noktalar = {
        "Orman": {"x": 15, "y": 30, "renk": "#28a745", "ikon": "🌲", "etiket": "Karanlık Orman"},
        "Maden": {"x": 38, "y": 20, "renk": "#7f8c8d", "ikon": "⛏️", "etiket": "Eski Maden"},
        "Tapınak": {"x": 62, "y": 20, "renk": "#9b51e0", "ikon": "🏛️", "etiket": "Tapınak"},
        "Ejderha": {"x": 85, "y": 30, "renk": "#e74c3c", "ikon": "🌋", "etiket": "Ejderha İni"},
        "Kasaba": {"x": 25, "y": 70, "renk": "#ffd700", "ikon": "🏘️", "etiket": "Pazar"},
        "Sığınak": {"x": 75, "y": 70, "renk": "#d2b48c", "ikon": "🏕️", "etiket": "Sığınak"}
    }
    
    konum_str = str(aktif_konum).lower()
    
    svg = """<svg width="100%" height="200" viewBox="0 0 100 85" preserveAspectRatio="xMidYMid meet" style="background:#110d0a; border:2px inset #8b6508; border-radius:6px; box-shadow: 2px 2px 8px #000;">
        <line x1="25" y1="70" x2="75" y2="70" stroke="#4a3b32" stroke-width="1.5" stroke-dasharray="2,2"/>
        <line x1="25" y1="70" x2="15" y2="30" stroke="#4a3b32" stroke-width="1.5" stroke-dasharray="2,2"/>
        <line x1="15" y1="30" x2="38" y2="20" stroke="#4a3b32" stroke-width="1.5" stroke-dasharray="2,2"/>
        <line x1="38" y1="20" x2="62" y2="20" stroke="#4a3b32" stroke-width="1.5" stroke-dasharray="2,2"/>
        <line x1="62" y1="20" x2="85" y2="30" stroke="#4a3b32" stroke-width="1.5" stroke-dasharray="2,2"/>
        <line x1="75" y1="70" x2="85" y2="30" stroke="#4a3b32" stroke-width="1.5" stroke-dasharray="2,2"/>"""
    
    for anahtar, v in noktalar.items():
        is_active = False
        if anahtar.lower() in konum_str: is_active = True
        elif "pazar" in konum_str and anahtar == "Kasaba": is_active = True
        elif "orman" in konum_str and anahtar == "Orman": is_active = True
        elif "maden" in konum_str and anahtar == "Maden": is_active = True
        elif "tapınak" in konum_str and anahtar == "Tapınak": is_active = True
        elif "ejderha" in konum_str and anahtar == "Ejderha": is_active = True
            
        border = "#ffd700" if is_active else "#000"
        r = "4" if is_active else "2.5"
        
        svg += f"""<circle cx="{v['x']}" cy="{v['y']}" r="{r}" fill="{v['renk']}" stroke="{border}" stroke-width="1"/>
        <text x="{v['x']}" y="{v['y'] + 8}" fill="#e6c280" font-size="3.5" font-family="sans-serif" font-weight="bold" text-anchor="middle">{v['ikon']} {v['etiket']}</text>"""
        
        if is_active:
            svg += f"""<circle cx="{v['x']}" cy="{v['y']}" r="6" fill="none" stroke="#ffd700" stroke-width="0.8">
                <animate attributeName="r" values="4;8;4" dur="1.5s" repeatCount="indefinite" />
                <animate attributeName="opacity" values="1;0.2;1" dur="1.5s" repeatCount="indefinite" />
            </circle>
            <text x="{v['x']}" y="{v['y'] - 5}" fill="#ffd700" font-size="6" text-anchor="middle">♟️</text>"""
            
    svg += "</svg>"
    return svg

# --- GELİŞMİŞ CUSTOM CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap');
html, body, [class*="css"] { font-family: 'MedievalSharp', cursive !important; }
[data-testid="stAppViewContainer"] { background-color: #1a1612; background-image: radial-gradient(#2d241c 1px, transparent 1px); background-size: 20px 20px; color: #e6c280; }
[data-testid="stSidebar"] { background-color: #120e0a; border-right: 3px solid #8b6508; }
.ana-baslik { text-align: center; color: #ffd700; text-shadow: 2px 2px 4px #000; font-weight: 900; font-size: 3.2em; margin-bottom: 0; }
.alt-baslik { text-align: center; color: #a0522d; font-size: 1.2em; margin-bottom: 20px; text-shadow: 1px 1px 0px #000; }

.rpg-kart {
    background: linear-gradient(180deg, #2a1f18 0%, #1a120c 100%);
    border: 3px outset #8b6508;
    padding: 15px;
    text-align: center;
    box-shadow: 4px 4px 0px #000;
    color: #e6c280;
}
.rpg-kart img, .rpg-kart-canavar img {
    border: 2px solid #8b6508;
    border-radius: 6px;
    object-fit: cover;
    height: 200px;
    width: 100%;
}

.rpg-kart-canavar {
    background: linear-gradient(180deg, #3d1414 0%, #1a0808 100%);
    border: 3px outset #8b0000;
    padding: 15px;
    text-align: center;
    box-shadow: 4px 4px 0px #000;
}

.aksiyon-kutusu { background-color: #1c1c1c; border: 3px inset #4a4a4a; padding: 20px; text-align: center; min-height: 180px; box-shadow: 2px 2px 0px #000; }
.savas-log { background-color: #110d0a; border: 2px inset #8b6508; padding: 10px; max-height: 150px; overflow-y: auto; font-size: 14px; line-height: 1.4; }
div.stButton > button { background: linear-gradient(180deg, #5c4033 0%, #3e2723 100%); border: 2px outset #b8860b !important; color: #f5deb3 !important; font-family: 'MedievalSharp', cursive !important; font-size: 16px !important; text-shadow: 1px 1px 0px black; box-shadow: 3px 3px 0px #000; border-radius: 0px !important; width: 100%; }
div.stButton > button:hover { border: 2px inset #ffd700 !important; background: linear-gradient(180deg, #6b4c3a 0%, #4e342e 100%); color: #fff !important; transform: translateY(2px) translateX(2px); }
.kaynak-grid { display: flex; justify-content: space-between; gap: 10px; margin-top: 10px; margin-bottom: 20px; }
.kaynak-kutu { background: #110d0a; border: 2px inset #5c4033; padding: 10px 5px; text-align: center; flex: 1; font-weight: bold; font-size: 16px; box-shadow: 2px 2px 0px #000; }
.k-altin { color: #ffd700;} .k-odun { color: #d2b48c;} .k-demir { color: #c0c0c0;}
.esya-kart { background-color: #2a1f18; border: 2px solid #8b6508; border-left: 8px solid #b8860b; padding: 12px; margin-bottom: 10px; box-shadow: 3px 3px 0px #000; }
div[data-baseweb="input"] > div, div[data-baseweb="select"] > div { background-color: #1a120c !important; border: 2px inset #8b6508 !important; border-radius: 0px !important; color: #e6c280 !important; }
button[data-baseweb="tab"] { background-color: #1a120c !important; border: 2px outset #8b6508 !important; border-bottom: none !important; color: #8b6508 !important; font-family: 'MedievalSharp', cursive !important; margin-right: 4px; }
button[data-baseweb="tab"][aria-selected="true"] { background-color: #2a1f18 !important; color: #ffd700 !important; border-color: #ffd700 !important; }
</style>
""", unsafe_allow_html=True)

# --- 1. OTURUM HAFIZASI ---
if "oyun_basladi" not in st.session_state:
    st.session_state.oyun_basladi = False
    st.session_state.isim = ""; st.session_state.sinif = ""
    st.session_state.seviye = 1; st.session_state.deneyim = 0
    st.session_state.altin = 200; st.session_state.max_hp = 100; st.session_state.hp = 100
    st.session_state.guc = 10; st.session_state.ceviklik = 10; st.session_state.iksir = 3
    st.session_state.odun = 30; st.session_state.demir = 15
    st.session_state.kereste_seviye = 0; st.session_state.maden_seviye = 0
    st.session_state.konum = "Sığınak"
    st.session_state.kusandigi_silah = "Paslı Kılıç"; st.session_state.kusandigi_zirh = "Eski Giysi"
    st.session_state.silah_bonusu = 0; st.session_state.zirh_bonusu = 0; st.session_state.envanter = []
    st.session_state.secilen_bolge = "Karanlık Orman"
    st.session_state.aktif_olay = None; st.session_state.dusman_adi = ""
    st.session_state.dusman_hp = 0; st.session_state.dusman_max_hp = 0; st.session_state.dusman_guc = 0
    st.session_state.savas_loglari = []; st.session_state.aksiyon_efekti = "⚔️ Hatlar Kuruluyor, Savaşa Hazırlan!"
    st.session_state.son_kazanilan_xp = 0; st.session_state.son_kazanilan_altin = 0
    st.session_state.son_kazanilan_odun = 0; st.session_state.son_kazanilan_demir = 0
    st.session_state.seviye_atlama_mujdesi = False; st.session_state.sandik_mesaji = ""

def pasif_uretim():
    if st.session_state.kereste_seviye > 0: st.session_state.odun += st.session_state.kereste_seviye * 3
    if st.session_state.maden_seviye > 0: st.session_state.demir += st.session_state.maden_seviye * 2

if st.session_state.oyun_basladi: pasif_uretim()

def bar_ciz(mevcut, maksimum, tip="hp"):
    oran = max(0.0, min(1.0, mevcut / maksimum)); yuzde = int(oran * 100)
    if tip == "hp": renk1 = "#8b0000"; renk2 = "#ff0000"; yazi = f"❤️ {int(mevcut)}/{maksimum} HP"
    else: renk1 = "#006400"; renk2 = "#32cd32"; yazi = f"✨ {int(mevcut)}/{maksimum} XP"
    st.markdown(f"""<div style='background-color:#110d0a; border-radius:0px; width:100%; height:24px; margin-bottom:12px; border:2px inset #8b6508; position: relative;'>
        <div style='background: linear-gradient(90deg, {renk1} 0%, {renk2} 100%); width:{yuzde}%; height:100%;'></div>
        <div style='position: absolute; top: 0; left: 0; width: 100%; height: 100%; text-align: center; color: white; font-weight: bold; font-size: 13px; line-height: 20px;'>{yazi}</div>
    </div>""", unsafe_allow_html=True)

# --- 2. GİRİŞ EKRANI ---
if not st.session_state.oyun_basladi:
    st.markdown("<h1 class='ana-baslik'>KRALLIK SAVAŞLARI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='alt-baslik'>Miras ve Büyü Çağı</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_yeni, tab_yukle = st.tabs(["🔥 Yeni Maceracı", "📜 Parşömen Mührü Dök"])
        with tab_yeni:
            isim_girdisi = st.text_input("Kahramanın Adı:", "Tince")
            sinif_girdisi = st.selectbox("Sınıfın (Kaderin):", ["Savaşçı", "Okçu", "Büyücü"])
            st.write("")
            if st.button("Macerayı Başlat! 🔥", use_container_width=True):
                st.session_state.isim = isim_girdisi; st.session_state.sinif = sinif_girdisi
                st.session_state.oyun_basladi = True
                if sinif_girdisi == "Savaşçı":
                    st.session_state.max_hp = 160; st.session_state.hp = 160; st.session_state.guc = 20; st.session_state.ceviklik = 8; st.session_state.kusandigi_silah = "Paslı Kılıç"
                elif sinif_girdisi == "Okçu":
                    st.session_state.max_hp = 115; st.session_state.hp = 115; st.session_state.guc = 14; st.session_state.ceviklik = 22; st.session_state.kusandigi_silah = "Yıpranmış Yay"
                elif sinif_girdisi == "Büyücü":
                    st.session_state.max_hp = 100; st.session_state.hp = 100; st.session_state.guc = 18; st.session_state.ceviklik = 10; st.session_state.kusandigi_silah = "Eski Asa"
                st.rerun()
        with tab_yukle:
            girilen_kod = st.text_area("Parşömen Kodu:", placeholder="TINCE-eyJzZXZpeW...").strip()
            if st.button("Kodu Oku ve Kaldığın Yerden Devam Et 🔮", use_container_width=True):
                if girilen_kod and kayit_kodu_yukle(girilen_kod): st.toast("Kayıt yüklendi!", icon="✨"); st.rerun()
                else: st.error("📜 Geçersiz Parşömen Kodu!")

# --- 3. ANA OYUN ---
else:
    toplam_guc = st.session_state.guc + st.session_state.silah_bonusu

    with st.sidebar:
        dosya = KAHRAMAN_DOSYALARI.get(st.session_state.sinif, "")
        src = gorsel_yukle(dosya)
        img_html = f"<img src='{src}'>" if src else f"<div style='font-size:80px; padding:20px;'>🛡️</div>"
        
        st.markdown(f"<div class='rpg-kart'>{img_html}<h2 style='margin:10px 0 0 0; color:#ffd700;'>{st.session_state.isim}</h2><p style='margin:5px 0; color:#c0c0c0;'>Seviye {st.session_state.seviye} {st.session_state.sinif}</p></div>", unsafe_allow_html=True)
        st.write("")
        bar_ciz(st.session_state.hp, st.session_state.max_hp, "hp")
        bar_ciz(st.session_state.deneyim, st.session_state.seviye * 100, "xp")
        st.divider()
        st.markdown(f"**⚔️ Toplam Saldırı:** `{toplam_guc}`")
        st.markdown(f"**🛡️ Defans Bonusu:** `+{st.session_state.zirh_bonusu}`")
        st.markdown(f"**🎒 Silah:** `{st.session_state.kusandigi_silah}`")
        st.markdown(f"**🛡️ Zırh:** `{st.session_state.kusandigi_zirh}`")
        st.markdown(f"**🧪 İksirler:** `{st.session_state.iksir} Adet`")
        st.divider()
        st.markdown("<h3 style='color:#ffd700;'>👑 Ambar</h3>", unsafe_allow_html=True)
        st.markdown(f"""<div class='kaynak-grid'>
            <div class='kaynak-kutu k-altin'>🪙<br>{st.session_state.altin}</div>
            <div class='kaynak-kutu k-odun'>🪵<br>{st.session_state.odun}</div>
            <div class='kaynak-kutu k-demir'>⛓️<br>{st.session_state.demir}</div>
        </div>""", unsafe_allow_html=True)
        st.divider()
        st.markdown("<h3 style='color:#ffd700;'>📜 Macerayı Kaydet</h3>", unsafe_allow_html=True)
        st.code(kayit_kodu_olustur(), language="text")
        st.divider()
        if st.button("Karakteri Sıfırla", use_container_width=True): st.session_state.clear(); st.rerun()

    st.markdown("<h2 style='text-align:center; color:#e6c280;'>🗺️ Diyar Haritası</h2>", unsafe_allow_html=True)
    st.markdown(harita_ciz(st.session_state.konum), unsafe_allow_html=True)
    st.write("")

    tab_kesif, tab_envanter, tab_kasaba, tab_siginak = st.tabs(["⚔️ Macera", "🎒 Çanta", "🏘️ Pazar", "🏕️ Sığınak"])

    # --- TAB 1: SAVAŞ VE KEŞİF ---
    with tab_kesif:
        st.session_state.konum = st.session_state.secilen_bolge
        if st.session_state.aktif_olay is None:
            if st.session_state.son_kazanilan_xp > 0:
                st.markdown(f"""<div class='rpg-kart' style='margin-bottom: 20px; border-color: #28a745;'>
                    <h3 style='color: #32cd32; margin-top:0;'>🏆 ZAFER RAPORU</h3>
                    <div style='display:flex; justify-content:space-around; font-size:18px;'>
                        <span>✨ +{st.session_state.son_kazanilan_xp} XP</span>
                        <span>🪙 +{st.session_state.son_kazanilan_altin} Altın</span>
                        <span>🪵 +{st.session_state.son_kazanilan_odun} Odun</span>
                        <span>⛓️ +{st.session_state.son_kazanilan_demir} Demir</span>
                    </div>
                </div>""", unsafe_allow_html=True)
                if st.session_state.seviye_atlama_mujdesi:
                    st.toast(f"🚀 Seviye {st.session_state.seviye} oldun!", icon="🔥")
                    st.session_state.seviye_atlama_mujdesi = False
                if st.button("Raporu Parşömene Sar 📝", use_container_width=True):
                    st.session_state.son_kazanilan_xp = 0; st.rerun()

            st.markdown("<h3 style='color:#ffd700;'>🗺️ Hedef Seçimi</h3>", unsafe_allow_html=True)
            st.session_state.secilen_bolge = st.radio(
                "Keşfetmek İstediğin Bölgeyi Seç:",
                ["Karanlık Orman (Seviye 1-2)", "Eski Maden Ocakları (Seviye 3-4)", "Terk Edilmiş Tapınak (Seviye 5-6)", "Kadim Ejderha İni (Seviye 7+)"],
                horizontal=True
            )
            st.write("")
            if st.button("Bölgeye Adım At", use_container_width=True, type="primary"):
                if "Maden" in st.session_state.secilen_bolge and st.session_state.seviye < 3: st.error("🔒 En az 3. seviye olmalısın!")
                elif "Tapınak" in st.session_state.secilen_bolge and st.session_state.seviye < 5: st.error("🔒 En az 5. seviye olmalısın!")
                elif "Ejderha" in st.session_state.secilen_bolge and st.session_state.seviye < 7: st.error("🔒 En az 7. seviye olmalısın!")
                else:
                    if random.random() < 0.2:
                        st.session_state.aktif_olay = "sandik"; st.session_state.sandik_mesaji = ""
                    else:
                        st.session_state.aktif_olay = "savas"
                        if "Orman" in st.session_state.secilen_bolge:
                            dusmanlar = [
                                {"ad": "Vahşi Kurt", "hp": 45, "guc": 8, "xp": 40, "altin": 25, "odun_odul": 8, "demir_odul": 0},
                                {"ad": "Yaban Domuzu", "hp": 55, "guc": 11, "xp": 50, "altin": 35, "odun_odul": 12, "demir_odul": 0},
                                {"ad": "Gölge Haydutu", "hp": 65, "guc": 13, "xp": 60, "altin": 45, "odun_odul": 10, "demir_odul": 2}
                            ]
                        elif "Maden" in st.session_state.secilen_bolge:
                            dusmanlar = [
                                {"ad": "Goblin Savaşçısı", "hp": 85, "guc": 15, "xp": 75, "altin": 60, "odun_odul": 5, "demir_odul": 12},
                                {"ad": "Kaya Golemi", "hp": 115, "guc": 19, "xp": 95, "altin": 80, "odun_odul": 0, "demir_odul": 20},
                                {"ad": "Zehirli Örümcek", "hp": 90, "guc": 17, "xp": 85, "altin": 70, "odun_odul": 8, "demir_odul": 8}
                            ]
                        elif "Tapınak" in st.session_state.secilen_bolge:
                            dusmanlar = [
                                {"ad": "İskelet Şövalye", "hp": 140, "guc": 22, "xp": 130, "altin": 110, "odun_odul": 10, "demir_odul": 25},
                                {"ad": "Lanetli Rahip", "hp": 125, "guc": 26, "xp": 145, "altin": 130, "odun_odul": 15, "demir_odul": 15},
                                {"ad": "Gölgeler Efendisi", "hp": 210, "guc": 30, "xp": 250, "altin": 220, "odun_odul": 25, "demir_odul": 35}
                            ]
                        else:
                            dusmanlar = [
                                {"ad": "Zindan Muhafızı", "hp": 220, "guc": 32, "xp": 220, "altin": 200, "odun_odul": 20, "demir_odul": 30},
                                {"ad": "Lav Elementali", "hp": 260, "guc": 36, "xp": 280, "altin": 250, "odun_odul": 10, "demir_odul": 45},
                                {"ad": "Kadim Ejderha Ignis", "hp": 500, "guc": 45, "xp": 1000, "altin": 1000, "odun_odul": 100, "demir_odul": 100}
                            ]
                        
                        secilen = random.choice(dusmanlar)
                        st.session_state.dusman_adi = secilen["ad"]
                        st.session_state.dusman_hp = secilen["hp"]
                        st.session_state.dusman_max_hp = secilen["hp"]
                        st.session_state.dusman_guc = secilen["guc"]
                        st.session_state.dusman_xp = secilen["xp"]
                        st.session_state.dusman_altin = secilen["altin"]
                        st.session_state.dusman_odun = secilen["odun_odul"]
                        st.session_state.dusman_demir = secilen["demir_odul"]
                        st.session_state.savas_loglari = [f"[{secilen['ad']}] karanlıkların içinden üzerine atıldı!"]
                        st.session_state.aksiyon_efekti = "Karşı Karşıyasınız!"
                    st.rerun()

        elif st.session_state.aktif_olay == "sandik":
            st.markdown("<div class='aksiyon-kutusu' style='border-color:#ffd700;'><h2 style='color:#ffd700;'>🔒 Ganimet Sandığı Belirdi!</h2></div>", unsafe_allow_html=True)
            st.write("")
            if st.session_state.sandik_mesaji == "":
                if st.button("Sandığı Aç", use_container_width=True, type="primary"):
                    if random.random() < 0.6:
                        altin_odul = random.randint(70, 200)
                        st.session_state.altin += altin_odul
                        st.session_state.sandik_mesaji = f"💰 Sandıktan tam **{altin_odul} Altın** çıktı!"
                    else:
                        esya_turu = random.choice(["silah", "zırh"])
                        if esya_turu == "silah":
                            bonus = random.randint(15, 30)
                            yeni_silah = {"ad": f"Efsanevi Savaş Baltası (+{bonus})", "tip": "silah", "özellik": f"+{bonus} Güç", "değer": bonus}
                            st.session_state.envanter.append(yeni_silah)
                            st.session_state.sandik_mesaji = f"⚔️ Sandıktan **{yeni_silah['ad']}** çıktı!"
                        else:
                            bonus = random.randint(30, 60)
                            yeni_zirh = {"ad": f"Ejderha Pullu Zırh (+{bonus})", "tip": "zırh", "özellik": f"+{bonus} Defans", "değer": bonus}
                            st.session_state.envanter.append(yeni_zirh)
                            st.session_state.sandik_mesaji = f"🛡️ Sandıktan **{yeni_zirh['ad']}** çıktı!"
                    st.rerun()
            else:
                st.success(st.session_state.sandik_mesaji)
                if st.button("Devam Et", use_container_width=True):
                    st.session_state.aktif_olay = None; st.session_state.sandik_mesaji = ""; st.rerun()

        elif st.session_state.aktif_olay == "savas":
            kart_sol, kart_orta, kart_sag = st.columns([2, 3, 2])
            with kart_sol:
                dosya = KAHRAMAN_DOSYALARI.get(st.session_state.sinif, "")
                src = gorsel_yukle(dosya)
                img_html = f"<img src='{src}'>" if src else f"<div style='font-size:80px; padding:20px;'>🛡️</div>"
                st.markdown(f"<div class='rpg-kart'>{img_html}<h3 style='color:#ffd700;'>{st.session_state.isim}</h3></div>", unsafe_allow_html=True)
                st.write(""); bar_ciz(st.session_state.hp, st.session_state.max_hp, "hp")
            with kart_orta:
                st.markdown(f"<div class='aksiyon-kutusu'><h4>MUHAREBE AKIŞI</h4><h2 style='color: #ff4b4b;'>{st.session_state.aksiyon_efekti}</h2></div>", unsafe_allow_html=True)
                st.write("")
                b_col1, b_col2 = st.columns(2)
                with b_col1:
                    if st.button("Saldır", use_container_width=True, type="primary"):
                        kritik = random.randint(1, 100) <= (st.session_state.ceviklik * 2)
                        hasar = toplam_guc + random.randint(-2, 5)
                        if kritik: hasar *= 2; st.session_state.savas_loglari.append(f"<span style='color:#ffd700;'>KRİTİK VURUŞ! Düşmana {hasar} hasar verdin!</span>")
                        else: st.session_state.savas_loglari.append(f"Düşmana {hasar} hasar verdin.")
                        st.session_state.dusman_hp -= hasar
                        
                        if st.session_state.dusman_hp <= 0:
                            if st.session_state.dusman_adi == "Kadim Ejderha Ignis":
                                st.balloons(); st.success("EJDERHA KATİLİ OLDUN! KRALLIĞI KURTARDIN!"); st.session_state.clear(); st.stop()
                            st.session_state.son_kazanilan_xp = st.session_state.dusman_xp
                            st.session_state.son_kazanilan_altin = st.session_state.dusman_altin
                            st.session_state.son_kazanilan_odun = st.session_state.dusman_odun
                            st.session_state.son_kazanilan_demir = st.session_state.dusman_demir
                            st.session_state.altin += st.session_state.dusman_altin
                            st.session_state.deneyim += st.session_state.dusman_xp
                            st.session_state.odun += st.session_state.dusman_odun
                            st.session_state.demir += st.session_state.dusman_demir
                            if st.session_state.deneyim >= st.session_state.seviye * 100:
                                st.session_state.deneyim -= (st.session_state.seviye * 100)
                                st.session_state.seviye += 1
                                st.session_state.max_hp += 25; st.session_state.guc += 4; st.session_state.hp = st.session_state.max_hp
                                st.session_state.seviye_atlama_mujdesi = True
                            st.session_state.aktif_olay = None; st.rerun()

                        d_hasar = max(1, st.session_state.dusman_guc - (st.session_state.zirh_bonusu // 2) + random.randint(-2, 3))
                        st.session_state.hp -= d_hasar
                        st.session_state.aksiyon_efekti = f"Düşman Atak Yaptı! (-{d_hasar} HP)"
                        st.session_state.savas_loglari.append(f"<span style='color:#ff4b4b;'>{st.session_state.dusman_adi} sana {d_hasar} vurdu.</span>")
                        if st.session_state.hp <= 0:
                            st.session_state.altin = max(0, st.session_state.altin - 50)
                            st.session_state.hp = int(st.session_state.max_hp * 0.5); st.session_state.aktif_olay = None; st.rerun()
                        st.rerun()
                with b_col2:
                    if st.button("İksir İç (+50 HP)", use_container_width=True):
                        if st.session_state.iksir > 0:
                            st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + 50); st.session_state.iksir -= 1
                            st.session_state.savas_loglari.append("<span style='color:#32cd32;'>İksir içtin. 50 HP yenilendi.</span>")
                            st.rerun()

                st.write("")
                log_html = "<div class='savas-log'>" + "<br>".join(reversed(st.session_state.savas_loglari)) + "</div>"
                st.markdown(log_html, unsafe_allow_html=True)
            with kart_sag:
                c_dosya = CANAVAR_DOSYALARI.get(st.session_state.dusman_adi, "")
                c_src = gorsel_yukle(c_dosya)
                c_img_html = f"<img src='{c_src}'>" if c_src else f"<div style='font-size:80px; padding:20px;'>👾</div>"
                st.markdown(f"<div class='rpg-kart-canavar'>{c_img_html}<h3 style='color:#ff4b4b;'>{st.session_state.dusman_adi}</h3></div>", unsafe_allow_html=True)
                st.write(""); bar_ciz(st.session_state.dusman_hp, st.session_state.dusman_max_hp, "hp")

    # --- TAB 2: ENVANTER ---
    with tab_envanter:
        if not st.session_state.envanter: st.info("Çantan bomboş.")
        else:
            for i, esya in enumerate(st.session_state.envanter):
                st.markdown(f"<div class='esya-kart'><b>{esya['ad']}</b><br>Tür: {esya['tip'].upper()} | Özellik: {esya['özellik']}</div>", unsafe_allow_html=True)
                if st.button(f"Kuşan ({esya['ad']})", key=f"kus_{i}_{esya['ad']}"):
                    if esya["tip"] == "silah": st.session_state.kusandigi_silah = esya["ad"]; st.session_state.silah_bonusu = esya["değer"]
                    elif esya["tip"] == "zırh": st.session_state.kusandigi_zirh = esya["ad"]; st.session_state.zirh_bonusu = esya["değer"]
                    st.toast(f"{esya['ad']} kuşanıldı!", icon="⚔️"); st.rerun()

    # --- TAB 3: PAZAR ---
    with tab_kasaba:
        st.session_state.konum = "Kasaba"
        colP1, colP2 = st.columns(2)
        with colP1:
            st.markdown("<div class='aksiyon-kutusu'><h3>Şifacı Dükkanı</h3></div>", unsafe_allow_html=True)
            st.write("")
            if st.button("Sağlık İksiri (25 Altın)", use_container_width=True):
                if st.session_state.altin >= 25: st.session_state.altin -= 25; st.session_state.iksir += 1; st.rerun()
                else: st.error("Yetersiz Altın!")
        with colP2:
            st.markdown("<div class='aksiyon-kutusu'><h3>Kasaba Hanı</h3></div>", unsafe_allow_html=True)
            st.write("")
            if st.button("Han'da Dinlen (20 Altın)", use_container_width=True):
                if st.session_state.altin >= 20: st.session_state.altin -= 20; st.session_state.hp = st.session_state.max_hp; st.rerun()
                else: st.error("Yetersiz Altın!")

    # --- TAB 4: SIĞINAK VE CRAFTING ---
    with tab_siginak:
        st.session_state.konum = "Sığınak"
        b1, b2 = st.columns(2)
        with b1:
            st.markdown(f"<div class='esya-kart'><h3>Kereste Kampı</h3>Mevcut Seviye: <b>{st.session_state.kereste_seviye}</b></div>", unsafe_allow_html=True)
            maliyet = (st.session_state.kereste_seviye + 1) * 80
            if st.button(f"Kampı Büyüt ({maliyet} Altın)", use_container_width=True):
                if st.session_state.altin >= maliyet: st.session_state.altin -= maliyet; st.session_state.kereste_seviye += 1; st.rerun()
                else: st.error("Yetersiz Altın!")
        with b2:
            st.markdown(f"<div class='esya-kart'><h3>Demir Madeni</h3>Mevcut Seviye: <b>{st.session_state.maden_seviye}</b></div>", unsafe_allow_html=True)
            maliyet_a = (st.session_state.maden_seviye + 1) * 100; maliyet_o = (st.session_state.maden_seviye + 1) * 25
            if st.button(f"Madeni Derinleştir ({maliyet_a} A, {maliyet_o} O)", use_container_width=True):
                if st.session_state.altin >= maliyet_a and st.session_state.odun >= maliyet_o:
                    st.session_state.altin -= maliyet_a; st.session_state.odun -= maliyet_o; st.session_state.maden_seviye += 1; st.rerun()
                else: st.error("Yetersiz Kaynak!")
        st.divider()
        st.markdown("<h3 style='text-align:center; color:#ffd700;'>Demirci Örsü</h3>", unsafe_allow_html=True)
        cr1, cr2 = st.columns(2)
        with cr1:
            if st.button("Çelik Kılıç Döv (40 Odun, 25 Demir)", use_container_width=True):
                if st.session_state.odun >= 40 and st.session_state.demir >= 25:
                    st.session_state.odun -= 40; st.session_state.demir -= 25
                    st.session_state.envanter.append({"ad": f"Dövme Çelik Kılıç V{random.randint(1,9)}", "tip": "silah", "özellik": "+15 Güç", "değer": 15})
                    st.toast("Kılıç dövüldü!", icon="⚔️"); st.rerun()
                else: st.error("Kaynak eksik!")
        with cr2:
            if st.button("Şövalye Plakası Döv (20 Odun, 50 Demir)", use_container_width=True):
                if st.session_state.odun >= 20 and st.session_state.demir >= 50:
                    st.session_state.odun -= 20; st.session_state.demir -= 50
                    st.session_state.envanter.append({"ad": f"Ağır Demir Göğüslük V{random.randint(1,9)}", "tip": "zırh", "özellik": "+30 Defans", "değer": 30})
                    st.toast("Zırh dövüldü!", icon="🛡️"); st.rerun()
                else: st.error("Kaynak eksik!")
