from telethon import TelegramClient, events
from deep_translator import GoogleTranslator
import asyncio

# --- AYARLAR KISMI (BURAYI DOLDUR) ---

# 1. my.telegram.org sitesinden aldığın sayılar ve kodlar:
api_id = 36788592                   # Buraya kendi api_id'ni yaz
api_hash = 'd695460e880cc1703a305cc52c2b2e08' # Buraya api_hash'i tırnak içinde yaz

# 2. Konuştuğun kişinin kullanıcı adı (başında @ olmadan):
hedef_kisi = '@Marchen_E' 

# -------------------------------------
# 1. Python 3.14 Hatasını Çözen Yama:
# Döngüyü (Loop) manuel olarak oluşturup tanımlıyoruz.
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 2. Client'ı oluştururken bu döngüyü kullanmasını söylüyoruz
client = TelegramClient('benim_oturum', api_id, api_hash, loop=loop)

def koreceye_cevir(metin):
    try:
        return GoogleTranslator(source='tr', target='ko').translate(metin)
    except Exception as e:
        return f"Hata: {e}"

def turkceye_cevir(metin):
    try:
        return GoogleTranslator(source='ko', target='tr').translate(metin)
    except Exception as e:
        return f"Hata: {e}"

@client.on(events.NewMessage)
async def mesaj_yakalayici(event):
    sender = await event.get_sender()
    
    # SENARYO 1: KARŞI TARAFTAN MESAJ GELDİĞİNDE
    if event.is_private and sender and (sender.username == hedef_kisi or sender.id == hedef_kisi):
        orijinal_mesaj = event.raw_text
        if original_mesaj:
            cevirisi = turkceye_cevir(orijinal_mesaj)
            await client.send_message('me', 
                f"🇰🇷 **Koreli Arkadaş:** {cevirisi}\n"
                f"📝 *Orijinal:* {orijinal_mesaj}"
            )

    # SENARYO 2: SEN MESAJ ATTIĞINDA (.ko ile başlıyorsa)
    elif event.out and event.raw_text.startswith('.ko '):
        yazilacak_metin = event.raw_text[4:]
        await event.edit(f"{yazilacak_metin} (Çevriliyor...)")
        korece_hali = koreceye_cevir(yazilacak_metin)
        await event.edit(korece_hali)

# --- ANA ÇALIŞTIRMA BLOĞU ---
async def baslat():
    print("Bot başlatılıyor... Telefon onayı gerekebilir.")
    await client.start()
    print("--- SİSTEM AKTİF ---")
    print("1. Karşıdan mesaj gelince 'Kaydedilen Mesajlar'a çevirisi düşecek.")
    print("2. Sen cevap verirken '.ko Merhaba' yazarsan, otomatik Koreceye dönüşüp gidecek.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Python 3.14 uyumluluğu için döngüyü elle çalıştırıyoruz
    loop.run_until_complete(baslat())