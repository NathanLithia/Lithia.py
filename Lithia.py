import sys
sys.path.insert(1, './packages')

import discord, asyncio, os, sys, traceback
from discord.ext import commands


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
    # Allow us to reply to webhooks and other bots
    # please write a cooldown on this otherwise bad things will happen.
    ctx = await client.get_context(message)
    if ctx.valid: # Verify that the context has a command and can be used
        await client.invoke(ctx)


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
    with open ("./auth.token", "r") as Token:
        client.run(Token.readlines()[0])
