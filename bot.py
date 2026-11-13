import os
import time
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton,
    BotCommand
)
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("9030686804:AAHOKUUZX9mgSpS6878lK4GKnomRau92Zf4", "").strip()
OWNER_ID = int(os.getenv("6648333398", "0") or 0)
BOT_NAME = os.getenv("BOT_NAME", "ZYRO BOT")
START_TIME = time.time()

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is missing. Add it in your hosting Environment Variables.")

dp = Dispatcher()

def main_keyboard(is_owner: bool = False) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(text="🏠 Start", callback_data="home"),
            InlineKeyboardButton(text="❓ Help", callback_data="help"),
        ],
        [
            InlineKeyboardButton(text="ℹ️ About", callback_data="about"),
            InlineKeyboardButton(text="👑 Owner", callback_data="owner"),
        ],
        [
            InlineKeyboardButton(text="⚡ Ping", callback_data="ping"),
            InlineKeyboardButton(text="🪪 My ID", callback_data="myid"),
        ],
        [
            InlineKeyboardButton(text="🧭 Commands", callback_data="commands"),
            InlineKeyboardButton(text="🔗 Support", url="https://t.me/"),
        ],
    ]
    if is_owner:
        rows.append([InlineKeyboardButton(text="🛡️ Admin Panel", callback_data="admin")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Back to menu", callback_data="home")]
    ])

def is_owner(user_id: int) -> bool:
    return OWNER_ID != 0 and user_id == OWNER_ID

def welcome_text(first_name: str) -> str:
    return (
        "👑 <b>WELCOME TO ZYRO BOT</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"Hey <b>{first_name}</b>! 👋\n\n"
        "💜 Your powerful Telegram assistant is ready.\n"
        "⚡ Fast • Smart • Reliable\n\n"
        "👑 <b>Owner:</b> ZYRO\n"
        "🤖 <b>Status:</b> Online 🟢\n"
        "✨ <b>Version:</b> PRO 1.0\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "👇 <b>Choose an option below:</b>"
    )

@dp.message(CommandStart())
async def start(message: Message):
    owner = is_owner(message.from_user.id)
    caption = welcome_text(message.from_user.first_name)
    banner_path = os.path.join(os.path.dirname(__file__), "zyro_banner.png")
    if os.path.isfile(banner_path):
        from aiogram.types import FSInputFile
        await message.answer_photo(
            photo=FSInputFile(banner_path),
            caption=caption,
            reply_markup=main_keyboard(owner)
        )
    else:
        await message.answer(caption, reply_markup=main_keyboard(owner))

@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "✨ <b>ZYRO BOT — HELP CENTER</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "/start — Open welcome menu\n"
        "/help — Show help\n"
        "/menu — Open buttons menu\n"
        "/about — About this bot\n"
        "/owner — Owner information\n"
        "/ping — Check bot response\n"
        "/id — Show your Telegram ID\n"
        "━━━━━━━━━━━━━━━━━━",
        reply_markup=back_keyboard()
    )

@dp.message(Command("menu"))
async def menu_cmd(message: Message):
    await message.answer("💜 <b>ZYRO PRO MENU</b>\nChoose a feature:", reply_markup=main_keyboard(is_owner(message.from_user.id)))

@dp.message(Command("about"))
async def about_cmd(message: Message):
    await message.answer(
        "💎 <b>ABOUT ZYRO BOT</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "A custom Telegram assistant powered by <b>Python + Aiogram 3</b>.\n\n"
        "👑 Brand: <b>ZYRO</b>\n"
        "🚀 Edition: <b>PRO</b>\n"
        "🟢 Status: <b>Online</b>\n"
        "━━━━━━━━━━━━━━━━━━",
        reply_markup=back_keyboard()
    )

@dp.message(Command("owner"))
async def owner_cmd(message: Message):
    owner_line = f'<code>{OWNER_ID}</code>' if OWNER_ID else "Not configured yet"
    await message.answer(
        "👑 <b>BOT OWNER</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "Name: <b>ZYRO</b>\n"
        f"Telegram ID: {owner_line}\n"
        "━━━━━━━━━━━━━━━━━━",
        reply_markup=back_keyboard()
    )

