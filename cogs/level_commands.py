import discord
from discord.ext import commands
from discord import app_commands

class LevelCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.level_system = bot.level_system
        
    @commands.command(name='addpoints')
    @commands.has_role('Moderator')
    async def addpoints(self, ctx, member: discord.Member, *, args):
        """Bir kullanıcıya puan ekler
        Kullanım: !addpoints @kullanıcı <ders_adı> <puan>
        Örnek: !addpoints @kullanıcı "Ancient Runes" 1500"""
        try:
            # Son kelimeyi puan olarak al
            args_split = args.rsplit(' ', 1)
            if len(args_split) != 2:
                await ctx.send('Hata: Komut formatı yanlış! Örnek: !addpoints @kullanıcı "Ancient Runes" 1500')
                return
                
            lesson = args_split[0].strip('"').strip("'")  # Tırnak işaretlerini kaldır
            try:
                points = int(args_split[1])
            except ValueError:
                await ctx.send('Hata: Puan sayı olmalıdır!')
                return

            # Kullanıcı verilerini al veya oluştur
            user_id = str(member.id)
            if user_id not in self.level_system.data['users']:
                self.level_system.data['users'][user_id] = {
                    'categories': {},
                    'main_area': None,
                    'upper_areas': {},
                    'earned_rewards': []  # Kazanılan ödüller listesi
                }
                
            user_data = self.level_system.data['users'][user_id]
            if 'earned_rewards' not in user_data:
                user_data['earned_rewards'] = []
            
            # Dersin hangi alana ait olduğunu bul
            lesson_area = None
            for area, area_data in self.level_system.areas.items():
                if lesson in area_data['lessons']:
                    lesson_area = area
                    break
                    
            if lesson_area is None and lesson not in self.level_system.independent_lessons:
                await ctx.send(f"Hata: {lesson} geçerli bir ders değil!")
                return
                
            # Eski seviyeyi kaydet
            old_level = 0
            if lesson_area:
                if lesson_area in user_data['categories'] and lesson in user_data['categories'][lesson_area]:
                    old_points = user_data['categories'][lesson_area][lesson]
                    old_level = self.level_system.calculate_lesson_level(old_points, area=lesson_area)
            else:
                if 'independent' in user_data['categories'] and lesson in user_data['categories']['independent']:
                    old_points = user_data['categories']['independent'][lesson]
                    old_level = self.level_system.calculate_lesson_level(old_points)
                
            # Puanları ekle
            if lesson_area:
                if lesson_area not in user_data['categories']:
                    user_data['categories'][lesson_area] = {}
                if lesson not in user_data['categories'][lesson_area]:
                    user_data['categories'][lesson_area][lesson] = 0
                
                # Önce tüm derslerin 100 levele ulaşıp ulaşmadığını kontrol et
                all_max_level = True
                for lesson_name in self.level_system.areas[lesson_area]['lessons']:
                    if lesson_name != lesson:  # Şu anki dersi kontrol etmiyoruz çünkü henüz puan eklenmedi
                        lesson_points = user_data['categories'][lesson_area].get(lesson_name, 0)
                        lesson_level = self.level_system.calculate_lesson_level(lesson_points, area=lesson_area)
                        if lesson_level < 100:
                            all_max_level = False
                            break
                
                # Şu anki dersin yeni puanlarını hesapla
                current_points = user_data['categories'][lesson_area].get(lesson, 0)
                current_level = self.level_system.calculate_lesson_level(current_points, area=lesson_area)
                
                # Eğer tüm dersler 100 levelse ve bu ders de 100 levelse
                if all_max_level and current_level >= 100:
                    # Puanları direkt üst alana ekle (eğer üst alan seçilmişse)
                    if lesson_area in user_data.get('upper_areas', {}):
                        if 'upper_points' not in user_data:
                            user_data['upper_points'] = {}
                        if lesson_area not in user_data['upper_points']:
                            user_data['upper_points'][lesson_area] = 10000  # Başlangıç puanı
                        old_upper_points = user_data['upper_points'][lesson_area]
                        old_upper_level = self.level_system.calculate_upper_area_level(old_upper_points, area=lesson_area)
                        user_data['upper_points'][lesson_area] += points
                        new_upper_points = user_data['upper_points'][lesson_area]
                        new_upper_level = self.level_system.calculate_upper_area_level(new_upper_points, area=lesson_area)
                        # Üst alan ödüllerini ver (her seviye için)
                        reward_cog = self.bot.get_cog('RewardCommands')
                        if reward_cog:
                            upper_area = user_data['upper_areas'][lesson_area]
                            for lvl in range(old_upper_level + 1, new_upper_level + 1):
                                reward_cog.check_and_give_upper_area_reward(user_data, upper_area, lvl)
                        await ctx.send(f"{member.mention} artık bu alandaki tüm dersler maksimum seviyede! {points} puan direkt olarak {user_data['upper_areas'][lesson_area]} üst alanına eklendi.")
                    else:
                        await ctx.send(f"{member.mention} bu alandaki tüm dersler maksimum seviyede! Üst alan seçersen kazandığın puanlar oraya eklenecek.")
                else:
                    # Normal puan ekleme
                    new_points = current_points + points
                    
                    # SoulMaster alanı için maksimum 12500 puan (100 level)
                    # Diğer alanlar için maksimum 2500 puan (100 level)
                    max_points = 12500 if lesson_area == 'SoulMaster' else 2500
                    
                    # Eğer yeni puanlar maksimumu aşıyorsa
                    if new_points > max_points:
                        excess_points = new_points - max_points
                        new_points = max_points
                        
                        # Eğer kullanıcının bu alanda bir üst alanı varsa, fazla puanları oraya ekle
                        if lesson_area in user_data.get('upper_areas', {}):
                            if 'upper_points' not in user_data:
                                user_data['upper_points'] = {}
                            if lesson_area not in user_data['upper_points']:
                                user_data['upper_points'][lesson_area] = 10000
                            user_data['upper_points'][lesson_area] += excess_points
                            await ctx.send(f"{member.mention} {lesson} dersi maksimum seviyeye ulaştı! Fazla olan {excess_points} puan {user_data['upper_areas'][lesson_area]} üst alanına eklendi.")
                        else:
                            # Üst alan seçilmemişse, fazla puanları depola
                            if 'stored_points' not in user_data:
                                user_data['stored_points'] = {}
                            if lesson_area not in user_data['stored_points']:
                                user_data['stored_points'][lesson_area] = 0
                            user_data['stored_points'][lesson_area] += excess_points
                            await ctx.send(f"{member.mention} {lesson} dersi maksimum seviyeye ulaştı! Fazla olan {excess_points} puan depolandı ve üst alan seçildiğinde aktarılacak.")
                    
                    user_data['categories'][lesson_area][lesson] = new_points
                
                new_points = user_data['categories'][lesson_area][lesson]
            else:
                # Bağımsız dersler için normal puan ekleme
                if 'independent' not in user_data['categories']:
                    user_data['categories']['independent'] = {}
                if lesson not in user_data['categories']['independent']:
                    user_data['categories']['independent'][lesson] = 0
                
                current_points = user_data['categories']['independent'].get(lesson, 0)
                new_points = current_points + points
                max_points = 2500  # Bağımsız dersler için maksimum puan (100 level)
                
                # Eğer yeni puanlar maksimumu aşıyorsa
                if new_points > max_points:
                    excess_points = new_points - max_points
                    new_points = max_points
                    await ctx.send(f"{member.mention} {lesson} dersi maksimum seviyeye ulaştı! Fazla olan {excess_points} puan depolandı ve üst alan seçildiğinde aktarılacak.")
                
                user_data['categories']['independent'][lesson] = new_points
            
            # Yeni seviyeyi hesapla
            new_level = self.level_system.calculate_lesson_level(new_points, area=lesson_area)
            
            # Ödülleri kontrol et - sadece kullanıcının ana alanı veya açık alanları için
            if 'rewards' in self.level_system.data and lesson in self.level_system.data['rewards']:
                # Kullanıcının bu alandan ödül alıp alamayacağını kontrol et
                can_receive_rewards = (
                    not lesson_area or  # Bağımsız dersler her zaman ödül alabilir
                    lesson_area == user_data.get('main_area') or  # Ana alan
                    lesson_area in user_data.get('unlocked_areas', [])  # Açık alanlar
                )
                
                if can_receive_rewards:
                    try:
                        lesson_rewards = self.level_system.data['rewards'][lesson]
                        for level_str, reward in lesson_rewards.items():
                            level = int(level_str)
                            if old_level < level <= new_level:  # Sadece yeni ulaşılan seviyelerin ödüllerini ver
                                if isinstance(reward, list):
                                    # Seçilebilir ödül
                                    reward_message = await ctx.send(
                                        f"{member.mention}, {lesson} dersinde {level}. seviyeye ulaştınız!\n"
                                        f"Lütfen bir ödül seçin:\n" + 
                                        "\n".join(f"{i+1}. {r}" for i, r in enumerate(reward))
                                    )
                                    
                                    # Tepki ekle
                                    for i in range(len(reward)):
                                        await reward_message.add_reaction(f"{i+1}\u20e3")
                                        
                                    def check(reaction, user):
                                        return user == member and str(reaction.emoji)[0].isdigit() and int(str(reaction.emoji)[0]) <= len(reward)
                                        
                                    try:
                                        reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check)
                                        selected_index = int(str(reaction.emoji)[0]) - 1
                                        selected_reward = reward[selected_index]
                                        if 'earned_rewards' not in user_data:
                                            user_data['earned_rewards'] = []
                                        user_data['earned_rewards'].append(selected_reward)
                                    except TimeoutError:
                                        await ctx.send(f"{member.mention} süre doldu! Ödül seçimi daha sonra tekrar yapılabilir.")
                                else:
                                    # Normal ödül
                                    if 'earned_rewards' not in user_data:
                                        user_data['earned_rewards'] = []
                                    user_data['earned_rewards'].append(reward)
                    except Exception as e:
                        await ctx.send(f"Ödül verme sırasında bir hata oluştu: {str(e)}")
            
            # Verileri kaydet
            self.level_system.save_data()
            
            # Level kontrolü ve bildirim
            if lesson_area:
                # Derslerin seviyelerini hesapla
                lesson_levels = []
                for lesson_name in self.level_system.areas[lesson_area]['lessons']:
                    lesson_points = user_data['categories'][lesson_area].get(lesson_name, 0)
                    lesson_level = self.level_system.calculate_lesson_level(lesson_points, area=lesson_area)
                    lesson_levels.append(lesson_level)
                
                # Alan seviyesini hesapla (tüm dersler 60. seviyeye ulaştığında alan 12. seviyeye ulaşır)
                min_lesson_level = min(lesson_levels) if lesson_levels else 0
                area_level = min_lesson_level // 5
                
                # Alan ödülünü ver (her seviye için)
                reward_cog = self.bot.get_cog('RewardCommands')
                if reward_cog:
                    for lvl in range(area_level - ((old_level // 5) if lesson_area else 0)):
                        reward_cog.check_and_give_area_reward(user_data, lesson_area, ((old_level // 5) if lesson_area else 0) + lvl + 1)
                
                # Üst alan seçimi kontrolü - alan seviyesi 20'ye ulaştığında
                if area_level >= 20 and lesson_area not in user_data.get('upper_areas', {}):
                    # Üst alan seçim mesajını gönder
                    upper_area_emojis = {
                        'Alchemist': '⚗️',
                        'Oracle': '🔮',
                        'Inventor': '⚙️',
                        'Pagan': '🌙',
                        'Duellist': '⚔️',
                        'Curse Breaker': '🏺',
                        'Enchanter/ess': '✨',
                        'Charms Specialist': '🎭',
                        'Healer': '💚',
                        'Magizoologist': '🦁',
                        'Wandmaker': '⚡',
                        'Potioneer': '🧪',
                        'Transfiguration Master': '🎯',
                        'Herbologist': '🌿',
                        'Dark Wizard': '💀',
                        'Seer': '👁️',
                        'Astrologer': '⭐',
                        'Mystic': '🌌'
                    }
                    
                    available_upper_areas = self.level_system.upper_areas.get(lesson_area, [])
                    
                    if available_upper_areas:
                        message_content = [
                            f"{member.mention} tebrikler! {lesson_area} alanında 20. seviyeye ulaştın!",
                            "Artık bir üst alan seçebilirsin. Seçmek istediğin üst alanın emojisine tıkla:",
                            "İstediğin zaman seçimini yapabilirsin, acele etmene gerek yok.",
                            ""  # Boş satır
                        ]
                        
                        # Mevcut üst alanları listele
                        for upper_area in available_upper_areas:
                            message_content.append(f"{upper_area_emojis.get(upper_area, '❓')} {upper_area}")
                        
                        message = await ctx.send("\n".join(message_content))
                        
                        # Sadece mevcut üst alanların emojilerini ekle
                        for upper_area in available_upper_areas:
                            if upper_area in upper_area_emojis:
                                await message.add_reaction(upper_area_emojis[upper_area])
                        
                        def check(reaction, user):
                            return (user == member and 
                                   str(reaction.emoji) in [upper_area_emojis[area] for area in available_upper_areas if area in upper_area_emojis])
                        
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', check=check)
                            
                            # Seçilen emojiyi üst alana çevir
                            selected_upper_area = None
                            for upper_area, emoji in upper_area_emojis.items():
                                if str(reaction.emoji) == emoji and upper_area in available_upper_areas:
                                    selected_upper_area = upper_area
                                    break
                            
                            if selected_upper_area:
                                # Üst alanı ayarla
                                if 'upper_areas' not in user_data:
                                    user_data['upper_areas'] = {}
                                user_data['upper_areas'][lesson_area] = selected_upper_area
                                
                                # Üst alan puanlarını başlat ve depolanmış puanları ekle
                                if 'upper_points' not in user_data:
                                    user_data['upper_points'] = {}
                                if lesson_area not in user_data['upper_points']:
                                    user_data['upper_points'][lesson_area] = 10000  # Başlangıç puanı
                                
                                # Depolanmış puanları ekle
                                if 'stored_points' in user_data and lesson_area in user_data['stored_points']:
                                    stored_points = user_data['stored_points'][lesson_area]
                                    user_data['upper_points'][lesson_area] += stored_points
                                    del user_data['stored_points'][lesson_area]  # Depolanmış puanları temizle
                                    await ctx.send(f"{member.mention} {selected_upper_area} üst alanını seçtin! Depolanmış {stored_points} puan üst alana eklendi.")
                                else:
                                    await ctx.send(f"{member.mention} {selected_upper_area} üst alanını seçtin! Artık bu alanda kazandığın puanlar üst alanına eklenecek.")

                                # Başlangıç seviyesine kadar olan ödülleri ver
                                reward_cog = self.bot.get_cog('RewardCommands')
                                if reward_cog:
                                    initial_level = self.level_system.calculate_upper_area_level(user_data['upper_points'][lesson_area], area=lesson_area)
                                    for level in range(1, initial_level + 1):
                                        reward_cog.check_and_give_upper_area_reward(user_data, selected_upper_area, level)
                                
                                self.level_system.save_data()
                        except Exception as e:
                            await ctx.send(f"Bir hata oluştu: {str(e)}")
                
                # Alan kilidi kontrolü - tüm dersler en az 60. seviyede olmalı
                if min_lesson_level >= 60:  # 60/5 = 12. seviye
                    if 'unlocked_areas' not in user_data:
                        user_data['unlocked_areas'] = []
                    if 'areas_reached_12' not in user_data:
                        user_data['areas_reached_12'] = []
                    if lesson_area not in user_data['areas_reached_12']:
                        user_data['areas_reached_12'].append(lesson_area)
                        # Kullanıcının ana alanı ve açtığı alanlar dışındaki alanları bul
                        available_areas = []
                        for area_name in ['Eclectic', 'Defender', 'CareTaker', 'SoulMaster']:
                            if (area_name != user_data.get('main_area') and 
                                area_name != lesson_area and 
                                area_name not in user_data.get('unlocked_areas', [])):
                                available_areas.append(area_name)
                        if available_areas:
                            # Alan seçim mesajını gönder
                            area_emojis = {
                                'Eclectic': '⚡',
                                'Defender': '🛡️',
                                'CareTaker': '🌿',
                                'SoulMaster': '🔮'
                            }
                            message_content = [
                                f"{member.mention} tebrikler! {lesson_area} alanında 12. seviyeye ulaştın!",
                                "Yeni bir alan açabilirsin. Seçmek istediğin alanın emojisine tıkla:",
                                ""  # Boş satır
                            ]
                            for area_name in available_areas:
                                message_content.append(f"{area_emojis[area_name]} {area_name}")
                            message = await ctx.send("\n".join(message_content))
                            for area_name in available_areas:
                                await message.add_reaction(area_emojis[area_name])
                            def check(reaction, user):
                                return (user == member and 
                                       str(reaction.emoji) in [area_emojis[area] for area in available_areas])
                            try:
                                reaction, user = await self.bot.wait_for('reaction_add', check=check)
                                selected_area = None
                                for area_name, emoji in area_emojis.items():
                                    if str(reaction.emoji) == emoji:
                                        selected_area = area_name
                                        break
                                if selected_area and selected_area not in user_data['unlocked_areas']:
                                    user_data['unlocked_areas'].append(selected_area)
                                    self.level_system.save_data()
                                    role = discord.utils.get(ctx.guild.roles, name=selected_area)
                                    if role:
                                        await member.add_roles(role)
                                    await ctx.send(f"🎉 {member.mention} artık bir {selected_area}! Yeni alan açıldı ve rol eklendi.")
                            except Exception as e:
                                await ctx.send(f'Hata oluştu: {str(e)}')
            
            # Puan ve seviye bildirimini gönder
            if new_level > old_level:
                await ctx.send(f"{member.mention} {lesson} {points} kazandı ({old_level} --> {new_level})")
            else:
                await ctx.send(f"{member.mention} {lesson} {points} kazandı")
                
        except Exception as e:
            await ctx.send(f'Hata oluştu: {str(e)}')
        
    @commands.command(name='checklevel')
    async def checklevel(self, ctx, member: discord.Member = None):
        """Kullanıcının seviyelerini gösterir"""
        if member is None:
            member = ctx.author
            
        user_id = str(member.id)
        user_data = self.level_system.data['users'].get(user_id, {})
        categories = user_data.get('categories', {})
        
        embed = discord.Embed(
            title=f"{member.name} Seviye Bilgileri",
            color=discord.Color.blue()
        )
        
        # Bağımsız dersler - her zaman göster
        independent_info = "**Bağımsız Dersler**\n"
        for lesson in self.level_system.independent_lessons:
            points = categories.get('independent', {}).get(lesson, 0)
            lesson_level = self.level_system.calculate_lesson_level(points)
            independent_info += f"{lesson}: Seviye {lesson_level} (Puan: {points})\n"
        embed.add_field(name="\u200b", value=independent_info, inline=False)
        
        # Tüm alanları ve dersleri göster
        for area in self.level_system.areas:
            # Derslerin seviyelerini hesapla
            lesson_levels = []
            area_total_points = 0
            
            if area in categories:
                for lesson in self.level_system.areas[area]['lessons']:
                    points = categories[area].get(lesson, 0)
                    lesson_level = self.level_system.calculate_lesson_level(points, area=area)
                    lesson_levels.append(lesson_level)
                    area_total_points += points
            
            # Alan seviyesini hesapla (en düşük ders seviyesi / 5)
            area_level = min(lesson_levels) // 5 if lesson_levels else 0
            
            # Alan başlığı
            area_title = f"{area} Alanı"
            if area == user_data.get('main_area'):
                area_title += " (Ana Alan)"
            elif area in user_data.get('unlocked_areas', []):
                area_title += " (Açık)"
                
            # Alan bilgileri
            area_info = f"Toplam Seviye: {area_level}\nToplam Puan: {area_total_points}\n\n"
            
            # Derslerin puanları
            lessons_info = []
            for lesson in self.level_system.areas[area]['lessons']:
                points = categories.get(area, {}).get(lesson, 0)
                lesson_level = self.level_system.calculate_lesson_level(points, area=area)
                lessons_info.append(f"{lesson}: Seviye {lesson_level} (Puan: {points})")
            
            area_info += "Dersler:\n" + "\n".join(lessons_info)
            
            # Depolanmış puanları göster
            if 'stored_points' in user_data and area in user_data['stored_points']:
                stored_points = user_data['stored_points'][area]
                area_info += f"\n\nDepolanmış Puanlar: {stored_points}"
            
            # Üst alan bilgisi
            if area in user_data.get('upper_areas', {}):
                upper_area = user_data['upper_areas'][area]
                upper_points = user_data.get('upper_points', {}).get(area, 0)
                upper_level = self.level_system.calculate_upper_area_level(upper_points, area=area)
                area_info += f"\n\nÜst Alan: {upper_area} (Seviye {upper_level})"
            
            embed.add_field(
                name=area_title,
                value=area_info,
                inline=False
            )
        
        await ctx.send(embed=embed)
        
    @commands.command(name='changearea')
    @commands.has_role('Moderator')
    async def changearea(self, ctx, member: discord.Member, new_area: str):
        """Kullanıcının ana alanını değiştirir"""
        if new_area not in self.level_system.areas:
            await ctx.send(f"Hata: {new_area} geçerli bir alan değil!")
            return
            
        user_id = str(member.id)
        if user_id not in self.level_system.data['users']:
            self.level_system.data['users'][user_id] = {
                'categories': {},
                'main_area': None,
                'upper_areas': {}
            }
            
        user_data = self.level_system.data['users'][user_id]
        old_area = user_data.get('main_area')
        user_data['main_area'] = new_area
        
        # Verileri kaydet
        self.level_system.save_data()
        
        await ctx.send(f"{member.mention} için ana alan {old_area if old_area else 'yok'} -> {new_area} olarak değiştirildi!")
        
    @commands.command(name='chooseupper')
    async def chooseupper(self, ctx, area: str, upper_area: str):
        """Üst alan seçer"""
        if area not in self.level_system.areas:
            await ctx.send(f"Hata: {area} geçerli bir alan değil!")
            return
            
        if upper_area not in self.level_system.upper_areas[area]:
            await ctx.send(f"Hata: {upper_area} {area} için geçerli bir üst alan değil!")
            return
            
        user_id = str(ctx.author.id)
        if user_id not in self.level_system.data['users']:
            await ctx.send("Hata: Henüz hiç puanınız yok!")
            return
            
        user_data = self.level_system.data['users'][user_id]
        
        # Alan seviyesini kontrol et
        area_points = sum(user_data.get('categories', {}).get(area, {}).values())
        area_level = self.level_system.calculate_area_level(area_points)
        
        if area_level < 20:
            await ctx.send(f"Hata: {area} alanında 20. seviyeye ulaşmanız gerekiyor!")
            return
            
        # Üst alanı ayarla
        if 'upper_areas' not in user_data:
            user_data['upper_areas'] = {}
            
        user_data['upper_areas'][area] = upper_area
        
        # Üst alan puanlarını başlat ve depolanmış puanları ekle
        if 'upper_points' not in user_data:
            user_data['upper_points'] = {}
            
        user_data['upper_points'][area] = 10000  # Başlangıç puanı
        
        # Depolanmış puanları ekle
        if 'stored_points' in user_data and area in user_data['stored_points']:
            stored_points = user_data['stored_points'][area]
            user_data['upper_points'][area] += stored_points
            del user_data['stored_points'][area]  # Depolanmış puanları temizle
            await ctx.send(f"Depolanmış {stored_points} puan üst alana eklendi!")

        # Başlangıç seviyesine kadar olan ödülleri ver
        reward_cog = self.bot.get_cog('RewardCommands')
        if reward_cog:
            initial_level = self.level_system.calculate_upper_area_level(user_data['upper_points'][area], area=area)
            for level in range(1, initial_level + 1):
                reward_cog.check_and_give_upper_area_reward(user_data, upper_area, level)
        
        # Verileri kaydet
        self.level_system.save_data()
        
        # Discord rolü ekle
        role = discord.utils.get(ctx.guild.roles, name=upper_area)
        if role:
            await ctx.author.add_roles(role)
            
        await ctx.send(f"{ctx.author.mention} için {area} alanında {upper_area} üst alanı seçildi!")
        
    @commands.command(name='setarea')
    @commands.has_role('Moderator')
    async def setarea(self, ctx, member: discord.Member, area: str):
        """Kullanıcının ana alanını ayarlar"""
        # Alan adını düzelt (ilk harf büyük, diğerleri küçük)
        area = area.capitalize()
        
        # Alan kontrolü
        if area not in ['Eclectic', 'Defender', 'CareTaker']:
            await ctx.send(f"Hata: {area} geçerli bir alan değil! Geçerli alanlar: Eclectic, Defender, CareTaker")
            return
            
        # Kullanıcı verilerini al veya oluştur
        user_id = str(member.id)
        if user_id not in self.level_system.data['users']:
            self.level_system.data['users'][user_id] = {
                'categories': {},
                'main_area': None,
                'upper_areas': {}
            }
            
        user_data = self.level_system.data['users'][user_id]
        old_area = user_data.get('main_area')
        
        # Eğer kullanıcının zaten bu alan atanmışsa uyar
        if old_area == area:
            await ctx.send(f"{member.mention} zaten {area} alanına sahip!")
            return
            
        # Alanı değiştir
        user_data['main_area'] = area
        
        # Diğer alanları temizle
        if 'unlocked_areas' in user_data:
            user_data['unlocked_areas'] = []
            
        # Verileri kaydet
        self.level_system.save_data()
        
        # Discord rollerini güncelle
        # Eski alan rolünü kaldır
        if old_area:
            old_role = discord.utils.get(ctx.guild.roles, name=old_area)
            if old_role:
                await member.remove_roles(old_role)
                
        # Yeni alan rolünü ekle
        new_role = discord.utils.get(ctx.guild.roles, name=area)
        if new_role:
            await member.add_roles(new_role)
            
        # Bildirim gönder
        await ctx.send(f"{member.mention} için ana alan {old_area if old_area else 'yok'} -> {area} olarak değiştirildi!")
        
        # Eğer kullanıcının üst alanı varsa, kaldır
        if 'upper_areas' in user_data and old_area in user_data['upper_areas']:
            old_upper_area = user_data['upper_areas'][old_area]
            old_upper_role = discord.utils.get(ctx.guild.roles, name=old_upper_area)
            if old_upper_role:
                await member.remove_roles(old_upper_role)
            del user_data['upper_areas'][old_area]
            self.level_system.save_data()
            await ctx.send(f"{member.mention} için {old_area} alanındaki {old_upper_area} üst alanı kaldırıldı!")
        
    @commands.command(name='removepoints')
    @commands.has_role('Moderator')
    async def removepoints(self, ctx, member: discord.Member, *, args):
        """Bir kullanıcıdan puan çıkarır
        Kullanım: !removepoints @kullanıcı <ders_adı> <puan>
        Örnek: !removepoints @kullanıcı "Ancient Runes" 1500"""
        try:
            # Son kelimeyi puan olarak al
            args_split = args.rsplit(' ', 1)
            if len(args_split) != 2:
                await ctx.send('Hata: Komut formatı yanlış! Örnek: !removepoints @kullanıcı "Ancient Runes" 1500')
                return
                
            lesson = args_split[0].strip('"').strip("'")  # Tırnak işaretlerini kaldır
            try:
                points = int(args_split[1])
            except ValueError:
                await ctx.send('Hata: Puan sayı olmalıdır!')
                return

            # Kullanıcı verilerini al
            user_id = str(member.id)
            if user_id not in self.level_system.data['users']:
                await ctx.send(f"Hata: {member.mention} henüz hiç puan kazanmamış!")
                return
                
            user_data = self.level_system.data['users'][user_id]
            
            # Dersin hangi alana ait olduğunu bul
            lesson_area = None
            for area, area_data in self.level_system.areas.items():
                if lesson in area_data['lessons']:
                    lesson_area = area
                    break
                    
            if lesson_area is None and lesson not in self.level_system.independent_lessons:
                await ctx.send(f"Hata: {lesson} geçerli bir ders değil!")
                return
            
            # Eski seviyeyi kaydet
            old_level = 0
            if lesson_area:
                if lesson_area in user_data['categories'] and lesson in user_data['categories'][lesson_area]:
                    old_points = user_data['categories'][lesson_area][lesson]
                    old_level = self.level_system.calculate_lesson_level(old_points, area=lesson_area)
                else:
                    await ctx.send(f"Hata: {member.mention} henüz {lesson} dersinden puan kazanmamış!")
                    return
            else:
                if 'independent' in user_data['categories'] and lesson in user_data['categories']['independent']:
                    old_points = user_data['categories']['independent'][lesson]
                    old_level = self.level_system.calculate_lesson_level(old_points)
                else:
                    await ctx.send(f"Hata: {member.mention} henüz {lesson} dersinden puan kazanmamış!")
                    return
            
            # Puanları çıkar
            if lesson_area:
                new_points = max(0, user_data['categories'][lesson_area][lesson] - points)  # Puanlar 0'ın altına düşemez
                user_data['categories'][lesson_area][lesson] = new_points
            else:
                new_points = max(0, user_data['categories']['independent'][lesson] - points)  # Puanlar 0'ın altına düşemez
                user_data['categories']['independent'][lesson] = new_points
            
            # Yeni seviyeyi hesapla
            new_level = self.level_system.calculate_lesson_level(new_points, area=lesson_area)
            
            # Verileri kaydet
            self.level_system.save_data()
            
            # Puan ve seviye bildirimini gönder
            if new_level < old_level:
                await ctx.send(f"{member.mention} {lesson} {points} kaybetti ({old_level} --> {new_level})")
            else:
                await ctx.send(f"{member.mention} {lesson} {points} kaybetti")
                
        except Exception as e:
            await ctx.send(f'Hata oluştu: {str(e)}')
        
    @commands.command(name='removepointsall')
    @commands.has_role('Moderator')
    async def removepointsall(self, ctx, member: discord.Member):
        """Bir kullanıcının tüm verilerini sıfırlar
        Kullanım: !removepointsall @kullanıcı"""
        try:
            # Kullanıcı verilerini al
            user_id = str(member.id)
            if user_id not in self.level_system.data['users']:
                await ctx.send(f"Hata: {member.mention} henüz hiç puan kazanmamış!")
                return
                
            user_data = self.level_system.data['users'][user_id]
            
            # Eski rolleri kaydet ve kaldır
            old_roles = []
            if user_data.get('main_area'):
                old_roles.append(user_data['main_area'])
            if 'unlocked_areas' in user_data:
                old_roles.extend(user_data['unlocked_areas'])
            if 'upper_areas' in user_data:
                old_roles.extend(user_data['upper_areas'].values())
                
            # Discord rollerini kaldır
            for role_name in old_roles:
                role = discord.utils.get(ctx.guild.roles, name=role_name)
                if role and role in member.roles:
                    await member.remove_roles(role)
            
            # Kullanıcının tüm verilerini sıfırla
            self.level_system.data['users'][user_id] = {
                'categories': {},
                'main_area': None,
                'upper_areas': {},
                'earned_rewards': [],
                'unlocked_areas': []
            }
            
            # Verileri kaydet
            self.level_system.save_data()
            
            await ctx.send(f"{member.mention} kullanıcısının tüm verileri sıfırlandı ve rolleri kaldırıldı!")
            
        except Exception as e:
            await ctx.send(f'Hata oluştu: {str(e)}')

    @commands.command(name='choosearea')
    async def choosearea(self, ctx):
        """İlk alanını seçer
        Kullanım: !choosearea"""
        try:
            user_id = str(ctx.author.id)
            
            # Kullanıcı verilerini al veya oluştur
            if user_id not in self.level_system.data['users']:
                self.level_system.data['users'][user_id] = {
                    'categories': {},
                    'main_area': None,
                    'upper_areas': {},
                    'earned_rewards': [],
                    'unlocked_areas': []
                }
                
            user_data = self.level_system.data['users'][user_id]
            
            # Eğer kullanıcının zaten bir alanı varsa
            if user_data.get('main_area'):
                await ctx.send(f"Hata: Zaten bir alana sahipsin ({user_data['main_area']})!")
                return
            
            # Alan seçim mesajını gönder
            area_emojis = {
                'Eclectic': '⚡',
                'Defender': '🛡️',
                'CareTaker': '🌿',
                'SoulMaster': '🔮'
            }
            
            area_descriptions = {
                'Eclectic': 'Büyü teorisi ve antik bilgilere odaklanan çok yönlü büyücüler.',
                'Defender': 'Savunma ve koruma büyülerine odaklanan güçlü koruyucular.',
                'CareTaker': 'Yaşam ve şifa büyülerine odaklanan şifacı büyücüler.',
                'SoulMaster': 'Karanlık sanatlar ve kehanet üzerine uzmanlaşan gizemli büyücüler.'
            }
            
            message_content = [
                f"{ctx.author.mention}, lütfen ana alanını seç!",
                "Her alan farklı derslere ve yeteneklere odaklanır:",
                ""  # Boş satır
            ]
            
            # Alanları ve açıklamalarını listele
            for area_name in area_emojis:
                message_content.append(f"{area_emojis[area_name]} **{area_name}**: {area_descriptions[area_name]}")
            
            message = await ctx.send("\n".join(message_content))
            
            # Emojileri ekle
            for emoji in area_emojis.values():
                await message.add_reaction(emoji)
            
            def check(reaction, user):
                return (user == ctx.author and 
                       str(reaction.emoji) in area_emojis.values())
            
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check)
                
                # Seçilen emojiyi alana çevir
                selected_area = None
                for area_name, emoji in area_emojis.items():
                    if str(reaction.emoji) == emoji:
                        selected_area = area_name
                        break
                
                if selected_area:
                    # Ana alanı ayarla
                    user_data['main_area'] = selected_area
                    self.level_system.save_data()
                    
                    # Discord rolü ekle
                    role = discord.utils.get(ctx.guild.roles, name=selected_area)
                    if role:
                        await ctx.author.add_roles(role)
                    
                    await ctx.send(f"🎉 Tebrikler {ctx.author.mention}! Artık bir {selected_area} büyücüsüsün!")
                    
            except TimeoutError:
                await message.clear_reactions()
                await ctx.send(f"{ctx.author.mention} alan seçimi için süre doldu! Tekrar dene: !choosearea")
                
        except Exception as e:
            await ctx.send(f'Hata oluştu: {str(e)}')

    @commands.command(name='checkrewards')
    async def checkrewards(self, ctx, member: discord.Member = None):
        """Kullanıcının kazandığı ödülleri gösterir
        Kullanım: !checkrewards veya !checkrewards @kullanıcı"""
        if member is None:
            member = ctx.author
            
        user_id = str(member.id)
        user_data = self.level_system.data['users'].get(user_id)
        
        if not user_data:
            await ctx.send(f"{member.mention} henüz hiç ödül kazanmamış!")
            return
            
        embed = discord.Embed(
            title=f"{member.name} Ödül Listesi",
            color=discord.Color.gold()
        )
        
        # Kazanılan ödülleri göster
        earned_rewards = user_data.get('earned_rewards', [])
        if earned_rewards:
            # Sickle ödüllerini topla
            total_sickles = 0
            special_rewards = []
            
            for reward in earned_rewards:
                if isinstance(reward, str) and "sickle" in reward.lower():
                    try:
                        sickle_amount = int(''.join(filter(str.isdigit, reward)))
                        total_sickles += sickle_amount
                    except ValueError:
                        special_rewards.append(reward)
                else:
                    special_rewards.append(reward)
            
            # Ödülleri gruplar halinde göster
            reward_chunks = []
            current_chunk = []
            current_length = 0
            
            # Önce toplam sickle miktarını ekle
            if total_sickles > 0:
                current_chunk.append(f"• Toplam {total_sickles} Sickle\n")
                current_length += len(current_chunk[-1])
            
            # Sonra özel ödülleri ekle
            for reward in special_rewards:
                reward_line = f"• {reward}\n"
                if current_length + len(reward_line) > 1000:  # Biraz margin bırak
                    reward_chunks.append(current_chunk)
                    current_chunk = []
                    current_length = 0
                current_chunk.append(reward_line)
                current_length += len(reward_line)
            
            if current_chunk:
                reward_chunks.append(current_chunk)
            
            # Her chunk için yeni bir alan oluştur
            for i, chunk in enumerate(reward_chunks, 1):
                field_name = "🏆 Kazanılan Ödüller" if i == 1 else f"🏆 Kazanılan Ödüller (Devam {i})"
                embed.add_field(
                    name=field_name,
                    value="".join(chunk),
                    inline=False
                )
        else:
            embed.add_field(
                name="🏆 Kazanılan Ödüller",
                value="Henüz hiç ödül kazanılmamış!",
                inline=False
            )
            
        await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(LevelCommands(bot)) 