# Roleplay Level Botu

Bu Discord botu, roleplay sunucuları için karakter levellerini ve ödüllerini takip eder.

## Özellikler

- Ders, alan ve üst alan seviye sistemi
- Otomatik ödül dağıtımı
- Alan kilidi ve tepki mekanizması
- Detaylı seviye ve ödül görüntüleme

## Kurulum

1. Python 3.8 veya üstü sürümü yükleyin
2. Gerekli paketleri yükleyin:
   ```
   pip install -r requirements.txt
   ```
3. `.env` dosyası oluşturun ve Discord token'ınızı ekleyin:
   ```
   DISCORD_TOKEN=your_token_here
   ```
4. Botu başlatın:
   ```
   python bot.py
   ```

## Komutlar

### Level Komutları

- `!addpoints @user <ders> <puan>`: Kullanıcıya puan ekler (Moderator)
- `!checklevel @user`: Kullanıcının seviyelerini gösterir
- `!changearea @user <alan>`: Ana alanı değiştirir (Moderator)
- `!chooseupper <alan> <üst_alan>`: Üst alan seçer

### Ödül Komutları

- `!setreward <ders> <seviye> <ödül>`: Ders için ödül tanımlar (Moderator)
- `!setsubreward <alan> <üst_alan> <seviye> <ödül>`: Üst alan için ödül tanımlar (Moderator)
- `!checkrewards @user`: Kullanıcının ödüllerini gösterir

### Yardım

- `!yardim`: Tüm komutların listesini gösterir

## Level Sistemi

### Ders Seviyeleri
- Her 25 puan = 1 level
- Maksimum 100 level

### Alan Seviyeleri
- En düşük ders seviyesi / 5
- Maksimum 20 level

### Üst Alan Seviyeleri
- 20. levele ulaşınca seçilebilir
- Başlangıç: 10.000 puan (4. level)
- Her 2.500 puan = 1 level

## Alanlar ve Dersler

### Eclectic
- History of Magic
- Arithmancy
- Ancient Studies
- Simya

### Defender
- Charms
- KSKS
- Ancient Runes
- Muggle Bilimi

### CareTaker
- Herbology
- COMC
- Transfiguration
- Potions

### Bağımsız Dersler
- Asa Bilimi

## Üst Alanlar

### Eclectic
- Alchemist
- Oracle
- Inventor
- Pagan

### Defender
- Duellist
- Curse Breaker
- Enchanter/ess
- Charms Specialist

### CareTaker
- Healer
- Magizoologist
- Wandmaker
- Potioneer
- Transfiguration Master
- Herbologist

## Gereksinimler

- discord.py==2.3.2
- python-dotenv==1.0.0 