@dp.message(Command("ping"))
async def ping_cmd(message: Message):
    started = time.perf_counter()
    sent = await message.answer("⚡ Checking...")
    ms = (time.perf_counter() - started) * 1000
    uptime = int(time.time() - START_TIME)
    await sent.edit_text(
        f"⚡ <b>PONG!</b>\nResponse: <code>{ms:.0f} ms</code>\nUptime: <code>{uptime}s</code>",
        reply_markup=back_keyboard()
    )

@dp.message(Command("id"))
async def id_cmd(message: Message):
    await message.answer(
        f"🪪 <b>Your Telegram ID</b>\n<code>{message.from_user.id}</code>",
        reply_markup=back_keyboard()
    )

@dp.message(Command("admin"))
async def admin_cmd(message: Message):
    if not is_owner(message.from_user.id):
        await message.answer("⛔ This command is for the bot owner only.")
        return
    await message.answer(
        "🛡️ <b>ZYRO OWNER PANEL</b>\n━━━━━━━━━━━━━━━━━━\n"
        "👑 Owner access confirmed.\n"
        "Use the buttons to inspect bot status.",
        reply_markup=main_keyboard(True)
    )

@dp.callback_query(F.data == "home")
async def cb_home(call: CallbackQuery):
    await call.message.edit_text(
        welcome_text(call.from_user.first_name),
        reply_markup=main_keyboard(is_owner(call.from_user.id))
    )
    await call.answer()

@dp.callback_query(F.data == "help")
async def cb_help(call: CallbackQuery):
    await call.message.edit_text(
        "✨ <b>HELP CENTER</b>\n━━━━━━━━━━━━━━━━━━\n"
        "/start — Welcome\n/help — Help\n/menu — Menu\n/about — About\n"
        "/owner — Owner\n/ping — Speed test\n/id — Your ID\n/admin — Owner panel",
        reply_markup=back_keyboard()
    )
    await call.answer()

@dp.callback_query(F.data == "about")
async def cb_about(call: CallbackQuery):
    await call.message.edit_text(
        "💎 <b>ZYRO BOT PRO</b>\nPython • Aiogram 3\nOwner: <b>ZYRO</b>\nStatus: 🟢 Online",
        reply_markup=back_keyboard()
    )
    await call.answer()

@dp.callback_query(F.data == "owner")
async def cb_owner(call: CallbackQuery):
    owner_line = f"<code>{OWNER_ID}</code>" if OWNER_ID else "Not configured"
    await call.message.edit_text(
        f"👑 <b>OWNER: ZYRO</b>\nTelegram ID: {owner_line}",
        reply_markup=back_keyboard()
    )
    await call.answer()

@dp.callback_query(F.data == "ping")
async def cb_ping(call: CallbackQuery):
    await call.answer("⚡ ZYRO is online!", show_alert=True)

@dp.callback_query(F.data == "myid")
async def cb_myid(call: CallbackQuery):
    await call.answer(f"Your ID: {call.from_user.id}", show_alert=True)

@dp.callback_query(F.data == "commands")
async def cb_commands(call: CallbackQuery):
    await call.message.edit_text(
        "📚 <b>COMMAND LIST</b>\n/start /help /menu /about\n/owner /ping /id /admin",
        reply_markup=back_keyboard()
    )
    await call.answer()

@dp.callback_query(F.data == "admin")
async def cb_admin(call: CallbackQuery):
    if not is_owner(call.from_user.id):
        await call.answer("Owner only 🔒", show_alert=True)
        return
    await call.message.edit_text(
        "🛡️ <b>OWNER PANEL</b>\n\n"
        "👑 Owner verified\n🟢 Bot process is active\n"
        "Use /ping to check response time.",
        reply_markup=back_keyboard()
    )
    await call.answer()

@dp.message()
async def fallback(message: Message):
    await message.answer(
        "💜 I received your message!\nUse /menu to see what I can do.",
        reply_markup=main_keyboard(is_owner(message.from_user.id))
    )

async def main():
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.set_my_commands([
        BotCommand(command="start", description="Open welcome menu"),
        BotCommand(command="help", description="Help center"),
        BotCommand(command="menu", description="Open bot menu"),
        BotCommand(command="about", description="About ZYRO BOT"),
        BotCommand(command="owner", description="Owner information"),
        BotCommand(command="ping", description="Check bot speed"),
        BotCommand(command="id", description="Show your Telegram ID"),
        BotCommand(command="admin", description="Owner panel"),
    ])
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
