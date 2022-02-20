from discord.ext import commands

class crypto(commands.Cog):
    """Lithia HWID Cryptographics Module"""
    def __init__(self, client):
        print("Initiating Cryptographics Module.")
        self.client = client

def setup(client):
    client.add_cog(crypto(client))