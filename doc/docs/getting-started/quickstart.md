# Quick Start

---

before to quick start, If you have not created an teamly.one bot. Lets create it before the quick start guide:
[create your teamly bot](../create-your-teamly-bot)


First, we need to import the `teamly` package to access its functions and classes:

```python
import teamly
```

Next, create a Client instance for your bot.
This instance will be used to interact with the Teamly API and handle events.

```Python
import teamly

client = teamly.Client()
```

Now we’re ready to use the functions and events provided by our client instance.
Let’s start by defining the `on_ready` event — this event is triggered when the bot has successfully connected and is ready to operate.

```Python
import teamly

client = teamly.Client()

@client.event
async def on_ready():
    print('The bot is Ready to go')
```

After adding your event functions, you need to run the client to start the bot:

```Python
import teamly

client = teamly.Client()

@client.event
async def on_ready():
    print('The bot is Ready to go')

client.run('TOKEN')
```

Replace `TOKEN` with your actual API token from Teamly.
