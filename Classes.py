import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
import discord
import asyncio


file = open('Token.txt','r')
TOKEN = file.read()
file.close()


class Bosses:
    def __init__(self, nome, boss_cycle, end_time,time_left):
        self.nome = nome
        self.boss_cycle = boss_cycle
        self.end_time = end_time
        self.time_left = time_left
        
#update the left time

def att_Timer():
    for m in lista_bosses:
        tempo_atual = datetime.datetime.now()
        if tempo_atual < m.end_time:
            m.time_left = m.end_time - datetime.datetime.now()
        else:
            m.end_time = m.end_time + datetime.timedelta(hours=m.boss_cycle)

#scrap the web for the time left and create objects for every boss
def extrair_da_web():
    webdriver_service = Service('chromedriver.exe')
    # load the settings of the webdriver and open it
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    driver = webdriver.Chrome(service=webdriver_service, options=options)

    # go to the site where the data is
    url = 'https://babel-pteu.netlify.app/'
    driver.get(url)

    asyncio.sleep(3)
    # search for the boss name and the time left
    web_time_left = driver.find_elements(By.CLASS_NAME, "count-down")
    bosses_name = driver.find_elements(By.CLASS_NAME, "countdown-boss-name")
    #iterate every boss and create a object for each one
    tempo_atual = datetime.datetime.now()
    for c, i in enumerate(web_time_left):
        hor = str(i.text)
        if len(hor) == 8:
            hora = float(hor[0:2])
            min = float(hor[3:5])
            sec = float(hor[6:7])
        end_time = tempo_atual + datetime.timedelta(hours=hora, minutes=min, seconds=sec)
        boss = Bosses(nome=bosses_name[c].text,boss_cycle=boss_cycle[c],end_time=end_time, time_left=i.text)
        lista_bosses.append(boss)
    driver.quit()

    
    
lista_bosses = list()
#bosses cycle
boss_cycle = [1,2,2,3,3,3,3,4,4,4,6,6,6,12,12]

#discord intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#detects when the bot is runing
@client.event
async def on_ready():
    print(f'{client.user} está online')

#detects a message on the chat and verifies if its a command or not
@client.event  
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '!boss':
        #insert on the chat the bosses timer.
        embed=discord.Embed(title="Timer dos bosses", color=0xFF5733)
        for d in lista_bosses:
            embed.add_field(name = '', value = f'**➤{d.nome} **: {str(d.time_left)[:7]}', inline=False)
        embed.set_footer(text = f'Ultima atualização: {str(datetime.datetime.now())[:16]}')
        embed.set_image(url="https://static.subagames.com/PT1/images/guide/charinfo/priest1.jpg")
        msg = await message.channel.send(embed=embed)
        #refresh the timers a range of times
        for c in range(1000):
            att_Timer()
            embed=discord.Embed(title="Timer dos bosses", color=0xFF5733)
            for d in lista_bosses:
                    embed.add_field(name = '', value = f'**➤{d.nome} **: {str(d.time_left)[:7]}', inline=False)
            embed.set_footer(text = f'Ultima atualização: {str(datetime.datetime.now())[:16]}\nJoão Lisboa')
            embed.set_image(url="https://static.subagames.com/PT1/images/guide/charinfo/priest1.jpg")
            await msg.edit(embed=embed)
            asyncio.sleep(4)
        embed = discord.Embed(title="Timer Finalizado:", color=0xFF5733)
        await msg.edit(embed=embed)

    #refresh the reference values.
    if message.content == '!upboss':
        extrair_da_web()

#extract the bosses timer and starts the bot
extrair_da_web()
client.run(TOKEN)
