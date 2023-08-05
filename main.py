import pymongo
import telegram
import requests
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
import os

load_dotenv()
app = FastAPI()
TOKEN = os.getenv('TOKEN')
URL = os.getenv('URL')
uri = os.getenv('uri')

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
# use a database named "testdb"
db = client.testdb
# use a collection named "testcollection2"
my_collection = db["testcollection2"]

bot = telegram.Bot(token=TOKEN)


async def setup_webhook():
    await bot.setWebhook(url=f"{URL}/{TOKEN}")
    print("[WEBHOOK] Webhook has been set!")


@app.post(f"/{TOKEN}")
async def webhook(request: Request):
    update = await request.json()
    update_data = telegram.Update.de_json(update, bot)
    print("[WEBHOOK] Data has been received from webhook.")
    return process_data(update_data)


async def process_data(data):
    """Find ChatID, Text and send to correct function"""
    chatid = data['message']['chat']['id']
    text = data['message']['text']
    # Check db for data on user using chatid
    try:




async def start(chat_id, message):
    # Insert document when user starts using bot.
    add_document =[{"chatid": chat_id, "convstate": "0", "name": "", "fac": "", "degree": "", "completion": "False"}]
    try:
        result = my_collection.insert_one(add_document)
    # return a friendly error if the operation fails
    except pymongo.errors.OperationFailure:
        print(
            "An authentication error was received. Are you sure your database user is authorized to perform write operations?")
        sys.exit(1)
    else:
        inserted_count = len(result.inserted_ids)
        print("I inserted %x documents." % inserted_count)

        print("\n")
    await bot.send_message(chat_id=chat_id, text=f"Hi, {telegram.User.mention_markdown_v2()}")


async def help(chat_id, message):
    await bot.send_message(chat_id=chat_id, text="Follow along as the bot guides you to enter your details!")


async def name(chat_id, message):
    await









