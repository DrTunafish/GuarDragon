import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

# .env dosyasından token'ı yükle
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot ayarları
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
intents.guilds = True
intents.guild_messages = True
intents.guild_reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Veri yapısı
class LevelSystem:
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data.json'
        self.data = self.load_data()
        
        # Alan ve ders yapılandırması
        self.areas = {
            'Eclectic': {
                'emoji': '⚡',
                'lessons': ['History of Magic', 'Arithmancy', 'Ancient Studies', 'Simya']
            },
            'Defender': {
                'emoji': '🛡️',
                'lessons': ['Charms', 'KSKS', 'Ancient Runes', 'Muggle Bilimi']
            },
            'CareTaker': {
                'emoji': '🌿',
                'lessons': ['Herbology', 'COMC', 'Transfiguration', 'Potions']
            },
            'SoulMaster': {
                'emoji': '🔮',
                'lessons': ['Dark Arts', 'Mythology', 'Astronomy', 'Divination']
            }
        }
        
        self.upper_areas = {
            'Eclectic': ['Alchemist', 'Oracle', 'Inventor', 'Pagan'],
            'Defender': ['Duelist', 'Curse Breaker', 'Enchanter/ess', 'Charm Specialist'],
            'CareTaker': ['Healer', 'Magizoologist', 'Herbologist', 'Potineer', 'Transfiguration Master'],
            'SoulMaster': ['Necromancer', 'Necrozoologist', 'Dark Mage', 'Ritualist']
        }
        
        # Bağımsız dersler
        self.independent_lessons = ['Asa Bilimi']
        
        # Alan ödülleri
        self.area_rewards = {
            'Defender': {
                '1': 'Probity Probe (+d10 perception)',
                '2': 'Durability Prof. Bonus',
                '3': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '4': 'Accio Mastery',
                '5': '+d6 Charm',
                '6': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '7': 'Depulso Mastery',
                '8': 'Descendo Mastery',
                '9': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '10': 'Wiggentree Kevlar',
                '11': '+d6 Charm',
                '12': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '13': 'Çok Amaçlı Oda (Genişleme)',
                '14': '+d6 Charm',
                '15': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '16': '+d6 Charm',
                '17': 'Bombarda Mastery',
                '18': 'Protego Mastery',
                '19': 'Durs Mastery',
                '20': 'Alanla ilgili kişisel Kırılmaz Tılsım yapma'
            },
            'Eclectic': {
                '1': 'Intelligence Prof. Bonus',
                '2': 'Archivist Spectacles',
                '3': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '4': 'Wisdom Prof. Bonus',
                '5': '+d6 Stealth',
                '6': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '7': 'Scroll Case of Holding',
                '8': 'Quill of names',
                '9': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '10': 'Düşünseli',
                '11': '+d6 Arcana',
                '12': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '13': 'Çok Amaçlı Oda (Genişleme)',
                '14': 'Phantom Steps',
                '15': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '16': 'Mask of Memories',
                '17': 'Hand of Glory',
                '18': 'Zümrüt Tablet',
                '19': 'Bell Jar Of Time',
                '20': 'Alanla ilgili kişisel Kırılmaz Tılsım yapma'
            },
            'CareTaker': {
                '1': 'Constitution Prof. Bonus',
                '2': 'Brewing prof. bonus',
                '3': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '4': 'Diffindo Mastery',
                '5': '+d6 Element',
                '6': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '7': 'Incendio Mastery',
                '8': 'Glacius Mastery',
                '9': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '10': 'Altın Pusula',
                '11': 'Confringo Mastery',
                '12': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '13': 'Çok Amaçlı Oda (Genişleme)',
                '14': 'Intelligence Prof. Bonus',
                '15': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '16': 'Wisdom Prof. Bonus',
                '17': 'Transformation Mastery',
                '18': 'Oppugno Mastery',
                '19': 'Çoklu Transformation Mastery',
                '20': 'Alanla ilgili kişisel Kırılmaz Tılsım yapma'
            },
            'SoulMaster': {
                '1': 'Kristal Küre',
                '2': 'Intelligence Prof. bonus',
                '3': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '4': 'Expelliarmus Curse',
                '5': '+d6 Religion',
                '6': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '7': "Stupefy'ın Lanet Etkisi",
                '8': 'Zümrüt Teleskop',
                '9': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '10': 'Scrying Aynası',
                '11': 'Wisdom Prof. bonus',
                '12': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '13': 'Çok Amaçlı Oda (Genişleme)',
                '14': 'Ghostcatcher',
                '15': 'Antik Büyü Sayfası (Alanla ilgili - Kişiye göre değişir)',
                '16': 'Aresto Momentum Lanet Etkisi',
                '17': 'Çoklu Düşman Lanetleme',
                '18': 'Dark Magic Prof. bonus',
                '19': 'Red Magic Prof. bonus',
                '20': 'Alanla ilgili kişisel Kırılmaz Tılsım yapma'
            }
        }
        
        # Üst alan ödülleri
        self.upper_area_rewards = {
            'Duelist': {
                '1': 'Savunma Büyüleri +d6',
                '2': 'Saldırı Büyüleri +d6',
                '3': 'Savunma Büyüleri +d6',
                '4': 'Saldırı Büyüleri +d6',
                '5': 'KOMBO BONUSU',
                '6': 'Spell Resistance +10',
                '7': 'Spell Resistance +10',
                '8': 'Spell Resistance +10',
                '9': 'Durability Prof. Bonus',
                '10': 'BRACES OF THE SUN FURY',
                '11': 'Dexterity Prof. Bonus',
                '12': 'Savunma Büyüleri +d6',
                '13': 'Saldırı Büyüleri +d6',
                '14': 'Insight +d6',
                '15': 'STORM RIDER JACKET',
                '16': 'Strenght Prof. Bonus',
                '17': 'Spell Resistance +10',
                '18': 'Spell Resistance +10',
                '19': 'Insight +d6',
                '20': 'GLASSES OF DUELIST'
            },
            'Curse Breaker': {
                '1': 'Spell Resistance +5',
                '2': 'Arcana +d6',
                '3': 'Spell Resistance +5',
                '4': 'Stealth +d6',
                '5': 'Absorbations Glove',
                '6': 'Spell Resistance +5',
                '7': 'History +d6',
                '8': 'Sleight Of Hand +d6',
                '9': 'Intelligence Prof. Bonus',
                '10': "FANCY GRAVEROBBER'S DAGGER",
                '11': 'Wisdom Prof. Bonus',
                '12': 'Spell Resistance +5',
                '13': 'History +d6',
                '14': 'Arcana +d6',
                '15': "BRINEHEART'S FABORINE COAT",
                '16': 'Durability Prof. Bonus',
                '17': 'Insight +d6',
                '18': 'Stealth +d6',
                '19': 'Sleight Of Hand +d6',
                '20': 'SUIT OF GOLDEN SHADOW'
            },
            'Enchanter/ess': {
                '1': 'Arcana +d6',
                '2': 'Arcana +d6',
                '3': 'Arcana +d6',
                '4': 'Arcana +d6',
                '5': "STRANGE'S CAPE",
                '6': 'Mana +10',
                '7': 'Mana +10',
                '8': 'Mana +10',
                '9': 'Intelligence Prof. Bonus',
                '10': 'TIME TURNER',
                '11': 'Wisdom Prof. Bonus',
                '12': 'Will (Stat) +10',
                '13': 'Will (Stat) +10',
                '14': 'Will (Stat) +10',
                '15': 'BLOOD CRYSTALS',
                '16': 'Mana +10',
                '17': 'Mana +10',
                '18': 'Will (Stat) +10',
                '19': 'Will (Stat) +10',
                '20': 'PÜFÜR'
            },
            'Charm Specialist': {
                '1': 'Charm Büyüleri +d6',
                '2': 'Charm Büyüleri +d6',
                '3': 'Charm Büyüleri +d6',
                '4': 'Charm Büyüleri +d6',
                '5': 'Oz Pendants',
                '6': 'Arcana +d6',
                '7': 'Mana +5',
                '8': 'Arcana +d6',
                '9': 'Mana +5',
                '10': 'SANDS OF AVALON',
                '11': 'Non-Verbal Prof. Bonus',
                '12': 'Mana +5',
                '13': 'Arcana +d6',
                '14': 'Mana +5',
                '15': 'FORGET ME KNOT',
                '16': 'Wandless-Magic Prof. Bonus',
                '17': 'Mana +5',
                '18': 'Arcana +d6',
                '19': 'Mana +5',
                '20': 'CHROMATIC CHRONOMETER'
            },
            'Healer': {
                '1': 'Medicine +d6',
                '2': 'Medicine +d6',
                '3': 'Medicine +d6',
                '4': 'Medicine +d6',
                '5': 'Abracadabra Kabbalah Necklace',
                '6': 'Investigation +d6',
                '7': 'Insight +d6',
                '8': 'Focus +10',
                '9': 'Constitution Prof. Bonus',
                '10': 'RING OF REGENERATION',
                '11': 'Brewing Prof. Bonus',
                '12': 'Focus +10',
                '13': 'Investigation +d6',
                '14': 'Focus +10',
                '15': "HEALER'S Enchanted Pendant",
                '16': 'Insight +d6',
                '17': 'Focus +10',
                '18': 'Investigation +d6',
                '19': 'Constitution Prof. Bonus',
                '20': 'Asklepios'
            },
            'Magizoologist': {
                '1': 'Animal Handling +d6',
                '2': 'Comc +d6',
                '3': 'Animal Handling +d6',
                '4': 'Comc +d6',
                '5': 'EYE OF FLAME',
                '6': 'Nature +d6',
                '7': 'Insight +d6',
                '8': 'Survival +d6',
                '9': 'Durability Prof. Bonus',
                '10': 'EJDER GÖZÜ',
                '11': 'Decterity Prof. Bonus',
                '12': 'Comc +d6',
                '13': 'Animal Handling +d6',
                '14': 'Comc +d6',
                '15': "Shepherd's Instrument",
                '16': 'Survival +d6',
                '17': 'Nature +d6',
                '18': 'Animal Handling +d6',
                '19': 'Survival +d6',
                '20': 'Crown of the Primal Sovereign'
            },
            'Potineer': {
                '1': 'İksir +d6',
                '2': 'İksir +d6',
                '3': 'İksir +d6',
                '4': 'Brewing Prof. Bonus',
                '5': "POTIONEER'S LIFE SAVER",
                '6': 'İksir +d6',
                '7': 'Investigation +d6',
                '8': 'Nature +d6',
                '9': 'Investigation +d6',
                '10': 'SCARF OF POISONS',
                '11': 'Nature +d6',
                '12': 'Nature +d6',
                '13': 'Investigation +d6',
                '14': 'Constitution Prof. Bonus',
                '15': 'PATLAMA KARŞITI KAZAN',
                '16': 'Medicine +d4',
                '17': 'Medicine +d4',
                '18': 'Medicine +d4',
                '19': 'Intelligence Prof. Bonus',
                '20': 'Alkahest'
            },
            'Herbologist': {
                '1': 'Nature +d6',
                '2': 'Nature +d6',
                '3': 'Nature +d6',
                '4': 'Nature +d6',
                '5': 'Filizlenme Eldivenleri',
                '6': 'Survival +d6',
                '7': 'Medicine +d6',
                '8': 'Medicine +d6',
                '9': 'Constitution Prof. Bonus',
                '10': 'Crown of Ancient Branches',
                '11': 'Intelligence Prof. Bonus',
                '12': 'Survival +d6',
                '13': 'Medicine +d6',
                '14': 'Nature +d6',
                '15': "Yggdrasil's Pouch",
                '16': 'Wisdom Prof. Bonus',
                '17': 'Survival +d6',
                '18': 'Survival +d6',
                '19': 'Brewing Prof. Bonus',
                '20': 'Staff of the Eternal Garden'
            },
            'Transfiguration Master': {
                '1': 'Biçim Değiştirme Büyüsü +d4',
                '2': 'Biçim Değiştirme Büyüsü +d4',
                '3': 'Biçim Değiştirme Büyüsü +d4',
                '4': 'Biçim Değiştirme Büyüsü +d4',
                '5': 'Barkskin',
                '6': 'Arcana +d6',
                '7': 'Biçim Değiştirme Büyüsü +d4',
                '8': 'Biçim Değiştirme Büyüsü +d4',
                '9': 'Intelligence Prof. Bonus',
                '10': 'Figurine of Wondrous Power',
                '11': 'Arcana +d6',
                '12': 'Biçim Değiştirme Büyüsü +d4',
                '13': 'Biçim Değiştirme Büyüsü +d4',
                '14': 'Arcana +d6',
                '15': "Athanor'un Aynası (Mirror of the Transmuter)",
                '16': 'Arcana +d6',
                '17': 'Biçim Değiştirme Büyüsü +d4',
                '18': 'Arcana +d6',
                '19': 'Apparation Prof. Bonus',
                '20': 'Dopple Gänger Mastery'
            },
            'Alchemist': {
                '1': 'Simya +d6',
                '2': 'Simya +d6',
                '3': 'Simya +d6',
                '4': 'Simya +d6',
                '5': 'Scarf of Cleansing',
                '6': 'Brewing Prof. Bonus',
                '7': 'İksir +d6',
                '8': 'İksir +d6',
                '9': 'İksir +d6',
                '10': 'Athame',
                '11': 'Intelligence Prof. Bonus',
                '12': 'Nature +d6',
                '13': 'Nature +d6',
                '14': 'Arcana +d6',
                '15': 'HAND OF MIDAS',
                '16': 'Arcana +d6',
                '17': 'Focus +10',
                '18': 'Focus +10',
                '19': 'Focus +10',
                '20': 'Felsefe Taşı'
            },
            'Oracle': {
                '1': 'Kehanet +d6',
                '2': 'Kehanet +d6',
                '3': 'Kehanet +d6',
                '4': 'Foretelling Prof. Bonus',
                '5': 'Book of Hidden Paths',
                '6': 'Wisdom Prof. Bonus',
                '7': 'Kehanet +d6',
                '8': 'Focus +10',
                '9': 'Focus +10',
                '10': 'Nightward Candle',
                '11': 'Wandless Magic Prof. Bonus',
                '12': 'Focus +10',
                '13': 'Perception +d6',
                '14': 'Perception +d6',
                '15': 'skull-hookah',
                '16': 'Perception +d6',
                '17': 'Insight +d6',
                '18': 'Insight +d6',
                '19': 'Written Magic Prof. Bonus',
                '20': 'Duru Görü'
            },
            'Inventor': {
                '1': 'Tılsımcılık +d6',
                '2': 'Tılsımcılık +d6',
                '3': 'Tılsımcılık +d6',
                '4': 'Crafting Prof. Bonus',
                '5': 'Cober Page',
                '6': 'Intelligence Prof. Bonus',
                '7': 'Tılsımcılık +d6',
                '8': 'Arcana +d6',
                '9': 'Arcana +d6',
                '10': 'Magic Magnifier',
                '11': 'Investigation +d6',
                '12': 'Investigation +d6',
                '13': 'Tılsımcılık +d6',
                '14': 'Investigation +d6',
                '15': 'FIRE OF PROMETHEUS',
                '16': 'Arcana +d6',
                '17': 'Arcana +d6',
                '18': 'Investigation +d6',
                '19': 'Written Magic Prof. Bonus',
                '20': 'HAT OF SURPRISES'
            },
            'Pagan': {
                '1': 'Religion +d6',
                '2': 'Religion +d6',
                '3': 'Religion +d6',
                '4': 'Wisdom Prof. Bonus',
                '5': 'Görünmez Koruma Tebeşiri',
                '6': 'Religion +d6',
                '7': 'Insight +d6',
                '8': 'Insight +d6',
                '9': 'Intelligence Prof. Bonus',
                '10': 'AMULET OF GODS',
                '11': 'Arcana +d6',
                '12': 'Arcana +d6',
                '13': 'Ancient Studies +d6',
                '14': 'Ancient Studies +d6',
                '15': 'BRACELET OF EREBUS',
                '16': 'Tılsımcılık +d6',
                '17': 'Tılsımcılık +d6',
                '18': 'History +d6',
                '19': 'History +d6',
                '20': 'SHADE FAMILIAR'
            },
            'Necromancer': {
                '1': "Negatif Büyü Boost'u +d6",
                '2': "Negatif Büyü Boost'u +d6",
                '3': "Negatif Büyü Boost'u +d6",
                '4': 'Dark Magic Prof. Boost',
                '5': 'Speak With Dead Dust',
                '6': 'Constitution Prof. Boost',
                '7': "Negatif Büyü Boost'u +d6",
                '8': 'Arcana +d6',
                '9': 'Intelligence Prof. Boost',
                '10': 'Grave Guiders',
                '11': 'Wisdom Prof. Boost',
                '12': 'Medicine +d6',
                '13': 'Will +d10',
                '14': 'Medicine +d6',
                '15': 'Enchanted Candle',
                '16': 'Will +d10',
                '17': 'Medicine +d6',
                '18': 'Arcana +d6',
                '19': 'Red Magic Prof. Boost',
                '20': 'Life Death Control Amulet'
            },
            'Necrozoologist': {
                '1': 'Comc +d6',
                '2': 'Animal Handling +d6',
                '3': 'Comc +d6',
                '4': 'Dark Magic Prof. Boost',
                '5': 'Soul Armour',
                '6': 'Comc +d6',
                '7': 'Animal Handling +d6',
                '8': 'Comc +d6',
                '9': 'Intelligence Prof. Boost',
                '10': 'Phurba of the Severed Earth',
                '11': 'Animal Handling +d6',
                '12': 'Arcana +d6',
                '13': 'Animal Handling +d6',
                '14': "Negatif Büyü Boost'u +d6",
                '15': 'Aegis of the Baneful Dawn',
                '16': 'Will (Stat) +10',
                '17': 'Will (Stat) +10',
                '18': 'Will (Stat) +10',
                '19': 'Red Magic Prof. Boost',
                '20': 'Crown of the Dark Sovereign'
            },
            'Dark Mage': {
                '1': "Negatif Büyü Boost'u +d6",
                '2': "Negatif Büyü Boost'u +d6",
                '3': "Negatif Büyü Boost'u +d6",
                '4': 'Dark Magic Prof. Boost',
                '5': "Maui's Fish Hook",
                '6': "Negatif Büyü Boost'u +d6",
                '7': 'Arcana +d6',
                '8': 'Arcana +d6',
                '9': 'Intelligence Prof. Boost',
                '10': 'SHROUD OF DARKNESS',
                '11': 'Arcana +d6',
                '12': 'Arcana +d6',
                '13': 'Dark Magic Prof. Bonus',
                '14': 'Will +d10',
                '15': 'Umbra Ægis',
                '16': 'Will +d10',
                '17': 'Will +d10',
                '18': 'Intimidation +d6',
                '19': 'Red Magic Prof. Boost',
                '20': "Nekrah's Veil"
            },
            'Ritualist': {
                '1': 'Religion +d6',
                '2': 'Religion +d6',
                '3': 'Religion +d6',
                '4': 'Religion +d6',
                '5': 'Lamba Cini',
                '6': 'Arcana +d6',
                '7': 'Perception +d6',
                '8': 'Insight +d6',
                '9': 'Red Magic Prof. Boost',
                '10': 'Seal of Solomon',
                '11': 'Intelligence Prof. Bonus',
                '12': 'Focus +d10',
                '13': 'Focus +d10',
                '14': 'Focus +d10',
                '15': 'Familiar Statü',
                '16': 'Will (Stat) +10',
                '17': 'Will (Stat) +10',
                '18': 'Will (Stat) +10',
                '19': 'Red Magic Prof. Boost',
                '20': 'Invocation'
            }
        }
        
        # Ödül sistemi
        self.rewards = {
            # DEFENDER ALANI
            'Charms': {
                **{str(i): '+5 Sickle' for i in range(1, 50)},
                '50': "Champion's Charm Bracelet",
                **{str(i): '+10 Sickle' for i in range(51, 100)},
                '100': "Non-Verbal prof. bonus"
            },
            'KSKS': {
                **{str(i): '+5 Sickle' for i in range(1, 50)},
                '50': "Doomslayer's Gloves",
                **{str(i): '+10 Sickle' for i in range(51, 100)},
                '100': "Dexterity prof. bonus"
            },
            'Ancient Runes': {
                **{str(i): '+5 Sickle' for i in range(1, 50)},
                '50': 'Thurisaz–Isa–Hagalaz Bindrune',
                **{str(i): '+10 Sickle' for i in range(51, 100)},
                '100': 'Written Magic Prof. Bonus'
            },
            'Muggle Bilimi': {
                **{str(i): '+5 Sickle' for i in range(1, 50)},
                '50': 'Büyü gizleme tılsımı',
                **{str(i): '+10 Sickle' for i in range(51, 100)},
                '100': 'Crafting Proficiency Bonus'
            },
            
            # ECLECTIC ALANI
            'History of Magic': {
                **{str(i): '+5 Sickle' for i in range(1, 50)},
                '50': '+d4 History Bonus',
                **{str(i): '+10 Sickle' for i in range(51, 100)},
                '100': 'INT prof. Bonus'
            },
            'Arithmancy': {
                **{str(i): '+5 Sickle' for i in range(1, 50)},
                '50': 'Aritmansi Kağıdı',
                **{str(i): '+10 Sickle' for i in range(51, 100)},
                '100': 'WIS prof. Bonus'
            },
            'Ancient Studies': {
                **{str(i): '+5 Sickle' for i in range(1, 50)},
                '50': '+d4 Written Magic Bonus',
                **{str(i): '+10 Sickle' for i in range(51, 100)},
                '100': 'CRF prof bonus'
            },
            'Simya': {
                **{str(i): '+5 Sickle' for i in range(1, 50)},
                '50': "Master's Alchemical Kit",
                **{str(i): '+10 Sickle' for i in range(51, 100)},
                '100': 'Simya +d10'
            },
            
            # CARETAKER ALANI
            'Herbology': {
                **{str(i): '+5 Sickle' for i in range(1, 50)},
                '50': 'Taşınabilir Sera',
                **{str(i): '+10 Sickle' for i in range(51, 100)},
                '100': '+3d4 Nature bonus'
            },
            'COMC': {
                **{str(i): '+5 Sickle' for i in range(1, 50)},
                '50': 'Forest Vivarium',
                **{str(i): '+10 Sickle' for i in range(51, 100)},
                '100': 'Swamp Vivarium'
            },
            'Transfiguration': {
                **{str(i): '+5 Sickle' for i in range(1, 50)},
                '50': "Transmuter's Talisman",
                **{str(i): '+10 Sickle' for i in range(51, 100)},
                '100': 'Tüm TRNF büyülerine +d6'
            },
            'Potions': {
                **{str(i): '+5 Sickle' for i in range(1, 50)},
                '50': '1 şişe Felix Felicis (tek kullanımlık)',
                **{str(i): '+10 Sickle' for i in range(51, 100)},
                '100': 'BRW prof. bonus'
            },
            
            # SOULMASTER ALANI
            'Dark Arts': {
                **{str(i): '+5 Sickle' for i in range(1, 50)},
                '50': '+d6 Negatif Büyü Bonusu',
                **{str(i): '+10 Sickle' for i in range(51, 100)},
                '100': '+d6 Negatif Büyü Bonusu'
            },
            'Mythology': {
                **{str(i): '+5 Sickle' for i in range(1, 50)},
                '50': '+d6 Religion bonusu',
                **{str(i): '+10 Sickle' for i in range(51, 100)},
                '100': '+d6 Religion bonusu'
            },
            'Astronomy': {
                **{str(i): '+5 Sickle' for i in range(1, 50)},
                '50': '+d6 perception bonusu',
                **{str(i): '+10 Sickle' for i in range(51, 100)},
                '100': 'INT prof. bonus'
            },
            'Divination': {
                **{str(i): '+5 Sickle' for i in range(1, 50)},
                '50': '+d12 Kehanet bonusu',
                **{str(i): '+10 Sickle' for i in range(51, 100)},
                '100': 'FT prof. bonus'
            }
        }
        
    def load_data(self):
        """Veri dosyasını yükle veya yeni oluştur"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'users': {},
                'rewards': {},
                'subrewards': {}
            }
            
    def save_data(self):
        """Verileri kaydet"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
            
    def calculate_lesson_level(self, points, area=None):
        """Ders seviyesini hesaplar
        SoulMaster alanı için: 125 puan = 1 level (max 12500 puan = 100 level)
        Diğer alanlar için: 25 puan = 1 level (max 2500 puan = 100 level)"""
        if points == 0:
            return 0
            
        # SoulMaster alanı için özel hesaplama (daha yavaş level atlama)
        if area == 'SoulMaster':
            level = points // 125  # Her 125 puan = 1 level (max 12500 puan)
        else:
            # Diğer tüm alanlar ve bağımsız dersler için normal hesaplama
            level = points // 25  # Her 25 puan = 1 level (max 2500 puan)
            
        # Maksimum 100 level
        return min(level, 100)
        
    def calculate_upper_area_level(self, points, area=None):
        """Üst alan seviyesini hesapla"""
        if points < 10000:
            return 0
            
        # SoulMaster üst alanları için özel hesaplama
        if area == 'SoulMaster':
            return (points - 10000) // 10000 + 4
            
        # Diğer alanlar için normal hesaplama
        return (points - 10000) // 2500 + 4

