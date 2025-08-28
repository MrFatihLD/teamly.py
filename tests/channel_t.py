import teamly
import json

from dotenv import dotenv_values
config = dotenv_values(".env")

client = teamly.Client(enable_debug=True)


@client.event
async def on_ready():
    print("the bot is ready")




@client.event
async def on_channel(channel):
    print(json.dumps(channel.to_dict(), indent=4, ensure_ascii=False))

@client.event
async def on_channel_updated(channel):
    print(json.dumps(channel.to_dict(), indent=4, ensure_ascii=False))

@client.event
async def on_channel_deleted(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))



client.run(config["TEST_KEY"])
