import telebot
import requests
import time
import json
import os
import csv
import io
import threading
from datetime import datetime
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ===== CONFIGURATION =====
BOT_TOKEN = "8434035883:AAGJKCzOI5Gk4GnvMqMZHE0viFQpUOHBHqA"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

BOT_USERNAME = "@Bhhhdh_bot"
DEFAULT_ADMIN = 5389788898
DEVELOPER_USERNAME = "@https://t.me/bhsgyi"
DEVELOPER_FOOTER = f"""
<code>━━━━━━━━━━━━━━━━━━━━</code>
<b>🔍 Powered by Darknyte Exodus & Team</b>
<b>📞 Contact: {https://t.me/bhsgyi}</b>
"""

# ===== JSON FILE STORAGE =====
DATA_FILE = "users_data.json"

# ===== API KEYS =====
NUMBER_API_KEY = "ak_87487e015d126abfee103403cdf43c8f"

# ===== WORKING APIS =====
INDIA_NUMBER_API = "https://abduldevstorebot.up.railway.app/api/v1?key={}&num={}"
PAKISTAN_NUMBER_API = "https://abbas-apis.vercel.app/api/pakistan?number={}"
NAME_TO_AADHAAR_API = "https://aadhar.ek4nsh.in/?name={}"
VEHICLE_API = "https://new-vehicle-api-eosin.vercel.app/vehicle?rc={}"
BIN_API = "https://lookup.binlist.net/{}"
BIN_NEW_API = "https://api.b77bf911.workers.dev/bin?bin={}"
IP_API = "http://ip-api.com/json/{}"
GITHUB_API = "https://abbas-apis.vercel.app/api/github?username={}"
EMAIL_API = "https://abbas-apis.vercel.app/api/email?mail={}"
IFSC_API = "https://api.b77bf911.workers.dev/ifsc?code={}"
IFSC_OLD_API = "https://abbas-apis.vercel.app/api/ifsc?ifsc={}"
FF_INFO_API = "https://abbas-apis.vercel.app/api/ff-info?uid={}"
FF_BAN_API = "https://abbas-apis.vercel.app/api/ff-ban?uid={}"
NUM_FAMILY_API = "https://source-code-api.vercel.app/?num={}"
NUM_OWNER_API = "https://abbas-apis.vercel.app/api/num-name?number=91{}"
DOMAIN_API = "https://api.b77bf911.workers.dev/whois?domain={}"

# ===== MUST JOIN CHANNELS =====
REQUIRED_CHANNELS = [
    {
        "name": "Main Channel", 
        "url": "https://t.me/+_7Yuac3L2-A0MmI1", 
        "icon": "📢", 
        "chat_id": "-1002806543363",
        "type": "telegram_private"
    },
    {
        "name": "darknyteexodus", 
        "url": "https://t.me/+99fs4PAwOO41NWE1", 
        "icon": "🌑", 
        "chat_id": "-1002330272825",
        "type": "telegram_private"
    },
    {
        "name": "Backup Channel", 
        "url": "https://t.me/Access_Allowed", 
        "icon": "💾", 
        "username": "Access_Allowed", 
        "type": "telegram_public"
    },
    {
        "name": "EXODUS YOUTUBE", 
        "url": "https://youtube.com/@exodus-m1i?si=ES85UdtoKL-SFWou", 
        "icon": "▶️", 
        "type": "youtube"
    }
]

# ===== API ENDPOINTS =====
API_ENDPOINTS = {
    "vehicle": VEHICLE_API,
    "bin": BIN_API,
    "bin_new": BIN_NEW_API,
    "ip": IP_API,
    "github": GITHUB_API,
    "email": EMAIL_API,
    "ifsc": IFSC_API,
    "ifsc_old": IFSC_OLD_API,
    "ff_info": FF_INFO_API,
    "ff_ban": FF_BAN_API,
    "number_to_family": NUM_FAMILY_API,
    "number_to_owner": NUM_OWNER_API,
    "domain": DOMAIN_API,
    "name_to_aadhaar": NAME_TO_AADHAAR_API
}

