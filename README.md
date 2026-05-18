# ⏰ reminder_bot_v2

> Advanced reminder bot with multi-language support

A Telegram bot for setting reminders on specific days and times with admin controls, captcha verification, and multi-language support (English, Russian, Ukrainian).

## ✨ Features

- **Daily reminders** — Set reminders for specific days and times
- **Admin controls** — Manage users, reminders, and settings
- **User management** — Add/remove users from reminder list
- **Day control** — Enable/disable reminders for specific days of the week
- **Time management** — Set different times for each day
- **Multi-language** — Supports English, Russian, and Ukrainian
- **Timezone support** — UTC and custom timezone handling
- **Captcha verification** — Admin-level protection
- **Group/Private** — Works in group chats with admin controls

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Telegram Bot Token
- pyTelegramBotAPI
- pytz (timezone support)

### Installation

```bash
git clone https://github.com/w1cee/reminder_bot_v2.git
cd reminder_bot_v2
pip install -r requirements.txt
```

### Configuration

1. Edit `bot_config.py` and add your bot token:

```python
BOT_TOKEN = 'YOUR_BOT_TOKEN'
```

2. Edit `config.json` for default settings:

```json
{
  "admins": ["@your_username"],
  "workers": ["@target_username"],
  "group_id": 0,
  "timezone": "UTC",
  "lang_file": "en.json"
}
```

3. Run the bot:

```bash
python main.py
```

## 💻 How to Use

### For Users

```
User: /start
Bot: [Menu options]

User: /reminder_text
Bot: Send a new reminder text
User: "Don't forget to check emails"

User: /day_on
Bot: Send me the number of the day (1=Monday, 7=Sunday)
User: 1
Bot: Reminder enabled for Monday
```

### For Admins

```
User: /admin
Bot: [Admin menu]

# Add user to reminder list
User: /add_user
Bot: Send me @username
User: @john_doe

# Set reminder time
User: /set_time
Bot: Send me day number (1-7)
Bot: Send me time in HH:MM format
User: 1
User: 09:00

# Manage admins
User: /add_admin
Bot: Send me @username of new admin
```

## 🛠️ Tech Stack

- **Language**: Python 3.7+
- **Bot Framework**: pyTelegramBotAPI
- **Timezone**: pytz
- **Configuration**: JSON files
- **Languages**: JSON language files (en.json, ru.json, uk.json)

## 📚 Code Structure

### Main Components

```python
# Core imports
import telebot
import json
import pytz
from datetime import datetime
from threading import Thread
from bot_config import BOT_TOKEN

# Initialize bot
TOKEN = BOT_TOKEN
bot = telebot.TeleBot(TOKEN)

# Configuration
LIST_OF_ADMINS = []
GROUP_ID = 0
config_file = 'config.json'
lang_dir_path = 'lang/'
```

### Configuration Structure

#### `config.json`
```json
{
  "day_status": {
    "day_1": "OFF",  // Monday off
    "day_2": "ON",   // Tuesday on
    // ...
    "day_7": "OFF"   // Sunday off
  },
  "day_time": {
    "day_1": "09:00:00",
    "day_2": "14:30:00",
    // ...
  },
  "workers": ["@username1", "@username2"],  // Reminder recipients
  "text": "",  // Reminder text
  "admins": ["@admin1"],  // Bot admins
  "group_id": 0,  // Group chat ID
  "lang_file": "en.json",  // Current language
  "available_lang": ["English", "Русский", "Українська"],
  "timezone": "UTC"
}
```

### Language Files

Each language has a JSON file in `lang/` folder:

**lang/en.json:**
```json
{
  "lang_name": "English (default)",
  "reminder_text": "Text to remind:",
  "day_on": "Enable reminder for day:",
  "day_off": "Disable reminder for day:",
  "day_time": "Time for reminder",
  "not_admin": "You are not allowed to use this command.",
  ...
}
```

Same structure for `ru.json` (Russian) and `uk.json` (Ukrainian).

## 📅 Day Numbering

```
1 = Monday (Пн)
2 = Tuesday (Вт)
3 = Wednesday (Ср)
4 = Thursday (Чт)
5 = Friday (Пт)
6 = Saturday (Сб)
7 = Sunday (Вс)
```

## 🔌 Key Features Implementation

### 1. Day Management

```python
# Enable/disable reminders for specific day
day_status = {
    "day_1": "ON",   # Monday enabled
    "day_2": "OFF",  # Tuesday disabled
    ...
}
```

### 2. Time Management

