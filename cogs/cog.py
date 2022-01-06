from discord.ext import commands
import discord

class cog_manager(commands.Cog):
    """Client Module Management"""
    def __init__(self, client):
        self.client = client
        self.lastcog = None


    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload_cog(self, ctx, *, cog: str):
        """Command which Unloads Modules."""
        if str(cog).startswith('cogs.') == False:
            cog = f'cogs.{cog}'
        try:
            self.client.unload_extension(cog)
            await ctx.reply(f'`🔽Unloaded_Cog:` {cog}')
        except Exception as e:
            await ctx.reply(f'`🔴{type(e).__name__}` - {e}')


    @commands.command(hidden=True, aliases=['reload', 'load'])
    @commands.is_owner()
    async def load_cog(self, ctx, *, cog: str = None):
        """Command which Loads and Reloads Modules."""
        if cog == None: 
            if self.lastcog == None: return await ctx.send(f'``🔴GenericError`` - Last known Cog is ``None``')
            cog = self.lastcog
        else: self.lastcog = cog
        if str(cog).startswith('cogs.') == False:
            cog = f'cogs.{cog}'
        try:
            self.client.unload_extension(cog)
            self.client.load_extension(cog)
            return await ctx.reply(f'`🔁Reloaded_Cog:` {cog}')  
        except Exception as e:
            if type(e).__name__ == 'ExtensionNotLoaded':
                try:
                    self.client.load_extension(cog)   
                    return await ctx.reply(f'`🔼Loaded_Cog:` {cog}')
                except Exception as e:
                    await ctx.reply(f'`🔴{type(e).__name__}` - {e}')
            else:
                await ctx.reply(f'`🔴{type(e).__name__}` - {e}')


    @commands.command(hidden=True, aliases=['enable', 'Enable'])
    @commands.is_owner()
    async def enable_cog(self, ctx, *, cog: str = None):
        """Enables a Disabled Cog."""
        pass


    @commands.command(hidden=True, aliases=['disable', 'Disable'])
    @commands.is_owner()
    async def disable_cog(self, ctx, *, cog: str = None):
        """Disables a Enabled Cog."""
        pass


def setup(client):
    client.add_cog(cog_manager(client))