# ===== JSON DATABASE =====
class JSONDatabase:
    def __init__(self):
        self.users = {}
        self.admins = {}
        self.stats = {"total_users": 0, "total_api_calls": 0}
        self.load_data()
        self.import_old_data()
        self.add_default_admin()
        print(f"✅ Total users loaded: {len(self.users)}")
    
    def load_data(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.users = data.get('users', {})
                    self.admins = data.get('admins', {})
                    self.stats = data.get('stats', {"total_users": len(self.users), "total_api_calls": 0})
                print(f"✅ Loaded {len(self.users)} users from {DATA_FILE}")
            else:
                print(f"📁 {DATA_FILE} not found, creating new...")
                self.save_data()
        except Exception as e:
            print(f"❌ Error loading data: {e}")
    
    def save_data(self):
        try:
            data = {
                'users': self.users,
                'admins': self.admins,
                'stats': self.stats
            }
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return False
    
    def import_old_data(self):
        csv_file = "users_20260219_171310.csv"
        if os.path.exists(csv_file) and len(self.users) == 0:
            try:
                imported = 0
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        user_id = row['User ID']
                        if user_id not in self.users:
                            joined = time.time()
                            try:
                                if row['Joined'] != 'N/A':
                                    joined = datetime.strptime(row['Joined'], '%Y-%m-%d').timestamp()
                            except:
                                pass
                            
                            self.users[user_id] = {
                                'username': row['Username'],
                                'name': row['Name'],
                                'joined': joined,
                                'last_seen': joined,
                                'api_uses': int(row['API Uses']),
                                'banned': 1 if row['Banned'] == 'Yes' else 0,
                                'total_joins': 1
                            }
                            imported += 1
                
                self.stats['total_users'] = len(self.users)
                self.save_data()
                print(f"✅ Imported {imported} users from CSV")
            except Exception as e:
                print(f"❌ Error importing CSV: {e}")
    
    def add_default_admin(self):
        admin_id = str(DEFAULT_ADMIN)
        if admin_id not in self.admins:
            self.admins[admin_id] = {
                'username': 'D4RkNYTEAdmin',
                'added_by': DEFAULT_ADMIN,
                'added_date': time.time()
            }
            self.save_data()
    
    def get_user(self, user_id):
        return self.users.get(str(user_id))
    
    def user_exists(self, user_id):
        return str(user_id) in self.users
    
    def add_user(self, user_id, username, name):
        try:
            user_id = str(user_id)
            if user_id not in self.users:
                timestamp = time.time()
                self.users[user_id] = {
                    'username': username,
                    'name': name,
                    'joined': timestamp,
                    'last_seen': timestamp,
                    'api_uses': 0,
                    'banned': 0,
                    'total_joins': 1
                }
                self.stats['total_users'] = len(self.users)
                self.save_data()
                print(f"✅ New user added: {user_id}")
                return True
            return False
        except Exception as e:
            print(f"❌ Error adding user: {e}")
            return False
    
    def add_api_usage(self, user_id):
        user_id = str(user_id)
        if user_id in self.users:
            self.users[user_id]['api_uses'] = self.users[user_id].get('api_uses', 0) + 1
            self.stats['total_api_calls'] = self.stats.get('total_api_calls', 0) + 1
            self.save_data()
            return True
        return False
    
    def update_last_seen(self, user_id):
        user_id = str(user_id)
        if user_id in self.users:
            self.users[user_id]['last_seen'] = time.time()
            self.users[user_id]['total_joins'] = self.users[user_id].get('total_joins', 0) + 1
            self.save_data()
            return True
        return False
    
    def is_banned(self, user_id):
        return self.users.get(str(user_id), {}).get('banned', 0) == 1
    
    def ban_user(self, user_id):
        user_id = str(user_id)
        if user_id in self.users:
            self.users[user_id]['banned'] = 1
            self.save_data()
            return True
        return False
    
    def unban_user(self, user_id):
        user_id = str(user_id)
        if user_id in self.users:
            self.users[user_id]['banned'] = 0
            self.save_data()
            return True
        return False
    
    def get_all_users(self):
        users_list = []
        for user_id, user_data in self.users.items():
            users_list.append((
                user_id,
                user_data.get('username', 'N/A'),
                user_data.get('name', 'User'),
                user_data.get('joined', 0),
                user_data.get('last_seen', 0),
                user_data.get('api_uses', 0),
                user_data.get('banned', 0)
            ))
        return sorted(users_list, key=lambda x: x[3], reverse=True)
    
    def get_total_users(self):
        return len(self.users)
    
    def is_admin(self, user_id):
        return str(user_id) in self.admins
    
    def get_stats(self):
        return self.stats

# Initialize Database
db = JSONDatabase()

# ===== UTILITY FUNCTIONS =====
def add_footer(text, user_id=None):
    return text + DEVELOPER_FOOTER

def check_channel_join(user_id):
    """Channel join check karo - with error handling"""
    not_joined = []
    
    for channel in REQUIRED_CHANNELS:
        try:
            if channel["type"] == "youtube":
                continue
            elif channel["type"] == "telegram_public":
                try:
                    chat_member = bot.get_chat_member("@" + channel["username"], user_id)
                    if chat_member.status not in ["member", "administrator", "creator"]:
                        not_joined.append(channel)
                except Exception as e:
                    print(f"⚠️ Could not check {channel['name']}: {e}")
                    not_joined.append(channel)
                    
            elif channel["type"] == "telegram_private":
                try:
                    chat_member = bot.get_chat_member(int(channel['chat_id']), user_id)
                    if chat_member.status not in ["member", "administrator", "creator"]:
                        not_joined.append(channel)
                except Exception as e:
                    print(f"⚠️ Could not check private channel {channel['name']}: {e}")
                    not_joined.append(channel)
        except Exception as e:
            print(f"Error checking {channel['name']}: {e}")
            not_joined.append(channel)
    
    return not_joined

def animated_loading(chat_id, text="Processing"):
    msg = bot.send_message(chat_id, f"{text} 🔄")
    dots = ["🔘", "🔵", "⚪", "🔵", "🔘"]
    for dot in dots:
        try:
            bot.edit_message_text(f"{text} {dot}", chat_id, msg.message_id)
            time.sleep(0.2)
        except:
            pass
    return msg

def safe_delete_message(chat_id, message_id):
    """Safe message delete with error handling"""
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass

# ===== MENU =====
def get_main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    keyboard.row("📱 India Number", "🇵🇰 Pakistan Num", "🚗 Vehicle")
    keyboard.row("💳 BIN", "🌐 IP", "👤 Username")
    keyboard.row("📧 Email", "🏦 IFSC", "🎮 FF Info")
    keyboard.row("🎮 FF Ban", "💻 GitHub", "👨‍👩‍👧‍👦 Num Family")
    keyboard.row("👤 Num Owner", "🏦 IFSC Lookup", "💳 BIN Lookup")
    keyboard.row("🌐 Domain", "🆔 Name to Aadhaar", "📊 Dashboard")
    keyboard.row("ℹ️ Help", "👑 Admin")
    return keyboard

def get_admin_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.row("📊 Stats", "👥 All Users")
    keyboard.row("⛔ Ban User", "✅ Unban User")
    keyboard.row("📢 Broadcast", "📥 Export Data")
    keyboard.row("🔙 Main Menu")
    return keyboard

# ===== START COMMAND =====
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = str(message.from_user.id)
    
    if db.is_banned(user_id):
        bot.send_message(message.chat.id, add_footer("🚫 You are banned.", user_id))
        return
    
    if not db.user_exists(user_id):
        username = message.from_user.username or "N/A"
        name = message.from_user.first_name or "User"
        db.add_user(user_id, username, name)
    else:
        db.update_last_seen(user_id)
    
    not_joined = check_channel_join(message.from_user.id)
    
    if not_joined:
        keyboard = InlineKeyboardMarkup()
        for channel in REQUIRED_CHANNELS:
            keyboard.add(InlineKeyboardButton(f"{channel['icon']} {channel['name']}", url=channel['url']))
        keyboard.add(InlineKeyboardButton("✅ I've Joined Channels", callback_data="verify_join"))
        
        status_text = "<b>🔐 VERIFICATION REQUIRED</b>\n<code>━━━━━━━━━━━━━━━━━━━━</code>\n"
        status_text += "⚠️ <b>Join all Telegram channels to use this bot!</b>\n\n"
        
        for channel in REQUIRED_CHANNELS:
            if channel["type"] == "youtube":
                status_text += f"▶️ {channel['icon']} <b>{channel['name']}</b> (optional)\n"
            else:
                if channel in not_joined:
                    status_text += f"❌ {channel['icon']} <b>{channel['name']}</b>\n"
                else:
                    status_text += f"✅ {channel['icon']} <b>{channel['name']}</b>\n"
        
        try:
            bot.send_message(message.chat.id, add_footer(status_text, user_id), reply_markup=keyboard, disable_web_page_preview=True)
        except:
            pass
        return
    
    total_users = db.get_total_users()
    welcome_text = f"""
<b>🔥 EXODUS OSINT BOT</b>
<code>━━━━━━━━━━━━━━━━━━━━</code>
👤 Welcome {message.from_user.first_name}!
✅ Status: VERIFIED
👥 Total Users: {total_users}
<code>━━━━━━━━━━━━━━━━━━━━</code>

guys niche ke channel me sare hacking tools hya database hya YouTube pe tutorials hya join karlo 

bot is fully free .no credit.no adds . unlimited use .
<code>━━━━━━━━━━━━━━━━━━━━</code>
"""
    try:
        bot.send_message(message.chat.id, add_footer(welcome_text, user_id), reply_markup=get_main_menu(), disable_web_page_preview=True)
    except:
        pass

# ===== USERS COUNT COMMAND =====
@bot.message_handler(commands=['users', 'status', 'stats'])
def users_count_handler(message):
    user_id = str(message.from_user.id)
    total_users = db.get_total_users()
    
    text = f"""
# Exodus osint bot

# Exodus_osint_bot
{total_users} users

# Exodus osint bot [ Educational Purpose... ]

# Exodus_osint_bot
{total_users} users
"""
    bot.send_message(message.chat.id, add_footer(text, user_id))

# ===== CALLBACK =====
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "verify_join":
        not_joined = check_channel_join(call.from_user.id)
        telegram_not_joined = [c for c in not_joined if c["type"] != "youtube"]
        
        if telegram_not_joined:
            bot.answer_callback_query(call.id, "Join all Telegram channels first!", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "✅ Verification successful!", show_alert=True)
            safe_delete_message(call.message.chat.id, call.message.message_id)
            
            total_users = db.get_total_users()
            welcome_text = f"""
<b>🔥 EXODUS OSINT BOT</b>
<code>━━━━━━━━━━━━━━━━━━━━</code>
👤 Welcome {call.from_user.first_name}!
✅ Status: VERIFIED
👥 Total Users: {total_users}
<code>━━━━━━━━━━━━━━━━━━━━</code>

guys niche ke channel me sare hacking tools hya database hya YouTube pe tutorials hya join karlo 

bot is fully free .no credit.no adds . unlimited use .
<code>━━━━━━━━━━━━━━━━━━━━</code>
"""
            bot.send_message(call.message.chat.id, add_footer(welcome_text, str(call.from_user.id)), 
                           reply_markup=get_main_menu(), disable_web_page_preview=True)

# ===== INDIA NUMBER =====
@bot.message_handler(func=lambda m: m.text == "📱 India Number")
def india_number_handler(message):
    user_id = str(message.from_user.id)
    msg = bot.send_message(
        message.chat.id,
        add_footer("📱 <b>ENTER INDIAN MOBILE NUMBER</b>\nExample: <code>8755481593</code>", user_id)
    )
    bot.register_next_step_handler(msg, process_india_number)

def process_india_number(message):
    user_id = str(message.from_user.id)
    loading = animated_loading(message.chat.id, "📱 Fetching")
    
    try:
        number = message.text.strip().replace(" ", "")
        if not number.isdigit() or len(number) != 10:
            safe_delete_message(message.chat.id, loading.message_id)
            bot.send_message(message.chat.id, add_footer("❌ Invalid number! Use 10 digits.", user_id))
            return
        
        db.add_api_usage(user_id)
        api_url = INDIA_NUMBER_API.format(NUMBER_API_KEY, number)
        response = requests.get(api_url, timeout=15)
        
        safe_delete_message(message.chat.id, loading.message_id)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('status') and data.get('results'):
                results = data['results']
                
                if isinstance(results, list):
                    # Count unique records
                    seen = set()
                    unique_records = []
                    for record in results:
                        if isinstance(record, dict):
                            record_key = f"{record.get('name', '')}_{record.get('address', '')}"
                            if record_key not in seen:
                                seen.add(record_key)
                                unique_records.append(record)
                    
                    summary = f"\n━━━━━━━━━━━━━━━━━━━━\n✅ INDIA NUMBER DETAILS\n━━━━━━━━━━━━━━━━━━━━\n"
                    summary += f"Mobile      : {number}\n"
                    summary += f"Total Records: {len(unique_records)}\n"
                    summary += "━━━━━━━━━━━━━━━━━━━━\n"
                    bot.send_message(message.chat.id, add_footer(summary, user_id))
                    
                    for i, record in enumerate(unique_records, 1):
                        text = f"\n━━━━━━━━━━━━━━━━━━━━\n📞 Record #{i}\n━━━━━━━━━━━━━━━━━━━━\n"
                        text += f"Mobile      : {record.get('mobile', 'N/A')}\n"
                        text += f"Name        : {record.get('name', 'N/A')}\n"
                        text += f"Father      : {record.get('fname', 'N/A')}\n"
                        text += f"Address     : {str(record.get('address', 'N/A'))[:100]}\n"
                        if record.get('alt'):
                            text += f"Alternate   : {record['alt']}\n"
                        text += f"Circle      : {record.get('circle', 'N/A')}\n"
                        text += "━━━━━━━━━━━━━━━━━━━━\n"
                        bot.send_message(message.chat.id, add_footer(text, user_id))
                        time.sleep(0.3)
                else:
                    bot.send_message(message.chat.id, add_footer("❌ Invalid response format", user_id))
            else:
                bot.send_message(message.chat.id, add_footer("❌ No data found", user_id))
        else:
            bot.send_message(message.chat.id, add_footer("❌ API Error", user_id))
            
    except Exception as e:
        safe_delete_message(message.chat.id, loading.message_id)
        bot.send_message(message.chat.id, add_footer(f"❌ Error occurred", user_id))

# ===== PAKISTAN NUMBER =====
@bot.message_handler(func=lambda m: m.text == "🇵🇰 Pakistan Num")
def pakistan_number_handler(message):
    user_id = str(message.from_user.id)
    msg = bot.send_message(
        message.chat.id,
        add_footer("🇵🇰 <b>ENTER PAKISTAN NUMBER</b>\nExample: <code>3359736848</code>", user_id)
    )
    bot.register_next_step_handler(msg, process_pakistan_number)

def process_pakistan_number(message):
    user_id = str(message.from_user.id)
    loading = animated_loading(message.chat.id, "🇵🇰 Fetching")
    
    try:
        number = message.text.strip()
        if not number.isdigit() or len(number) != 10:
            safe_delete_message(message.chat.id, loading.message_id)
            bot.send_message(message.chat.id, add_footer("❌ Invalid number! Use 10 digits.", user_id))
            return
        
        db.add_api_usage(user_id)
        response = requests.get(PAKISTAN_NUMBER_API.format(number), timeout=15)
        safe_delete_message(message.chat.id, loading.message_id)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success') and data.get('data', {}).get('count', 0) > 0:
                results = data['data']['results']
                
                summary = f"\n━━━━━━━━━━━━━━━━━━━━\n✅ PAKISTAN NUMBER\n━━━━━━━━━━━━━━━━━━━━\n"
                summary += f"Mobile      : {number}\n"
                summary += f"Records     : {len(results)}\n"
                summary += "━━━━━━━━━━━━━━━━━━━━\n"
                bot.send_message(message.chat.id, add_footer(summary, user_id))
                
                for i, record in enumerate(results[:5], 1):
                    text = f"\n━━━━━━━━━━━━━━━━━━━━\n🇵🇰 Record #{i}\n━━━━━━━━━━━━━━━━━━━━\n"
                    text += f"Name        : {record.get('name', 'N/A')}\n"
                    text += f"CNIC        : {record.get('cnic', 'N/A')}\n"
                    text += f"Address     : {record.get('address', 'N/A')[:100]}\n"
                    text += "━━━━━━━━━━━━━━━━━━━━\n"
                    bot.send_message(message.chat.id, add_footer(text, user_id))
                    time.sleep(0.3)
            else:
                bot.send_message(message.chat.id, add_footer("❌ No data found", user_id))
        else:
            bot.send_message(message.chat.id, add_footer("❌ API Error", user_id))
            
    except Exception as e:
        safe_delete_message(message.chat.id, loading.message_id)
        bot.send_message(message.chat.id, add_footer(f"❌ Error", user_id))

# ===== VEHICLE =====
@bot.message_handler(func=lambda m: m.text == "🚗 Vehicle")
def vehicle_handler(message):
    user_id = str(message.from_user.id)
    msg = bot.send_message(
        message.chat.id,
        add_footer("🚗 <b>Enter RC Number:</b>\nExample: <code>UP26R4007</code>", user_id)
    )
    bot.register_next_step_handler(msg, process_vehicle)

def process_vehicle(message):
    user_id = str(message.from_user.id)
    loading = animated_loading(message.chat.id, "🚗 Fetching Vehicle Info")
    
    try:
        rc = message.text.strip().upper()
        if len(rc) < 5:
            safe_delete_message(message.chat.id, loading.message_id)
            bot.send_message(message.chat.id, add_footer("❌ Invalid RC Number!", user_id))
            return
        
        db.add_api_usage(user_id)
        response = requests.get(VEHICLE_API.format(rc), timeout=15)
        safe_delete_message(message.chat.id, loading.message_id)
        
        if response.status_code == 200:
            data = response.json()
            
            text = f"\n━━━━━━━━━━━━━━━━━━━━\n✅ VEHICLE DETAILS\n━━━━━━━━━━━━━━━━━━━━\n"
            
            if 'Ownership Details' in data:
                od = data['Ownership Details']
                text += f"Owner       : {od.get('Owner Name', 'N/A')}\n"
                # FIXED: Backslash hata diya - ab single quotes use kiye
                fathers_name = od.get("Father's Name", 'N/A')
                text += f"Father      : {fathers_name}\n"
                text += f"Owner No.   : {od.get('Owner Serial No', 'N/A')}\n"
                text += f"RTO         : {od.get('Registered RTO', 'N/A')}\n"
            
            if 'Vehicle Details' in data:
                vd = data['Vehicle Details']
                text += f"Model       : {vd.get('Model Name', 'N/A')}\n"
                text += f"Maker       : {vd.get('Maker Model', 'N/A')}\n"
                text += f"Class       : {vd.get('Vehicle Class', 'N/A')}\n"
                text += f"Fuel        : {vd.get('Fuel Type', 'N/A')}\n"
            
            if 'Important Dates & Validity' in data:
                idv = data['Important Dates & Validity']
                text += f"Reg Date    : {idv.get('Registration Date', 'N/A')}\n"
                text += f"Fitness Upto: {idv.get('Fitness Upto', 'N/A')}\n"
                text += f"Tax Upto    : {idv.get('Tax Upto', 'N/A')}\n"
                text += f"PUC Upto    : {idv.get('PUC Upto', 'N/A')}\n"
                text += f"Insurance   : {idv.get('Insurance Upto', 'N/A')}\n"
            
            text += "━━━━━━━━━━━━━━━━━━━━\n"
            bot.send_message(message.chat.id, add_footer(text, user_id))
            
            if 'Insurance Alert' in data:
                alert = data['Insurance Alert']
                if int(alert.get('Expired Days', 0)) > 0:
                    bot.send_message(message.chat.id, add_footer(f"⚠️ Insurance expired {alert['Expired Days']} days ago!", user_id))
        else:
            bot.send_message(message.chat.id, add_footer("❌ API Error", user_id))
            
    except Exception as e:
        safe_delete_message(message.chat.id, loading.message_id)
        bot.send_message(message.chat.id, add_footer(f"❌ Error", user_id))

# ===== NAME TO AADHAAR =====
@bot.message_handler(func=lambda m: m.text == "🆔 Name to Aadhaar")
def name_to_aadhaar_handler(message):
    user_id = str(message.from_user.id)
    msg = bot.send_message(
        message.chat.id,
        add_footer("🆔 <b>ENTER NAME FOR AADHAAR SEARCH</b>\nExample: <code>Rahul</code>", user_id)
    )
    bot.register_next_step_handler(msg, process_name_to_aadhaar)

def process_name_to_aadhaar(message):
    user_id = str(message.from_user.id)
    loading = animated_loading(message.chat.id, "🆔 Searching Aadhaar")
    
    try:
        name = message.text.strip()
        if len(name) < 3:
            safe_delete_message(message.chat.id, loading.message_id)
            bot.send_message(message.chat.id, add_footer("❌ Name too short! Minimum 3 characters.", user_id))
            return
        
        db.add_api_usage(user_id)
        
        api_url = NAME_TO_AADHAAR_API.format(name)
        response = requests.get(api_url, timeout=60)
        safe_delete_message(message.chat.id, loading.message_id)
        
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                total = len(data)
                summary = f"\n━━━━━━━━━━━━━━━━━━━━\n✅ AADHAAR SEARCH RESULTS\n━━━━━━━━━━━━━━━━━━━━\n"
                summary += f"Name        : {name}\n"
                summary += f"Total Records: {total}\n"
                summary += "━━━━━━━━━━━━━━━━━━━━\n"
                bot.send_message(message.chat.id, add_footer(summary, user_id))
                
                chunk_size = 10
                for i in range(0, len(data), chunk_size):
                    chunk_text = ""
                    chunk = data[i:i+chunk_size]
                    
                    for j, record in enumerate(chunk, i+1):
                        if isinstance(record, dict):
                            chunk_text += f"\n━━━━━━━━━━━━━━━━━━━━\n🆔 Record #{j}\n━━━━━━━━━━━━━━━━━━━━\n"
                            chunk_text += f"Aadhaar     : {record.get('aadhaar', 'N/A')}\n"
                            chunk_text += f"Name        : {record.get('name', 'N/A')}\n"
                            chunk_text += f"State       : {record.get('state', 'N/A')}\n"
                            chunk_text += f"DOB         : {record.get('dob', 'N/A')}\n"
                    
                    if chunk_text:
                        bot.send_message(message.chat.id, add_footer(chunk_text, user_id))
                        time.sleep(1.5)
                    
                    if i + chunk_size >= len(data):
                        bot.send_message(message.chat.id, add_footer(f"✅ Total {total} records found", user_id))
            else:
                bot.send_message(message.chat.id, add_footer("❌ No data found", user_id))
        else:
            bot.send_message(message.chat.id, add_footer("❌ API Error", user_id))
            
    except requests.exceptions.Timeout:
        safe_delete_message(message.chat.id, loading.message_id)
        bot.send_message(message.chat.id, add_footer("❌ Request timeout! Too much data.", user_id))
    except Exception as e:
        safe_delete_message(message.chat.id, loading.message_id)
        bot.send_message(message.chat.id, add_footer(f"❌ Error", user_id))

# ===== BIN =====
@bot.message_handler(func=lambda m: m.text == "💳 BIN")
def bin_handler(message):
    user_id = str(message.from_user.id)
    msg = bot.send_message(
        message.chat.id,
        add_footer("💳 <b>Enter 6-digit BIN:</b>\nExample: <code>414709</code>", user_id)
    )
    bot.register_next_step_handler(msg, lambda m: process_general_tool(m, "bin", "BIN DETAILS", 
        {"scheme": "Scheme", "type": "Type", "brand": "Brand", "bank": "Bank", "country": "Country"}))

# ===== IP =====
@bot.message_handler(func=lambda m: m.text == "🌐 IP")
def ip_handler(message):
    user_id = str(message.from_user.id)
    msg = bot.send_message(
        message.chat.id,
        add_footer("🌐 <b>Enter IP Address:</b>\nExample: <code>8.8.8.8</code>", user_id)
    )
    bot.register_next_step_handler(msg, lambda m: process_general_tool(m, "ip", "IP DETAILS", 
        {"query": "IP", "country": "Country", "city": "City", "regionName": "Region", 
         "isp": "ISP", "org": "Organization", "timezone": "Timezone"}))

# ===== USERNAME =====
@bot.message_handler(func=lambda m: m.text == "👤 Username")
def username_handler(message):
    user_id = str(message.from_user.id)
    msg = bot.send_message(
        message.chat.id,
        add_footer("👤 <b>Enter Username:</b>\nExample: <code>john123</code>", user_id)
    )
    bot.register_next_step_handler(msg, process_username)

def process_username(message):
    user_id = str(message.from_user.id)
    loading = animated_loading(message.chat.id, "👤 Searching")
    
    try:
        username = message.text.strip()
        sites = [
            {"name": "Instagram", "url": f"https://instagram.com/{username}", "icon": "📷"},
            {"name": "Twitter", "url": f"https://twitter.com/{username}", "icon": "🐦"},
            {"name": "GitHub", "url": f"https://github.com/{username}", "icon": "💻"},
            {"name": "Telegram", "url": f"https://t.me/{username}", "icon": "📱"}
        ]
        
        db.add_api_usage(user_id)
        found = []
        
        for site in sites:
            try:
                r = requests.get(site["url"], timeout=5)
                if r.status_code == 200:
                    found.append(site)
            except:
                continue
        
        safe_delete_message(message.chat.id, loading.message_id)
        
        text = f"\n━━━━━━━━━━━━━━━━━━━━\n✅ USERNAME SEARCH\n━━━━━━━━━━━━━━━━━━━━\n"
        text += f"Username    : {username}\n"
        text += f"Found       : {len(found)}/4\n"
        text += "━━━━━━━━━━━━━━━━━━━━\n"
        bot.send_message(message.chat.id, add_footer(text, user_id))
        
        if found:
            for site in found:
                site_text = f"\n{site['icon']} {site['name']}:\n<code>{site['url']}</code>\n"
                bot.send_message(message.chat.id, add_footer(site_text, user_id), disable_web_page_preview=True)
        else:
            bot.send_message(message.chat.id, add_footer("❌ Not found on any platform", user_id))
            
    except Exception as e:
        safe_delete_message(message.chat.id, loading.message_id)
        bot.send_message(message.chat.id, add_footer("❌ Error", user_id))

# ===== NUM OWNER =====
@bot.message_handler(func=lambda m: m.text == "👤 Num Owner")
def num_owner_handler(message):
    user_id = str(message.from_user.id)
    msg = bot.send_message(
        message.chat.id,
        add_footer("👤 <b>Enter Mobile Number with 91:</b>\nExample: <code>919087654321</code>", user_id)
    )
    bot.register_next_step_handler(msg, process_num_owner)

def process_num_owner(message):
    user_id = str(message.from_user.id)
    loading = animated_loading(message.chat.id, "👤 Fetching Owner Info")
    
    try:
        number = message.text.strip()
        if not number.isdigit() or len(number) != 12 or not number.startswith('91'):
            safe_delete_message(message.chat.id, loading.message_id)
            bot.send_message(message.chat.id, add_footer("❌ Invalid! Use 91 followed by 10 digits", user_id))
            return
        
        db.add_api_usage(user_id)
        response = requests.get(NUM_OWNER_API.format(number), timeout=15)
        safe_delete_message(message.chat.id, loading.message_id)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success') and data.get('data'):
                owner = data['data']
                text = f"\n━━━━━━━━━━━━━━━━━━━━\n✅ NUMBER OWNER\n━━━━━━━━━━━━━━━━━━━━\n"
                text += f"Name        : {owner.get('name', 'N/A')}\n"
                text += f"Number      : {owner.get('number', 'N/A')}\n"
                text += "━━━━━━━━━━━━━━━━━━━━\n"
                bot.send_message(message.chat.id, add_footer(text, user_id))
            else:
                bot.send_message(message.chat.id, add_footer("❌ No data found", user_id))
        else:
            bot.send_message(message.chat.id, add_footer("❌ API Error", user_id))
            
    except Exception as e:
        safe_delete_message(message.chat.id, loading.message_id)
        bot.send_message(message.chat.id, add_footer(f"❌ Error", user_id))

# ===== GENERAL TOOL PROCESSOR =====
@bot.message_handler(func=lambda m: m.text in [
    "📧 Email", "🏦 IFSC", "🎮 FF Info", "🎮 FF Ban", "💻 GitHub",
    "👨‍👩‍👧‍👦 Num Family", "🏦 IFSC Lookup", "💳 BIN Lookup", "🌐 Domain"
])
def general_tool_handler(message):
    user_id = str(message.from_user.id)
    
    tool_map = {
        "📧 Email": ("email", "EMAIL DETAILS", {"email": "Email", "name": "Name", "domain": "Domain"}),
        "🏦 IFSC": ("ifsc", "IFSC CODE DETAILS", {"BANK": "Bank", "BRANCH": "Branch", "IFSC": "IFSC", "MICR": "MICR", "ADDRESS": "Address", "CITY": "City", "DISTRICT": "District", "STATE": "State"}),
        "🎮 FF Info": ("ff_info", "FREE FIRE INFO", {"nickname": "Nickname", "uid": "UID", "level": "Level", "region": "Region"}),
        "🎮 FF Ban": ("ff_ban", "FREE FIRE BAN STATUS", {"uid": "UID", "status": "Status", "ban_type": "Ban Type", "reason": "Reason"}),
        "💻 GitHub": ("github", "GITHUB INFO", {"login": "Username", "name": "Name", "bio": "Bio", "public_repos": "Repos", "followers": "Followers", "following": "Following"}),
        "👨‍👩‍👧‍👦 Num Family": ("number_to_family", "NUMBER FAMILY", {"number": "Number", "family": "Family Members"}),
        "🏦 IFSC Lookup": ("ifsc_old", "IFSC LOOKUP", {"BANK": "Bank", "BRANCH": "Branch", "IFSC": "IFSC", "ADDRESS": "Address"}),
        "💳 BIN Lookup": ("bin_new", "BIN LOOKUP", {"bank": "Bank", "scheme": "Scheme", "type": "Type", "country": "Country"}),
        "🌐 Domain": ("domain", "DOMAIN INFO", {"domain": "Domain", "registrar": "Registrar", "creation_date": "Created", "expiration_date": "Expires", "name_servers": "Name Servers"})
    }
    
    tool_type, title, field_map = tool_map.get(message.text, (None, None, None))
    if not tool_type:
        return
    
    msg = bot.send_message(
        message.chat.id,
        add_footer(f"{message.text}\nEnter value:", user_id)
    )
    bot.register_next_step_handler(msg, lambda m: process_general_tool(m, tool_type, title, field_map))

def process_general_tool(message, tool_type, title, field_map):
    user_id = str(message.from_user.id)
    loading = animated_loading(message.chat.id, f"🔍 Fetching")
    
    try:
        query = message.text.strip()
        
        if tool_type in API_ENDPOINTS:
            api_url = API_ENDPOINTS[tool_type].format(query)
            
            db.add_api_usage(user_id)
            response = requests.get(api_url, timeout=15)
            
            safe_delete_message(message.chat.id, loading.message_id)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, dict):
                    if data.get('success') == False:
                        bot.send_message(message.chat.id, add_footer(f"❌ No data found for {query}", user_id))
                    else:
                        result_data = {}
                        if 'data' in data:
                            result_data = data['data']
                        elif 'results' in data and len(data['results']) > 0:
                            if isinstance(data['results'], list) and len(data['results']) > 0:
                                result_data = data['results'][0]
                        else:
                            result_data = data
                        
                        text = f"\n━━━━━━━━━━━━━━━━━━━━\n✅ {title}\n━━━━━━━━━━━━━━━━━━━━\n"
                        for api_key, display_key in field_map.items():
                            value = result_data.get(api_key, 'N/A')
                            if value and str(value).strip() and str(value).lower() != 'null':
                                if isinstance(value, list):
                                    value = ', '.join(str(v) for v in value[:3])
                                text += f"{display_key:<12}: {value}\n"
                        text += "━━━━━━━━━━━━━━━━━━━━\n"
                        
                        bot.send_message(message.chat.id, add_footer(text, user_id))
                else:
                    bot.send_message(message.chat.id, add_footer(f"✅ {title} completed", user_id))
            else:
                bot.send_message(message.chat.id, add_footer("❌ API Error", user_id))
        else:
            bot.send_message(message.chat.id, add_footer("❌ Tool unavailable", user_id))
            
    except Exception as e:
        safe_delete_message(message.chat.id, loading.message_id)
        bot.send_message(message.chat.id, add_footer("❌ Error", user_id))

