import os
import asyncio

from fastapi import FastAPI
from rubka.asynco import Robot, Message
from rubka.button import InlineBuilder

TOKEN = os.getenv("RUBIKA_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not TOKEN:
    raise RuntimeError("RUBIKA_TOKEN is not set")

if not WEBHOOK_URL:
    raise RuntimeError("WEBHOOK_URL is not set")

bot = Robot(
    TOKEN,
    web_hook=WEBHOOK_URL
)

app = FastAPI()


@app.get("/")
async def home():
    return {"status": "ok", "message": "Rubika bot is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@bot.on_message(commands=["start"])
async def start(_, m: Message):
    k = InlineBuilder().row(
        InlineBuilder().button_simple("btn", "دکمه")
    ).build()

    await m.reply("شروع:", inline_keypad=k)


@bot.on_callback("btn")
async def btn(_, m: Message):
    await m.reply("سلام")


async def run_bot():
    await bot.run()


@app.on_event("startup")
async def startup():
    asyncio.create_task(run_bot())
