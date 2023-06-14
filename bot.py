import nextcord, asyncio
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

admins = [1234, 5678]

def getAcc():
    with open('acc.txt', 'r') as f:
        accounts = f.readlines()
        f.close()
    if len(accounts) == 0:
        return False
    account = accounts[0].replace("\n", "")
    accounts = [acc.strip() for acc in accounts if acc.strip() != account]
    with open('acc.txt', 'w') as file:
        file.write('\n'.join(accounts))
    return account

def checkCount():
    with open('acc.txt', 'r') as f:
        accounts = f.readlines()
        f.close()
    return len(accounts)

@bot.command() 
async def 젠(ctx):
    if ctx.channel.id != 1234:
        return await ctx.reply('**```css\n[ ⛔ ] 해당채널에서는 명령어를 사용할 수 없어요 !```**')
    acc = getAcc()
    if acc == False:
        return await ctx.reply('**```css\n[ ⛔ ] 재고가 없습니다 !```**')
    try:
        await ctx.author.send(f'**```css\n[ ✅ ] {acc}```**')
        await ctx.reply('**```css\n[ ✅ ] DM 을 확인해주세요 !```**')
    except:
        return await ctx.reply('**```css\n[ ⛔ ] DM 전송에 실패하였습니다 !```**')

@bot.command() 
async def 재고확인(ctx):
    if ctx.author.id in admins or ctx.channel.id == 1234:
        count = checkCount()
        return await ctx.reply(f'**```css\n[ ✅ ] 남은 재고는 {count}개 입니다 !```**')
    else:
        return await ctx.reply('**```css\n[ ⛔ ] 해당채널에서는 명령어를 사용할 수 없어요 !```**')
    
@bot.command() 
async def 재고추가(ctx):
    if not ctx.author.id in admins:
        return await ctx.reply('**```css\n[ ⛔ ] 당신은 해당 명령어를 사용할 수 없습니다 !```**')
    try:
        await ctx.author.send(f'**```css\n[ ✅ ] 재고를 줄바꿈을 통해 입력하여 주세요 !```**')
        await ctx.reply('**```css\n[ ✅ ] DM 을 확인해주세요 !```**')
    except:
        return await ctx.reply('**```css\n[ ⛔ ] DM 전송에 실패하였습니다 !```**')
    
    def check(msg):
        return (isinstance(msg.channel, nextcord.channel.DMChannel) and (ctx.author.id == msg.author.id))
    
    try:
        msg = await bot.wait_for("message", timeout=60, check=check)
        new_account = msg.content
        with open('acc.txt', 'r') as f:
            accounts = f.readlines()
            f.close()
        accountString = ''
        for a in accounts:
            acc = a.replace("\n", "")
            accountString += f'{acc}\n'
        accountString += new_account
        with open('acc.txt', 'w') as file:
            file.write(accountString)
            file.close()
        await ctx.author.send('**```css\n[ ✅ ] 성공적으로 재고를 추가하였습니다 !```**')
    except asyncio.TimeoutError:
        return await ctx.author.send('**```css\n[ ⛔ ] 시간이 초과되었습니다 !```**')
    
bot.run('')