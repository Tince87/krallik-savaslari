import streamlit as st
import random

st.set_page_config(page_title="Krallık Savaşları: Tince'nin Kahramanları", layout="wide", page_icon="⚔️")

# --- KIRILMAZ VE YEREL VEKTÖREL RPG KARAKTER ÇİZİMLERİ (SVG MOTORU) ---
KAHRAMAN_ÇİZİMLERİ = {
    "Savaşçı": """<svg width="100%" height="220" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet"><circle cx="50" cy="50" r="40" fill="url(#warriorGlow)" opacity="0.3"/><defs><radialGradient id="warriorGlow" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#ffaa00" /><stop offset="100%" stop-color="#000" stop-opacity="0" /></radialGradient></defs><path d="M30 85 L40 45 L60 45 L70 85 Z" fill="#4e5d6c" stroke="#7a8a9e" stroke-width="2"/><path d="M42 45 L50 85 L58 45 Z" fill="#3a4652"/><circle cx="35" cy="48" r="7" fill="#6c7a89" stroke="#ffaa00" stroke-width="1.5"/><circle cx="65" cy="48" r="7" fill="#6c7a89" stroke="#ffaa00" stroke-width="1.5"/><path d="M50 53 L55 60 L50 67 L45 60 Z" fill="#ffaa00"/><circle cx="50" cy="28" r="11" fill="#7a8a9e" stroke="#222" stroke-width="2"/><path d="M45 28 L55 28 L53 37 L47 37 Z" fill="#2c3e50"/><path d="M50 12 L52 20 L48 20 Z" fill="#e74c3c"/><path d="M22 25 L25 22 L50 45 L47 48 Z" fill="#d1d5db" stroke="#374151"/><path d="M20 20 L24 24" stroke="#ffaa00" stroke-width="3"/></svg>""",
    "Okçu": """<svg width="100%" height="220" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet"><circle cx="50" cy="50" r="40" fill="url(#archerGlow)" opacity="0.3"/><defs><radialGradient id="archerGlow" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#28a745" /><stop offset="100%" stop-color="#000" stop-opacity="0" /></radialGradient></defs><path d="M25 85 C30 40, 70 40, 75 85 Z" fill="#143d22" stroke="#28a745" stroke-width="2"/><path d="M42 35 C42 20, 58 20, 58 35 Z" fill="#2d3748"/><path d="M40 25 L50 12 L60 25 Z" fill="#1b4d3e"/><circle cx="46" cy="26" r="1.5" fill="#2ecc71"/><circle cx="54" cy="26" r="1.5" fill="#2ecc71"/><path d="M72 20 C85 45, 85 55, 72 80" fill="none" stroke="#d4af37" stroke-width="3"/><line x1="72" y1="20" x2="72" y2="80" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="2,2"/></svg>""",
    "Büyücü": """<svg width="100%" height="220" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet"><circle cx="50" cy="50" r="40" fill="url(#mageGlow)" opacity="0.4"/><defs><radialGradient id="mageGlow" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#9b51e0" /><stop offset="100%" stop-color="#000" stop-opacity="0" /></radialGradient></defs><path d="M30 85 L45 38 L55 38 L70 85 Z" fill="#3b1d5c" stroke="#9b51e0" stroke-width="2"/><path d="M44 35 L56 35 L50 55 Z" fill="#e2e8f0"/><circle cx="50" cy="30" r="8" fill="#fbd38d"/><path d="M38 25 L50 5 L62 25 Z" fill="#2d144d" stroke="#9b51e0"/><line x1="28" y1="90" x2="28" y2="25" stroke="#718096" stroke-width="3"/><circle cx="28" cy="20" r="6" fill="#00ffff" opacity="0.8"/><circle cx="28" cy="20" r="2" fill="#fff"/></svg>"""
}

