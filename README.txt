ZYRO PRO TELEGRAM BOT
=====================

FILES
- bot.py: Aiogram 3 bot with welcome menu and commands
- requirements.txt: required Python package\n- zyro_banner.png: welcome banner image shown by /start

BOT-HOSTING.NET SETUP
1. Open your server Files.
2. Upload bot.py and requirements.txt to /home/container (main folder).
3. In Startup, set the startup file/command to:
   python bot.py
   If the panel has a dedicated Python file field, enter bot.py there.
4. In Variables / Environment, add:
   BOT_TOKEN = your BotFather token
   OWNER_ID = your numeric Telegram user ID
   BOT_NAME = ZYRO BOT (optional)
5. Save, then Restart the server.
6. Open your bot in Telegram and send /start.

GET YOUR TELEGRAM USER ID
- Start your bot and send /id. This shows your ID.
- Put that number into OWNER_ID in hosting Variables, then restart.
- If you cannot use /id until after setup, temporarily leave OWNER_ID as 0,
  start the bot, send /id, then update OWNER_ID and restart.

IMPORTANT
- Never share BOT_TOKEN.
- Do not paste your token into public chats or screenshots.
- This code provides a styled message and inline buttons; it cannot change
  Telegram's app-wide theme or the bot profile's official appearance.
