# Pyxgram

[Español](https://github.com/Borisd93/pyxgram/blob/main/README_ES.md)

A bit of history... Pyxgram was born when i create the [Reisub Bot](https://t.me/reisub_bot), my code it was very unreadable, but i have the idea of create a framework for fix my code and help the python community.

The pyxgram framework works thanks the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library, wich has a big comunity, but that library its hard to use for some people, but you can use the code of this library with update and context objects or self.dispatcher and self.updater

# More info

You can see the wiki here. [**Wiki**](https://github.com/Borisd93/pyxgram/wiki/).

# Examples

This is a code example for the people has no knowedge about this framework. Works in the 1.1 Versions or higher

```
from pyxgram.bot import Basebot

bot=Basebot('mytoken')

@bot.normal_command
def start(update,context):
  bot.send_text('Hello',update,context)

bot.start()
```

You need to replace the 'mytoken' string to your bot token

Other example, this only works in versions 1.2 or higher

```
from pyxgram import BaseBot

bot=BaseBot('mytoken')

@bot.normal_command
def start(update,context):
  bot.send_text('Hello',update,context)

bot.start()
```
