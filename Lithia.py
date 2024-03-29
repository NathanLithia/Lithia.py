import sys
import os
sys.path.insert(1, './packages')

import discord, asyncio, os, sys, traceback
from discord.ext import commands

TokenPath = "./auth.token"

def get_token():
    print("https://discord.com/developers")
    



def get_prefix(client, message):
    """A callable Prefix for our client."""
    if not message.guild:
        return '<'
    return commands.when_mentioned_or(*client.prefixes)(client, message)


client = commands.Bot(command_prefix=get_prefix, description='https://github.com/NathanLithia/Lithia.py')


@client.event
async def on_ready():
    if not hasattr(client, 'appinfo'):
        client.appinfo = await client.application_info()
    for error in boot_errors:
        try:
            await client.fetch_user(client.appinfo.owner.id).send(error)
        except: print(f'Could relay error over discord.\n{error}')
    print(f'Logged in as: {client.user.name} - {client.user.id}\nVersion: {discord.__version__}')


@client.event
async def on_message(message):
    ctx = await client.get_context(message)

    #dont talk to self
    if ctx.author.id == client.user.id: return 
    #blacklist test
    if ctx.author.id == 132291947573280768 or ctx.author.id == 386291328629211147: return 

    try:
        await client.process_commands(message)
    except commands.CommandError as error:
        await on_command_error(ctx, error)
        

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound) and ctx.author.id == client.application.owner.id:
        await ctx.reply("**Invalid command. Try using** `help` **to figure out commands!**")
    if isinstance(error, commands.MissingRequiredArgument) and ctx.author.id == client.application.owner.id:
        await ctx.reply('**Please pass in all requirements.**')
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("**You dont have all the requirements or permissions for using this command :angry:**")
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply("**Command is on cooldown, Please dont spam it.**")


if __name__ == '__main__':
    boot_errors = []
    initial_extensions = []
    client.prefixes = ['<', '<<']
    for file in os.listdir(os.fsencode('./cogs/core')):
        filename = os.fsdecode(file)
        if filename.endswith(".cog") or filename.endswith(".py"): initial_extensions.append(str('cogs.core.'+str(filename)).replace('.py',''))
    for extension in initial_extensions:
        try: client.load_extension(extension)
        except Exception as e: boot_errors.append(f'`🔴{type(e).__name__}` - {e}')
    else:
        while True:
            try:
                with open (TokenPath, "r") as Token:
                    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
                    client.run(Token.readlines()[0])
            except FileNotFoundError:
                inputtoken = ""
                while inputtoken == "":
                    print("No Token was found. please generate one at https://discord.com/developers")
                    inputtoken = input("Please Enter your Client Token: ")
                    if inputtoken == "":
                        print("No Token Provided")
                    else:
                        f = open(TokenPath, "w")
                        f.write(inputtoken)
                        f.close()
            except discord.errors.LoginFailure:
                print("Token is invalid")
                os.remove(TokenPath)
                sys.exit(0)
            except Exception as e: 
                print(f"Unexpected {e=}, {type(e)=}")
                sys.exit(1)
