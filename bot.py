import asyncio,re
from main import *
from aiogram import Bot,Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command

token="7954588258:AAHQfI5TrvEljhRKT3yCGxKxsM0GHBIJPcw"
bot=Bot(token=token,default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp=Dispatcher()
@dp.message(Command("start"))
async def welcome_message(message:Message):
    username=message.from_user.username or message.from_user.first_name
    await message.answer(f"Hello {username}! 👋 Welcome to MagnetLink Bot.\nJust Send the Magnet Link I will Send the Direct Downloadable link!!")

@dp.message()
async def handle_magnet(message: Message):
    try:
        links = getmovie_link(message.text)
        if not links:
            await message.answer("⚠️ No valid links found in the message.")
            return

        for link in links:
            print(link)
            # Escape the link to prevent HTML parsing errors
            await message.answer(
                "🚀 <b>Magnet Link:</b>\n\n"
                f'🔗 <code>{link}</code>',
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
    except Exception as e:
        print(f"Error processing message: {e}")
        await message.answer("⚠️ An error occurred while processing your request.")
            
async def on_startup(app: web.Application):
    await bot.set_webhook("https://magnetlinksbot.onrender.com/webhook")

def main():
    # Create aiohttp application
    app = web.Application()
    
    # Register webhook handler
    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_handler.register(app, path="/webhook")
    
    # Setup application
    setup_application(app, dp, bot=bot)
    
    # Add startup callback
    app.on_startup.append(on_startup)
    
    # Add health check endpoint
    async def health_check(request):
        return web.Response(text="OK")
    app.router.add_get("/health", health_check)
    
    # Run app (Render requires port 10000)
    web.run_app(app, host="0.0.0.0", port=10000)

if __name__ == "__main__":
    main()
