from telethon import TelegramClient, events
from deep_translator import GoogleTranslator
import asyncio

# --- AYARLAR ---
api_id = 36788592                   # Buraya kendi api_id'ni yaz
api_hash = 'd695460e880cc1703a305cc52c2b2e08' # Buraya api_hash'i tırnak içinde yaz
# ---------------

# Python 3.14 Fix
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
client = TelegramClient('benim_oturum', api_id, api_hash, loop=loop)

def turkceye_cevir(metin):
    try:
        # Otomatik algıla ve Türkçeye çevir
        return GoogleTranslator(source='auto', target='tr').translate(metin)
    except:
        return None

def koreceye_cevir(metin):
    try:
        return GoogleTranslator(source='tr', target='ko').translate(metin)
    except Exception as e:
        return f"Hata: {e}"

# 1. GELEN MESAJLARI YAKALA (Gelen Kutusu)
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def gelen_mesajlar(event):
    sender = await event.get_sender()
    
    if event.raw_text:
        try:
            orijinal = event.raw_text
            cevirisi = turkceye_cevir(orijinal)
            
            # SPAM KORUMASI:
            # Sadece çeviri orijinalden farklıysa (yani mesaj yabancı dildeyse) gönder.
            if cevirisi and cevirisi.lower() != orijinal.lower():
                
                # --- İSİM ALMA KISMI ---
                if sender:
                    ad = sender.first_name if sender.first_name else ""
                    soyad = sender.last_name if sender.last_name else ""
                    # Ad ve soyadı birleştir, kenar boşluklarını temizle
                    tam_isim = f"{ad} {soyad}".strip()
                    
                    # Eğer isim yoksa (gizliyse vs.)
                    if not tam_isim:
                        tam_isim = "Bilinmeyen Kullanıcı"
                else:
                    tam_isim = "Gizli Gönderici"
                # -----------------------

                # Kaydedilen Mesajlar'a (Saved Messages) Rapor
                await client.send_message('me', 
                    f"👤 **Gönderen:** {tam_isim}\n"
                    f"🇹🇷 **Çeviri:** {cevirisi}\n"
                    f"─────────────────\n"
                    f"📝 `{orijinal}`"
                )
        except Exception:
            pass

# 2. GİDEN MESAJLARI YAKALA (.ko ile başlayanlar)
@client.on(events.NewMessage(outgoing=True))
async def giden_mesajlar(event):
    if event.raw_text.startswith('.ko '):
        yazilacak_metin = event.raw_text[4:]
        await event.edit(f"{yazilacak_metin} (Çevriliyor...)")
        korece_hali = koreceye_cevir(yazilacak_metin)
        await event.edit(korece_hali)

async def baslat():
    print("--- İSİM GÖSTEREN BOT AKTİF ---")
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    loop.run_until_complete(baslat())