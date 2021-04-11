import discord
import asyncio
import json
import random
import os
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import requests

client = discord.Client()



with open('data.json', 'r') as f:
    data = json.load(f)

with open('coin.json', 'r') as f:
    coin = json.load(f)





@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Game('김민수'))

@client.event
async def on_message(message):

    if message.author.bot:
        return None

    if message.content.startswith("제리야"):
        if str(message.author.id) not in coin:
            coin[str(message.author.id)] = [500000, 0, 0]
        if message.content[4:] == "":
            async with message.channel.typing():
                await asyncio.sleep(0.07)
            await message.channel.send('🤔')
        else:
            vote = message.content[4:].split(" ")
            a = vote[0]

        if a == "도움":
            embed = discord.Embed(title="정찰목록", description="-제리", color=0xFFE400)
            embed.add_field(name="제리야 배워", value="사용법:```제리야 배워 (단어)/(뜻)```\n단어에는 띄어쓰기를 사용할수 없어요.", inline=True)
            embed.add_field(name="제리야 코인", value="사용법:```제리야 종목```\n종목들을 한번에 확인하세요!", inline=True)
            await message.channel.send(embed=embed)

        elif a == "배워":
            i = message.content[7:].split("/")
            if i[0] in data:
                data[i[0]].append(i[1])
                coin[str(message.author.id)][0] += 300
            else:
                data[i[0]] = [i[1]]
                coin[str(message.author.id)][0] += 300

            await message.channel.send("아주~ 잘 배웠음")

        elif a == "디버깅":
            await message.channel.send(data[vote[1]])
            for i in data:
                print(i)

        elif a == "개발자":
           if message.author.id ==  507504723184844813:
                if vote[1] == "삭제":
                   i = message.content[11:].split("/")
                   await message.channel.send("`" + str(data[i[0]]) + "`1에서 `" + i[1] + "`삭제")
                   data[i[0]].remove(i[1])
                if vote[1] == "삭제2":
                    i = message.content[12:]
                    await message.channel.send(i)
                    del data[i]

        elif a == "종목":
            embed = discord.Embed(title="종목", description="자산 : " + str(coin[str(message.author.id)][0]), color=0xFFE400)
            embed.add_field(name="톰코인", value=str(coin["coin"]), inline=True)
            embed.add_field(name="제리전자", value=str(coin["coin2"]), inline=True)
            await message.channel.send(embed=embed)

        elif a == "톰코인":
            try:
                if vote[1] == "매수":
                    if coin[str(message.author.id)][0] >= coin["coin"] * int(vote[2]):
                        coin[str(message.author.id)][0] -= coin["coin"] * int(vote[2])
                        coin[str(message.author.id)][1] += int(vote[2])

                
                if vote[1] == "매도":
                    if coin[str(message.author.id)][1] >= int(vote[2]):
                        coin[str(message.author.id)][0] += coin["coin"] * int(vote[2])
                        coin[str(message.author.id)][1] -= int(vote[2])

            except IndexError:
                pass

            embed = discord.Embed(title="톰코인", description="현재가 : " + str(coin["coin"]), color=0xFFE400)
            embed.add_field(name="총평가", value=str(coin["coin"] * coin[str(message.author.id)][1]), inline=True)
            embed.add_field(name="자산", value=str(coin[str(message.author.id)][0]), inline=True)
            embed.add_field(name="매도가능", value=str(coin[str(message.author.id)][1]), inline=True)
            await message.channel.send(embed=embed)

        elif a == "제리전자":
            try:
                if vote[1] == "매수":
                    if coin[str(message.author.id)][0] >= coin["coin2"] * int(vote[2]):
                        coin[str(message.author.id)][0] -= coin["coin2"] * int(vote[2])
                        coin[str(message.author.id)][2] += int(vote[2])

                
                if vote[1] == "매도":
                    if coin[str(message.author.id)][2] >= int(vote[2]):
                        coin[str(message.author.id)][0] += coin["coin2"] * int(vote[2])
                        coin[str(message.author.id)][2] -= int(vote[2])

            except IndexError:
                pass

            embed = discord.Embed(title="제리전자", description="현재가 : " + str(coin["coin2"]), color=0xFFE400)
            embed.add_field(name="총평가", value=str(coin["coin2"] * coin[str(message.author.id)][1]), inline=True)
            embed.add_field(name="자산", value=str(coin[str(message.author.id)][0]), inline=True)
            embed.add_field(name="매도가능", value=str(coin[str(message.author.id)][2]), inline=True)
            await message.channel.send(embed=embed)

        else:
            if a in data:
                await message.channel.send(data[a][random.randrange(0, len(data[a]))])
                coin[str(message.author.id)][0] += 100
                

    with open('data.json', 'w') as f:
        json.dump(data, f, indent="\t")

    with open('coin.json', 'w') as f:
        json.dump(coin, f, indent="\t")

async def bt():
    await client.wait_until_ready()

    while not client.is_closed():

        if random.choice([True, False]):
            coin["coin"] += 1000
            if random.choice([True, False]):
                coin["coin2"] += 500
                await client.change_presence(status=discord.Status.online, activity=discord.Game("톰코인 : " + str(coin["coin"]) + "↑\n제리전자 : " + str(coin["coin2"]) + "↑"))
            else:
                if coin["coin2"] != 0:
                    coin["coin2"] -= 500
                    await client.change_presence(status=discord.Status.online, activity=discord.Game("톰코인 : " + str(coin["coin"]) + "↑\n제리전자 : " + str(coin["coin2"]) + "↓"))
        else:
            if coin["coin"] != 0:
                coin["coin"] -= 1000
            if random.choice([True, False]):
                coin["coin2"] += 500
                await client.change_presence(status=discord.Status.online, activity=discord.Game("톰코인 : " + str(coin["coin"]) + "↓\n제리전자 : " + str(coin["coin2"]) + "↑"))
            else:
                if coin["coin2"] != 0:
                    coin["coin2"] -= 500
                    await client.change_presence(status=discord.Status.online, activity=discord.Game("버섯코인 : " + str(coin["coin"]) + "↓\n티모전자 : " + str(coin["coin2"]) + "↓"))
    
        await asyncio.sleep(random.randrange(4, 6))













