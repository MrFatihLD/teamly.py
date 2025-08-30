import teamly
import json

from dotenv import dotenv_values
config = dotenv_values(".env")

client = teamly.Client(enable_debug=True)


@client.event
async def on_ready():
    print("the bot is ready")




@client.event
async def on_todo_item(todo):
    print(json.dumps(todo.to_dict(), indent=4, ensure_ascii=False))

@client.event
async def on_todo_item_updated(todo):
    print(json.dumps(todo.to_dict(), indent=4, ensure_ascii=False))

@client.event
async def on_todo_item_deleted(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))



client.run(config["TEST_KEY"])
