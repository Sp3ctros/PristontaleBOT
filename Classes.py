import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
import discord


file = open('Token.txt','r')
TOKEN = file.read()
file.close()


class Bosses:
    def __init__(self, nome, periodo, tempo_final,tempo_restante):
        self.nome = nome
        self.periodo = periodo
        self.tempo_final = tempo_final
        self.tempo_restante = tempo_restante
#atualiza o tempo restante para o boss nascer
def att_Timer():
    for m in lista_bosses:
        tempo_atual = datetime.datetime.now()
        if tempo_atual < m.tempo_final:
            m.tempo_restante = m.tempo_final - datetime.datetime.now()
        else:
            m.tempo_final = m.tempo_final + datetime.timedelta(hours=m.periodo)
#Pega os valores de referencia dos timers e cria um objeto da classe Bosses para cada um dos boss
def extrair_da_web():
    # Configurar o caminho para o driver do navegador
    webdriver_service = Service('chromedriver.exe')
    # Configurar as opções do navegador
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Executar o navegador em headless
    driver = webdriver.Chrome(service=webdriver_service, options=options)

    # Acessar o site desejado
    url = 'https://babel-pteu.netlify.app/'
    driver.get(url)

    time.sleep(3)
    # Extrair a informação desejada (nome dos bosses e o tempo restante para nascer)
    element = driver.find_elements(By.CLASS_NAME, "count-down")
    element2 = driver.find_elements(By.CLASS_NAME, "countdown-boss-name")
    #Itera cada um dos bosses e cria um objeto na classe Bosses para cada um.
    tempo_atual = datetime.datetime.now()
    for c, i in enumerate(element):
        hor = str(i.text)
        if len(hor) == 8:
            hora = float(hor[0:2])
            min = float(hor[3:5])
            sec = float(hor[6:7])
        tempo_final = tempo_atual + datetime.timedelta(hours=hora, minutes=min, seconds=sec)
        boss = Bosses(nome=element2[c].text,periodo=Periodo[c],tempo_final=tempo_final, tempo_restante=i.text)
        lista_bosses.append(boss)
    driver.quit()

lista_bosses = list()
#Período de nascimento de cada um dos bosses
Periodo = [1,2,2,3,3,3,3,4,4,4,6,6,6,12,12]

#Permissões necessárias do bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#detecta quando o bot é iniciado
@client.event
async def on_ready():
    print(f'{client.user} está online')

#Detecta quando tem alguma mensagem no chat e verifica se é algum comando.
@client.event  
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '!boss':
        #Adiciona no chat a tabela com o tempo dos bosses
        embed=discord.Embed(title="Timer dos bosses", color=0xFF5733)
        for d in lista_bosses:
            embed.add_field(name = '', value = f'**➤{d.nome} **: {str(d.tempo_restante)[:7]}', inline=False)
        embed.set_footer(text = f'Ultima atualização: {str(datetime.datetime.now())[:16]}')
        embed.set_image(url="https://static.subagames.com/PT1/images/guide/charinfo/priest1.jpg")
        msg = await message.channel.send(embed=embed)
        #Atualiza a tabela dos tempos uma certa quantidade de vezes
        for c in range(1000):
            att_Timer()
            embed=discord.Embed(title="Timer dos bosses", color=0xFF5733)
            for d in lista_bosses:
                    embed.add_field(name = '', value = f'**➤{d.nome} **: {str(d.tempo_restante)[:7]}', inline=False)
            embed.set_footer(text = f'Ultima atualização: {str(datetime.datetime.now())[:16]}\nJoão Lisboa')
            embed.set_image(url="https://static.subagames.com/PT1/images/guide/charinfo/priest1.jpg")
            await msg.edit(embed=embed)
            await asyncio.sleep(4)
        embed = discord.Embed(title="Timer Finalizado:", color=0xFF5733)
        await msg.edit(embed=embed)

    #Atualiza os valores de referencia para os timers.
    if message.content == '!upboss':
        extrair_da_web()

#EXTRAIR O TIMER DOS BOSSES E INICIAR O BOT
extrair_da_web()
client.run(TOKEN)
