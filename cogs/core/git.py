from discord.ext import commands
import zipfile
import json
import os
import urllib.request
import hashlib

class gitcog(commands.Cog):
    """Client Module Management"""
    def __init__(self, client):
        print("Initiating Git Module Manager.")

        self.client = client
        self.lastcog = None

        if os.path.exists("./cogs/core/git/") == False:
            os.mkdir("./cogs/core/git/")
            print("Created Git Data Directory.")
        if os.path.exists("./cogs/core/git/cache/") == False:
            os.mkdir("./cogs/core/git/cache/")
            print("Created Git Module Cache Directory.")
        if os.path.exists("./cogs/git/") == False:
            os.mkdir("./cogs/git/")
            print("Created Git Module Directory.")


    def RequestJson(self, URL, TimeOutInSeconds = 15):
        try:
            RequestedJson = json.loads(urllib.request.urlopen(URL, timeout=TimeOutInSeconds).read().decode("utf8"))
        except Exception as e:
            print(str(e))
            return e
        else:
            return RequestedJson


    def shahash(self, repository):
        RequestedJson = self.RequestJson(f"https://api.github.com/repos/{repository}/branches/main")
        return RequestedJson['commit']['sha']


    def download(self, url, save_path):
        print(f"Downloading: {save_path} from {url}")
        with urllib.request.urlopen(url) as dl_file:
            with open(save_path, 'wb') as out_file:
                out_file.write(dl_file.read())


    def unzipfile(self, filezip, path):
        print(f"Unzipping {filezip} to {path}.")
        with zipfile.ZipFile(filezip, 'r') as unzip:
            unzip.extractall(path)


    def clone(self, repository, save_path):
        url = f"https://github.com/{repository}/archive/refs/heads/main.zip"
        repohash = self.shahash(repository)
        #print(f"Cloning: {save_path} from https://github.com/{repository}\nHash: {repohash}")
        with urllib.request.urlopen(url) as dl_file:
            with open(save_path, 'wb') as out_file:
                try:
                    #sha1 = hashlib.sha1()
                    file = dl_file.read()
                    #sha1.update(('blob %u\0' % len(file)).encode('ascii'))
                    #sha1.update(file)
                    out_file.write(file)
                    print(f"Wrote: {save_path}")
                    #return sha1.hexdigest()
                except Exception as e: print(e)


    @commands.command(hidden=True, aliases=['install', 'git'])
    @commands.is_owner()
    async def install_cog(self, ctx, cog: str = None):
        """DEV"""
        if cog == None:
            return await ctx.send(f'``🔴GenericError`` - No Cog specified.')
        cogstring = cog.replace('/','@')
        if os.path.isfile(f'./cogs/core/git/{cogstring}.zip') == False:
            self.clone(cog, f'./cogs/core/git/{cogstring}.zip')
        else:
            print(f"{cog} already exists in cache. Skipping download.")
        archive = zipfile.ZipFile(f'./cogs/core/git/{cogstring}.zip', 'r')
        filetocheck = cog.split('/')[1]
        try:
            imgfile = archive.open(f'{filetocheck}-main/main.py')
        except KeyError: 
            return print(f"WARNING: <{cog}> has no main.py file. Skipping.")

        if os.path.exists(f"./cogs/core/git/{cog.split('/')[0]}/") == False:
            os.mkdir(f"./cogs/core/git/{cog.split('/')[0]}/")
            print(f"Created {cog.split('/')[0]} Directory.")

        self.unzipfile(f'./cogs/core/git/{cogstring}.zip', f"./cogs/git/{cog.split('/')[0]}")


def setup(client):
    client.add_cog(gitcog(client))