############




    if message.content.startswith('제리야 티어'):


        Name = message.content[4:len(message.content)]

        if Name == "":
            await message.channel.send("닉네임을 입력해주세요.")
        else:
            print(Name)

            req = requests.get('http://www.op.gg/summoner/userName='+Name)
            print(req)
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')

            Champ = [0,1,2,3,4]
            Champ_game = [0,1,2,3,4]
            Champ_ratio = [0,1,2,3,4]


            SoloRank = soup.find_all('div', {'class': 'TierRank'})
            SoloRank2 = str(SoloRank[0])[str(SoloRank[0]).find('TierRank">') + 10:str(SoloRank[0]).find('</div>')]


            Rank_Side = soup.find_all('div', {'class':'SideContent' })

            for side in Rank_Side:
                img = side.find('img')
                img_src = 'https:'+img['src']
            
            if len(SoloRank2) > 35:
                embed_default = discord.Embed(title="롤 전적검색", description="op.gg 를 활용한 전적 검색 봇입니다", color=0xd5d5d5)
                embed_default.add_field(name="닉네임:  "+Name, value="Unranked", inline=False)
                embed_default.set_thumbnail(url=img_src)
                embed_default.set_footer(text='CuriHuS LAB')
                await message.channel.send(embed=embed_default)

            else:

                # 2가 붙은 변수는 print 를 위한 str
                # Embed 구성을 위한 내용 추출
                SoloRank_LP = soup.find_all('span', {'class' : 'LeaguePoints'})
                print(SoloRank_LP)
                print(type(SoloRank_LP))
                SoloRank_LP2 = str(SoloRank_LP[0])[str(SoloRank_LP[0]).find('">') + 3:str(SoloRank_LP[0]).find('</span>')]
                SoloRank_wins = soup.find_all('span', {'class': 'wins'})
                SoloRank_wins2 = str(SoloRank_wins[0])[str(SoloRank_wins[0]).find('">') + 2:str(SoloRank_wins[0]).find('</span>')]
                SoloRank_losses = soup.find_all('span', {'class': 'losses'})
                SoloRank_losses2 = str(SoloRank_losses[0])[str(SoloRank_losses[0]).find('">') + 2:str(SoloRank_losses[0]).find('</span>')]
                SoloRank_winratio = soup.find_all('span', {'class': 'winratio'})
                SoloRank_winratio2 = str(SoloRank_winratio[0])[str(SoloRank_winratio[0]).find('">') + 5:str(SoloRank_winratio[0]).find('</span>')]

                # 주목할만한 챔피언 system
                for a in range(0,5):
                    Champion = soup.select('div.ChampionName')[a].text
                    Champ[a] = Champion.strip()
                    Champion_game = soup.select('div.Title')[a].text
                    Champ_game[a] = Champion_game.replace(" Played", "")
                    Champion_ratio = soup.select('div.WinRatio')[a].text
                    Champ_ratio[a] = Champion_ratio.strip()

                # 변수
                ChampList = []  # 20판 이상의 챔피언 등록
                Champ_ratio_Top = 0
                Champ_game_Top = 0
                Champ_index = 0

                for a in range(0,5):
                    if int(Champ_game[a]) > 20:
                        ChampList.append(a)
                    
                    if Champ[a] in ChampList: # 승률 높은 걸로 산출, 승률 같다면 판수 높은 걸로 산출
                        if Champ_ratio_Top == 0 or Champ_ratio[a] > Champ_ratio_Top:
                            Champ_ratio_Top = Champ_ratio[a]
                            Champ_game_Top = Champ_game[a]
                            Champ_index = a
                        elif Champ_ratio[a] == Champ_ratio_Top:
                            if Champ_game[a] > Champ_game_Top:
                                Champ_ratio_Top = Champ_ratio[a]
                                Champ_game_Top = Champ_game[a]
                                Champ_index = a
                            else:
                                continue

                        else:
                            continue
                    else:
                        continue
            
                # Embed 메시지 구성

                # 소환사 아이콘
                Player_image = soup.find_all('img',{'class' : 'ProfileImage'})
                Player_image = str(Player_image[0])[str(Player_image[0]).find('src="') + 5:str(Player_image[0]).find('"/>')]
                Player_image = str("https:"+ Player_image)


                embed = discord.Embed(title="", description="", color=0xd5d5d5)
                embed.set_author(name=Name +"님의 전적 검색", url="http://www.op.gg/summoner/userName="+Name, icon_url=Player_image)
                embed.add_field(name=SoloRank2+SoloRank_LP2, value= SoloRank_wins2 + "  " +SoloRank_losses2 + " | " +SoloRank_winratio2 , inline=True)
                embed.add_field(name="주목할 만한 챔피언", value= Champ[Champ_index] +" "+ Champ_game[Champ_index] +"게임  "+ Champ_ratio[Champ_index], inline= False)
                embed.set_thumbnail(url=img_src)
                embed.set_footer(text='CuriHuS LAB')


                # 메시지 보내기
                await message.channel.send(embed=embed)






client.run(os.environ['token'])
