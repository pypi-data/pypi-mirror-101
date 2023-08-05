
## Installation
`pip install voidbots`

## Documentation
To see the Doc [click here](https://docs.voidbots.net/).

Before using the pypi modules please view VoidBots api docs [Ratelimit](https://docs.voidbots.net/#/ratelimits) [Caching](https://docs.voidbots.net/#/caching)

## Example
```
import voidbots as vd
from discord.ext.commands import Bot

bot = Bot(command_prefix='vd!')
# Functions
Void = vd.VoidClient(bot, apikey='Your api key', autopost=True) #autopost is to autopost stats
awiat Void.voteinfo('A bot id','A user id')
await Void.botinfo('A bot id')
await Void.postStats(bot.user.id, len(bot.guilds), bot.shard_count or 0)
await Void.botanalytics(bot.user.id)
await Void.botreviews(bot.user.id)
await Void.widget(bot.user.id, theme='dark or light')
await Void.close() #To close autoposting
```