import aiohttp, asyncio
import html
import discord
from asyncio.tasks import Task
class VoidClient:
    def __init__(self, bot: discord.Client, apikey: str, autopost: bool =False, **kwargs):
        self.base_url = 'https://api.voidbots.net/bot'
        self.apikey = apikey
        self.bot = bot
        self._autopost = autopost
        self.module_closed = False
        self.task_auto_post = Task
        self.loop = kwargs.get('loop', bot.loop)
        
        if self._autopost:
            self.task_auto_post = self.loop.create_task(self.__auto_post__())
        
        
    async def __auto_post__(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            try:
                await self.postStats(self.bot.user.id, len(self.bot.guilds), self.bot.shard_count)
            except Exception:
                pass
            await asyncio.sleep(210)
    
    async def voteinfo(self, bot_id: int, user_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.base_url}/voted/{bot_id}/{user_id}', headers={'Authorization': self.apikey}) as req:
                req = await req.json()
        return req
    
    async def botinfo(self, bot_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.base_url}/info/{bot_id}', headers={'Authorization': self.apikey}) as req:
                req = await req.json()
        return html.unescape(req)
    
    async def postStats(self, bot_id, server_count: int, shard_count: int=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.base_url}/stats/{bot_id}',
                                   headers={'Authorization': self.apikey}, json={'server_count': server_count, 'shard_count': shard_count or 0}) as req:
                req = await req.json()
        return req
    
    async def botanalytics(self, bot_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.base_url}/analytics/{bot_id}', headers={'Authorization': self.apikey}) as req:
                req = await req.json()
        return req
        
    async def botreviews(self, bot_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.base_url}/reviews/{bot_id}', headers={'Authorization': self.apikey}) as req:
                req = await req.json()
        return req
    
    async def widget(self, bot_id, theme='dark'):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://voidbots.net/api/embed/{bot_id}?theme={theme}') as req:
                req = await req.json()     
        return req.url
    
    async def close(self):
        if self.module_closed == True:
            return
        else:
            if self._autopost:
                self.task_auto_post.cancel()
            self.module_closed = True
