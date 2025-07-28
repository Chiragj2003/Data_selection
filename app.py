# app.py

import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, request, Response
from botbuilder.schema import Activity
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from bot.echo_bot import EchoBot

load_dotenv()

app = Flask(__name__)

# Bot credentials from .env
bot_settings = BotFrameworkAdapterSettings(
    os.getenv("MicrosoftAppId"),
    os.getenv("MicrosoftAppPassword")
)
adapter = BotFrameworkAdapter(bot_settings)
bot = EchoBot()

# Flask endpoint
@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")

    async def call_bot():
        await adapter.process_activity(activity, auth_header, bot.on_turn)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(call_bot())
    return Response(status=200)
