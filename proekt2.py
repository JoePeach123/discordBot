import sqlite3
import discord
import time
from googletrans import Translator
from random import randint

import discord.utils
from discord.ext import commands



intents = discord.Intents.default()
intents.members = True
intents.message_content = True
badWords2=['пидор','пидорас', 'пидрилкин',
           'блять','блядина','блядота','хуесос','выблядок','уебки','уебок']
        
badWords=['бля','пидор','хуй','хер','пидорас','пидрила','пидоры','пидорасина','уебан']

db=sqlite3.connect('discordServerCasino.db')
sql=db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS users(
login TEXT,
cash BIGINT,
id INT
)""")
db.commit()

db1=sqlite3.connect('discordUsers.db')
sql1=db1.cursor()
sql1.execute("""CREATE TABLE IF NOT EXISTS badwords(
login TEXT,
id TEXT,
amount INT,
words INT
)""")
db1.commit()

def adduser(message: discord.Message):
    sql1.execute(f"INSERT INTO badwords VALUES (?,?,?,?)", (message.author.name,message.author.id,5,1))
    db1.commit()

async def editrole(message: discord.Message):
    s=[1165687202852909098,1165687700985237604,1165687993642778696,1165688157975617596]
    sql1.execute(f"SELECT words FROM badwords WHERE id={message.author.id}")
    words=sql1.fetchone()[0]
    if words>=5 and words<7:
        #print(f'Выдаю роль "Общительный" ')
        role=discord.utils.get(message.author.guild.roles, id=1165687202852909098)
        await message.author.remove_roles(role)
        role = discord.utils.get(message.author.guild.roles, id=1165687700985237604)
        await message.author.add_roles(role)
    elif words>=10 and words<12:
        #print(f'Выдаю роль "Бывалый"')
        role = discord.utils.get(message.author.guild.roles, id=1165687700985237604)
        await message.author.remove_roles(role)
        role = discord.utils.get(message.author.guild.roles, id=1165687993642778696)
        await message.author.add_roles(role)
    elif words>=15 and words<17:
        #print(f'Выдаю роль "Ветеран чата"')
        role = discord.utils.get(message.author.guild.roles, id=1165687993642778696)
        await message.author.remove_roles(role)
        role = discord.utils.get(message.author.guild.roles, id=1165688157975617596)
        await message.author.add_roles(role)



def badword(message: discord.Message):
    sql1.execute(f"SELECT amount FROM badwords WHERE id={message.author.id}")
    am=sql1.fetchone()[0]
    sql1.execute(f"UPDATE badwords SET amount={am-1} WHERE id={message.author.id}")
    db1.commit()


async def check(message: discord.Message):
    checker=False
    x=message.content.lower()
    s=''
    for i in x:
        if i.islower():
            s+=i
        elif i=='0' or i=='o':
            s+='о'
        else:
            s+=' '
    s=s.split()
    for i in badWords2:
        if message.content.lower().__contains__(i) and not(message.author.id==bot.user.id):
            checker=True
            break
    for i in s:
        for j in badWords:
            if i==j:
                checker=True
                break
    if checker:
        sql1.execute(f"SELECT id FROM badwords WHERE id={message.author.id}")
        #await message.author.send('Плохое слово')
        await message.delete(delay=0.2)
        if sql1.fetchone() == None:
            adduser(message)
            sql1.execute(f"SELECT amount FROM badwords WHERE id ={message.author.id}")
            await message.author.send(f"Не матерись! Мут будет после еще {sql1.fetchone()[0]} подобных слов! ")
        else:
            sql1.execute(f"SELECT amount FROM badwords WHERE id ={message.author.id}")
            am=sql1.fetchone()[0]
            if am<=1:
                sql1.execute(f"UPDATE badwords SET amount={5} WHERE id={message.author.id}")
                db1.commit()
                role = discord.utils.get(message.author.guild.roles, id=1164680179315126352)
                await message.author.add_roles(role)
                await message.author.send('Ты получаешь мут за плохие слова. (Пиши модераторам для снятия мута)')

            else:
                badword(message)
                sql1.execute(f"SELECT amount FROM badwords WHERE id ={message.author.id}")
                await message.author.send(f"Не матерись! Мут будет после еще {sql1.fetchone()[0]} подобных слов! ")
    else:
        sql1.execute(f"SELECT id FROM badwords where id={message.author.id}")
        if sql1.fetchone()==None:
            adduser(message)


'''
async def check1(message: discord.Message):
    for i in badWords2:
        if message.content.lower().__contains__(i) and not(message.author.id==bot.user.id):
            await message.author.send('Плохое слово')
            await message.delete(delay=0.2)
            break
'''

async def banblyat(message: discord.Message):
    await message.reply('тебе бан',mention_author=True)
    time.sleep(4)
    
    await message.author.kick(reason=None)
    await message.channel.send('Пользователь забанен. Чат сейчас под запретом')



bot=commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    #await bot.get_channel(1053016753082486906).send(f'Бот {bot.user} запущен')
    #print('Бот {bot.user}({bot.user.id}) успешно запущен.')
    await bot.get_channel(1053016753082486906).send('Что-бы узнать команды бота напиши !all_commands')
    print('Что-бы узнать команды бота напиши !all_commands')
    print('-------------------------------------------------')

# Новичок 1165687202852909098
# Общительный 1165687700985237604
# Бывалый 1165687993642778696
# Ветеран чата 1165688157975617596

@bot.event
async def on_member_join(member):
    await bot.get_channel(1087758591907348540).send(f'Пользователь  *{member.name}* влетел на сервер! :smiley:',mention_author=True)
    await member.send('Добро пожаловать на сервер. :grinning:\n'
                      'Напиши !all_commands что-бы узнать команды.')

    role = discord.utils.get(member.guild.roles, id=1165687202852909098)
    await member.add_roles(role)

@bot.event
async def on_message(message: discord.Message):
    sec=time.time()
    dat=time.ctime(sec)
    mes=f"<{dat}><{message.channel}><{message.author.id}({message.author.name})>:{message.content}"


    print(mes)
    with open ('discord_message_logs.txt','a+') as file:
        file.write(f'{mes}\n')

    if message.content.lower().__contains__('бот привет'):
        if not(message.author.id==bot.user.id):
            await message.reply('Привет браток.',mention_author=True)

    if message.content.lower().__contains__('бот лох'):
        if not(message.author.id==bot.user.id):
            role = discord.utils.get(message.author.guild.roles, id=1164668723228049509)
            if message.author.get_role(1164668723228049509):
                await message.reply('Ты уже петух')
            else:
                await message.author.add_roles(role)
                await message.reply(f'Вам добавлена роль "Petushara" :chicken: ')

            
            '''
    for i in badWords:
        if message.content.lower().__contains__(i) and not(message.author.id==bot.user.id):
            await message.channel.send('Слово плохо')
            await message.author.edit(nick='Нарушитель чата')
            time.sleep(1)
            await message.delete(delay=None,reason=None)
            await message.channel.send('Теперь ты нарушитель.')
            time.sleep(1)
            '''
    if not(message.author.id==bot.user.id):
        await check(message)

    if not(message.author.id==bot.user.id):
        sql1.execute(f"SELECT words FROM badwords WHERE id={message.author.id}")
        x = sql1.fetchone()[0]
        sql1.execute(f"UPDATE badwords SET words={x + 1} WHERE id={message.author.id}")
        db1.commit()

    if not(message.author.id==bot.user.id):
        await editrole(message)





    await bot.process_commands(message)

@bot.command()
async def casino(message: discord.Message):
    await message.reply\
        ('Все команды казика на данный момент:\n'
         '-------------------------\n'
         '!reg (регистрация в казино)\n'
         '!play *ставка* (50 на 50)\n'
         '!givemoney *сумма* (выдает тебе кэш)\n'
         '!balance (показывает твой текущий баланс)\n'
         '!cboard (таблица игроков)\n'
         '!kubik *ставка* (шанс 20% и x4 множ.)\n'
        )


@bot.command()
async def cboard(message: discord.message):

    sql.execute(f"SELECT login FROM users")
    for i in sql.execute(f"SELECT * FROM users"):
        await message.channel.send(f'Ник: {i[0]}, Баланс: {i[1]}')


@bot.command()
async def reg(message: discord.Message):
    sql.execute(f"SELECT id FROM users WHERE id ={message.author.id}")
    if sql.fetchone() is None:
        await message.reply(f'Ты успешно зарегестрировал себя в казино. Твой стартовый баланс: 10000')
        sql.execute(f"INSERT INTO users VALUES (?,?,?)", (message.author.name, 10000,message.author.id))
        db.commit()
    else:
        await message.reply(f'Ты уже зарегестрирован в Casino.')

@bot.command()
async def roll(message: discord.Message):
    await message.reply(randint(0,100))

@bot.command()
async def play(message: discord.message, stavka: int):
    sql.execute(f"SELECT id FROM users WHERE id ={message.author.id}")
    if sql.fetchone() is None:
        await message.reply('Ты не зарегестрирован. Напиши !reg что-бы это сделать.')
    else:
        sql.execute(f"SELECT cash FROM users WHERE id={message.author.id}")
        balance=sql.fetchone()[0]
        casik=randint(1,2)
        if balance>0:
            if casik==1:
                sql.execute(f"UPDATE users SET cash={balance+stavka} WHERE id={message.author.id}")
                db.commit()
                await message.reply(f'Ты выйграл {stavka}  :money_mouth:. Твой баланс теперь: {balance+stavka}. ')
            else:
                sql.execute(f"UPDATE users SET cash={balance-stavka} WHERE id={message.author.id}")
                db.commit()
                await message.reply(f'Ты проиграл {stavka}  :worried:. Твой баланс теперь: {balance-stavka} ')
        else:
            await message.reply(f'Недостаточно средств.')

@bot.command()
async def givemoney(message: discord.message, money: int):
    limit=50000
    sql.execute(f"SELECT id FROM users WHERE id ={message.author.id}")
    if sql.fetchone() is None:
        await message.reply('Ты не зарегестрирован. Напиши !reg что-бы это сделать.')
    else:
        if money<0:
            await message.reply(f'Недопустимое значение.')
        else:
            if money>limit:
                await message.reply(f'Слишком большая сумма. Лимит: {limit}')
            else:
                sql.execute(f"SELECT cash FROM users WHERE id={message.author.id}")
                balance=sql.fetchone()[0]
                sql.execute(f"UPDATE users SET cash={balance+money} WHERE id={message.author.id}")
                db.commit()
                await message.reply(f'На твой счёт добавлено: {money} :moneybag:.')

@bot.command()
async def buyvip(message: discord.Message):
    role = discord.utils.get(message.author.guild.roles, id=1167197192268816414)
    price=100000
    sql.execute(f"SELECT id FROM users WHERE id={message.author.id}")
    if sql.fetchone() is None:
        await message.reply('Ты не зарегестрирован. Напиши !reg что-бы это сделать.')
    else:
        if message.author.get_role(1167197192268816414):
            await message.author.reply(f"У вас уже есть VIP статус")
        else:
            sql.execute(f"SELECT cash FROM users WHERE id={message.author.id}")
            balance=sql.fetchone()[0]
            if balance<price:
                await message.author.send(f"Недостаточно средств")
            else:
                await message.author.add_roles(role)
                sql.execute(f"UPDATE users SET cash={balance-price} WHERE id={message.author.id}")
                db.commit()

@bot.command()
async def vip(message: discord.Message):
    await message.channel.send("Вип статус имеет:\nДоступ в отдельный канал\nРасширенные возможности\nЧто-бы купить, напиши !buyvip (цена 100000)")


@bot.command()
async def balance(message: discord.Message):
    sql.execute(f"SELECT id FROM users WHERE id ={message.author.id}")
    if sql.fetchone() is None:
        await message.reply('Ты не зарегестрирован. Напиши !reg что-бы это сделать.')
    else:
        sql.execute(f"SELECT cash FROM users WHERE id={message.author.id}")
        balance=sql.fetchone()[0]
        await message.author.send(f"Твой баланс сейчас: {balance} :moneybag:.")


@bot.command()
async def kubik(message: discord.Message, stavka: int):
    sql.execute(f"SELECT id FROM users WHERE id ={message.author.id}")
    if sql.fetchone() is None:
        await message.reply('Ты не зарегестрирован. Напиши !reg что-бы это сделать.')
    else:
        sql.execute(f"SELECT cash FROM users WHERE id={message.author.id}")
        balance=sql.fetchone()[0]
        kub1=randint(1,5)
        kub2=randint(1,5)
        if kub1==kub2:
            await message.reply(f"Ты выйграл: {stavka*4} :moneybag:")
            sql.execute(f"UPDATE users SET cash={balance+stavka*4} WHERE id={message.author.id}")
            db.commit()
        else:
            await message.reply(f"Ты проиграл: {stavka} :pensive:")
            sql.execute(f"UPDATE users SET cash={balance-stavka} WHERE id={message.author.id}")
            db.commit()
'''
@bot.command()
async def gif1(ctx: commands.Context):
    await ctx.send('https://tenor.com/view/%D0%B8%D0%B4%D0%B8%D0%BD%D0%B0%D1%85%D1%83%D0%B9-%D0%BF%D1%83%D0%B4%D0%B6-%D0%B8%D0%B4%D0%B8%D0%BD%D0%B0%D1%85%D1%83%D0%B9%D0%B4%D0%BE%D1%82%D0%B0-%D0%B8%D0%B4%D0%B8%D0%BD%D0%B0%D1%85%D1%83%D0%B9%D0%BF%D1%83%D0%B4%D0%B6-%D0%B8%D0%B4%D0%B8%D0%BD%D0%B0%D1%85%D1%83%D0%B9pudge-gif-26100509')
'''
@bot.command()
async def all_commands(ctx: commands.Context):
    await ctx.send('Все команды на данный момент:\n'
                   ' -------------------------\n'
                   #'!gif1\n'
                   '!lucky *ваш шанс везения*\n'
                   '!chancer (шанс) (нужно удачных раз)\n'
                   #'!capibara\n'
                   '!nickname *ник* (цена 100000)\n'
                   #'!badwords\n'
                   '!casino *команды казино*\n'
                   '!roll\n'
                   '!vip\n'
                   '!eng (текст) переводит на Английский язык\n'
                   '!rus (text) translating your text to Russian\n'
                    )

        
@bot.command()
async def lucky(message: discord.Message, chancee):
    chance=''
    ch=False
    for i in chancee:
        if i.isdigit():
            chance+=str(i)
        else:
            ch=True
    if ch==False:
        if (int(chance)<0) or (int(chance)>100):
            await message.reply(f'Недопустимое значение для шанса: ( Шанс: {chance}% ). :pensive:')
        else:
            await message.channel.send('Крутим... :robot: ')
            time.sleep(2)
            x=randint(1,100)
            if x<=int(chance):  
                await message.reply(f'Тебе повезло! :smiley: ( Шанс: {chance}% )',mention_author=True)
            else:
                await message.reply(f'Тебе не повезло. :worried:  ( Шанс: {chance}% )',mention_author=True)
    else:
        await message.reply(f'Пиши числа!!  :angry:')


@bot.command()
async def eng(ctx,*,arg: str):
    google=Translator()
    result=google.translate(text=arg,dest='en')
    await ctx.send(f' Translated text:   {result.text}')

@bot.command()
async def rus(ctx,*,arg: str):
    google=Translator()
    result=google.translate(text=arg,dest='ru')
    await ctx.send(f' Переведенный текст:   {result.text}')


@bot.command()
async def chancer(ctx: commands.Context,chance: int,am: int):
    if am>1000000:
        await ctx.send('Слишком огромное значение. :pensive:')
    else:
        k=0
        r=0
        if not(chance <=0):
            while not(k==am):
                x=randint(1,100)
                if x<=chance:
                    k+=1
                    r+=1
                else:
                    r+=1
            await ctx.send(f'До скольки идти: {am}')
            await ctx.send(f'Понадобилось попыток: {r}')
            await ctx.send(f'Твой шанс: {chance}')
        else:
            await ctx.send('Недопустимое число. :pensive:')
'''
@bot.command()
async def capibara(ctx: commands.Context):
    await ctx.send('https://sun9-85.userapi.com/impg/LpMARmE1tzmucwzyqjbUo8S9HPZ2WbFWXnvnDw/Aea0jp3dnxE.jpg?size=1042x1312&quality=95&sign=0bafd5787d8461d5107626b67e0e10fe&type=album')
    await ctx.send('https://sun9-24.userapi.com/impg/hdVbAEE4Sg779ToQHpxNqSTEF5XwLb2pkBjvuA/eJc9tZdHJG8.jpg?size=696x697&quality=95&sign=0fb4808fbc001bd93d58ecbdf27dc9e0&type=album')
'''

@bot.command()
async def nickname(message: discord.Message, ni: str):
    sql.execute(f"SELECT id FROM users WHERE id={message.author.id}")
    if sql.fetchone() == None:
        await message.author.send('Тебя нету в системе казино, напиши !reg')
    else:
        sql.execute(f"SELECT cash FROM users WHERE id={message.author.id}")
        balance = sql.fetchone()[0]
        if balance<100000:
            await message.author.send('Недостаточно средств.')
        else:
            sql.execute(f"UPDATE users SET cash={balance-100000} WHERE id={message.author.id}")
            db.commit()
            await message.author.edit(nick=ni)
            await message.author.send('Ник изменен.')
'''
@bot.command()
async def badwords(message: discord.Message):
    await message.author.send('Запрещенные слова: ')
    await message.author.send(badWords)
    await message.author.send(badWords2)
'''

bot.run('token')


# https://discord.gg/DXADAQySUA

# py -3 -m pip install -U py-cord --pre