# ===== DASHBOARD =====
@bot.message_handler(func=lambda m: m.text == "📊 Dashboard")
def dashboard_handler(message):
    user_id = str(message.from_user.id)
    user = db.get_user(user_id)
    
    if not user:
        bot.send_message(message.chat.id, add_footer("❌ Send /start first", user_id))
        return
    
    api_uses = user.get('api_uses', 0)
    total_users = db.get_total_users()
    
    text = f"""
━━━━━━━━━━━━━━━━━━━━
📊 DASHBOARD
━━━━━━━━━━━━━━━━━━━━
👤 User      : {message.from_user.first_name}
🆔 ID        : {user_id}
📊 API Uses  : {api_uses}
👥 Total Users: {total_users}
━━━━━━━━━━━━━━━━━━━━
"""
    bot.send_message(message.chat.id, add_footer(text, user_id))

# ===== HELP =====
@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def help_handler(message):
    user_id = str(message.from_user.id)
    
    text = f"""
━━━━━━━━━━━━━━━━━━━━
ℹ️ HELP - EXODUS OSINT BOT
━━━━━━━━━━━━━━━━━━━━
📞 NUMBER LOOKUP:
• 📱 India Number
• 🇵🇰 Pakistan Num

🆔 IDENTITY:
• 🆔 Name to Aadhaar

🚗 VEHICLE:
• 🚗 Vehicle RC

💳 FINANCIAL:
• 💳 BIN
• 💳 BIN Lookup
• 🏦 IFSC
• 🏦 IFSC Lookup

🌐 NETWORK:
• 🌐 IP
• 🌐 Domain

👤 SOCIAL:
• 👤 Username
• 📧 Email
• 💻 GitHub

🎮 GAMING:
• 🎮 FF Info
• 🎮 FF Ban

📱 OTHER:
• 👨‍👩‍👧‍👦 Num Family
• 👤 Num Owner

━━━━━━━━━━━━━━━━━━━━
"""
    bot.send_message(message.chat.id, add_footer(text, user_id))

