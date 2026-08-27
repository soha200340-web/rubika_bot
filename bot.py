import os
import asyncio

from fastapi import FastAPI
from rubka.asynco import Robot, Message
from rubka.button import InlineBuilder


# دریافت توکن از Environment Variable
TOKEN = os.getenv("RUBIKA_TOKEN")

if not TOKEN:
    raise RuntimeError("RUBIKA_TOKEN is not set")


# آدرس Webhook؛ فعلاً می‌تواند خالی باشد
WEBHOOK_URL = os.getenv("WEBHOOK_URL")


# ساخت ربات
if WEBHOOK_URL:
    bot = Robot(
        TOKEN,
        web_hook=WEBHOOK_URL
    )
else:
    bot = Robot(TOKEN)


# ساخت سرور وب
app = FastAPI()


@app.get("/")
async def home():
    return {
        "status": "ok",
        "message": "Rubika bot is running"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


# دستور /start
@bot.on_message(commands=["start"])
async def start(_, m: Message):

    keypad = (
        InlineBuilder()
        .row(
            InlineBuilder().button_simple(
                "btn",
                "دکمه"
            )
        )
        .build()
    )

    await m.reply(
        "شروع:",
        inline_keypad=keypad
    )


# وقتی روی دکمه کلیک شد
@bot.on_callback("btn")
async def btn(_, m: Message):

    await m.reply("سلام")


# اجرای ربات
async def run_bot():
    await bot.run()


# هنگام بالا آمدن FastAPI، ربات هم اجرا شود
@app.on_event("startup")
async def startup():

    asyncio.create_task(run_bot())