# --- CANAVAR SVG ÇİZİMLERİ ---
CANAVAR_ÇİZİMLERİ = {
    "Vahşi Kurt": """<svg width="100%" height="200" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="#3a1c1c"/><path d="M30 60 L45 35 L60 45 L75 35 L80 60 Z" fill="#7f8c8d"/><circle cx="45" cy="45" r="3" fill="#ff0000"/><circle cx="65" cy="45" r="3" fill="#ff0000"/><path d="M48 55 L52 55 L50 60 Z" fill="#000"/></svg>""",
    "Yaban Domuzu": """<svg width="100%" height="200" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="#2c1e14"/><path d="M25 65 Q50 30 75 65 Z" fill="#5d4037"/><circle cx="40" cy="50" r="4" fill="#e74c3c"/><path d="M35 60 L30 70 L40 65 Z" fill="#fff"/><path d="M65 60 L70 70 L60 65 Z" fill="#fff"/></svg>""",
    "Goblin Savaşçısı": """<svg width="100%" height="200" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="#1b381e"/><circle cx="50" cy="40" r="20" fill="#27ae60"/><circle cx="43" cy="38" r="3" fill="#f1c40f"/><circle cx="57" cy="38" r="3" fill="#f1c40f"/><path d="M20 30 L35 40 L25 45 Z" fill="#27ae60"/></svg>""",
    "Kaya Golemi": """<svg width="100%" height="200" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="#2c3e50"/><rect x="30" y="30" width="40" height="40" fill="#7f8c8d" rx="5"/><circle cx="42" cy="42" r="4" fill="#00ffff"/><circle cx="58" cy="42" r="4" fill="#00ffff"/></svg>""",
    "Zindan Muhafızı": """<svg width="100%" height="200" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="#1a1a2e"/><path d="M30 30 L70 30 L60 80 L40 80 Z" fill="#16213e" stroke="#e94560" stroke-width="2"/><circle cx="45" cy="45" r="3" fill="#e94560"/><circle cx="55" cy="45" r="3" fill="#e94560"/></svg>""",
    "Kadim Ejderha Ignis": """<svg width="100%" height="200" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="url(#dragGlow)"/><defs><radialGradient id="dragGlow"><stop offset="0%" stop-color="#ff4500"/><stop offset="100%" stop-color="#000" stop-opacity="0"/></radialGradient></defs><path d="M20 70 Q50 10 80 70 Z" fill="#900c3f"/><circle cx="40" cy="40" r="4" fill="#ff4d4d"/><circle cx="60" cy="40" r="4" fill="#ff4d4d"/></svg>"""
}