# ===== ADMIN COMMAND =====
@bot.message_handler(commands=['admin'])
def admin_command(message):
    user_id = message.from_user.id
    if not db.is_admin(user_id):
        bot.send_message(message.chat.id, add_footer("❌ ACCESS DENIED"))
        return
    
    total_users = db.get_total_users()
    stats = db.get_stats()
    
    text = f"""
━━━━━━━━━━━━━━━━━━━━
👑 ADMIN PANEL
━━━━━━━━━━━━━━━━━━━━
Admin ID    : {user_id}
Total Users : {total_users}
API Calls   : {stats.get('total_api_calls', 0)}
━━━━━━━━━━━━━━━━━━━━
"""
    bot.send_message(message.chat.id, add_footer(text, str(user_id)), reply_markup=get_admin_menu())

# ===== ADMIN STATS =====
@bot.message_handler(func=lambda m: m.text == "📊 Stats")
def admin_stats_handler(message):
    user_id = message.from_user.id
    if not db.is_admin(user_id):
        return
    
    total_users = db.get_total_users()
    users = db.get_all_users()
    
    banned_count = sum(1 for u in users if u[6] == 1)
    total_api_uses = sum(u[5] for u in users)
    
    active_users = 0
    current_time = time.time()
    for user in users:
        if user[4] and (current_time - user[4]) < 86400:
            active_users += 1
    
    text = f"""
━━━━━━━━━━━━━━━━━━━━
📊 ADMIN STATISTICS
━━━━━━━━━━━━━━━━━━━━
Total Users : {total_users}
Active Today: {active_users}
Banned      : {banned_count}
API Uses    : {total_api_uses}
━━━━━━━━━━━━━━━━━━━━
"""
    bot.send_message(message.chat.id, add_footer(text, str(user_id)))