# Level sistemini başlat
level_system = LevelSystem(bot)
bot.level_system = level_system

@bot.event
async def on_ready():
    """Bot hazır olduğunda çalışır"""
    print(f'{bot.user} olarak giriş yapıldı!')
    print('Veriler yüklendi!')
    
    # Komutları yükle
    await load_extensions()

# Komutları yükle
async def load_extensions():
    """Komut dosyalarını yükle"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"{filename} yüklendi!")
            except Exception as e:
                print(f"{filename} yüklenirken hata oluştu: {e}")

@bot.command(name='yardim')
async def yardim(ctx):
    """Komutlar hakkında bilgi verir"""
    commands_info = {
        'addpoints': 'Puan ekler (Moderator) (örn: !addpoints @kullanıcı History of Magic 100)',
        'checklevel': 'Seviye bilgisini gösterir (örn: !checklevel @kullanıcı)',
        'checkrewards': 'Ödülleri gösterir (örn: !checkrewards @kullanıcı)',
        'changearea': 'Ana alanı değiştirir (Moderator) (örn: !changearea @kullanıcı Eclectic)',
        'chooseupper': 'Üst alan seçer (örn: !chooseupper Eclectic Alchemist)'
    }
    
    embed = discord.Embed(
        title="Komut Listesi",
        description="Kullanılabilir komutlar:",
        color=discord.Color.blue()
    )
    
    for cmd, desc in commands_info.items():
        embed.add_field(name=f"!{cmd}", value=desc, inline=False)
        
    await ctx.send(embed=embed)

# Botu başlat
bot.run(TOKEN) 