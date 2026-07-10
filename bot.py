import os
import asyncio
import random
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# GitHub Secrets မှ Token ကို လှမ်းယူခြင်း
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing!")

bot = AsyncTeleBot(BOT_TOKEN)

async def generate_random_mac():
    mac = [random.randint(0x00, 0xff) for _ in range(6)]
    return ':'.join(f"{x:02x}" for x in mac)

async def solve_captcha_simple_async(image_bytes=None):
    await asyncio.sleep(1.5)
    return "MOCK_CAPTCHA_CODE_123"

async def check_balance(session_id):
    await asyncio.sleep(1)
    return {"status": "success", "balance": "5,500 MMK"}

def get_main_menu_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("📊 Check Status", callback_data="check_status"),
        InlineKeyboardButton("⚙️ Settings / Mode", callback_data="mode_menu"),
        InlineKeyboardButton("🛑 Stop Bot", callback_data="stop_bot")
    )
    return markup

@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    welcome_text = "🤖 Welcome to Automation Control Dashboard\nအောက်ပါ Menu မှတစ်ဆင့် ထိန်းချုပ်နိုင်ပါသည်။"
    await bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu_keyboard())

@bot.callback_query_handler(func=lambda call: True)
async def callback_listener(call):
    if call.data == "back_main":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="🤖 Main Menu သို့ ပြန်ရောက်ပါပြီ။", reply_markup=get_main_menu_keyboard())
    elif call.data == "mode_menu":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("⬅️ Back to Main", callback_data="back_main"))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="⚙️ **Settings Mode**\n\nဤနေရာတွင် Bot ၏ စနစ်များကို ပြင်ဆင်နိုင်ပါသည်။", reply_markup=markup, parse_mode="Markdown")
    elif call.data == "check_status":
        await bot.answer_callback_query(call.id, "Checking system status...")
        mac_addr = await generate_random_mac()
        captcha_res = await solve_captcha_simple_async()
        bal_info = await check_balance(session_id="dummy_sid")
        
        status_text = (
            f"📊 **Live Dashboard Update**\n\n"
            f"🔹 **Generated MAC:** `{mac_addr}`\n"
            f"🔹 **Captcha Solver:** `{captcha_res}`\n"
            f"🔹 **Account Balance:** `{bal_info['balance']}`\n\n"
            f"စနစ်သည် ပုံမှန်အလုပ်လုပ်နေပါသည်။"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("⬅️ Back", callback_data="back_main"))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=status_text, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "stop_bot":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="🛑 Bot automatic operations have been paused.")

if __name__ == "__main__":
    print("🤖 Telegram Bot is starting...")
    asyncio.run(bot.polling(non_stop=True))
