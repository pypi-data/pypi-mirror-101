import requests
import html
class void:
    def __init__(self, apikey):
        self.base_url = 'https://api.voidbots.net/bot'
        self.apikey = apikey
        
            
    
    def voteinfo(self, bot_id, user_id):
        req = requests.get(f'{self.base_url}/voted/{bot_id}/{user_id}', headers={'Authorization': self.apikey}).json()
        return req
    
    def botinfo(self, bot_id):
        req = requests.get(f'{self.base_url}/info/{bot_id}', headers={'Authorization': self.apikey}).json()
        return html.unescape(req)
    
    def postStats(self, bot_id, server_count: int, shard_count=None):
        req = requests.post(f'{self.base_url}/stats/{bot_id}',
                           headers={'Authorization': self.apikey}, json={'server_count': server_count, 'shard_count': shard_count or 0}).json()
        return req
    
    def botanalytics(self, bot_id):
        req = requests.get(f'{self.base_url}/analytics/{bot_id}', headers={'Authorization': self.apikey}).json()
        
        return req
        
    def botreviews(self, bot_id):
        req = requests.get(f'{self.base_url}/reviews/{bot_id}', headers={'Authorization': self.apikey}).json()
        return req
