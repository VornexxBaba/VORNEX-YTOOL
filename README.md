cat << 'EOF' > README.md
# ⚡ VORNEX-YTOOL – Telegram & Discord Multi-Tool

![Version](https://img.shields.io/badge/version-2.0-red)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Platform](https://img.shields.io/badge/platform-Termux%20%7C%20Linux%20%7C%20macOS%20%7C%20Windows-brightgreen)
![License](https://img.shields.io/badge/license-MIT-orange)

> **Vornex Gücü – Sistem sınırlarını aş, kontrolü eline al.**

Bu araç, Telegram ve Discord altyapılarını hedef alan, **anti-ban** önlemleri, **proxy desteği** ve **çoklu iş parçacığı (multi-threading)** ile çalışan gelişmiş bir test ve yönetim aracıdır.  
Menü tabanlı arayüzü sayesinde tüm ayarlar (thread sayısı, süre, anti-ban, proxy) kolayca yapılandırılabilir.

---

## 🔥 Özellikler

- 🎯 **Telegram & Discord Desteği** – Bot token veya webhook üzerinden işlem yeteneği.
- 🛡️ **Anti-Ban Sistemi** – 429/403 hız sınırı (rate-limit) durumlarında otomatik bekleme ve User-Agent rotasyonu.
- 🌐 **Proxy Desteği** – SOCKS5 ve HTTP proxy listeleri ile dinamik IP rotasyonu.
- ⚙️ **Ayarlanabilir Thread Sayısı** – Performansa göre 50–300 arası optimize edilebilir iş parçacığı kontrolü.
- ⏱️ **Süre Sınırı** – Özelleştirilebilir işlem süresi (saniye cinsinden).
- 🖥️ **Çapraz Platform** – Termux, Linux (Debian/Arch), macOS ve Windows tam uyumluluğu.
- 🎨 **Terminal Arayüzü** – Colorama destekli renkli durum göstergeleri.

---

## ⚠️ Yasal Uyarı

Bu araç yalnızca **güvenlik testleri, eğitim ve izinli sistem analizleri** için geliştirilmiştir. İzin alınmayan hedef sistemler üzerinde kullanılması yasal sorumluluk doğurabilir. Kullanıcı, aracın kullanımından doğan tüm hukuki sorumluluğu kabul etmiş sayılır.

---

## 📦 Gereksinimler

- Python 3.8 veya üzeri
- `pip` (Python Paket Yöneticisi)
- Aktif İnternet Bağlantısı

---

## 🚀 Tüm Platformlar İçin Kurulum (Tek Kod Bloğu)

```bash
# ----------------------------------------------------
# 1️⃣ TERMUX (ANDROID)
# ----------------------------------------------------
pkg update -y && pkg upgrade -y
pkg install -y python python-pip git
termux-setup-storage
pip install --upgrade pip
git clone https://github.com/VornexxBaba/VORNEX-YTOOL.git
cd VORNEX-YTOOL
pip install aiohttp colorama aiohttp-socks
python3 main.py

# ----------------------------------------------------
# 2️⃣ DEBIAN / UBUNTU LINUX
# ----------------------------------------------------
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip git
git clone https://github.com/VornexxBaba/VORNEX-YTOOL.git
cd VORNEX-YTOOL
pip3 install aiohttp colorama aiohttp-socks
python3 main.py

# ----------------------------------------------------
# 3️⃣ ARCH LINUX
# ----------------------------------------------------
sudo pacman -Syu
sudo pacman -S --needed python python-pip git
git clone https://github.com/VornexxBaba/VORNEX-YTOOL.git
cd VORNEX-YTOOL
pip install aiohttp colorama aiohttp-socks
python main.py

# ----------------------------------------------------
# 4️⃣ MACOS
# ----------------------------------------------------
brew update
brew install python git
git clone https://github.com/VornexxBaba/VORNEX-YTOOL.git
cd VORNEX-YTOOL
pip3 install aiohttp colorama aiohttp-socks
python3 main.py

# ----------------------------------------------------
# 5️⃣ WINDOWS (CMD / PowerShell)
# ----------------------------------------------------
git clone https://github.com/VornexxBaba/VORNEX-YTOOL.git
cd VORNEX-YTOOL
pip install aiohttp colorama aiohttp-socks
python main.py

VORNEX-YTOOL – Telegram &amp; Discord bot spam aracı | Anti-Ban, Proxy, Tek komut kurulum