# ===== ALL USERS =====
@bot.message_handler(func=lambda m: m.text == "👥 All Users")
def all_users_handler(message):
    user_id = message.from_user.id
    if not db.is_admin(user_id):
        return
    
    users = db.get_all_users()
    if not users:
        bot.send_message(message.chat.id, add_footer("No users found.", str(user_id)))
        return
    
    text = f"━━━━━━━━━━━━━━━━━━━━\n👥 ALL USERS ({len(users)})\n━━━━━━━━━━━━━━━━━━━━\n"
    for i, user in enumerate(users[:20], 1):
        username = user[1] if user[1] != 'N/A' else 'NoUsername'
        name = user[2][:15]
        api_uses = user[5]
        text += f"{i}. @{username[:15]} - {name} - {api_uses} uses\n"
    
    bot.send_message(message.chat.id, add_footer(text, str(user_id)))

# ===== BAN USER =====
@bot.message_handler(func=lambda m: m.text == "⛔ Ban User")
def ban_user_handler(message):
    user_id = message.from_user.id
    if not db.is_admin(user_id):
        return
    
    msg = bot.send_message(
        message.chat.id,
        add_footer("⛔ Enter User ID to ban:", str(user_id))
    )
    bot.register_next_step_handler(msg, process_ban_user)

