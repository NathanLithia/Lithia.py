from discord.ext import commands
import asyncio
import discord
import datetime
import os

class dmlog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.log_direct_messages = True
        self.log_guild_messages = False


    def quickwrite(self, path, data):
        filename = path
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(data)


    def log_direct_message(self, message):
        self.quickwrite(f"./cogs/dmlogger/dm/{message.author.id}.log", f"\n[{datetime.datetime.utcnow()}][{message.author.name}]: {message.content}.")

    def log_guild_message(self, message):
        self.quickwrite(f"./cogs/dmlogger/guild/{message.author.guild.id}/{message.channel.id}.log", f"\n[{datetime.datetime.utcnow()}][{message.author.name}]: {message.content}.")


    @commands.Cog.listener()
    async def on_message(self, message):
        if self.log_direct_messages == True:
            if message.guild == None:
                self.log_direct_message(message)
        if self.log_guild_messages == True:
            if message.guild != None:
                self.log_guild_message(message)


def setup(client):
    client.add_cog(dmlog(client))
