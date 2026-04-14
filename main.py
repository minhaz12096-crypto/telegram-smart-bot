import asyncio
from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest, Message

# --- CONFIGURATION ---
# Replace these with your own credentials
API_ID = 35558637  
API_HASH = "93bb67b4c3c1d5553d191fea10fdd591"  
BOT_TOKEN = "8316263300:AAEMqM5Cpc--OidqJOVpWgBHW5OFyLb-hOg"  

app = Client("management_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 1. AUTO ACCEPT JOIN REQUEST & WELCOME MESSAGE
@app.on_chat_join_request()
async def auto_approve(client, request: ChatJoinRequest):
    try:
        await request.approve()
        user = request.from_user
        # Pure English Welcome Message
        welcome_text = (
            f"Hello {user.mention}, welcome to our community!\n\n"
            f"Your request to join **{request.chat.title}** has been automatically approved. "
            "Please follow the group rules and enjoy your stay!"
        )
        await client.send_message(request.chat.id, welcome_text)
    except Exception as e:
        print(f"Error in auto_approve: {e}")

# 2. ANTI-LEAVE (BAN), SPAM DELETE & AUTO REACTION
@app.on_message(filters.group | filters.channel)
async def group_handler(client, message: Message):
    # Auto Ban if user leaves the group
    if message.left_chat_member:
        try:
            await client.ban_chat_member(message.chat.id, message.left_chat_member.id)
            print(f"User {message.left_chat_member.id} banned for leaving.")
        except:
            pass

    # Delete Spam Links and Send Warning in English
    if message.entities:
        for entity in message.entities:
            if entity.type in ["url", "text_link"]:
                try:
                    await message.delete()
                    warning = await message.reply_text(
                        f"Hey {message.from_user.mention}, spam links are not allowed here! Your message has been removed."
                    )
                    await asyncio.sleep(10) # Delete warning after 10 seconds
                    await warning.delete()
                except:
                    pass
                return

    # Auto Reaction on every message/post
    try:
        await message.react("👍")
    except:
        pass

# 3. ID COMMAND (USER & CHAT ID)
@app.on_message(filters.command("id"))
async def show_id(client, message: Message):
    id_text = (
        f"👤 **User ID:** `{message.from_user.id}`\n"
        f"👥 **Chat ID:** `{message.chat.id}`"
    )
    await message.reply_text(id_text)

# 4. AUTO MESSAGE LOOP (EVERY 24 HOURS)
async def auto_broadcast():
    while True:
        await asyncio.sleep(86400) # 86400 seconds = 24 hours
        # Add your group/channel IDs here (Example: -100123456789)
        target_chat_ids = [-100123456789] 
        for chat_id in target_chat_ids:
            try:
                msg = "📢 **Auto Notification:** Hello everyone! Stay tuned for our latest updates."
                await app.send_message(chat_id, msg)
            except Exception as e:
                print(f"Broadcast error: {e}")

# MAIN START FUNCTION
async def main():
    await app.start()
    print("Bot is started successfully!")
    asyncio.create_task(auto_broadcast())
    await asyncio.idle()

if __name__ == "__main__":
    app.run(main())