def process_ban_user(message):
    user_id = str(message.from_user.id)
    target_id = message.text.strip()
    
    if not db.get_user(target_id):
        bot.send_message(message.chat.id, add_footer("❌ User not found!", user_id))
        return
    
    db.ban_user(target_id)
    bot.send_message(message.chat.id, add_footer(f"✅ User {target_id} banned!", user_id))

# ===== UNBAN USER =====
@bot.message_handler(func=lambda m: m.text == "✅ Unban User")
def unban_user_handler(message):
    user_id = message.from_user.id
    if not db.is_admin(user_id):
        return
    
    msg = bot.send_message(
        message.chat.id,
        add_footer("✅ Enter User ID to unban:", str(user_id))
    )
    bot.register_next_step_handler(msg, process_unban_user)

def process_unban_user(message):
    user_id = str(message.from_user.id)
    target_id = message.text.strip()
    
    if not db.get_user(target_id):
        bot.send_message(message.chat.id, add_footer("❌ User not found!", user_id))
        return
    
    db.unban_user(target_id)
    bot.send_message(message.chat.id, add_footer(f"✅ User {target_id} unbanned!", user_id))

# ===== BROADCAST =====
@bot.message_handler(func=lambda m: m.text == "📢 Broadcast")
def broadcast_handler(message):
    user_id = message.from_user.id
    if not db.is_admin(user_id):
        return
    
    msg = bot.send_message(
        message.chat.id,
        add_footer("📢 Enter broadcast message:", str(user_id))
    )
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    user_id = str(message.from_user.id)
    broadcast_msg = message.text
    
    users = db.get_all_users()
    total = len(users)
    sent = 0
    
    for user in users:
        try:
            if user[6] == 0:
                bot.send_message(int(user[0]), add_footer(f"📢 BROADCAST\n\n{broadcast_msg}", user[0]))
                sent += 1
                time.sleep(0.05)
        except:
            pass
    
    bot.send_message(message.chat.id, add_footer(f"✅ Broadcast sent to {sent}/{total} users", user_id))

