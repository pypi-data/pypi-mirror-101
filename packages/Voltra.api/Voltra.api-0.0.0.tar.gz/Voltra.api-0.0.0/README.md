# Voltra.api



## Exmaple
``` 
from Voltra import VoltraClient

volt = VoltraClient(token="SID token")
#Functions
volt.get_channel(channel_id)
volt.get_user(user_id)
await volt.join_guild(guild_id) //Not working atm
```