```python
# Set different times for each day
day_time = {
    "day_1": "09:00:00",   # 9 AM on Monday
    "day_2": "14:30:00",   # 2:30 PM on Tuesday
    ...
}
```

### 3. User Management

```python
# Add/remove users from reminder list
workers = ["@user1", "@user2", "@user3"]

# Admin-only commands can:
# - Add users to list
# - Remove users from list
# - View current list
```

### 4. Admin Controls

```python
LIST_OF_ADMINS = ["@admin1", "@admin2"]

# Admin-only commands:
/admin              # Admin menu
/add_user          # Add user to recipients
/del_user          # Remove user
/set_text          # Set reminder text
/set_time          # Set reminder time
/add_admin         # Make user admin
/del_admin         # Remove admin
/list_users        # View recipient list
/list_admins       # View admin list
/lang              # Change language
/set_timezone      # Change timezone
```

### 5. Captcha Verification

```python
# Admins must solve captcha for certain operations
"solve_captcha": "Solve the captcha to continue."
"captcha_fail": "You did not pass the captcha, please try again."
```

### 6. Multi-Language Support

```python
# Load language file
lang_file = 'lang/en.json'  # English
lang_file = 'lang/ru.json'  # Russian
lang_file = 'lang/uk.json'  # Ukrainian

# Use language strings
bot.send_message(chat_id, lang["reminder_text"])
```

### 7. Timezone Support

```python
import pytz

# Set timezone
timezone = pytz.timezone('UTC')
timezone = pytz.timezone('Europe/Kyiv')
timezone = pytz.timezone('US/Eastern')

# Get current time in timezone
now = datetime.now(timezone)
```

## 📁 File Structure

```
reminder_bot_v2/
├── main.py              # Main bot script
├── bot_config.py        # Bot token configuration
├── config.json          # Bot settings and configuration
├── lang/                # Language files
│   ├── en.json         # English
│   ├── ru.json         # Russian
│   └── uk.json         # Ukrainian
├── requirements.txt     # Python dependencies
├── LICENSE
└── README.md
```

## 📝 Requirements

```
pytz
pyTelegramBotAPI
```

## 🐛 Troubleshooting

### Bot not starting
```
BotException: A request to the Telegram API was unsuccessful. Error code: 401
```
- Verify bot token is correct
- Token must be copied completely without spaces
- Bot token may have expired

### Reminders not sending
- Verify `day_status` for that day is "ON"
- Check `day_time` is set correctly
- Ensure bot is running (no crashes)
- Check if users are in `workers` list

### Group chat not working
- Set `group_id` in config.json
- Add bot to group as admin
- Verify group ID is correct (negative number for groups)

### Language not changing
- Verify language file exists in `lang/` folder
- Check JSON syntax in language files
- Restart bot after changing language

### Timezone issues
- Use valid pytz timezone strings
- List valid timezones: `pytz.all_timezones`
- UTC is the default

## 🔄 Workflow

```
Bot starts
        ↓
Load config.json
        ↓
Load language file
        ↓
Set timezone
        ↓
Wait for commands
        ↓
On scheduled time:
  Check day_status for today
  If "ON":
    Send reminder to all workers
    Use reminder text from config
        ↓
Process user commands:
  /start → Show menu
  /admin → Admin menu (if admin)
  /set_text → Update reminder text
  /day_on → Enable day
  /set_time → Set time for day
  /lang → Change language
        ↓
Save changes to config.json
```

## 📊 Configuration Example

**config.json for daily 9 AM reminder:**
```json
{
  "day_status": {
    "day_1": "ON",   // Monday
    "day_2": "ON",   // Tuesday
    "day_3": "ON",   // Wednesday
    "day_4": "ON",   // Thursday
    "day_5": "ON",   // Friday
    "day_6": "OFF",  // Saturday
    "day_7": "OFF"   // Sunday
  },
  "day_time": {
    "day_1": "09:00:00",
    "day_2": "09:00:00",
    "day_3": "09:00:00",
    "day_4": "09:00:00",
    "day_5": "09:00:00",
    "day_6": "09:00:00",
    "day_7": "09:00:00"
  },
  "workers": ["@john", "@jane"],
  "text": "Check your emails!",
  "admins": ["@admin_user"],
  "timezone": "UTC"
}
```

## 📄 License

MIT License - See LICENSE file

## 👨‍💻 Author

**w1cee** — Backend Developer | Systems Builder  
💬 [GitHub](https://github.com/w1cee)

---

**Building things that work while I sleep** ⏰