# ===== EXPORT DATA =====
@bot.message_handler(func=lambda m: m.text == "📥 Export Data")
def export_data_handler(message):
    user_id = message.from_user.id
    if not db.is_admin(user_id):
        return
    
    loading = bot.send_message(message.chat.id, "📥 Exporting...")
    
    users = db.get_all_users()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['User ID', 'Username', 'Name', 'Joined', 'Last Seen', 'API Uses', 'Banned'])
    
    for user in users:
        writer.writerow([
            user[0], user[1], user[2],
            datetime.fromtimestamp(user[3]).strftime('%Y-%m-%d') if user[3] else 'N/A',
            datetime.fromtimestamp(user[4]).strftime('%Y-%m-%d %H:%M') if user[4] else 'N/A',
            user[5], 'Yes' if user[6] == 1 else 'No'
        ])
    
    output.seek(0)
    bot.delete_message(message.chat.id, loading.message_id)
    
    filename = f"users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    bot.send_document(
        message.chat.id,
        (filename, io.BytesIO(output.getvalue().encode())),
        caption=add_footer(f"✅ Exported {len(users)} users", str(user_id))
    )

# ===== BACK TO MAIN =====
@bot.message_handler(func=lambda m: m.text == "🔙 Main Menu")
def back_to_main_handler(message):
    user_id = str(message.from_user.id)
    bot.send_message(
        message.chat.id,
        add_footer("🏠 MAIN MENU\nSelect a tool:", user_id),
        reply_markup=get_main_menu()
    )

