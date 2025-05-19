import discord
from discord.ext import commands

class RewardCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.level_system = bot.level_system
        
        # Tüm derslerin ödüllerini tanımla
        self.default_rewards = {
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
            },
            # Asa Bilimi ödülleri
            'Asa Bilimi': {
                **{str(i): "5 Sickle" for i in range(1, 10)},
                "10": "Bir Aylık Asa Bakım Seti",
                **{str(i): "5 Sickle" for i in range(11, 20)},
                "20": "Üç Aylık Asa Bakım Seti",
                **{str(i): "5 Sickle" for i in range(21, 25)},
                "25": "Mücevherli Asa Süsü",
                **{str(i): "10 Sickle" for i in range(26, 30)},
                "30": "Altı Aylık Asa Bakım Seti",
                **{str(i): "10 Sickle" for i in range(31, 35)},
                "35": "Asa Kını / Baston",
                **{str(i): "10 Sickle" for i in range(36, 40)},
                "40": "On İki Aylık Asa Bakım Seti",
                **{str(i): "10 Sickle" for i in range(41, 45)},
                "45": "Asa Değiştirme Hakkı",
                **{str(i): "10 Sickle" for i in range(46, 50)},
                "50": "Asa Üretme"
            }
        }
        
        # Ödülleri otomatik olarak yükle
        if 'rewards' not in self.level_system.data:
            self.level_system.data['rewards'] = {}
        
        # Her dersin ödüllerini kontrol et ve eksik olanları ekle
        for lesson, rewards in self.default_rewards.items():
            # Eğer ilgili alanlardan biri ise, ödülleri sıfırla
            if lesson in ["History of Magic", "KSKS", "Transfiguration", "Charms"]:
                self.level_system.data['rewards'][lesson] = rewards
            elif lesson not in self.level_system.data['rewards']:
                self.level_system.data['rewards'][lesson] = rewards
        
        # Değişiklikleri kaydet
        self.level_system.save_data()
        
        # Alan ödülleri
        self.default_area_rewards = {
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
                '7': 'Stupefyın Lanet Etkisi',
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

        # Alan ödüllerini otomatik olarak yükle
        if 'area_rewards' not in self.level_system.data:
            self.level_system.data['area_rewards'] = {}
        for area, rewards in self.default_area_rewards.items():
            self.level_system.data['area_rewards'][area] = rewards
        self.level_system.save_data()
        
        # Üst alan ödülleri
        self.default_upper_area_rewards = {
            'Duellist': {str(i+1): reward for i, reward in enumerate([
                'Savunma Büyüleri +d6', 'Saldırı Büyüleri +d6', 'Savunma Büyüleri +d6', 'Saldırı Büyüleri +d6',
                'KOMBO BONUSU', 'Spell Resistance +10', 'Spell Resistance +10', 'Spell Resistance +10',
                'Durability Prof. Bonus', 'BRACES OF THE SUN FURY', 'Dexterity Prof. Bonus', 'Savunma Büyüleri +d6',
                'Saldırı Büyüleri +d6', 'Insight +d6', 'STORM RIDER JACKET', 'Strenght Prof. Bonus',
                'Spell Resistance +10', 'Spell Resistance +10', 'Insight +d6', 'GLASSES OF DUELIST'])},
            'Curse Breaker': {str(i+1): reward for i, reward in enumerate([
                'Spell Resistance +5', 'Arcana +d6', 'Spell Resistance +5', 'Stealth +d6', 'Absorbations Glove',
                'Spell Resistance +5', 'History +d6', 'Sleight Of Hand +d6', 'Intelligence Prof. Bonus',
                "FANCY GRAVEROBBER'S DAGGER", 'Wisdom Prof. Bonus', 'Spell Resistance +5', 'History +d6',
                'Arcana +d6', "BRINEHEART'S FABORINE COAT", 'Durability Prof. Bonus', 'Insight +d6',
                'Stealth +d6', 'Sleight Of Hand +d6', 'SUIT OF GOLDEN SHADOW'])},
            'Enchanter/ess': {str(i+1): reward for i, reward in enumerate([
                'Arcana +d6', 'Arcana +d6', 'Arcana +d6', 'Arcana +d6', "STRANGE'S CAPE", 'Mana +10', 'Mana +10',
                'Mana +10', 'Intelligence Prof. Bonus', 'TIME TURNER', 'Wisdom Prof. Bonus', 'Will (Stat) +10',
                'Will (Stat) +10', 'Will (Stat) +10', 'BLOOD CRYSTALS', 'Mana +10', 'Mana +10', 'Will (Stat) +10',
                'Will (Stat) +10', 'PÜFÜR'])},
            'Charms Specialist': {str(i+1): reward for i, reward in enumerate([
                'Charm Büyüleri +d6', 'Charm Büyüleri +d6', 'Charm Büyüleri +d6', 'Charm Büyüleri +d6', 'Oz Pendants',
                'Arcana +d6', 'Mana +5', 'Arcana +d6', 'Mana +5', 'SANDS OF AVALON', 'Non-Verbal Prof. Bonus',
                'Mana +5', 'Arcana +d6', 'Mana +5', 'FORGET ME KNOT', 'Wandless-Magic Prof. Bonus', 'Mana +5',
                'Arcana +d6', 'Mana +5', 'CHROMATIC CHRONOMETER'])},
            'Healer': {str(i+1): reward for i, reward in enumerate([
                'Medicine +d6', 'Medicine +d6', 'Medicine +d6', 'Medicine +d6', 'Abracadabra Kabbalah Necklace',
                'Investigation +d6', 'Insight +d6', 'Focus +10', 'Constitution Prof. Bonus', 'RING OF REGENERATION',
                'Brewing Prof. Bonus', 'Focus +10', 'Investigation +d6', 'Focus +10', "HEALER'S Enchanted Pendant",
                'Insight +d6', 'Focus +10', 'Investigation +d6', 'Constitution Prof. Bonus', 'Asklepios'])},
            'Magizoologist': {str(i+1): reward for i, reward in enumerate([
                'Animal Handling +d6', 'Comc +d6', 'Animal Handling +d6', 'Comc +d6', 'EYE OF FLAME', 'Nature +d6',
                'Insight +d6', 'Survival +d6', 'Durability Prof. Bonus', 'EJDER GÖZÜ', 'Decterity Prof. Bonus',
                'Comc +d6', 'Animal Handling +d6', 'Comc +d6', "Shepherd's Instrument", 'Survival +d6', 'Nature +d6',
                'Animal Handling +d6', 'Survival +d6', 'Crown of the Primal Sovereign'])},
            'Potioneer': {str(i+1): reward for i, reward in enumerate([
                'İksir +d6', 'İksir +d6', 'İksir +d6', 'Brewing Prof. Bonus', "POTIONEER'S LIFE SAVER", 'İksir +d6',
                'Investigation +d6', 'Nature +d6', 'Investigation +d6', 'SCARF OF POISONS', 'Nature +d6', 'Nature +d6',
                'Investigation +d6', 'Constitution Prof. Bonus', 'PATLAMA KARŞITI KAZAN', 'Medicine +d4', 'Medicine +d4',
                'Medicine +d4', 'Intelligence Prof. Bonus', 'Alkahest'])},
            'Herbologist': {str(i+1): reward for i, reward in enumerate([
                'Nature +d6', 'Nature +d6', 'Nature +d6', 'Nature +d6', 'Filizlenme Eldivenleri', 'Survival +d6',
                'Medicine +d6', 'Medicine +d6', 'Constitution Prof. Bonus', 'Crown of Ancient Branches',
                'Intelligence Prof. Bonus', 'Survival +d6', 'Medicine +d6', 'Nature +d6', "Yggdrasil's Pouch",
                'Wisdom Prof. Bonus', 'Survival +d6', 'Survival +d6', 'Brewing Prof. Bonus', 'Staff of the Eternal Garden'])},
            'Transfiguration Master': {str(i+1): reward for i, reward in enumerate([
                'Biçim Değiştirme Büyüsü +d4', 'Biçim Değiştirme Büyüsü +d4', 'Biçim Değiştirme Büyüsü +d4',
                'Biçim Değiştirme Büyüsü +d4', 'Barkskin', 'Arcana +d6', 'Biçim Değiştirme Büyüsü +d4',
                'Biçim Değiştirme Büyüsü +d4', 'Intelligence Prof. Bonus', 'Figurine of Wondrous Power', 'Arcana +d6',
                'Biçim Değiştirme Büyüsü +d4', 'Biçim Değiştirme Büyüsü +d4', 'Arcana +d6', "Athanor'un Aynası (Mirror of the Transmuter)",
                'Arcana +d6', 'Biçim Değiştirme Büyüsü +d4', 'Arcana +d6', 'Apparation Prof. Bonus', 'Dopple Gänger Mastery'])},
            'Alchemist': {str(i+1): reward for i, reward in enumerate([
                'Simya +d6', 'Simya +d6', 'Simya +d6', 'Simya +d6', 'Scarf of Cleansing', 'Brewing Prof. Bonus',
                'İksir +d6', 'İksir +d6', 'İksir +d6', 'Athame', 'Intelligence Prof. Bonus', 'Nature +d6', 'Nature +d6',
                'Arcana +d6', 'HAND OF MIDAS', 'Arcana +d6', 'Focus +10', 'Focus +10', 'Focus +10', 'Felsefe Taşı'])},
            'Oracle': {str(i+1): reward for i, reward in enumerate([
                'Kehanet +d6', 'Kehanet +d6', 'Kehanet +d6', 'Foretelling Prof. Bonus', 'Book of Hidden Paths',
                'Wisdom Prof. Bonus', 'Kehanet +d6', 'Focus +10', 'Focus +10', 'Nightward Candle', 'Wandless Magic Prof. Bonus',
                'Focus +10', 'Perception +d6', 'Perception +d6', 'skull-hookah', 'Perception +d6', 'Insight +d6',
                'Insight +d6', 'Written Magic Prof. Bonus', 'Duru Görü'])},
            'Inventor': {str(i+1): reward for i, reward in enumerate([
                'Tılsımcılık +d6', 'Tılsımcılık +d6', 'Tılsımcılık +d6', 'Crafting Prof. Bonus', 'Cober Page',
                'Intelligence Prof. Bonus', 'Tılsımcılık +d6', 'Arcana +d6', 'Arcana +d6', 'Magic Magnifier',
                'Investigation +d6', 'Investigation +d6', 'Tılsımcılık +d6', 'Investigation +d6', 'FIRE OF PROMETHEUS',
                'Arcana +d6', 'Arcana +d6', 'Investigation +d6', 'Written Magic Prof. Bonus', 'HAT OF SURPRISES'])},
            'Pagan': {str(i+1): reward for i, reward in enumerate([
                'Religion +d6', 'Religion +d6', 'Religion +d6', 'Wisdom Prof. Bonus', 'Görünmez Koruma Tebeşiri',
                'Religion +d6', 'Insight +d6', 'Insight +d6', 'Intelligence Prof. Bonus', 'AMULET OF GODS', 'Arcana +d6',
                'Arcana +d6', 'Ancient Studies +d6', 'Ancient Studies +d6', 'BRACELET OF EREBUS', 'Tılsımcılık +d6',
                'Tılsımcılık +d6', 'History +d6', 'History +d6', 'SHADE FAMILIAR'])},
            'Necromancer': {str(i+1): reward for i, reward in enumerate([
                "Negatif Büyü Boost'u +d6", "Negatif Büyü Boost'u +d6", "Negatif Büyü Boost'u +d6", 'Dark Magic Prof. Boost',
                'Speak With Dead Dust', 'Constitution Prof. Boost', "Negatif Büyü Boost'u +d6", 'Arcana +d6',
                'Intelligence Prof. Boost', 'Grave Guiders', 'Wisdom Prof. Boost', 'Medicine +d6', 'Will +d10',
                'Medicine +d6', 'Enchanted Candle', 'Will +d10', 'Medicine +d6', 'Arcana +d6', 'Red Magic Prof. Boost',
                'Life Death Control Amulet'])},
            'Necrozoologist': {str(i+1): reward for i, reward in enumerate([
                'Comc +d6', 'Animal Handling +d6', 'Comc +d6', 'Dark Magic Prof. Boost', 'Soul Armour', 'Comc +d6',
                'Animal Handling +d6', 'Comc +d6', 'Intelligence Prof. Boost', 'Phurba of the Severed Earth',
                'Animal Handling +d6', 'Arcana +d6', 'Animal Handling +d6', "Negatif Büyü Boost'u +d6", 'Aegis of the Baneful Dawn',
                'Will (Stat) +10', 'Will (Stat) +10', 'Will (Stat) +10', 'Red Magic Prof. Boost', 'Crown of the Dark Sovereign'])},
            'Dark Mage': {str(i+1): reward for i, reward in enumerate([
                "Negatif Büyü Boost'u +d6", "Negatif Büyü Boost'u +d6", "Negatif Büyü Boost'u +d6", 'Dark Magic Prof. Boost',
                "Maui's Fish Hook", "Negatif Büyü Boost'u +d6", 'Arcana +d6', 'Arcana +d6', 'Intelligence Prof. Boost',
                'SHROUD OF DARKNESS', 'Arcana +d6', 'Arcana +d6', 'Dark Magic Prof. Bonus', 'Will +d10', 'Umbra Ægis',
                'Will +d10', 'Will +d10', 'Intimidation +d6', 'Red Magic Prof. Boost', "Nekrah's Veil"])},
            'Ritualist': {str(i+1): reward for i, reward in enumerate([
                'Religion +d6', 'Religion +d6', 'Religion +d6', 'Religion +d6', 'Lamba Cini', 'Arcana +d6', 'Perception +d6',
                'Insight +d6', 'Red Magic Prof. Boost', 'Seal of Solomon', 'Intelligence Prof. Bonus', 'Focus +d10',
                'Focus +d10', 'Focus +d10', 'Familiar Statü', 'Will (Stat) +10', 'Will (Stat) +10', 'Will (Stat) +10',
                'Red Magic Prof. Boost', 'Invocation'])}
        }

        # Üst alan ödüllerini otomatik olarak yükle
        if 'upper_area_rewards' not in self.level_system.data:
            self.level_system.data['upper_area_rewards'] = {}
        for upper_area, rewards in self.default_upper_area_rewards.items():
            self.level_system.data['upper_area_rewards'][upper_area] = rewards
        self.level_system.save_data()
        
    @commands.command(name='setreward')
    @commands.has_role('RewardManager')
    async def setreward(self, ctx, area: str, level: int, *, reward: str):
        """Bir alan için belirli bir seviyede ödül tanımlar"""
        if level < 1 or level > 20:
            await ctx.send("Hata: Seviye 1-20 arasında olmalıdır!")
            return
            
        if area not in self.level_system.areas and area != 'Asa Bilimi':
            await ctx.send(f"Hata: {area} geçerli bir alan değil!")
            return
            
        if 'rewards' not in self.level_system.data:
            self.level_system.data['rewards'] = {}
            
        if area not in self.level_system.data['rewards']:
            self.level_system.data['rewards'][area] = {}
            
        self.level_system.data['rewards'][area][str(level)] = reward
        self.level_system.save_data()
        
        await ctx.send(f"{area} alanı için {level}. seviye ödülü '{reward}' olarak ayarlandı!")
        
    @commands.command(name='setasarewards')
    @commands.has_role('RewardManager')
    async def setasarewards(self, ctx):
        """Asa Bilimi için tüm ödülleri otomatik olarak ayarlar"""
        if 'rewards' not in self.level_system.data:
            self.level_system.data['rewards'] = {}
            
        if 'Asa Bilimi' not in self.level_system.data['rewards']:
            self.level_system.data['rewards']['Asa Bilimi'] = {}
            
        # Asa Bilimi ödül listesi
        rewards = {
            "1": "5 Sickle",
            "2": "5 Sickle",
            "3": "5 Sickle",
            "4": "5 Sickle",
            "5": "5 Sickle",
            "6": "5 Sickle",
            "7": "5 Sickle",
            "8": "5 Sickle",
            "9": "5 Sickle",
            "10": "Bir Aylık Asa Bakım Seti",
            "11": "5 Sickle",
            "12": "5 Sickle",
            "13": "5 Sickle",
            "14": "5 Sickle",
            "15": "5 Sickle",
            "16": "5 Sickle",
            "17": "5 Sickle",
            "18": "5 Sickle",
            "19": "5 Sickle",
            "20": "Üç Aylık Asa Bakım Seti",
            "21": "5 Sickle",
            "22": "5 Sickle",
            "23": "5 Sickle",
            "24": "5 Sickle",
            "25": "Mücevherli Asa Süsü",
            "26": "10 Sickle",
            "27": "10 Sickle",
            "28": "10 Sickle",
            "29": "10 Sickle",
            "30": "Altı Aylık Asa Bakım Seti",
            "31": "10 Sickle",
            "32": "10 Sickle",
            "33": "10 Sickle",
            "34": "10 Sickle",
            "35": "Asa Kını / Baston",
            "36": "10 Sickle",
            "37": "10 Sickle",
            "38": "10 Sickle",
            "39": "10 Sickle",
            "40": "On İki Aylık Asa Bakım Seti",
            "41": "10 Sickle",
            "42": "10 Sickle",
            "43": "10 Sickle",
            "44": "10 Sickle",
            "45": "Asa Değiştirme Hakkı",
            "46": "10 Sickle",
            "47": "10 Sickle",
            "48": "10 Sickle",
            "49": "10 Sickle",
            "50": "Asa Üretme"
        }
        
        self.level_system.data['rewards']['Asa Bilimi'] = rewards
        self.level_system.save_data()
        
        await ctx.send("Asa Bilimi için tüm ödüller başarıyla ayarlandı!")
        
    @commands.command(name='setsubreward')
    @commands.has_role('Moderator')
    async def setsubreward(self, ctx, area: str, upper_area: str, level: int, *, reward: str):
        """Üst alan için ödül tanımlar"""
        if level < 1 or level > 20:
            await ctx.send("Hata: Seviye 1-20 arasında olmalıdır!")
            return
            
        if area not in self.level_system.areas:
            await ctx.send(f"Hata: {area} geçerli bir alan değil!")
            return
            
        if upper_area not in self.level_system.upper_areas[area]:
            await ctx.send(f"Hata: {upper_area} {area} için geçerli bir üst alan değil!")
            return
            
        # Ödülü kaydet
        if 'subrewards' not in self.level_system.data:
            self.level_system.data['subrewards'] = {}
            
        if area not in self.level_system.data['subrewards']:
            self.level_system.data['subrewards'][area] = {}
            
        if upper_area not in self.level_system.data['subrewards'][area]:
            self.level_system.data['subrewards'][area][upper_area] = {}
            
        self.level_system.data['subrewards'][area][upper_area][str(level)] = reward
        self.level_system.save_data()
        
        await ctx.send(f"{area} > {upper_area} için seviye {level} ödülü '{reward}' olarak ayarlandı!")

    def check_and_give_area_reward(self, user_data, area, new_area_level):
        """Kullanıcı bir alanın yeni seviyesine ulaştığında alan ödülünü verir. (Antik Büyü Sayfası dahil, her seviye için eklenir)"""
        if 'area_rewards' not in self.level_system.data:
            return
        area_rewards = self.level_system.data['area_rewards'].get(area, {})
        reward = area_rewards.get(str(new_area_level))
        if reward:
            if 'earned_rewards' not in user_data:
                user_data['earned_rewards'] = []
            user_data['earned_rewards'].append(reward)
            self.level_system.save_data()

    def check_and_give_upper_area_reward(self, user_data, upper_area, new_upper_area_level):
        """Kullanıcı bir üst alanın yeni seviyesine ulaştığında üst alan ödülünü verir."""
        if 'upper_area_rewards' not in self.level_system.data:
            return
        upper_area_rewards = self.level_system.data['upper_area_rewards'].get(upper_area, {})
        reward = upper_area_rewards.get(str(new_upper_area_level))
        if reward:
            if 'earned_rewards' not in user_data:
                user_data['earned_rewards'] = []
            user_data['earned_rewards'].append(reward)
            self.level_system.save_data()

    @commands.command(name='userewards')
    async def userewards(self, ctx, *, reward_name: str):
        """Kullanıcının belirli bir ödülü kullanmasını sağlar"""
        user_id = str(ctx.author.id)
        if user_id not in self.level_system.data['users']:
            await ctx.send("Henüz hiç ödülünüz bulunmuyor!")
            return

        user_data = self.level_system.data['users'][user_id]
        if 'earned_rewards' not in user_data or not user_data['earned_rewards']:
            await ctx.send("Henüz hiç ödülünüz bulunmuyor!")
            return

        # Ödülü bul ve kaldır
        if reward_name in user_data['earned_rewards']:
            user_data['earned_rewards'].remove(reward_name)
            self.level_system.save_data()
            await ctx.send(f"'{reward_name}' ödülünü başarıyla kullandınız!")
        else:
            await ctx.send(f"'{reward_name}' ödülüne sahip değilsiniz!")

    @commands.command(name='withdraw')
    async def withdraw(self, ctx):
        """Kullanıcının tüm Sickle ödüllerini kullanmasını sağlar"""
        user_id = str(ctx.author.id)
        if user_id not in self.level_system.data['users']:
            await ctx.send("Henüz hiç ödülünüz bulunmuyor!")
            return

        user_data = self.level_system.data['users'][user_id]
        if 'earned_rewards' not in user_data or not user_data['earned_rewards']:
            await ctx.send("Henüz hiç ödülünüz bulunmuyor!")
            return

        # Sickle ödüllerini bul ve kaldır
        sickle_rewards = [reward for reward in user_data['earned_rewards'] if 'Sickle' in reward]
        if not sickle_rewards:
            await ctx.send("Kullanılabilir Sickle ödülünüz bulunmuyor!")
            return

        # Her bir Sickle ödülünü kaldır
        for reward in sickle_rewards:
            user_data['earned_rewards'].remove(reward)

        self.level_system.save_data()
        await ctx.send(f"Toplam {len(sickle_rewards)} adet Sickle ödülünü başarıyla kullandınız!")

async def setup(bot):
    await bot.add_cog(RewardCommands(bot)) 