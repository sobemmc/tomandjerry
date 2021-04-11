import discord
import asyncio
import json
import random
import os

client = discord.Client()



with open('data.json', 'r') as f:
    data = json.load(f)

with open('coin.json', 'r') as f:
    coin = json.load(f)




tierScore = {
    'default' : 0,
    'iron' : 1,
    'bronze' : 2,
    'silver' : 3,
    'gold' : 4,
    'platinum' : 5,
    'diamond' : 6,
    'master' : 7,
    'grandmaster' : 8,
    'challenger' : 9
}
def tierCompare(solorank,flexrank):
    if tierScore[solorank] > tierScore[flexrank]:
        return 0
    elif tierScore[solorank] < tierScore[flexrank]:
        return 1
    else:
        return 2
warnings.filterwarnings(action='ignore')
bot = commands.Bot(command_prefix='!')

opggsummonersearch = 'https://www.op.gg/summoner/userName='

@bot.command()
async def test(ctx,arg):
    await ctx.send(arg)

@client.event
async def on_ready():
    await bt()

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




    #To user who sent message
    # await message.author.send(msg)
    print(message.content)
    if message.author == client.user:
        return

    if message.content.startswith("제리야 도움"):
        embed = discord.Embed(title="명령어 사용방법!", description="제리야 롤전적 (소환사 이름 - 띄어쓰기 붙여쓰기 상관없음)", color=0x5CD1E5)
        embed.set_footer(text='!SOBI#1919')
        await message.channel.send("도움말!", embed=embed)

    if message.content.startswith("제리야 롤전적"):
        try:
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(title="소환사 이름이 입력되지 않았습니다", description="", color=0x5CD1E5)
                embed.add_field(name="Summoner name not entered",
                                value="To use command 제리야 롤전적 : 제리야 롤전적 (Summoner Nickname)", inline=False)
                embed.set_footer(text='!SOBI#1919')
                await message.channel.send("Error : Incorrect command usage ", embed=embed)
            else:
                playerNickname = ''.join((message.content).split(' ')[1:])
                # Open URL
                checkURLBool = urlopen(opggsummonersearch + quote(playerNickname))
                bs = BeautifulSoup(checkURLBool, 'html.parser')



                Medal = bs.find('div', {'class': 'SideContent'})
                RankMedal = Medal.findAll('img', {'src': re.compile('\/\/[a-z]*\-[A-Za-z]*\.[A-Za-z]*\.[A-Za-z]*\/[A-Za-z]*\/[A-Za-z]*\/[a-z0-9_]*\.png')})



                mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})




                solorank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {'class': {'RankType', 'TierRank'}}))
                
                solorank_Point_and_winratio = deleteTags(
                    bs.findAll('span', {'class': {'LeaguePoints', 'wins', 'losses', 'winratio'}}))

                flexrank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {
                    'class': {'sub-tier__rank-type', 'sub-tier__rank-tier', 'sub-tier__league-point',
                              'sub-tier__gray-text'}}))

                flexrank_Point_and_winratio = deleteTags(bs.findAll('span', {'class': {'sub-tier__gray-text'}}))


                if len(solorank_Point_and_winratio) == 0 and len(flexrank_Point_and_winratio) == 0:
                    embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
                    embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,
                                    inline=False)
                    embed.add_field(name="Ranked Solo : Unranked", value="Unranked", inline=False)
                    embed.add_field(name="Flex 5:5 Rank : Unranked", value="Unranked", inline=False)
                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    embed.set_footer(text='!SOBI#1919')
                    await message.channel.send("소환사 " + playerNickname + "님의 전적", embed=embed)

   
                elif len(solorank_Point_and_winratio) == 0:

                    
                    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                    mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    FlexRankTier = flexrank_Types_and_Tier_Info[0] + ' : ' + flexrank_Types_and_Tier_Info[1]
                    FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + flexrank_Types_and_Tier_Info[-1]
                    embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
                    embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,
                                    inline=False)
                    embed.add_field(name="Ranked Solo : Unranked", value="Unranked", inline=False)
                    embed.add_field(name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
                    embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                    value="KDA : " + mostUsedChampionKDA + " / " + " WinRate : " + mostUsedChampionWinRate,
                                    inline=False)
                    embed.set_thumbnail(url='https:' + RankMedal[1]['src'])
                    embed.set_footer(text='!SOBI#1919')
                    await message.channel.send("소환사 " + playerNickname + "님의 전적", embed=embed)

                
                elif len(flexrank_Point_and_winratio) == 0:

                    
                    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                    mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    SoloRankTier = solorank_Types_and_Tier_Info[0] + ' : ' + solorank_Types_and_Tier_Info[1]
                    SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[
                        1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
                    embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
                    embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,
                                    inline=False)
                    embed.add_field(name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
                    embed.add_field(name="Flex 5:5 Rank : Unranked", value="Unranked", inline=False)
                    embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                    value="KDA : " + mostUsedChampionKDA + " / " + "WinRate : " + mostUsedChampionWinRate,
                                    inline=False)
                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    embed.set_footer(text='!SOBI#1919')
                    await message.channel.send("소환사 " + playerNickname + "님의 전적", embed=embed)
               
                else:
                    
                    solorankmedal = RankMedal[0]['src'].split('/')[-1].split('?')[0].split('.')[0].split('_')
                    flexrankmedal = RankMedal[1]['src'].split('/')[-1].split('?')[0].split('.')[0].split('_')

                    # Make State
                    SoloRankTier = solorank_Types_and_Tier_Info[0] + ' : ' + solorank_Types_and_Tier_Info[1]
                    SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[
                        1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
                    FlexRankTier = flexrank_Types_and_Tier_Info[0] + ' : ' + flexrank_Types_and_Tier_Info[1]
                    FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + " /" + flexrank_Types_and_Tier_Info[-1]

                    
                    mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[0]
                    mostUsedChampionWinRate = bs.find('div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    cmpTier = tierCompare(solorankmedal[0], flexrankmedal[0])
                    embed = discord.Embed(title="소환사 전적검색", description="", color=0x5CD1E5)
                    embed.add_field(name="Summoner Search From op.gg", value=opggsummonersearch + playerNickname,
                                    inline=False)
                    embed.add_field(name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
                    embed.add_field(name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
                    embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                    value="KDA : " + mostUsedChampionKDA + " / " + " WinRate : " + mostUsedChampionWinRate,
                                    inline=False)
                    if cmpTier == 0:
                        embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    elif cmpTier == 1:
                        embed.set_thumbnail(url='https:' + RankMedal[1]['src'])
                    else:
                        if solorankmedal[1] > flexrankmedal[1]:
                            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                        elif solorankmedal[1] < flexrankmedal[1]:
                            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                        else:
                            embed.set_thumbnail(url='https:' + RankMedal[0]['src'])

                    embed.set_footer(text='!SOBI#1919',)
                    await message.channel.send("소환사 " + playerNickname + "님의 전적", embed=embed)
        except HTTPError as e:
            embed = discord.Embed(title="소환사 전적검색 실패", description="", color=0x5CD1E5)
            embed.add_field(name="", value="올바르지 않은 소환사 이름입니다. 다시 확인해주세요!", inline=False)
            await message.channel.send("Wrong Summoner Nickname")

        except UnicodeEncodeError as e:
            embed = discord.Embed(title="소환사 전적검색 실패", description="", color=0x5CD1E5)
            embed.add_field(name="???", value="올바르지 않은 소환사 이름입니다. 다시 확인해주세요!", inline=False)
            await message.channel.send("Wrong Summoner Nickname", embed=embed)

        except AttributeError as e:
            embed = discord.Embed(title="존재하지 않는 소환사", description="", color=0x5CD1E5)
            embed.add_field(name="해당 닉네임의 소환사가 존재하지 않습니다.", value="소환사 이름을 확인해주세요", inline=False)
            embed.set_footer(text='!SOBI#1919')
            await message.channel.send("Error : Non existing Summoner ", embed=embed)

















client.run(os.environ['token'])