# ===== DEFAULT HANDLER =====
@bot.message_handler(func=lambda m: True)
def default_handler(message):
    user_id = str(message.from_user.id)
    user_data = db.get_user(user_id)
    
    if not user_data:
        bot.send_message(message.chat.id, add_footer("🤔 Send /start to begin!"))
        return
    
    if user_data.get('banned', 0) == 1:
        return
    
    db.update_last_seen(user_id)
    bot.send_message(
        message.chat.id,
        add_footer("💡 Use menu buttons to access tools.", user_id),
        reply_markup=get_main_menu()
    )

# ===== AUTO BACKUP =====
def auto_backup_task():
    while True:
        try:
            time.sleep(6 * 3600)
            backup_filename = f"backup_users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as original:
                    data = json.load(original)
                with open(backup_filename, 'w', encoding='utf-8') as backup:
                    json.dump(data, backup, indent=2, ensure_ascii=False)
                print(f"✅ Auto-backup: {backup_filename}")
                
                backup_files = sorted([f for f in os.listdir() if f.startswith('backup_users_') and f.endswith('.json')])
                if len(backup_files) > 5:
                    for old_file in backup_files[:-5]:
                        os.remove(old_file)
        except Exception as e:
            print(f"❌ Backup error: {e}")
            time.sleep(3600)

threading.Thread(target=auto_backup_task, daemon=True).start()

# ===== START BOT =====
if __name__ == "__main__":
    print(f"""
╔══════════════════════════════════════╗
║      EXODUS OSINT BOT STARTED       ║
║          Darknyte Exodus            ║
║       {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}       ║
╚══════════════════════════════════════╝

✅ JSON STORAGE: users_data.json
✅ EXISTING USERS: {db.get_total_users()}
✅ AUTO-SAVE: Enabled
✅ AUTO-BACKUP: Every 6 hours
✅ SYNTAX ERROR FIXED: Vehicle API

📢 MANDATORY CHANNELS (3):
   📢 Main Channel (Private)
   🌑 darknyteexodus (Private)
   💾 Backup Channel (Public)
   
▶️ OPTIONAL: EXODUS YOUTUBE

🚀 BOT IS RUNNING...
""")
    
    while True:
        try:
            bot.infinity_polling(timeout=60)
        except Exception as e:
            print(f"❌ Bot error: {e}")
            print("🔄 Restarting in 5 seconds...")
            time.sleep(5)
