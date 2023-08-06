import pymongo
import telegram
import sys
import asyncio
import requests
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
import os

load_dotenv()
app = FastAPI()
TOKEN = os.getenv('TOKEN')
URL = os.getenv('URL') # Get from Heroku
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
    print("[WEBHOOK] Awaiting data")
    update = await request.json()
    update_data = telegram.Update.de_json(update, bot)
    print("[WEBHOOK] Data has been received from webhook.")
    print("[WEBHOOK] Update data is:", update_data)
    data = await process_data(update_data)
    print(data)


async def process_data(data):
    """Find ChatID, Text and send to correct function"""

    chatid = data['message']['chat']['id']
    text = data['message']['text']
    print("[PROCESS UPDATE] ChatID is", chatid)
    print("[PROCESS UPDATE] Text is", text)
    # Check db for data on user using chatid
    if text == "/help":
        await help(chat_id=chatid)
    elif text == "/start":
        # try:
        #     existence = my_collection.find_one({"chatid": chatid})
        #     print("[DB EXISTENCE TEST] Current ChatID status in DB is", existence)
        # except False:
        #     try:
        #         add_document = [{"chatid": chatid, "convstate": "0", "name": "", "fac": "", "degree": "", "completion": "False"}]
        #         my_collection.insert_one(add_document)
        #     except pymongo.errors.OperationFailure:
        #         print("[DATABASE] Authentication error")
        #         sys.exit(1)
        #     else:
        #         print("[DATABASE] New record added")
        #         await start(chat_id=chatid)
        try:
            existence = my_collection.find_one({"chatid": chatid})
            print("[DB EXISTENCE TEST] Current ChatID status in DB is", existence)

            if existence is None:
                # Handle the case where no document was found
                print("[DB EXISTENCE TEST] No document found for chatid:", chatid)
            else:
                # Document was found, process the existing document
                await name(chat_id=chatid)
        except Exception as e:
            print("[DB EXISTENCE TEST] An error occurred:", str(e))
            # Handle the error scenario here if needed (e.g., logging, notifying, etc.)

    else:
        await others(chat_id=chatid)


async def start(chat_id):
  await bot.send_message(chat_id=chat_id, text=f"Hi, {telegram.User.mention_markdown_v2()}")


async def help(chat_id):
    await bot.send_message(chat_id=chat_id, text="Follow along as the bot guides you to enter your details!")


async def others(chat_id):
    await bot.send_message(chat_id=chat_id, text="Haha.")

async def name(chat_id):
    await bot.send_message(chat_id=chat_id, text="What is your name?")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_webhook())
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8443)









