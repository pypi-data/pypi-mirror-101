

## Example
```
import voidbots as vd

## functions
vd.void(apikey='Your api key') #do dir(vd.void) to see what in it, but theres vd.void(apikey='Your api key').voteinfo('A bot id','A user id')
vd.void(apikey='Your api key').botinfo('A bot id')
vd.void(apikey='Your api key').postStats(bot.user.id, len(bot.guilds), bot.shard_count or 0)
vd.void(apikey='Your api key').botanalytics(bot.user.id)
vd.void(apikey='Your api key').botreviews(bot.user.id)
```