# --- GELİŞMİŞ CUSTOM CSS (HEROES OF MIGHT AND MAGIC 2 STİLİ) ---
st.markdown("""
<style>
/* Medieval Font İçe Aktarımı */
@import url('https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap');

/* Tüm sayfa geneline fontu ve koyu arka planı uygula */
html, body, [class*="css"] {
    font-family: 'MedievalSharp', cursive !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #1a1612;
    background-image: radial-gradient(#2d241c 1px, transparent 1px);
    background-size: 20px 20px;
    color: #e6c280;
}

[data-testid="stSidebar"] {
    background-color: #120e0a;
    border-right: 3px solid #8b6508;
}

.ana-baslik {
    text-align: center;
    color: #ffd700;
    text-shadow: 2px 2px 4px #000;
    font-weight: 900;
    font-size: 3.5em;
    margin-bottom: 0;
    padding-bottom: 0;
    border-bottom: 2px solid #8b6508;
    display: inline-block;
    width: 100%;
}
.alt-baslik {
    text-align: center;
    color: #a0522d;
    font-size: 1.2em;
    margin-bottom: 30px;
    text-shadow: 1px 1px 0px #000;
}

/* HoMM Tarzı Kartlar */
.rpg-kart {
    background: linear-gradient(180deg, #2a1f18 0%, #1a120c 100%);
    border: 3px outset #8b6508;
    padding: 15px;
    text-align: center;
    box-shadow: 4px 4px 0px #000;
    color: #e6c280;
}

.rpg-kart-canavar {
    background: linear-gradient(180deg, #3d1414 0%, #1a0808 100%);
    border: 3px outset #8b0000;
    padding: 15px;
    text-align: center;
    box-shadow: 4px 4px 0px #000;
}

/* Aksiyon Kutuları (Taş Pano) */
.aksiyon-kutusu {
    background-color: #1c1c1c;
    border: 3px inset #4a4a4a;
    padding: 20px;
    text-align: center;
    min-height: 180px;
    box-shadow: 2px 2px 0px #000;
}

/* Savaş Kayıt Kutusu */
.savas-log {
    background-color: #110d0a;
    border: 2px inset #8b6508;
    padding: 10px;
    max-height: 150px;
    overflow-y: auto;
    font-size: 14px;
    line-height: 1.4;
}

/* Streamlit Butonlarını HoMM2 Stiline Çevirme */
div.stButton > button {
    background: linear-gradient(180deg, #5c4033 0%, #3e2723 100%);
    border: 2px outset #b8860b !important;
    color: #f5deb3 !important;
    font-family: 'MedievalSharp', cursive !important;
    font-size: 16px !important;
    text-shadow: 1px 1px 0px black;
    box-shadow: 3px 3px 0px #000;
    border-radius: 0px !important;
    transition: all 0.1s;
    width: 100%;
}

div.stButton > button:hover {
    border: 2px inset #ffd700 !important;
    background: linear-gradient(180deg, #6b4c3a 0%, #4e342e 100%);
    color: #fff !important;
    transform: translateY(2px) translateX(2px);
    box-shadow: 1px 1px 0px #000;
}

div.stButton > button:active {
    border: 2px inset #ff4b4b !important;
}

/* Ambar Kaynak Kutuları */
.kaynak-grid {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    margin-top: 10px;
    margin-bottom: 20px;
}
.kaynak-kutu {
    background: #110d0a;
    border: 2px inset #5c4033;
    padding: 10px 5px;
    text-align: center;
    flex: 1;
    font-weight: bold;
    font-size: 16px;
    box-shadow: 2px 2px 0px #000;
    cursor: help;
}
.k-altin { color: #ffd700; text-shadow: 1px 1px 0px #000;}
.k-odun { color: #d2b48c; text-shadow: 1px 1px 0px #000;}
.k-demir { color: #c0c0c0; text-shadow: 1px 1px 0px #000;}

/* Envanter Eşya Kartı */
.esya-kart {
    background-color: #2a1f18;
    border: 2px solid #8b6508;
    border-left: 8px solid #b8860b;
    padding: 12px;
    margin-bottom: 10px;
    box-shadow: 3px 3px 0px #000;
}

/* Girdiler (Text ve Selectbox) */
div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
    background-color: #1a120c !important;
    border: 2px inset #8b6508 !important;
    border-radius: 0px !important;
    color: #e6c280 !important;
}

/* Streamlit Tab (Sekme) Stilleri */
button[data-baseweb="tab"] {
    background-color: #1a120c !important;
    border: 2px outset #8b6508 !important;
    border-bottom: none !important;
    color: #8b6508 !important;
    font-family: 'MedievalSharp', cursive !important;
    margin-right: 4px;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #2a1f18 !important;
    color: #ffd700 !important;
    border-color: #ffd700 !important;
}
</style>
""", unsafe_allow_html=True)

# --- 1. OTURUM HAFIZASI ---
if "oyun_basladi" not in st.session_state:
    st.session_state.oyun_basladi = False
    st.session_state.isim = ""
    st.session_state.sinif = ""
    st.session_state.seviye = 1
    st.session_state.deneyim = 0
    st.session_state.altin = 200
    st.session_state.max_hp = 100
    st.session_state.hp = 100
    st.session_state.guc = 10
    st.session_state.ceviklik = 10
    st.session_state.iksir = 3
    st.session_state.odun = 30
    st.session_state.demir = 15
    st.session_state.kereste_seviye = 0
    st.session_state.maden_seviye = 0
    
    st.session_state.kusandigi_silah = "Paslı Kılıç"
    st.session_state.kusandigi_zirh = "Eski Giysi"
    st.session_state.silah_bonusu = 0
    st.session_state.zirh_bonusu = 0
    st.session_state.envanter = []
    
    st.session_state.secilen_bolge = "Karanlık Orman"
    st.session_state.aktif_olay = None
    st.session_state.dusman_adi = ""
    st.session_state.dusman_hp = 0
    st.session_state.dusman_max_hp = 0
    st.session_state.dusman_guc = 0
    st.session_state.savas_loglari = []
    st.session_state.aksiyon_efekti = "⚔️ Hatlar Kuruluyor, Savaşa Hazırlan!"
    
    st.session_state.son_kazanilan_xp = 0
    st.session_state.son_kazanilan_altin = 0
    st.session_state.son_kazanilan_odun = 0
    st.session_state.son_kazanilan_demir = 0
    st.session_state.seviye_atlama_mujdesi = False
    st.session_state.sandik_mesaji = ""

