import discord
from discord.ext import commands
import random
import os

# Botu başlatıyoruz
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Yeni üyeler için izin veriyoruz
bot = commands.Bot(command_prefix="!", intents=intents)

# Kullanıcıların To-Do listelerini tutmak için bir dictionary (sözlük)
todo_list = {}

# Çevre dostu görevler
tasks = [
    "Işıkları kapattın mı?",
    "Plastik kullanımını azalttın mı?",
    "Su tasarrufu sağlamak için duş süreni kısalttın mı?",
    "Geri dönüşüm kutusunu doğru ayırdın mı?",
    "Yeniden kullanılabilir alışveriş çantası kullandın mı?",
]

# Hayvanlar ve plastik atıklardan zarar görenler (örnek)
endangered_animals = [
    "Bir deniz kaplumbağası, plastiği yediği için boğulmuş.",
    "Bir kuş, plastik torbalardan dolayı açlık çekiyor ve kanatları hasar gördü.",
    "Bir yunus, denizlerdeki plastik çöpler yüzünden hastalanmış ve yaşam alanı daralmış.",
    "Bir deniz kuytusu, plastiği yuttuğu için sağlığı bozulmuş ve hayatta kalmakta zorlanıyor.",
    "Bir balina, denizlerdeki plastik atıklar nedeniyle ölüm riskiyle karşı karşıya."
]

# !todo komutu (To-Do List)
@bot.command()
async def todo(ctx):
    user_id = ctx.author.id
    if user_id not in todo_list:
        todo_list[user_id] = [False] * len(tasks)  # Kullanıcıya ait görevler (hepsi False)

    response = "**Çevre Dostu To-Do List'iniz:**\n"
    for i, task in enumerate(tasks):
        status = "✅" if todo_list[user_id][i] else "❌"
        response += f"{status} {task}\n"

    await ctx.send(response)


# !yap komutu (Görev tamamla)
@bot.command()
async def yap(ctx, task_num: int):
    user_id = ctx.author.id
    if user_id not in todo_list:
        todo_list[user_id] = [False] * len(tasks)

    if 1 <= task_num <= len(tasks):
        todo_list[user_id][task_num - 1] = True
        await ctx.send(f"✅ {tasks[task_num - 1]} görevini tamamladın!")
    else:
        await ctx.send("Lütfen geçerli bir görev numarası girin.")


# $hayvan komutu (Plastiklerden zarar gören hayvanlar)
@bot.command()
async def hayvan(ctx):
    animal_fact = random.choice(endangered_animals)
    await ctx.send(f"💔 {animal_fact}")


@bot.command(name="images")
async def images(ctx):
    folder_path = 'images'  # Resimlerin olduğu klasör
    try:
        # Klasördeki dosyaları listele
        files = os.listdir(folder_path)
        if not files:
            await ctx.send("Klasörde hiç dosya yok!")
            return

        # Rastgele bir dosya seç
        img_name = random.choice(files)
        img_path = os.path.join(folder_path, img_name)

        # Dosyayı gönder
        with open(img_path, 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)

    except Exception as e:
        # Hata mesajı gönder
        await ctx.send(f"Bir hata oluştu: {e}")


# Bot hazır olduğunda her sunucuya mesaj gönder
@bot.event
async def on_ready():
    for guild in bot.guilds:
        # Sunucudaki sistem kanalından mesaj gönderiyoruz
        if guild.system_channel:
            await guild.system_channel.send(
                f"Hoş geldin! To Do List'e ulaşmak için '!todo' yazınız, "
                f"hayvan resimlerine ulaşmak için '!images' yazınız, insanlara yapılan kirlilikten dolayı "
                f"hayvanlara verilen zararı görmek için '!hayvan' yazınız."
            )

bot.run('ENTER TOKEN')