def pasif_uretim():
    if st.session_state.kereste_seviye > 0:
        st.session_state.odun += st.session_state.kereste_seviye * 3
    if st.session_state.maden_seviye > 0:
        st.session_state.demir += st.session_state.maden_seviye * 2

if st.session_state.oyun_basladi:
    pasif_uretim()

def bar_ciz(mevcut, maksimum, tip="hp"):
    oran = max(0.0, min(1.0, mevcut / maksimum))
    yuzde = int(oran * 100)
    
    if tip == "hp":
        renk1 = "#8b0000"
        renk2 = "#ff0000"
        yazi = f"❤️ {int(mevcut)}/{maksimum} HP"
    else: 
        renk1 = "#006400"
        renk2 = "#32cd32"
        yazi = f"✨ {int(mevcut)}/{maksimum} XP"

    st.markdown(f"""
    <div style='background-color:#110d0a; border-radius:0px; width:100%; height:24px; margin-bottom:12px; border:2px inset #8b6508; position: relative; box-shadow: 2px 2px 0px #000;'>
        <div style='background: linear-gradient(90deg, {renk1} 0%, {renk2} 100%); width:{yuzde}%; height:100%; border-right: 2px solid #000; transition: width 0.3s ease;'></div>
        <div style='position: absolute; top: 0; left: 0; width: 100%; height: 100%; text-align: center; color: white; font-weight: bold; font-size: 13px; line-height: 20px; text-shadow: 1px 1px 0px #000; white-space: nowrap; pointer-events: none; z-index: 2;'>
            {yazi}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. GİRİŞ EKRANI ---
if not st.session_state.oyun_basladi:
    st.markdown("<h1 class='ana-baslik'>KRALLIK SAVAŞLARI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='alt-baslik'>Miras ve Büyü Çağı</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div class='rpg-kart'>", unsafe_allow_html=True)
        isim_girdisi = st.text_input("Kahramanın Adı:", "Tince")
        sinif_girdisi = st.selectbox("Sınıfın (Kaderin):", ["Savaşçı", "Okçu", "Büyücü"])
        st.write("")
        if st.button("Macerayı Başlat! 🔥", use_container_width=True):
            st.session_state.isim = isim_girdisi
            st.session_state.sinif = sinif_girdisi
            st.session_state.oyun_basladi = True
            
            if sinif_girdisi == "Savaşçı":
                st.session_state.max_hp = 160; st.session_state.hp = 160; st.session_state.guc = 20; st.session_state.ceviklik = 8
                st.session_state.kusandigi_silah = "Paslı Kılıç"
            elif sinif_girdisi == "Okçu":
                st.session_state.max_hp = 115; st.session_state.hp = 115; st.session_state.guc = 14; st.session_state.ceviklik = 22
                st.session_state.kusandigi_silah = "Yıpranmış Yay"
            elif sinif_girdisi == "Büyücü":
                st.session_state.max_hp = 100; st.session_state.hp = 100; st.session_state.guc = 18; st.session_state.ceviklik = 10
                st.session_state.kusandigi_silah = "Eski Asa"
                
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- 3. ANA OYUN ---
else:
    toplam_guc = st.session_state.guc + st.session_state.silah_bonusu

    # YAN PANEL (SIDEBAR)
    with st.sidebar:
        st.markdown(f"<div class='rpg-kart'>{KAHRAMAN_ÇİZİMLERİ[st.session_state.sinif]}<h2 style='margin:10px 0 0 0; color:#ffd700; text-shadow: 2px 2px #000;'>{st.session_state.isim}</h2><p style='margin:5px 0; color:#c0c0c0;'>Seviye {st.session_state.seviye} {st.session_state.sinif}</p></div>", unsafe_allow_html=True)
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
        st.markdown("<h3 style='color:#ffd700; text-shadow: 1px 1px #000;'>👑 Ambar</h3>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='kaynak-grid'>
            <div class='kaynak-kutu k-altin' title='Savaşlardan galip ayrılarak veya keşiflerde gizli sandıkları bularak elde edilir.'>🪙<br>{st.session_state.altin}</div>
            <div class='kaynak-kutu k-odun' title='Savaş ganimeti olarak düşer veya Sığınaktaki Kereste Kampı tarafından her tur üretilir.'>🪵<br>{st.session_state.odun}</div>
            <div class='kaynak-kutu k-demir' title='Güçlü canavarları yenerek kazanılır veya Demir Madeni geliştirilerek üretilir.'>⛓️<br>{st.session_state.demir}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Karakteri Sıfırla", use_container_width=True):
            st.session_state.clear(); st.rerun()

    # ANA EKRAN BAŞLIĞI
    st.markdown("<h2 style='text-align:center; color:#e6c280; margin-bottom:20px; border-bottom: 2px solid #8b6508;'>Diyara Hoş Geldin</h2>", unsafe_allow_html=True)
    
    # SEKMELER
    tab_kesif, tab_envanter, tab_kasaba, tab_siginak = st.tabs(["⚔️ Macera", "🎒 Çanta", "🏘️ Pazar", "🏕️ Sığınak"])

    # --- TAB 1: SAVAŞ VE KEŞİF ---
    with tab_kesif:
        if st.session_state.aktif_olay is None:
            
            if st.session_state.son_kazanilan_xp > 0:
                st.markdown(f"""
                <div class='rpg-kart' style='margin-bottom: 20px; border-color: #28a745;'>
                    <h3 style='color: #32cd32; margin-top:0;'>🏆 ZAFER RAPORU</h3>
                    <div style='display:flex; justify-content:space-around; font-size:18px;'>
                        <span>✨ +{st.session_state.son_kazanilan_xp} XP</span>
                        <span>🪙 +{st.session_state.son_kazanilan_altin} Altın</span>
                        <span>🪵 +{st.session_state.son_kazanilan_odun} Odun</span>
                        <span>⛓️ +{st.session_state.son_kazanilan_demir} Demir</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.session_state.seviye_atlama_mujdesi:
                    st.toast(f"🚀 Seviye {st.session_state.seviye} oldun! İstatistiklerin arttı.", icon="🔥")
                    st.session_state.seviye_atlama_mujdesi = False
                
                if st.button("Raporu Parşömene Sar 📝", use_container_width=True):
                    st.session_state.son_kazanilan_xp = 0; st.rerun()

            st.markdown("<h3 style='color:#ffd700;'>🗺️ Hedef Seçimi</h3>", unsafe_allow_html=True)
            st.session_state.secilen_bolge = st.radio(
                "Keşfetmek İstediğin Bölgeyi Seç:",
                ["Karanlık Orman (Seviye 1-2)", "Eski Maden Ocakları (Seviye 3-4)", "Kadim Ejderha İni (Seviye 5+)"],
                horizontal=True
            )
            st.write("")
            
            if st.button("Bölgeye Adım At", use_container_width=True, type="primary"):
                if "Maden" in st.session_state.secilen_bolge and st.session_state.seviye < 3:
                    st.error("🔒 Maden ocaklarına girebilmek için en az 3. seviye olmalısın!")
                elif "Ejderha" in st.session_state.secilen_bolge and st.session_state.seviye < 5:
                    st.error("🔒 Ejderha İni çok tehlikeli! En az 5. seviye olmalısın!")
                else:
                    if random.random() < 0.25:
                        st.session_state.aktif_olay = "sandik"; st.session_state.sandik_mesaji = ""
                    else:
                        st.session_state.aktif_olay = "savas"
                        if "Orman" in st.session_state.secilen_bolge:
                            dusmanlar = [{"ad": "Vahşi Kurt", "hp": 45, "guc": 8, "xp": 40, "altin": 25, "odun_odul": 8, "demir_odul": 0}, {"ad": "Yaban Domuzu", "hp": 55, "guc": 11, "xp": 50, "altin": 35, "odun_odul": 12, "demir_odul": 0}]
                        elif "Maden" in st.session_state.secilen_bolge:
                            dusmanlar = [{"ad": "Goblin Savaşçısı", "hp": 85, "guc": 15, "xp": 75, "altin": 60, "odun_odul": 5, "demir_odul": 12}, {"ad": "Kaya Golemi", "hp": 115, "guc": 19, "xp": 95, "altin": 80, "odun_odul": 0, "demir_odul": 20}]
                        else:
                            dusmanlar = [{"ad": "Zindan Muhafızı", "hp": 145, "guc": 23, "xp": 150, "altin": 120, "odun_odul": 10, "demir_odul": 22}, {"ad": "Kadim Ejderha Ignis", "hp": 360, "guc": 30, "xp": 1000, "altin": 500, "odun_odul": 50, "demir_odul": 50}]
                        
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
            st.markdown("<div class='aksiyon-kutusu' style='border-color:#ffd700;'><h2 style='color:#ffd700; text-shadow: 2px 2px #000;'>🔒 Ganimet Sandığı Belirdi!</h2></div>", unsafe_allow_html=True)
            st.write("")
            if st.session_state.sandik_mesaji == "":
                if st.button("Sandığı Aç", use_container_width=True, type="primary"):
                    şans = random.random()
                    if şans < 0.6:
                        altin_odul = random.randint(70, 150)
                        st.session_state.altin += altin_odul
                        st.session_state.sandik_mesaji = f"💰 Sandıktan tam **{altin_odul} Altın** çıktı!"
                    else:
                        esya_turu = random.choice(["silah", "zırh"])
                        if esya_turu == "silah":
                            bonus = random.randint(12, 22)
                            yeni_silah = {"ad": f"Zindan İşi Barbar Baltası (+{bonus})", "tip": "silah", "özellik": f"+{bonus} Güç", "değer": bonus}
                            st.session_state.envanter.append(yeni_silah)
                            st.session_state.sandik_mesaji = f"⚔️ Sandıktan nadir bir **{yeni_silah['ad']}** çıktı! Çantana eklendi."
                        else:
                            bonus = random.randint(25, 45)
                            yeni_zirh = {"ad": f"Kadim Muhafız Göğüslüğü (+{bonus})", "tip": "zırh", "özellik": f"+{bonus} Defans", "değer": bonus}
                            st.session_state.envanter.append(yeni_zirh)
                            st.session_state.sandik_mesaji = f"🛡️ Sandıktan asil bir **{yeni_zirh['ad']}** çıktı! Çantana eklendi."
                    st.rerun()
            else:
                st.success(st.session_state.sandik_mesaji)
                if st.button("Devam Et", use_container_width=True):
                    st.session_state.aktif_olay = None; st.session_state.sandik_mesaji = ""; st.rerun()

        # --- SAVAŞ ARENASI ---
        elif st.session_state.aktif_olay == "savas":
            kart_sol, kart_orta, kart_sag = st.columns([2, 3, 2])
            
            with kart_sol:
                st.markdown(f"<div class='rpg-kart'>{KAHRAMAN_ÇİZİMLERİ[st.session_state.sinif]}<h3 style='color:#ffd700; margin:10px 0 0 0;'>{st.session_state.isim}</h3></div>", unsafe_allow_html=True)
                st.write(""); bar_ciz(st.session_state.hp, st.session_state.max_hp, "hp")
                
            with kart_orta:
                st.markdown(f"<div class='aksiyon-kutusu'><h4 style='color: #c0c0c0; margin-top:0;'>MUHAREBE AKIŞI</h4><hr style='border-color: #4a4a4a;'><h2 style='color: #ff4b4b; text-shadow: 2px 2px #000; margin-top:20px;'>{st.session_state.aksiyon_efekti}</h2></div>", unsafe_allow_html=True)
                st.write("")
                b_col1, b_col2 = st.columns(2)
                with b_col1:
                    if st.button("Saldır", use_container_width=True, type="primary"):
                        kritik = random.randint(1, 100) <= (st.session_state.ceviklik * 2)
                        hasar = toplam_guc + random.randint(-2, 4)
                        if kritik: hasar *= 2; st.session_state.savas_loglari.append(f"<span style='color:#ffd700;'>Kritik vuruş! Düşmana {hasar} hasar verdin!</span>")
                        else: st.session_state.savas_loglari.append(f"Düşmana {hasar} hasar verdin.")
                        st.session_state.dusman_hp -= hasar
                        
                        if st.session_state.dusman_hp <= 0:
                            if st.session_state.dusman_adi == "Kadim Ejderha Ignis":
                                st.balloons(); st.success("EJDERHA KATİLİ OLDUN! OYUNU KAZANDIN!"); st.session_state.clear(); st.stop()
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

                        d_hasar = max(1, st.session_state.dusman_guc - (st.session_state.zirh_bonusu // 2) + random.randint(-2, 2))
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
                st.markdown("<div style='color: #c0c0c0; border-bottom: 1px solid #4a4a4a; margin-bottom: 5px;'>Savaş Kayıtları</div>", unsafe_allow_html=True)
                log_html = "<div class='savas-log'>" + "<br>".join(reversed(st.session_state.savas_loglari)) + "</div>"
                st.markdown(log_html, unsafe_allow_html=True)
                
            with kart_sag:
                st.markdown(f"<div class='rpg-kart-canavar'>{CANAVAR_ÇİZİMLERİ.get(st.session_state.dusman_adi, '<div style=\"font-size:70px;\">👾</div>')}<h3 style='color:#ff4b4b; text-shadow: 2px 2px #000; margin:10px 0 0 0;'>{st.session_state.dusman_adi}</h3></div>", unsafe_allow_html=True)
                st.write(""); bar_ciz(st.session_state.dusman_hp, st.session_state.dusman_max_hp, "hp")

    # --- TAB 2: ENVANTER ---
    with tab_envanter:
        if not st.session_state.envanter:
            st.info("Çantan bomboş. Sığınakta üretim yapabilir veya ormanda sandık kovalayabilirsin.")
        else:
            for i, esya in enumerate(st.session_state.envanter):
                st.markdown(f"""
                <div class='esya-kart'>
                    <div>
                        <span style='font-size: 18px; font-weight: bold; color: #ffd700; text-shadow: 1px 1px #000;'>{esya['ad']}</span><br>
                        <span style='color: #c0c0c0; font-size: 14px;'>Tür: {esya['tip'].upper()} | Özellik: <span style='color:#32cd32;'>{esya['özellik']}</span></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Kuşan ({esya['ad']})", key=f"kus_{i}_{esya['ad']}"):
                    if esya["tip"] == "silah":
                        st.session_state.kusandigi_silah = esya["ad"]
                        st.session_state.silah_bonusu = esya["değer"]
                    elif esya["tip"] == "zırh":
                        st.session_state.kusandigi_zirh = esya["ad"]
                        st.session_state.zirh_bonusu = esya["değer"]
                    st.toast(f"{esya['ad']} başarıyla kuşanıldı!", icon="⚔️")
                    st.rerun()

    # --- TAB 3: PAZAR ---
    with tab_kasaba:
        colP1, colP2 = st.columns(2)
        with colP1:
            st.markdown("<div class='aksiyon-kutusu'><h3 style='color:#ffd700;'>Şifacı Dükkanı</h3><p style='color:#c0c0c0;'>Yaralarını sarmak için hayat suyu.</p></div>", unsafe_allow_html=True)
            st.write("")
            if st.button("Sağlık İksiri (25 Altın)", use_container_width=True):
                if st.session_state.altin >= 25: 
                    st.session_state.altin -= 25; st.session_state.iksir += 1; st.rerun()
                else:
                    st.error(f"Şifacı kafasını iki yana salladı. {25 - st.session_state.altin} Altın eksiğin var.")
                    
        with colP2:
            st.markdown("<div class='aksiyon-kutusu'><h3 style='color:#ffd700;'>Kasaba Hanı</h3><p style='color:#c0c0c0;'>Sıcak bir çorba ve güvenli bir yatak.</p></div>", unsafe_allow_html=True)
            st.write("")
            if st.button("Han'da Dinlen (20 Altın)", use_container_width=True):
                if st.session_state.altin >= 20: 
                    st.session_state.altin -= 20; st.session_state.hp = st.session_state.max_hp; st.rerun()
                else:
                    st.error(f"Hancı seni kapıdan çevirdi. Geceyi handa geçirmek için {20 - st.session_state.altin} Altın lazım.")

    # --- TAB 4: SIĞINAK VE CRAFTING ---
    with tab_siginak:
        b1, b2 = st.columns(2)
        with b1:
            st.markdown("<div class='esya-kart' style='border-color:#5c4033;'><h3 style='color:#d2b48c;'>Kereste Kampı</h3>Mevcut Seviye: <b style='color:#ffd700;'>{}</b></div>".format(st.session_state.kereste_seviye), unsafe_allow_html=True)
            maliyet = (st.session_state.kereste_seviye + 1) * 80
            if st.button(f"Kampı Büyüt ({maliyet} Altın)", use_container_width=True):
                if st.session_state.altin >= maliyet: 
                    st.session_state.altin -= maliyet; st.session_state.kereste_seviye += 1; st.rerun()
                else:
                    st.error(f"İşçiler grevde! Kampı büyütmek için {maliyet - st.session_state.altin} Altına daha ihtiyacın var.")
                    
        with b2:
            st.markdown("<div class='esya-kart' style='border-color:#4a4a4a;'><h3 style='color:#c0c0c0;'>Demir Madeni</h3>Mevcut Seviye: <b style='color:#ffd700;'>{}</b></div>".format(st.session_state.maden_seviye), unsafe_allow_html=True)
            maliyet_a = (st.session_state.maden_seviye + 1) * 100
            maliyet_o = (st.session_state.maden_seviye + 1) * 25
            if st.button(f"Madeni Derinleştir ({maliyet_a} A, {maliyet_o} O)", use_container_width=True):
                if st.session_state.altin >= maliyet_a and st.session_state.odun >= maliyet_o:
                    st.session_state.altin -= maliyet_a; st.session_state.odun -= maliyet_o; st.session_state.maden_seviye += 1; st.rerun()
                else:
                    e_altin = max(0, maliyet_a - st.session_state.altin)
                    e_odun = max(0, maliyet_o - st.session_state.odun)
                    st.error(f"Yetersiz Kaynak! Kazmayı vurmak için {e_altin} Altın ve {e_odun} Odun eksiğin var.")
                    
        st.divider()
        st.markdown("<h3 style='text-align:center; color:#ffd700;'>Demirci Örsü</h3>", unsafe_allow_html=True)
        cr1, cr2 = st.columns(2)
        with cr1:
            if st.button("Çelik Kılıç Döv (40 Odun, 25 Demir)", use_container_width=True):
                if st.session_state.odun >= 40 and st.session_state.demir >= 25:
                    st.session_state.odun -= 40; st.session_state.demir -= 25
                    st.session_state.envanter.append({"ad": f"Dövme Çelik Kılıç V{random.randint(1,9)}", "tip": "silah", "özellik": "+15 Güç", "değer": 15})
                    st.toast("Kılıç başarıyla dövüldü ve çantana eklendi!", icon="⚔️"); st.rerun()
                else:
                    e_odun = max(0, 40 - st.session_state.odun)
                    e_demir = max(0, 25 - st.session_state.demir)
                    st.error(f"Örs soğudu! Çelik Kılıç için {e_odun} Odun ve {e_demir} Demir eksik.")
                    
        with cr2:
            if st.button("Şövalye Plakası Döv (20 Odun, 50 Demir)", use_container_width=True):
                if st.session_state.odun >= 20 and st.session_state.demir >= 50:
                    st.session_state.odun -= 20; st.session_state.demir -= 50
                    st.session_state.envanter.append({"ad": f"Ağır Demir Göğüslük V{random.randint(1,9)}", "tip": "zırh", "özellik": "+30 Defans", "değer": 30})
                    st.toast("Zırh başarıyla dövüldü ve çantana eklendi!", icon="🛡️"); st.rerun()
                else:
                    e_odun = max(0, 20 - st.session_state.odun)
                    e_demir = max(0, 50 - st.session_state.demir)
                    st.error(f"Ateş yetersiz! Göğüslük için {e_odun} Odun ve {e_demir} Demir eksik.")