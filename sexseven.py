#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import logging
import time
import random
from datetime import datetime
from threading import Lock

import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = "8651388063:AAHDwDc_oOSATUkL36l3huwcArdtOlXWswU"
BOT_USERNAME = "XStarPlayBot"
BRAND_NAME = "XStars"
ADMIN_IDS = [8691006987, 6358456805]
MIN_BET = 1
MIN_DEPOSIT = 5
MIN_WITHDRAW = 100
REQUIRED_CHANNEL = "xstarschan"
CHAT_LINK = "https://t.me/XstarsDep"
CHANNEL_LINK = "https://t.me/xstarschan"
COMMISSION = 0.05
REF_BONUS = 3

EMOJI_STAR = "5438496463044752972"
EMOJI_PLAY = "5361741454685256344"
EMOJI_PROFILE = "5416041192905265756"
EMOJI_STATS = "5445353829304387411"
EMOJI_DEPOSIT = "5443127283898405358"
EMOJI_WITHDRAW = "5445355530111437729"
EMOJI_BONUS = "5199552030615558774"
EMOJI_WIN = "5449683594425410231"
EMOJI_LOSE = "5447183459602669338"
EMOJI_RATING = "5445221832074483553"

DB_NAME = "xstars.db"
db_lock = Lock()

TEXTS = {
    'ru': {
        'welcome': "👋 <b>Добро пожаловать в XStars!</b>\n\n<blockquote>Здесь сбываются мечты и рождаются крупные выигрыши. Азарт — это не слепой риск, а искусство управлять удачей.</blockquote>",
        'balance': "Баланс", 'bet': "Ставка", 'choose_game': "🎮 <b>Выберите игру</b>",
        'ref_system_btn': "🎁 Реферальная система", 'play_btn': "🎮 Играть",
        'rating_btn': "🏆 Рейтинг", 'channel_btn': "📢 Канал", 'chat_btn': "💬 Чат",
        'top_title': "🏆 <b>Топ-10 игроков</b>",
        'profile_btn': "👤 Профиль", 'language_btn': "🌐 Язык",
        'dice_btn': "🎲 Кубик", 'football_btn': "⚽ Футбол", 'basket_btn': "🏀 Баскет",
        'darts_btn': "🎯 Дартс", 'bowling_btn': "🎳 Боулинг", 'slots_btn': "🎰 Слоты",
        'mines_btn': "💣 Мины", 'upgrader_btn': "⬆️ Апгрейдер", 'deposit_btn': "💚 Пополнить",
        'back_btn': "🔙 Назад",
        'ref_title': "🎁 <b>Реферальная система</b>",
        'ref_desc': "Приглашай друзей и получай <b>3 ⭐</b> за каждого!",
        'your_link': "🔗 Твоя ссылка:", 'invited': "👥 Приглашено", 'earned': "💰 Заработано",
        'share': "📤 Поделиться",
        'profile': "👤 <b>Профиль</b>", 'stats': "📊 <b>Статистика</b>",
        'turnover': "Оборот", 'wins': "Победы", 'losses': "Поражения",
        'deposits': "Пополнения", 'withdraws': "Выводы",
        'deposit': "⭐ <b>Пополнение звёздами</b>\n\nВведите количество (мин. 5):",
        'withdraw': "📤 <b>Вывод</b>",
        'lang_changed': "✅ Язык изменён", 'choose_lang': "🌐 <b>Выберите язык:</b>",
        'not_subbed': "❌ Ты не подписан!", 'banned': "🚫 Вы забанены.",
        'bet_min': "❌ Минимум 1 ⭐", 'bet_set': "✅ Ставка:",
        'bet_show': "🎯 <b>Текущая ставка:</b>", 'bet_not_set': "❌ Ставка не установлена. Напиши «ставка»",
        'no_money': "❌ Недостаточно средств", 'win_text': "🎉 <b>Выигрыш!</b>",
        'lose_msg': "😢 <b>Проигрыш</b>",
        'lose_texts': ["😢 <b>Проигрыш</b>", "💔 <b>Не повезло.</b> Ещё раз?", "😞 <b>Мимо.</b> Крути ещё!", "😔 <b>Обидно.</b> Попробуй снова"],
        'play_again': "Хочешь ещё? 😏",
        'bonus_btn': "🎁 Бонус", 'deposit_btn_short': "📥 Пополнить", 'withdraw_btn': "📤 Вывод",
        'bonus_title': "🎁 <b>Ежедневный бонус</b>",
        'bonus_desc': "Получи от 1 до 10 ⭐ раз в 24 часа!\n\nДля получения в профиле Telegram должно быть:\n<b>*лучший казик в телеграме @XStarPlayBot*</b>",
        'bonus_claim': "🎁 Получить", 'bonus_next': "⏳ Следующий бонус через",
        'spinning': "🎰 <b>Крутим...</b>", 'luck': "💫 Удачи!", 'take': "💰 Забрать",
        'mines_choose': "Выберите количество мин:", 'mines_custom': "✏️ Ввести своё (1-24)",
        'mines_3': "3 мины", 'mines_5': "5 мин", 'mines_10': "10 мин",
        'upg_choose': "Выберите шанс победы:", 'upg_custom': "✏️ Свой процент",
        'bet_choose': "Выберите новую:", 'bet_custom': "✏️ Своё",
        'not_your_game': "❌ Это не твоя игра!", 'open_at_least_one': "❌ Открой хотя бы одну клетку",
        'bomb': "💣 <b>Бомба!</b>", 'no_prev': "❌ Нет предыдущей игры",
        'nk_title': "💸 <b>Передача звёзд</b>",
        'nk_confirm': "Вы уверены, что хотите передать <b>@{name}</b> <b>{amount} ⭐</b>?",
        'nk_yes': "✅ Да", 'nk_no': "❌ Нет",
        'nk_sent': "✅ Передано <b>{amount} ⭐</b> → <b>@{name}</b>",
        'nk_received': "🎁 Вам передали <b>{amount} ⭐</b> от @{name}",
        'nk_no_money': "❌ Недостаточно средств. {balance} ⭐",
        'nk_cancelled': "❌ Отменено",
    },
    'en': {
        'welcome': "👋 <b>Welcome to XStars!</b>\n\n<blockquote>Dreams come true and big wins are born here.</blockquote>",
        'balance': "Balance", 'bet': "Bet", 'choose_game': "🎮 <b>Choose game</b>",
        'ref_system_btn': "🎁 Referral system", 'play_btn': "🎮 Play",
        'rating_btn': "🏆 Rating", 'channel_btn': "📢 Channel", 'chat_btn': "💬 Chat",
        'top_title': "🏆 <b>Top-10 players</b>",
        'profile_btn': "👤 Profile", 'language_btn': "🌐 Language",
        'dice_btn': "🎲 Dice", 'football_btn': "⚽ Football", 'basket_btn': "🏀 Basketball",
        'darts_btn': "🎯 Darts", 'bowling_btn': "🎳 Bowling", 'slots_btn': "🎰 Slots",
        'mines_btn': "💣 Mines", 'upgrader_btn': "⬆️ Upgrader", 'deposit_btn': "💚 Top up",
        'back_btn': "🔙 Back",
        'ref_title': "🎁 <b>Referral system</b>",
        'ref_desc': "Invite friends and get <b>3 ⭐</b> for each!",
        'your_link': "🔗 Your link:", 'invited': "👥 Invited", 'earned': "💰 Earned",
        'share': "📤 Share",
        'profile': "👤 <b>Profile</b>", 'stats': "📊 <b>Statistics</b>",
        'turnover': "Turnover", 'wins': "Wins", 'losses': "Losses",
        'deposits': "Deposits", 'withdraws': "Withdraws",
        'deposit': "⭐ <b>Top up with Stars</b>\n\nEnter amount (min. 5):",
        'withdraw': "📤 <b>Withdraw</b>",
        'lang_changed': "✅ Language changed", 'choose_lang': "🌐 <b>Choose language:</b>",
        'not_subbed': "❌ You are not subscribed!", 'banned': "🚫 You are banned.",
        'bet_min': "❌ Minimum 1 ⭐", 'bet_set': "✅ Bet:",
        'bet_show': "🎯 <b>Current bet:</b>", 'bet_not_set': "❌ Bet not set. Write «bet»",
        'no_money': "❌ Insufficient funds", 'win_text': "🎉 <b>Win!</b>",
        'lose_msg': "😢 <b>Lose</b>",
        'lose_texts': ["😢 <b>Lose</b>", "💔 <b>No luck.</b> Again?", "😞 <b>Missed.</b>", "😔 <b>Too bad.</b>"],
        'play_again': "Want more? 😏",
        'bonus_btn': "🎁 Bonus", 'deposit_btn_short': "📥 Deposit", 'withdraw_btn': "📤 Withdraw",
        'bonus_title': "🎁 <b>Daily bonus</b>",
        'bonus_desc': "Get from 1 to 10 ⭐ once per 24 hours!",
        'bonus_claim': "🎁 Claim", 'bonus_next': "⏳ Next bonus in",
        'spinning': "🎰 <b>Spinning...</b>", 'luck': "💫 Good luck!", 'take': "💰 Take",
        'mines_choose': "Choose number of mines:", 'mines_custom': "✏️ Custom (1-24)",
        'mines_3': "3 mines", 'mines_5': "5 mines", 'mines_10': "10 mines",
        'upg_choose': "Choose win chance:", 'upg_custom': "✏️ Custom %",
        'bet_choose': "Choose new:", 'bet_custom': "✏️ Custom",
        'not_your_game': "❌ Not your game!", 'open_at_least_one': "❌ Open at least one cell",
        'bomb': "💣 <b>Bomb!</b>", 'no_prev': "❌ No previous game",
        'nk_title': "💸 <b>Stars transfer</b>",
        'nk_confirm': "Send <b>@{name}</b> <b>{amount} ⭐</b>?",
        'nk_yes': "✅ Yes", 'nk_no': "❌ No",
        'nk_sent': "✅ Sent <b>{amount} ⭐</b> → <b>@{name}</b>",
        'nk_received': "🎁 You received <b>{amount} ⭐</b> from @{name}",
        'nk_no_money': "❌ Insufficient funds. {balance} ⭐",
        'nk_cancelled': "❌ Cancelled",
    },
    'uk': {
        'welcome': "👋 <b>Ласкаво просимо до XStars!</b>",
        'balance': "Баланс", 'bet': "Ставка", 'choose_game': "🎮 <b>Оберіть гру</b>",
        'ref_system_btn': "🎁 Реферальна система", 'play_btn': "🎮 Грати",
        'rating_btn': "🏆 Рейтинг", 'channel_btn': "📢 Канал", 'chat_btn': "💬 Чат",
        'top_title': "🏆 <b>Топ-10 гравців</b>",
        'profile_btn': "👤 Профіль", 'language_btn': "🌐 Мова",
        'dice_btn': "🎲 Кубик", 'football_btn': "⚽ Футбол", 'basket_btn': "🏀 Баскет",
        'darts_btn': "🎯 Дартс", 'bowling_btn': "🎳 Боулінг", 'slots_btn': "🎰 Слоти",
        'mines_btn': "💣 Міни", 'upgrader_btn': "⬆️ Апгрейдер", 'deposit_btn': "💚 Поповнити",
        'back_btn': "🔙 Назад",
        'ref_title': "🎁 <b>Реферальна система</b>", 'ref_desc': "Запрошуй друзів!",
        'your_link': "🔗 Твоє посилання:", 'invited': "👥 Запрошено", 'earned': "💰 Зароблено",
        'share': "📤 Поділитися",
        'profile': "👤 <b>Профіль</b>", 'stats': "📊 <b>Статистика</b>",
        'turnover': "Обіг", 'wins': "Перемоги", 'losses': "Поразки",
        'deposits': "Поповнення", 'withdraws': "Виведення",
        'deposit': "⭐ <b>Поповнення зірками</b>\n\nВведіть кількість (мін. 5):",
        'withdraw': "📤 <b>Виведення</b>",
        'lang_changed': "✅ Мову змінено", 'choose_lang': "🌐 <b>Оберіть мову:</b>",
        'not_subbed': "❌ Ти не підписаний!", 'banned': "🚫 Ви забанені.",
        'bet_min': "❌ Мінімум 1 ⭐", 'bet_set': "✅ Ставка:",
        'bet_show': "🎯 <b>Поточна ставка:</b>", 'bet_not_set': "❌ Ставка не встановлена",
        'no_money': "❌ Недостатньо коштів", 'win_text': "🎉 <b>Виграш!</b>",
        'lose_msg': "😢 <b>Програш</b>",
        'lose_texts': ["😢 <b>Програш</b>", "💔 <b>Не пощастило.</b>", "😞 <b>Мимо.</b>", "😔 <b>Шкода.</b>"],
        'play_again': "Хочеш ще? 😏",
        'bonus_btn': "🎁 Бонус", 'deposit_btn_short': "📥 Поповнити", 'withdraw_btn': "📤 Вивести",
        'bonus_title': "🎁 <b>Щоденний бонус</b>", 'bonus_desc': "Отримай від 1 до 10 ⭐ раз на 24 години!",
        'bonus_claim': "🎁 Отримати", 'bonus_next': "⏳ Наступний бонус через",
        'spinning': "🎰 <b>Крутимо...</b>", 'luck': "💫 Удачі!", 'take': "💰 Забрати",
        'mines_choose': "Оберіть кількість мін:", 'mines_custom': "✏️ Своє (1-24)",
        'mines_3': "3 міни", 'mines_5': "5 мін", 'mines_10': "10 мін",
        'upg_choose': "Оберіть шанс перемоги:", 'upg_custom': "✏️ Свій %",
        'bet_choose': "Оберіть нову:", 'bet_custom': "✏️ Своє",
        'not_your_game': "❌ Не твоя гра!", 'open_at_least_one': "❌ Відкрий хоча б одну клітинку",
        'bomb': "💣 <b>Бомба!</b>", 'no_prev': "❌ Немає попередньої гри",
        'nk_title': "💸 <b>Передача зірок</b>",
        'nk_confirm': "Передати <b>@{name}</b> <b>{amount} ⭐</b>?",
        'nk_yes': "✅ Так", 'nk_no': "❌ Ні",
        'nk_sent': "✅ Передано <b>{amount} ⭐</b> → <b>@{name}</b>",
        'nk_received': "🎁 Вам передали <b>{amount} ⭐</b> від @{name}",
        'nk_no_money': "❌ Недостатньо коштів. {balance} ⭐",
        'nk_cancelled': "❌ Скасовано",
    },
    'fa': {
        'welcome': "👋 <b>به XStars خوش آمدید!</b>",
        'balance': "موجودی", 'bet': "شرط", 'choose_game': "🎮 <b>بازی را انتخاب کنید</b>",
        'ref_system_btn': "🎁 سیستم ارجاع", 'play_btn': "🎮 بازی",
        'rating_btn': "🏆 رتبه", 'channel_btn': "📢 کانال", 'chat_btn': "💬 چت",
        'top_title': "🏆 <b>10 بازیکن برتر</b>",
        'profile_btn': "👤 پروفایل", 'language_btn': "🌐 زبان",
        'dice_btn': "🎲 تاس", 'football_btn': "⚽ فوتبال", 'basket_btn': "🏀 بسکتبال",
        'darts_btn': "🎯 دارت", 'bowling_btn': "🎳 بولینگ", 'slots_btn': "🎰 اسلات",
        'mines_btn': "💣 مین", 'upgrader_btn': "⬆️ آپگریدر", 'deposit_btn': "💚 شارژ",
        'back_btn': "🔙 بازگشت",
        'ref_title': "🎁 <b>سیستم ارجاع</b>", 'ref_desc': "دوستان را دعوت کنید!",
        'your_link': "🔗 لینک شما:", 'invited': "👥 دعوت شده", 'earned': "💰 درآمد",
        'share': "📤 اشتراک",
        'profile': "👤 <b>پروفایل</b>", 'stats': "📊 <b>آمار</b>",
        'turnover': "گردش", 'wins': "بردها", 'losses': "باخت‌ها",
        'deposits': "واریزها", 'withdraws': "برداشت‌ها",
        'deposit': "⭐ <b>شارژ با ستاره</b>\n\nمقدار (حداقل 5):",
        'withdraw': "📤 <b>برداشت</b>",
        'lang_changed': "✅ زبان تغییر کرد", 'choose_lang': "🌐 <b>زبان را انتخاب کنید:</b>",
        'not_subbed': "❌ شما عضو نیستید!", 'banned': "🚫 شما مسدود شده‌اید.",
        'bet_min': "❌ حداقل 1 ⭐", 'bet_set': "✅ شرط:",
        'bet_show': "🎯 <b>شرط فعلی:</b>", 'bet_not_set': "❌ شرط تعیین نشده",
        'no_money': "❌ موجودی کافی نیست", 'win_text': "🎉 <b>برد!</b>",
        'lose_msg': "😢 <b>باخت</b>",
        'lose_texts': ["😢 <b>باخت</b>", "💔 <b>شانس نبود.</b>", "😞 <b>از دست رفت.</b>", "😔 <b>افسوس.</b>"],
        'play_again': "بیشتر می‌خواهی؟ 😏",
        'bonus_btn': "🎁 جایزه", 'deposit_btn_short': "📥 شارژ", 'withdraw_btn': "📤 برداشت",
        'bonus_title': "🎁 <b>جایزه روزانه</b>", 'bonus_desc': "هر 24 ساعت 1 تا 10 ⭐!",
        'bonus_claim': "🎁 دریافت", 'bonus_next': "⏳ جایزه بعدی در",
        'spinning': "🎰 <b>در حال چرخش...</b>", 'luck': "💫 موفق باشید!", 'take': "💰 گرفتن",
        'mines_choose': "تعداد مین:", 'mines_custom': "✏️ سفارشی",
        'mines_3': "3 مین", 'mines_5': "5 مین", 'mines_10': "10 مین",
        'upg_choose': "شانس برد:", 'upg_custom': "✏️ درصد سفارشی",
        'bet_choose': "جدید:", 'bet_custom': "✏️ سفارشی",
        'not_your_game': "❌ بازی شما نیست!", 'open_at_least_one': "❌ حداقل یک خانه باز کن",
        'bomb': "💣 <b>بمب!</b>", 'no_prev': "❌ بازی قبلی نیست",
        'nk_title': "💸 <b>انتقال ستاره</b>",
        'nk_confirm': "ارسال <b>@{name}</b> <b>{amount} ⭐</b>?",
        'nk_yes': "✅ بله", 'nk_no': "❌ خیر",
        'nk_sent': "✅ ارسال شد <b>{amount} ⭐</b> → <b>@{name}</b>",
        'nk_received': "🎁 دریافت کردید <b>{amount} ⭐</b> از @{name}",
        'nk_no_money': "❌ موجودی کافی نیست. {balance} ⭐",
        'nk_cancelled': "❌ لغو شد",
    },
}


def init_db():
    with db_lock:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT,
            language TEXT DEFAULT 'ru', balance INTEGER DEFAULT 0,
            bet_amount INTEGER DEFAULT 0, total_bets INTEGER DEFAULT 0,
            total_wins INTEGER DEFAULT 0, total_losses INTEGER DEFAULT 0,
            total_deposits INTEGER DEFAULT 0, total_withdraws INTEGER DEFAULT 0,
            reg_date TEXT, banned INTEGER DEFAULT 0, last_bonus TEXT DEFAULT NULL,
            referrer_id INTEGER DEFAULT NULL, ref_bonus_paid INTEGER DEFAULT 0
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS bets (
            bet_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, game TEXT,
            amount INTEGER, strategy TEXT, coefficient REAL, result TEXT,
            win_amount INTEGER, created_at TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS withdrawals (
            withdraw_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,
            amount INTEGER, username_to TEXT, status TEXT DEFAULT 'pending',
            created_at TEXT, completed_at TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS referrals (
            referrer_id INTEGER, referred_id INTEGER, created_at TEXT
        )''')
        conn.commit()
        conn.close()


init_db()


def db_exec(query, params=(), fetch=False, commit=True):
    with db_lock:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(query, params)
        result = c.fetchall() if fetch else None
        if commit:
            conn.commit()
        conn.close()
        return result


def E(key, fallback="⭐"):
    ids = {
        'star': EMOJI_STAR, 'play': EMOJI_PLAY, 'profile': EMOJI_PROFILE,
        'stats': EMOJI_STATS, 'deposit': EMOJI_DEPOSIT, 'withdraw': EMOJI_WITHDRAW,
        'bonus': EMOJI_BONUS, 'win': EMOJI_WIN, 'lose': EMOJI_LOSE, 'rating': EMOJI_RATING
    }
    eid = ids.get(key)
    if eid:
        return f'<tg-emoji emoji-id="{eid}">{fallback}</tg-emoji>'
    return fallback


def S():
    return E('star', '⭐')


def rep(text):
    return text.replace('⭐', f'<tg-emoji emoji-id="{EMOJI_STAR}">⭐</tg-emoji>')


def get_user(uid):
    res = db_exec("SELECT * FROM users WHERE user_id=?", (uid,), fetch=True)
    if res:
        cols = ['user_id', 'username', 'first_name', 'language', 'balance', 'bet_amount',
                'total_bets', 'total_wins', 'total_losses', 'total_deposits',
                'total_withdraws', 'reg_date', 'banned', 'last_bonus',
                'referrer_id', 'ref_bonus_paid']
        return dict(zip(cols, res[0]))
    return None


def get_lang(uid):
    u = get_user(uid)
    return u.get('language', 'ru') if u else 'ru'


def T(uid, key):
    lang = get_lang(uid)
    d = TEXTS.get(lang, TEXTS['ru'])
    return d.get(key, TEXTS['ru'].get(key, key))


def create_user(uid, username, first_name, referrer_id=None):
    now = datetime.now().isoformat()
    db_exec("""INSERT OR IGNORE INTO users
        (user_id, username, first_name, language, balance, bet_amount, reg_date, referrer_id)
        VALUES (?, ?, ?, 'ru', 0, 0, ?, ?)""",
            (uid, username or '', first_name or '', now, referrer_id))
    if referrer_id:
        db_exec("INSERT OR IGNORE INTO referrals (referrer_id, referred_id, created_at) VALUES (?, ?, ?)",
                (referrer_id, uid, now))


def set_bet_amount(uid, amt):
    db_exec("UPDATE users SET bet_amount=? WHERE user_id=?", (amt, uid))


def set_language(uid, lang):
    db_exec("UPDATE users SET language=? WHERE user_id=?", (lang, uid))


def add_balance(uid, amt):
    db_exec("UPDATE users SET balance = balance + ? WHERE user_id=?", (amt, uid))


def get_balance(uid):
    u = get_user(uid)
    return u['balance'] if u else 0


def add_stat(uid, field, amt=1):
    db_exec(f"UPDATE users SET {field} = {field} + ? WHERE user_id=?", (amt, uid))


def save_bet(uid, game, amount, strategy, coef, result, win_amt):
    db_exec("""INSERT INTO bets (user_id, game, amount, strategy, coefficient, result, win_amount, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (uid, game, amount, strategy, coef, result, win_amt, datetime.now().isoformat()))


def get_ref_count(uid):
    res = db_exec("SELECT COUNT(*) FROM referrals WHERE referrer_id=?", (uid,), fetch=True)
    return res[0][0] if res else 0


def get_top_users(limit=10):
    res = db_exec("""SELECT user_id, first_name, username, balance, total_wins
        FROM users WHERE banned=0 AND total_bets > 0
        ORDER BY total_wins DESC, balance DESC LIMIT ?""", (limit,), fetch=True)
    if res:
        cols = ['user_id', 'first_name', 'username', 'balance', 'total_wins']
        return [dict(zip(cols, r)) for r in res]
    return []


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(message)s',
                    handlers=[logging.FileHandler("xstars.log", encoding='utf-8')])
logger = logging.getLogger("XStars")

telebot.apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='HTML')

OWNER_CHECK_PREFIXES = (
    'dice1_', 'dice2_', 'dice3_',
    'dice_throws_',
    'fb_', 'dt_', 'bw_', 'sl_',
    'mines_bombs_', 'mines_click_', 'mines_custom_',
    'mines_cash_', 'mines_noop_',
    'upg_pct_',
    'back_to_games_',
    'nk_yes_', 'nk_no_',
)


@bot.middleware_handler(update_types=['callback_query'])
def protect_buttons(bot_instance, call):
    try:
        data = call.data or ''
        if data.startswith('wd_ok_') or data.startswith('wd_no_'):
            if call.from_user.id not in ADMIN_IDS:
                bot_instance.answer_callback_query(call.id, "❌ Нет доступа", show_alert=True)
                call.data = "blocked_0"
            return
        if data.startswith(OWNER_CHECK_PREFIXES):
            parts = data.split('_')
            if parts[-1].isdigit():
                owner_id = int(parts[-1])
                if owner_id != 0 and call.from_user.id != owner_id:
                    bot_instance.answer_callback_query(call.id, "❌ Это не твоя игра!", show_alert=True)
                    call.data = "blocked_0"
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data == "blocked_0")
def blocked_cb(call):
    pass


def check_subscription(uid):
    try:
        member = bot.get_chat_member(f"@{REQUIRED_CHANNEL}", uid)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False


def give_ref_bonus(user):
    if not user or user.get('ref_bonus_paid'):
        return
    ref_id = user.get('referrer_id')
    if not ref_id:
        return
    if not check_subscription(user['user_id']):
        return
    add_balance(ref_id, REF_BONUS)
    db_exec("UPDATE users SET ref_bonus_paid=1 WHERE user_id=?", (user['user_id'],))
    try:
        bot.send_message(ref_id, rep(f"🎁 По вашей ссылке зашёл друг! +{REF_BONUS} ⭐"))
    except:
        pass


def get_reply_keyboard(lang='ru'):
    m = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    if lang == 'en':
        m.add(KeyboardButton("👤 Profile"), KeyboardButton("🎮 Play"), KeyboardButton("🌐 Language"))
    elif lang == 'uk':
        m.add(KeyboardButton("👤 Профіль"), KeyboardButton("🎮 Грати"), KeyboardButton("🌐 Мова"))
    elif lang == 'fa':
        m.add(KeyboardButton("👤 پروفایل"), KeyboardButton("🎮 بازی"), KeyboardButton("🌐 زبان"))
    else:
        m.add(KeyboardButton("👤 Профиль"), KeyboardButton("🎮 Играть"), KeyboardButton("🌐 Язык"))
    return m


def get_main_inline(uid):
    m = InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton(T(uid, 'play_btn'), callback_data="play_menu"))
    m.add(
        InlineKeyboardButton(T(uid, 'channel_btn'), url=CHANNEL_LINK),
        InlineKeyboardButton(T(uid, 'chat_btn'), url=CHAT_LINK)
    )
    return m


def get_main_text(user):
    bal = user.get('balance', 0) if user else 0
    lang = user.get('language', 'ru') if user else 'ru'
    w = TEXTS.get(lang, TEXTS['ru'])['welcome']
    return f"""{w}

💰 {TEXTS.get(lang, TEXTS['ru'])['balance']}: <b>{bal}</b> {S()}"""
@bot.message_handler(commands=['start'])
def start_handler(message):
    uid = message.from_user.id
    user = get_user(uid)
    ref_id = None
    if ' ' in message.text:
        parts = message.text.split()
        if len(parts) > 1 and parts[1].startswith('ref_'):
            try:
                ref_id = int(parts[1].replace('ref_', ''))
                if ref_id == uid:
                    ref_id = None
            except:
                ref_id = None
    if not user:
        create_user(uid, message.from_user.username, message.from_user.first_name, ref_id)
        user = get_user(uid)
        give_ref_bonus(user)
        user = get_user(uid)
    bot.send_message(uid, get_main_text(user), reply_markup=get_main_inline(uid))


@bot.callback_query_handler(func=lambda c: c.data == "play_menu")
def play_menu_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    text, m = get_play_menu(uid)
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=m)
    except:
        try:
            bot.send_message(uid, text, reply_markup=m)
        except:
            pass


def get_play_menu(uid):
    user = get_user(uid)
    bet = user.get('bet_amount', 0) if user else 0
    bal = user.get('balance', 0) if user else 0
    m = InlineKeyboardMarkup(row_width=3)
    m.add(
        InlineKeyboardButton("🎲", callback_data="game_dice"),
        InlineKeyboardButton("⚽", callback_data="game_football"),
        InlineKeyboardButton("🎯", callback_data="game_darts")
    )
    m.add(
        InlineKeyboardButton("🎳", callback_data="game_bowling"),
        InlineKeyboardButton("🎰", callback_data="game_slots"),
        InlineKeyboardButton("💣", callback_data="game_mines")
    )
    m.add(InlineKeyboardButton("⬆️", callback_data="game_upgrader"))
    m.add(InlineKeyboardButton(T(uid, 'back_btn'), callback_data="back_main"))
    text = f"""{T(uid, 'choose_game')}

<blockquote>💰 {T(uid, 'balance')}: <b>{bal}</b> {S()}
🎯 {T(uid, 'bet')}: <b>{bet}</b> {S()}</blockquote>"""
    return text, m


@bot.callback_query_handler(func=lambda c: c.data == "back_main")
def back_main_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    user = get_user(uid)
    try:
        bot.edit_message_text(get_main_text(user), call.message.chat.id, call.message.message_id,
                              reply_markup=get_main_inline(uid))
    except:
        pass


def check_bet(uid):
    user = get_user(uid)
    if not user:
        return None, "❌ Ошибка"
    if user.get('banned'):
        return None, T(uid, 'banned')
    bet = user.get('bet_amount', 0)
    if bet < MIN_BET:
        return None, rep(T(uid, 'bet_not_set'))
    if user.get('balance', 0) < bet:
        return None, rep(T(uid, 'no_money'))
    return bet, None


def get_result_context(call):
    return call.message.chat.id, (call.from_user.username or call.from_user.first_name)


def result_msg(chat_id, uid, win, bet, coef, username, call=None):
    user = get_user(uid)
    if win:
        gross = int(bet * coef)
        commission = int(gross * COMMISSION)
        net = gross - commission
        add_balance(uid, net)
        add_stat(uid, 'total_wins')
        add_stat(uid, 'total_bets', bet)
        w_e = E('win', '🎉')
        msg = f"{w_e} {T(uid, 'win_text')} +{net} {S()} (x{coef})\n\n{T(uid, 'play_again')}"
    else:
        add_balance(uid, -bet)
        add_stat(uid, 'total_losses')
        add_stat(uid, 'total_bets', bet)
        l_e = E('lose', '😢')
        phrase = random.choice(TEXTS.get(get_lang(uid), TEXTS['ru'])['lose_texts'])
        msg = f"{l_e} -{bet} {S()} (x{coef})\n\n<i>{phrase}</i>"
    bot.send_message(chat_id, msg)
    try:
        text, m = get_play_menu(uid)
        bot.send_message(chat_id, text, reply_markup=m)
    except:
        pass


def dice_get_kb_for_throws(uid, throws):
    m = InlineKeyboardMarkup(row_width=2)
    coef = {1: 1.6, 2: 2.8, 3: 5.5}.get(throws, 1.6)
    m.add(
        InlineKeyboardButton(f"Чётный • x{coef}", callback_data=f"dice{throws}_even_{uid}"),
        InlineKeyboardButton(f"Нечётный • x{coef}", callback_data=f"dice{throws}_odd_{uid}")
    )
    m.add(
        InlineKeyboardButton(f"Возрастающий • x{coef}", callback_data=f"dice{throws}_up_{uid}"),
        InlineKeyboardButton(f"Убывающий • x{coef}", callback_data=f"dice{throws}_down_{uid}")
    )
    m.add(InlineKeyboardButton(T(uid, 'back_btn'), callback_data=f"back_to_games_{uid}"))
    return m


@bot.callback_query_handler(func=lambda c: c.data == "game_dice")
def g_dice(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    bet, err = check_bet(uid)
    if err:
        bot.send_message(uid, err)
        return
    user = get_user(uid)
    m = InlineKeyboardMarkup(row_width=3)
    m.add(
        InlineKeyboardButton("1", callback_data=f"dice_throws_1_{uid}"),
        InlineKeyboardButton("2", callback_data=f"dice_throws_2_{uid}"),
        InlineKeyboardButton("3", callback_data=f"dice_throws_3_{uid}")
    )
    m.add(InlineKeyboardButton(T(uid, 'back_btn'), callback_data=f"back_to_games_{uid}"))
    text = f"""🎲 <b>{T(uid, 'dice_btn')}</b>

<blockquote>{T(uid, 'balance')}: {user.get('balance', 0)} {S()}
{T(uid, 'bet')}: {bet} {S()}</blockquote>

1 / 2 / 3:"""
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=m)
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith('dice_throws_'))
def dice_throws_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    parts = call.data.split('_')
    throws = int(parts[2])
    owner_id = int(parts[3])
    if uid != owner_id:
        bot.answer_callback_query(call.id, T(uid, 'not_your_game'), show_alert=True)
        return
    user = get_user(uid)
    bet, err = check_bet(uid)
    if err:
        bot.send_message(uid, err)
        return
    text = f"""🎲 <b>{T(uid, 'dice_btn')} — {throws}</b>

<blockquote>{T(uid, 'balance')}: {user.get('balance', 0)} {S()}
{T(uid, 'bet')}: {bet} {S()}</blockquote>"""
    m = dice_get_kb_for_throws(uid, throws)
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=m)
    except:
        pass


def play_dice(chat_id, uid, throws, strategy, username, call=None):
    bet, err = check_bet(uid)
    if err:
        bot.send_message(chat_id, err)
        return
    values = []
    for i in range(throws):
        msg = bot.send_dice(chat_id, emoji="🎲")
        values.append(msg.dice.value)
        if i < throws - 1:
            time.sleep(1.5)
    time.sleep(2)
    win = False
    if strategy == 'even':
        win = all(v % 2 == 0 for v in values)
    elif strategy == 'odd':
        win = all(v % 2 == 1 for v in values)
    elif strategy == 'up':
        win = all(values[i] < values[i + 1] for i in range(len(values) - 1))
    elif strategy == 'down':
        win = all(values[i] > values[i + 1] for i in range(len(values) - 1))
    coef_map = {1: 1.6, 2: 2.8, 3: 5.5}
    coef = coef_map.get(throws, 1.6)
    result_msg(chat_id, uid, win, bet, coef, username, call)
    save_bet(uid, 'dice', bet, f"{throws}_{strategy}", coef, 'win' if win else 'lose', int(bet * coef) if win else 0)


@bot.callback_query_handler(func=lambda c: c.data.startswith('dice1_') or c.data.startswith('dice2_') or c.data.startswith('dice3_'))
def dice_bet_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    parts = call.data.split('_')
    throws = int(parts[0].replace('dice', ''))
    strategy = parts[1]
    owner_id = int(parts[2])
    if uid != owner_id:
        bot.answer_callback_query(call.id, T(uid, 'not_your_game'), show_alert=True)
        return
    chat_id, username = get_result_context(call)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    play_dice(chat_id, uid, throws, strategy, username, None)


@bot.callback_query_handler(func=lambda c: c.data.startswith('back_to_games_'))
def back_games(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    owner_id = int(call.data.split('_')[-1])
    if owner_id != 0 and uid != owner_id:
        bot.answer_callback_query(call.id, T(uid, 'not_your_game'), show_alert=True)
        return
    text, m = get_play_menu(uid)
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=m)
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data == "game_football")
def g_football(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    bet, err = check_bet(uid)
    if err:
        bot.send_message(uid, err)
        return
    user = get_user(uid)
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("Гол в центр • x3.5", callback_data=f"fb_center_{uid}"),
        InlineKeyboardButton("Гол от штанги • x3.5", callback_data=f"fb_postgoal_{uid}")
    )
    m.add(
        InlineKeyboardButton("Гол в угол • x3.5", callback_data=f"fb_corner_{uid}"),
        InlineKeyboardButton("Любой гол • x1.4", callback_data=f"fb_anygoal_{uid}")
    )
    m.add(InlineKeyboardButton("Промах • x2.0", callback_data=f"fb_miss_{uid}"))
    m.add(InlineKeyboardButton(T(uid, 'back_btn'), callback_data=f"back_to_games_{uid}"))
    text = f"""⚽ <b>{T(uid, 'football_btn')}</b>

<blockquote>{T(uid, 'balance')}: {user.get('balance', 0)} {S()}
{T(uid, 'bet')}: {bet} {S()}</blockquote>"""
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=m)
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith('fb_'))
def fb_bet_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    parts = call.data.split('_')
    strategy = parts[1]
    owner_id = int(parts[2])
    if uid != owner_id:
        bot.answer_callback_query(call.id, T(uid, 'not_your_game'), show_alert=True)
        return
    bet, err = check_bet(uid)
    if err:
        bot.send_message(uid, err)
        return
    chat_id, username = get_result_context(call)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    d = bot.send_dice(chat_id, emoji="⚽")
    time.sleep(3)
    r = d.dice.value
    outcomes = {1: 'miss', 2: 'postgoal', 3: 'center', 4: 'postgoal', 5: 'corner'}
    coefs = {'center': 3.5, 'postgoal': 3.5, 'corner': 3.5, 'anygoal': 1.4, 'miss': 2.0}
    actual = outcomes.get(r, 'miss')
    if strategy == 'anygoal':
        win = actual in ['center', 'postgoal', 'corner']
    else:
        win = actual == strategy
    coef = coefs[strategy]
    result_msg(chat_id, uid, win, bet, coef, username, None)
    save_bet(uid, 'football', bet, strategy, coef, 'win' if win else 'lose', int(bet * coef) if win else 0)


@bot.callback_query_handler(func=lambda c: c.data == "game_darts")
def g_darts(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    bet, err = check_bet(uid)
    if err:
        bot.send_message(uid, err)
        return
    user = get_user(uid)
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("Красный • x2.2", callback_data=f"dt_red_{uid}"),
        InlineKeyboardButton("Белый • x2.2", callback_data=f"dt_white_{uid}")
    )
    m.add(
        InlineKeyboardButton("Центр • x4.0", callback_data=f"dt_center_{uid}"),
        InlineKeyboardButton("Отскок • x4.0", callback_data=f"dt_bounce_{uid}")
    )
    m.add(InlineKeyboardButton(T(uid, 'back_btn'), callback_data=f"back_to_games_{uid}"))
    text = f"""🎯 <b>{T(uid, 'darts_btn')}</b>

<blockquote>{T(uid, 'balance')}: {user.get('balance', 0)} {S()}
{T(uid, 'bet')}: {bet} {S()}</blockquote>"""
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=m)
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith('dt_'))
def dt_bet_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    parts = call.data.split('_')
    strategy = parts[1]
    owner_id = int(parts[2])
    if uid != owner_id:
        bot.answer_callback_query(call.id, T(uid, 'not_your_game'), show_alert=True)
        return
    bet, err = check_bet(uid)
    if err:
        bot.send_message(uid, err)
        return
    chat_id, username = get_result_context(call)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    d = bot.send_dice(chat_id, emoji="🎯")
    time.sleep(3)
    r = d.dice.value
    outcomes = {1: 'miss', 2: 'red', 3: 'white', 4: 'bounce', 5: 'bounce', 6: 'center'}
    coefs = {'red': 2.2, 'white': 2.2, 'center': 4.0, 'bounce': 4.0, 'miss': 1.5}
    actual = outcomes.get(r, 'miss')
    win = actual == strategy
    coef = coefs[strategy]
    result_msg(chat_id, uid, win, bet, coef, username, None)
    save_bet(uid, 'darts', bet, strategy, coef, 'win' if win else 'lose', int(bet * coef) if win else 0)


@bot.callback_query_handler(func=lambda c: c.data == "game_bowling")
def g_bowling(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    bet, err = check_bet(uid)
    if err:
        bot.send_message(uid, err)
        return
    user = get_user(uid)
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("Страйк • x4.0", callback_data=f"bw_strike_{uid}"),
        InlineKeyboardButton("Промах • x4.0", callback_data=f"bw_miss_{uid}")
    )
    m.add(InlineKeyboardButton(T(uid, 'back_btn'), callback_data=f"back_to_games_{uid}"))
    text = f"""🎳 <b>{T(uid, 'bowling_btn')}</b>

<blockquote>{T(uid, 'balance')}: {user.get('balance', 0)} {S()}
{T(uid, 'bet')}: {bet} {S()}</blockquote>"""
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=m)
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith('bw_'))
def bw_bet_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    parts = call.data.split('_')
    strategy = parts[1]
    owner_id = int(parts[2])
    if uid != owner_id:
        bot.answer_callback_query(call.id, T(uid, 'not_your_game'), show_alert=True)
        return
    bet, err = check_bet(uid)
    if err:
        bot.send_message(uid, err)
        return
    chat_id, username = get_result_context(call)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    d = bot.send_dice(chat_id, emoji="🎳")
    time.sleep(3)
    r = d.dice.value
    if strategy == 'strike':
        win = (r == 1)
    elif strategy == 'miss':
        win = (r == 6)
    else:
        win = False
    coef = 4.0
    result_msg(chat_id, uid, win, bet, coef, username, None)
    save_bet(uid, 'bowling', bet, strategy, coef, 'win' if win else 'lose', int(bet * coef) if win else 0)


@bot.callback_query_handler(func=lambda c: c.data == "game_slots")
def g_slots(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    bet, err = check_bet(uid)
    if err:
        bot.send_message(uid, err)
        return
    user = get_user(uid)
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("3 семёрки • x64", callback_data=f"sl_777_{uid}"),
        InlineKeyboardButton("3 лимона • x64", callback_data=f"sl_lemon_{uid}")
    )
    m.add(
        InlineKeyboardButton("3 винограда • x64", callback_data=f"sl_grape_{uid}"),
        InlineKeyboardButton("3 бара • x64", callback_data=f"sl_bar_{uid}")
    )
    m.add(InlineKeyboardButton("Любая • x12", callback_data=f"sl_any_{uid}"))
    m.add(InlineKeyboardButton(T(uid, 'back_btn'), callback_data=f"back_to_games_{uid}"))
    text = f"""🎰 <b>{T(uid, 'slots_btn')}</b>

<blockquote>{T(uid, 'balance')}: {user.get('balance', 0)} {S()}
{T(uid, 'bet')}: {bet} {S()}</blockquote>"""
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=m)
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith('sl_'))
def sl_bet_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    parts = call.data.split('_')
    strategy = parts[1]
    owner_id = int(parts[2])
    if uid != owner_id:
        bot.answer_callback_query(call.id, T(uid, 'not_your_game'), show_alert=True)
        return
    bet, err = check_bet(uid)
    if err:
        bot.send_message(uid, err)
        return
    chat_id, username = get_result_context(call)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    d = bot.send_dice(chat_id, emoji="🎰")
    time.sleep(3)
    v = d.dice.value
    win = False
    coef = 0
    if strategy == '777' and v == 64:
        win = True
        coef = 64.0
    elif strategy == 'lemon' and v == 43:
        win = True
        coef = 64.0
    elif strategy == 'grape' and v == 22:
        win = True
        coef = 64.0
    elif strategy == 'bar' and v == 1:
        win = True
        coef = 64.0
    elif strategy == 'any':
        if v in [1, 22, 43, 64]:
            win = True
            coef = 12.0
    result_msg(chat_id, uid, win, bet, coef, username, None)
    save_bet(uid, 'slots', bet, strategy, coef, 'win' if win else 'lose', int(bet * coef) if win else 0)
mines_games = {}


def make_mines_keyboard(uid, g=None):
    m = InlineKeyboardMarkup()
    row = []
    for i in range(25):
        if g and i in g.get('clicked', set()):
            btn = InlineKeyboardButton("💎", callback_data=f"mines_noop_{uid}")
        else:
            btn = InlineKeyboardButton("⬜", callback_data=f"mines_click_{i}_{uid}")
        row.append(btn)
        if len(row) == 5:
            m.row(*row)
            row = []
    if g:
        m.row(InlineKeyboardButton(f"{T(uid, 'take')} x{g['multiplier']}", callback_data=f"mines_cash_{uid}"))
    return m


@bot.callback_query_handler(func=lambda c: c.data == "game_mines")
def g_mines(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    bet, err = check_bet(uid)
    if err:
        bot.send_message(uid, err)
        return
    user = get_user(uid)
    m = InlineKeyboardMarkup(row_width=3)
    m.add(
        InlineKeyboardButton(T(uid, 'mines_3'), callback_data=f"mines_bombs_3_{uid}"),
        InlineKeyboardButton(T(uid, 'mines_5'), callback_data=f"mines_bombs_5_{uid}"),
        InlineKeyboardButton(T(uid, 'mines_10'), callback_data=f"mines_bombs_10_{uid}")
    )
    m.add(InlineKeyboardButton(T(uid, 'mines_custom'), callback_data=f"mines_custom_{uid}"))
    m.add(InlineKeyboardButton(T(uid, 'back_btn'), callback_data=f"back_to_games_{uid}"))
    text = f"""💣 <b>{T(uid, 'mines_btn')}</b>

<blockquote>{T(uid, 'balance')}: {user.get('balance', 0)} {S()}
{T(uid, 'bet')}: {bet} {S()}</blockquote>

{T(uid, 'mines_choose')}"""
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=m)
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith('mines_custom_'))
def mines_custom_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    owner_id = int(call.data.split('_')[-1])
    if uid != owner_id:
        bot.answer_callback_query(call.id, T(uid, 'not_your_game'), show_alert=True)
        return
    msg = bot.send_message(uid, "✏️ Введите количество мин (1-24):")
    bot.register_next_step_handler(msg, process_mines_custom)


def start_mines_game(uid, bombs, chat_id, msg_id=None):
    user = get_user(uid)
    bet, err = check_bet(uid)
    if err:
        bot.send_message(chat_id, err)
        return
    big_bet = bet >= 500
    cells = list(range(25))
    if big_bet:
        bomb_positions = random.sample(cells[:12], min(bombs, 12))
        while len(bomb_positions) < bombs:
            extra = random.choice([c for c in cells if c not in bomb_positions])
            bomb_positions.append(extra)
    else:
        bomb_positions = random.sample(cells, bombs)
    add_balance(uid, -bet)
    mines_games[uid] = {
        "amount": bet, "bombs": bombs, "opened": 0,
        "bomb_positions": set(bomb_positions), "clicked": set(),
        "multiplier": 1.0,
    }
    m = make_mines_keyboard(uid, mines_games[uid])
    text = f"""💣 <b>{T(uid, 'mines_btn')} — {bombs}</b>

<blockquote>{T(uid, 'balance')}: {user.get('balance', 0) - bet} {S()}
{T(uid, 'bet')}: {bet} {S()}
x1.00</blockquote>"""
    if msg_id:
        try:
            bot.edit_message_text(text, chat_id, msg_id, reply_markup=m)
            return
        except:
            pass
    bot.send_message(chat_id, text, reply_markup=m)


def process_mines_custom(message):
    uid = message.from_user.id
    try:
        bombs = int(message.text.strip())
    except:
        bot.reply_to(message, "❌ 1-24")
        return
    if bombs < 1 or bombs > 24:
        bot.reply_to(message, "❌ 1-24")
        return
    start_mines_game(uid, bombs, message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data.startswith('mines_bombs_'))
def mines_bombs_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    parts = call.data.split('_')
    bombs = int(parts[2])
    owner_id = int(parts[3])
    if uid != owner_id:
        bot.answer_callback_query(call.id, T(uid, 'not_your_game'), show_alert=True)
        return
    start_mines_game(uid, bombs, call.message.chat.id, call.message.message_id)


def mines_multiplier(bombs, opened):
    if bombs == 1:
        base = 1.05
    elif bombs == 3:
        base = 1.13
    elif bombs == 5:
        base = 1.22
    elif bombs == 10:
        base = 1.50
    elif bombs == 15:
        base = 1.90
    elif bombs == 24:
        base = 25.0
    else:
        base = 1.50
    m = 1.0
    for _ in range(opened):
        m *= base
    return round(m, 2)


@bot.callback_query_handler(func=lambda c: c.data.startswith('mines_click_'))
def mines_click_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    parts = call.data.split('_')
    cell = int(parts[2])
    owner_id = int(parts[3])
    if uid != owner_id:
        bot.answer_callback_query(call.id, T(uid, 'not_your_game'), show_alert=True)
        return
    g = mines_games.get(uid)
    if not g:
        return
    if cell in g['clicked']:
        return
    force_bomb = False
    if g['opened'] >= 3 and cell not in g['bomb_positions']:
        if random.random() < 0.45:
            force_bomb = True
    g['clicked'].add(cell)
    if cell in g['bomb_positions'] or force_bomb:
        chat_id = call.message.chat.id
        add_stat(uid, 'total_losses')
        add_stat(uid, 'total_bets', g['amount'])
        save_bet(uid, 'mines', g['amount'], f"bombs_{g['bombs']}", 0, 'lose', 0)
        del mines_games[uid]
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        l_e = E('lose', '😢')
        lose_phrase = random.choice(TEXTS.get(get_lang(uid), TEXTS['ru'])['lose_texts'])
        bot.send_message(chat_id, f"{l_e} {T(uid, 'bomb')} -{g['amount']} {S()}\n\n<i>{lose_phrase}</i>")
        text, m = get_play_menu(uid)
        try:
            bot.send_message(chat_id, text, reply_markup=m)
        except:
            pass
        return
    g['opened'] += 1
    g['multiplier'] = mines_multiplier(g['bombs'], g['opened'])
    m = make_mines_keyboard(uid, g)
    user = get_user(uid)
    text = f"""💣 <b>{T(uid, 'mines_btn')} — {g['bombs']}</b>

<blockquote>{T(uid, 'balance')}: {user.get('balance', 0)} {S()}
{T(uid, 'bet')}: {g['amount']} {S()}
x{g['multiplier']}</blockquote>"""
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=m)
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith('mines_noop_'))
def mines_noop_cb(call):
    bot.answer_callback_query(call.id, "Уже открыто")


@bot.callback_query_handler(func=lambda c: c.data.startswith('mines_cash_'))
def mines_cash_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    owner_id = int(call.data.split('_')[-1])
    if uid != owner_id:
        bot.answer_callback_query(call.id, T(uid, 'not_your_game'), show_alert=True)
        return
    g = mines_games.get(uid)
    if not g or g['opened'] == 0:
        bot.answer_callback_query(call.id, T(uid, 'open_at_least_one'), show_alert=True)
        return
    gross = int(g['amount'] * g['multiplier'])
    commission = int(gross * COMMISSION)
    net = gross - commission
    add_balance(uid, net)
    add_stat(uid, 'total_wins')
    add_stat(uid, 'total_bets', g['amount'])
    save_bet(uid, 'mines', g['amount'], f"bombs_{g['bombs']}", g['multiplier'], 'win', net)
    del mines_games[uid]
    chat_id = call.message.chat.id
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    w_e = E('win', '🎉')
    bot.send_message(chat_id, f"{w_e} {T(uid, 'win_text')} +{net} {S()} (x{g['multiplier']})\n\n{T(uid, 'play_again')}")
    text, m = get_play_menu(uid)
    try:
        bot.send_message(chat_id, text, reply_markup=m)
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data == "game_upgrader")
def g_upgrader(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    bet, err = check_bet(uid)
    if err:
        bot.send_message(uid, err)
        return
    user = get_user(uid)
    m = InlineKeyboardMarkup(row_width=3)
    m.add(
        InlineKeyboardButton("10%", callback_data=f"upg_pct_10_{uid}"),
        InlineKeyboardButton("50%", callback_data=f"upg_pct_50_{uid}"),
        InlineKeyboardButton("80%", callback_data=f"upg_pct_80_{uid}")
    )
    m.add(InlineKeyboardButton(T(uid, 'upg_custom'), callback_data=f"upg_pct_custom_{uid}"))
    m.add(InlineKeyboardButton(T(uid, 'back_btn'), callback_data=f"back_to_games_{uid}"))
    text = f"""⬆️ <b>{T(uid, 'upgrader_btn')}</b>

<blockquote>{T(uid, 'balance')}: {user.get('balance', 0)} {S()}
{T(uid, 'bet')}: {bet} {S()}</blockquote>

{T(uid, 'upg_choose')}"""
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=m)
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith('upg_pct_'))
def upg_pct_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    parts = call.data.split('_')
    pct = parts[2]
    owner_id = int(parts[3])
    if uid != owner_id:
        bot.answer_callback_query(call.id, T(uid, 'not_your_game'), show_alert=True)
        return
    if pct == 'custom':
        msg = bot.send_message(call.message.chat.id, "✏️ Введите процент (1-80):")
        bot.register_next_step_handler(msg, process_upg_custom_pct)
        return
    try:
        pct_int = int(pct)
        run_upgrader(uid, pct_int, call, chat_id=call.message.chat.id)
    except:
        pass


def process_upg_custom_pct(message):
    uid = message.from_user.id
    try:
        pct = int(message.text.strip())
        if pct < 1 or pct > 80:
            bot.reply_to(message, "❌ 1-80")
            return
        run_upgrader(uid, pct, None, message.chat.id)
    except:
        bot.reply_to(message, "❌ Введите число")


def upgrader_real_chance(shown_pct):
    if shown_pct <= 10:
        return shown_pct * 0.5
    elif shown_pct <= 30:
        return shown_pct * 0.6
    elif shown_pct <= 50:
        return shown_pct * 0.66
    elif shown_pct <= 80:
        return shown_pct * 0.75
    return shown_pct


def spinner_animation(chat_id, msg_id, percent, uid):
    frames = [
        "⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪",
        "🟢⚪⚪⚪⚪⚪⚪⚪⚪⚪",
        "🟢🟢⚪⚪⚪⚪⚪⚪⚪⚪",
        "🟢🟢🟢⚪⚪⚪⚪⚪⚪⚪",
        "🟢🟢🟢🟢⚪⚪⚪⚪⚪⚪",
        "🟢🟢🟢🟢🟢⚪⚪⚪⚪⚪",
        "🟢🟢🟢🟢🟢🟢⚪⚪⚪⚪",
        "🟢🟢🟢🟢🟢🟢🟢⚪⚪⚪",
        "🟢🟢🟢🟢🟢🟢🟢🟢⚪⚪",
        "🟢🟢🟢🟢🟢🟢🟢🟢🟢⚪",
        "🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢",
    ]
    random.shuffle(frames)
    frames = frames[:6]
    try:
        for frame in frames:
            text = rep(f"{T(uid, 'spinning')} {percent}%\n\n<code>{frame}</code>\n\n{T(uid, 'luck')}")
            try:
                bot.edit_message_text(text, chat_id, msg_id)
            except:
                pass
            time.sleep(0.4)
    except Exception as e:
        logger.error(f"Animation error: {e}")


def run_upgrader(uid, pct, call=None, chat_id=None):
    bet, err = check_bet(uid)
    if err:
        bot.send_message(uid if not chat_id else chat_id, err)
        return
    user = get_user(uid)
    if not user or user.get('balance', 0) < bet:
        bot.send_message(uid if not chat_id else chat_id, rep(T(uid, 'no_money')))
        return
    real_chance = upgrader_real_chance(pct)
    add_balance(uid, -bet)
    roll = random.uniform(0, 100)
    win = roll <= real_chance
    coef = round(100 / pct, 2)
    target_chat = chat_id or uid
    if call:
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
    try:
        anim_msg = bot.send_message(target_chat, rep(f"{T(uid, 'spinning')} {pct}%\n\n<code>⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪</code>\n\n{T(uid, 'luck')}"))
        spinner_animation(target_chat, anim_msg.message_id, pct, uid)
        time.sleep(0.3)
        try:
            bot.delete_message(target_chat, anim_msg.message_id)
        except:
            pass
    except Exception as e:
        logger.error(f"Animation error: {e}")
    if win:
        gross = int(bet * coef)
        commission = int(gross * COMMISSION)
        net = gross - commission
        add_balance(uid, net)
        add_stat(uid, 'total_wins')
        add_stat(uid, 'total_bets', bet)
        save_bet(uid, 'upgrader', bet, f"pct_{pct}", coef, 'win', net)
        w_e = E('win', '🎉')
        msg = f"{w_e} {T(uid, 'win_text')} +{net} {S()} (x{coef}, {pct}%)\n\n{T(uid, 'play_again')}"
    else:
        add_stat(uid, 'total_losses')
        add_stat(uid, 'total_bets', bet)
        save_bet(uid, 'upgrader', bet, f"pct_{pct}", 0, 'lose', 0)
        l_e = E('lose', '😢')
        msg = f"{l_e} {T(uid, 'lose_msg')} -{bet} {S()} ({pct}%)\n\n<i>Сожалеем, не повезло</i>"
    bot.send_message(target_chat, msg)
    text, m = get_play_menu(uid)
    try:
        bot.send_message(target_chat, text, reply_markup=m)
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data == "bonus")
def bonus_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    user = get_user(uid)
    if not user:
        return
    now = datetime.now()
    last = user.get('last_bonus')
    can_claim = True
    if last:
        try:
            diff = (now - datetime.fromisoformat(last)).total_seconds()
            if diff < 86400:
                can_claim = False
                rem = 86400 - diff
                h = int(rem // 3600)
                m = int((rem % 3600) // 60)
                text = f"{T(uid, 'bonus_title')}\n\n{T(uid, 'bonus_next')} <b>{h}ч {m}м</b>"
        except:
            pass
    if can_claim:
        text = f"{T(uid, 'bonus_title')}\n\n<blockquote>{T(uid, 'bonus_desc')}</blockquote>"
    m = InlineKeyboardMarkup(row_width=1)
    if can_claim:
        m.add(InlineKeyboardButton(T(uid, 'bonus_claim'), callback_data="claim_bonus"))
    m.add(InlineKeyboardButton(T(uid, 'back_btn'), callback_data="back_profile"))
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=m)
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data == "claim_bonus")
def claim_bonus_cb(call):
    uid = call.from_user.id
    user = get_user(uid)
    if not user:
        return
    try:
        chat = bot.get_chat(uid)
        bio = (chat.bio or "").lower()
        if "@xstarplaybot" not in bio:
            bot.answer_callback_query(call.id, "❌ *лучший казик в телеграме @XStarPlayBot*", show_alert=True)
            return
    except:
        bot.answer_callback_query(call.id, "❌ Не удалось проверить профиль", show_alert=True)
        return
    now = datetime.now()
    last = user.get('last_bonus')
    if last:
        try:
            diff = (now - datetime.fromisoformat(last)).total_seconds()
            if diff < 86400:
                rem = 86400 - diff
                h = int(rem // 3600)
                m = int((rem % 3600) // 60)
                bot.answer_callback_query(call.id, f"⏳ {h}ч {m}м", show_alert=True)
                return
        except:
            pass
    bonus = random.randint(1, 10)
    add_balance(uid, bonus)
    db_exec("UPDATE users SET last_bonus=? WHERE user_id=?", (now.isoformat(), uid))
    bot.answer_callback_query(call.id, rep(f"🎁 +{bonus} ⭐"), show_alert=True)
    bot.send_message(uid, rep(f"🎁 +{bonus} ⭐"))


@bot.callback_query_handler(func=lambda c: c.data == "deposit")
def deposit_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    msg = bot.send_message(uid, T(uid, 'deposit'))
    bot.register_next_step_handler(msg, process_stars)


def process_stars(message):
    uid = message.from_user.id
    try:
        stars = int(message.text.strip())
        if stars < MIN_DEPOSIT:
            bot.send_message(uid, rep(f"❌ {MIN_DEPOSIT} ⭐"))
            return
        bot.send_invoice(uid, title=f"Пополнение {BRAND_NAME}",
                         description=f"На {stars} ⭐",
                         invoice_payload=f"dep_{uid}_{stars}",
                         provider_token="", currency="XTR",
                         prices=[types.LabeledPrice(label="Пополнение", amount=stars)])
    except ValueError:
        bot.send_message(uid, "❌ Введите число")


@bot.pre_checkout_query_handler(func=lambda q: True)
def pre_checkout(query):
    bot.answer_pre_checkout_query(query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
def success_pay(message):
    uid = message.from_user.id
    stars = message.successful_payment.total_amount
    add_balance(uid, stars)
    add_stat(uid, 'total_deposits', stars)
    bot.send_message(uid, rep(f"✅ +{stars} ⭐"))


@bot.callback_query_handler(func=lambda c: c.data == "withdraw_start")
def withdraw_start_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    user = get_user(uid)
    bal = user.get('balance', 0) if user else 0
    if bal < MIN_WITHDRAW:
        bot.answer_callback_query(call.id, f"❌ {MIN_WITHDRAW} ⭐", show_alert=True)
        return
    msg = bot.send_message(uid, rep(f"{T(uid, 'withdraw')}\n\n{T(uid, 'balance')}: <b>{bal} ⭐</b>\n\nВведите сумму (мин. {MIN_WITHDRAW}):"))
    bot.register_next_step_handler(msg, wd_amount)


def wd_amount(message):
    uid = message.from_user.id
    user = get_user(uid)
    bal = user.get('balance', 0) if user else 0
    try:
        amount = int(message.text.strip())
        if amount < MIN_WITHDRAW:
            bot.send_message(uid, rep(f"❌ {MIN_WITHDRAW} ⭐"))
            return
        if amount > bal:
            bot.send_message(uid, rep(f"❌ {T(uid, 'balance')}: {bal} ⭐"))
            return
        msg = bot.send_message(uid, "📝 Введите @username:")
        bot.register_next_step_handler(msg, wd_username, amount)
    except ValueError:
        bot.send_message(uid, "❌ Введите число")


def wd_username(message, amount):
    uid = message.from_user.id
    user = get_user(uid)
    uname = message.text.strip().replace('@', '')
    if len(uname) < 3:
        bot.send_message(uid, "❌ Неверный username")
        return
    if get_balance(uid) < amount:
        bot.send_message(uid, "❌ Недостаточно")
        return
    add_balance(uid, -amount)
    add_stat(uid, 'total_withdraws', amount)
    now = datetime.now().isoformat()
    db_exec("""INSERT INTO withdrawals (user_id, amount, username_to, status, created_at)
        VALUES (?, ?, ?, 'pending', ?)""", (uid, amount, uname, now))
    last = db_exec("SELECT MAX(withdraw_id) FROM withdrawals", fetch=True)[0][0]
    bot.send_message(uid, rep(f"✅ #{last} {amount} ⭐ → @{uname}"))
    username = user.get('username', 'anon') if user else 'anon'
    atext = rep(f"📤 <b>Заявка #{last}</b>\n\n👤 @{username} (<code>{uid}</code>)\n💰 <b>{amount} ⭐</b>\n📝 @{uname}")
    m = InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton("✅", callback_data=f"wd_ok_{last}"),
          InlineKeyboardButton("❌", callback_data=f"wd_no_{last}"))
    for aid in ADMIN_IDS:
        try:
            bot.send_message(aid, atext, reply_markup=m)
        except:
            pass


@bot.callback_query_handler(func=lambda c: c.data.startswith('wd_ok_') or c.data.startswith('wd_no_'))
def wd_action(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    if uid not in ADMIN_IDS:
        return
    parts = call.data.split('_')
    action = parts[1]
    wid = int(parts[2])
    res = db_exec("SELECT * FROM withdrawals WHERE withdraw_id=?", (wid,), fetch=True)
    if not res:
        return
    cols = ['withdraw_id', 'user_id', 'amount', 'username_to', 'status', 'created_at', 'completed_at']
    w = dict(zip(cols, res[0]))
    if w['status'] != 'pending':
        bot.answer_callback_query(call.id, "❌", show_alert=True)
        return
    if action == 'ok':
        db_exec("UPDATE withdrawals SET status='completed', completed_at=? WHERE withdraw_id=?",
                (datetime.now().isoformat(), wid))
        bot.answer_callback_query(call.id, "✅")
        try:
            bot.send_message(w['user_id'], rep(f"✅ {w['amount']} ⭐ → @{w['username_to']}"))
        except:
            pass
    else:
        db_exec("UPDATE withdrawals SET status='rejected' WHERE withdraw_id=?", (wid,))
        add_balance(w['user_id'], w['amount'])
        db_exec("UPDATE users SET total_withdraws = total_withdraws - ? WHERE user_id=?", (w['amount'], w['user_id']))
        bot.answer_callback_query(call.id, "❌")
        try:
            bot.send_message(w['user_id'], rep(f"❌ +{w['amount']} ⭐"))
        except:
            pass
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
def get_admin_menu():
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("📊 Статистика", callback_data="adm_stats"),
        InlineKeyboardButton("💰 Выдать звёзды", callback_data="adm_give")
    )
    m.add(
        InlineKeyboardButton("🚫 Забанить", callback_data="adm_ban"),
        InlineKeyboardButton("✅ Разбанить", callback_data="adm_unban")
    )
    m.add(
        InlineKeyboardButton("📤 Заявки на вывод", callback_data="adm_withdrawals"),
        InlineKeyboardButton("📢 Рассылка", callback_data="adm_broadcast")
    )
    m.add(InlineKeyboardButton("🔙 Закрыть", callback_data="adm_close"))
    return m


@bot.message_handler(commands=['admin'])
def admin_cmd(message):
    uid = message.from_user.id
    if uid not in ADMIN_IDS:
        return
    try:
        bot.clear_step_handler_by_chat_id(uid)
    except:
        pass
    bot.send_message(uid, "👑 <b>Админ-панель XStars</b>\n\nВыберите действие:", reply_markup=get_admin_menu())


@bot.callback_query_handler(func=lambda c: c.data == "adm_close")
def adm_close_cb(call):
    bot.answer_callback_query(call.id)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data == "adm_stats")
def adm_stats_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    if uid not in ADMIN_IDS:
        return
    total_users = db_exec("SELECT COUNT(*) FROM users", fetch=True)[0][0]
    banned = db_exec("SELECT COUNT(*) FROM users WHERE banned=1", fetch=True)[0][0]
    total_deposits = db_exec("SELECT SUM(total_deposits) FROM users", fetch=True)[0][0] or 0
    total_withdraws = db_exec("SELECT SUM(total_withdraws) FROM users", fetch=True)[0][0] or 0
    total_balance = db_exec("SELECT SUM(balance) FROM users", fetch=True)[0][0] or 0
    pending = db_exec("SELECT COUNT(*) FROM withdrawals WHERE status='pending'", fetch=True)[0][0]
    total_bets = db_exec("SELECT SUM(amount) FROM bets", fetch=True)[0][0] or 0
    total_won = db_exec("SELECT SUM(win_amount) FROM bets WHERE result='win'", fetch=True)[0][0] or 0
    profit = total_bets - total_won
    text = rep(f"""📊 <b>Статистика XStars</b>

👥 Юзеров: <b>{total_users}</b>
🚫 Забанено: <b>{banned}</b>
💎 Общий баланс игроков: <b>{total_balance} ⭐</b>

📥 Пополнений: <b>{total_deposits} ⭐</b>
📤 Выводов: <b>{total_withdraws} ⭐</b>

🎲 Оборот ставок: <b>{total_bets} ⭐</b>
💰 Выплачено юзерам: <b>{total_won} ⭐</b>
📈 <b>Профит казино: {profit} ⭐</b>

⏳ Заявок на вывод: <b>{pending}</b>""")
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("🔙 Назад", callback_data="adm_back"))
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=m)
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data == "adm_back")
def adm_back_cb(call):
    bot.answer_callback_query(call.id)
    try:
        bot.edit_message_text("👑 <b>Админ-панель XStars</b>\n\nВыберите действие:",
                              call.message.chat.id, call.message.message_id, reply_markup=get_admin_menu())
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data == "adm_give")
def adm_give_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    if uid not in ADMIN_IDS:
        return
    try:
        bot.clear_step_handler_by_chat_id(uid)
    except:
        pass
    msg = bot.send_message(uid, "💰 <b>Выдать звёзды</b>\n\nФормат: <code>user_id сумма</code>\n\nОтмена: /cancel")
    bot.register_next_step_handler(msg, adm_give_step)


def adm_give_step(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        bot.clear_step_handler_by_chat_id(message.from_user.id)
    except:
        pass
    txt = (message.text or '').strip()
    if txt.startswith('/'):
        bot.reply_to(message, "❌ Отменено")
        return
    try:
        parts = txt.split()
        uid = int(parts[0])
        amt = int(parts[1])
        if not get_user(uid):
            bot.reply_to(message, "❌ Юзер не найден")
            return
        add_balance(uid, amt)
        bot.reply_to(message, rep(f"✅ +{amt} ⭐ → {uid}"))
        try:
            bot.send_message(uid, rep(f"🎁 +{amt} ⭐"))
        except:
            pass
    except Exception as e:
        bot.reply_to(message, f"❌ {e}")


@bot.callback_query_handler(func=lambda c: c.data == "adm_ban")
def adm_ban_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    if uid not in ADMIN_IDS:
        return
    try:
        bot.clear_step_handler_by_chat_id(uid)
    except:
        pass
    msg = bot.send_message(uid, "🚫 <b>Забанить</b>\n\nВведите <code>user_id</code>\n\nОтмена: /cancel")
    bot.register_next_step_handler(msg, adm_ban_step)


def adm_ban_step(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        bot.clear_step_handler_by_chat_id(message.from_user.id)
    except:
        pass
    txt = (message.text or '').strip()
    if txt.startswith('/'):
        bot.reply_to(message, "❌ Отменено")
        return
    try:
        target = int(txt)
        if not get_user(target):
            bot.reply_to(message, "❌ Юзер не найден")
            return
        db_exec("UPDATE users SET banned=1 WHERE user_id=?", (target,))
        bot.reply_to(message, f"✅ Забанен <code>{target}</code>")
    except Exception as e:
        bot.reply_to(message, f"❌ {e}")


@bot.callback_query_handler(func=lambda c: c.data == "adm_unban")
def adm_unban_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    if uid not in ADMIN_IDS:
        return
    try:
        bot.clear_step_handler_by_chat_id(uid)
    except:
        pass
    msg = bot.send_message(uid, "✅ <b>Разбанить</b>\n\nВведите <code>user_id</code>\n\nОтмена: /cancel")
    bot.register_next_step_handler(msg, adm_unban_step)


def adm_unban_step(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        bot.clear_step_handler_by_chat_id(message.from_user.id)
    except:
        pass
    txt = (message.text or '').strip()
    if txt.startswith('/'):
        bot.reply_to(message, "❌ Отменено")
        return
    try:
        target = int(txt)
        db_exec("UPDATE users SET banned=0 WHERE user_id=?", (target,))
        bot.reply_to(message, f"✅ Разбанен <code>{target}</code>")
    except Exception as e:
        bot.reply_to(message, f"❌ {e}")


@bot.callback_query_handler(func=lambda c: c.data == "adm_withdrawals")
def adm_withdrawals_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    if uid not in ADMIN_IDS:
        return
    ws = db_exec("SELECT * FROM withdrawals WHERE status='pending' ORDER BY created_at DESC", fetch=True)
    if not ws:
        try:
            bot.edit_message_text("📤 Нет заявок", call.message.chat.id, call.message.message_id,
                                  reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Назад", callback_data="adm_back")))
        except:
            pass
        return
    cols = ['withdraw_id', 'user_id', 'amount', 'username_to', 'status', 'created_at', 'completed_at']
    for r in ws:
        w = dict(zip(cols, r))
        u = get_user(w['user_id'])
        un = u.get('username', 'anon') if u else 'anon'
        atext = rep(f"📤 <b>#{w['withdraw_id']}</b>\n\n👤 @{un} (<code>{w['user_id']}</code>)\n💰 <b>{w['amount']} ⭐</b>\n📝 @{w['username_to']}")
        m = InlineKeyboardMarkup(row_width=2)
        m.add(InlineKeyboardButton("✅", callback_data=f"wd_ok_{w['withdraw_id']}"),
              InlineKeyboardButton("❌", callback_data=f"wd_no_{w['withdraw_id']}"))
        bot.send_message(uid, atext, reply_markup=m)


@bot.callback_query_handler(func=lambda c: c.data == "adm_broadcast")
def adm_broadcast_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    if uid not in ADMIN_IDS:
        return
    try:
        bot.clear_step_handler_by_chat_id(uid)
    except:
        pass
    msg = bot.send_message(uid, "📢 <b>Рассылка</b>\n\nВведите текст сообщения (HTML разрешён)\n\nОтмена: /cancel")
    bot.register_next_step_handler(msg, adm_broadcast_step)


def adm_broadcast_step(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    txt = (message.text or '').strip()
    if txt.startswith('/'):
        bot.reply_to(message, "❌ Отменено")
        return
    users = db_exec("SELECT user_id FROM users WHERE banned=0", fetch=True)
    count = 0
    fail = 0
    for (uid,) in users or []:
        try:
            bot.send_message(uid, txt)
            count += 1
            time.sleep(0.05)
        except:
            fail += 1
    bot.reply_to(message, f"✅ Отправлено: {count}\n❌ Ошибок: {fail}")


@bot.message_handler(commands=['stats'])
def stats_cmd(message):
    uid = message.from_user.id
    if uid not in ADMIN_IDS:
        return
    total_users = db_exec("SELECT COUNT(*) FROM users", fetch=True)[0][0]
    total_deposits = db_exec("SELECT SUM(total_deposits) FROM users", fetch=True)[0][0] or 0
    total_bets = db_exec("SELECT SUM(amount) FROM bets", fetch=True)[0][0] or 0
    total_won = db_exec("SELECT SUM(win_amount) FROM bets WHERE result='win'", fetch=True)[0][0] or 0
    profit = total_bets - total_won
    bot.send_message(uid, rep(f"📊 Юзеров: {total_users}\n💰 Депов: {total_deposits} ⭐\n🎲 Оборот: {total_bets} ⭐\n📈 Профит: {profit} ⭐"))


@bot.message_handler(commands=['ban'])
def ban_cmd(message):
    uid = message.from_user.id
    if uid not in ADMIN_IDS:
        return
    try:
        target = int(message.text.split()[1])
        db_exec("UPDATE users SET banned=1 WHERE user_id=?", (target,))
        bot.reply_to(message, f"✅ {target}")
    except:
        bot.reply_to(message, "❌ /ban user_id")


@bot.message_handler(commands=['unban'])
def unban_cmd(message):
    uid = message.from_user.id
    if uid not in ADMIN_IDS:
        return
    try:
        target = int(message.text.split()[1])
        db_exec("UPDATE users SET banned=0 WHERE user_id=?", (target,))
        bot.reply_to(message, f"✅ {target}")
    except:
        bot.reply_to(message, "❌ /unban user_id")


@bot.message_handler(commands=['cancel'])
def cancel_cmd(message):
    uid = message.from_user.id
    try:
        bot.clear_step_handler_by_chat_id(uid)
    except:
        pass
    bot.reply_to(message, "❌ Отменено")
def is_bet_command(text):
    if not text:
        return False
    t = text.lower().strip()
    if t in ['ставка', 'бет', 'bet']:
        return 'show'
    if t.startswith('ставка ') or t.startswith('бет ') or t.startswith('bet '):
        try:
            parts = t.split()
            val = int(parts[1])
            return ('set', val)
        except:
            return False
    return False


def get_bet_keyboard(prefix, uid):
    m = InlineKeyboardMarkup(row_width=3)
    m.add(
        InlineKeyboardButton("1", callback_data=f"{prefix}_1"),
        InlineKeyboardButton("5", callback_data=f"{prefix}_5"),
        InlineKeyboardButton("10", callback_data=f"{prefix}_10")
    )
    m.add(
        InlineKeyboardButton("50", callback_data=f"{prefix}_50"),
        InlineKeyboardButton("100", callback_data=f"{prefix}_100"),
        InlineKeyboardButton("500", callback_data=f"{prefix}_500")
    )
    m.add(InlineKeyboardButton("✏️ Своё", callback_data=f"{prefix}_custom"))
    return m


@bot.message_handler(content_types=['text'],
                     func=lambda m: m.chat.type in ['group', 'supergroup'] and is_bet_command(m.text or ''))
def bet_command_group(message):
    uid = message.from_user.id
    user = get_user(uid)
    if not user:
        create_user(uid, message.from_user.username, message.from_user.first_name)
        user = get_user(uid)
    uname = message.from_user.username or message.from_user.first_name
    res = is_bet_command(message.text)
    if res == 'show':
        cur = user.get('bet_amount', 0)
        m = get_bet_keyboard("setbetg", uid)
        bot.reply_to(message, rep(f"🎯 @{uname} {T(uid, 'bet_show')} <b>{cur} ⭐</b>"), reply_markup=m)
    elif isinstance(res, tuple) and res[0] == 'set':
        val = res[1]
        if val < MIN_BET:
            bot.reply_to(message, rep(T(uid, 'bet_min')))
            return
        set_bet_amount(uid, val)
        bot.reply_to(message, rep(f"✅ @{uname} {T(uid, 'bet_set')} <b>{val} ⭐</b>"))


@bot.callback_query_handler(func=lambda c: c.data.startswith('setbetg_'))
def setbetg_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    val = call.data.replace('setbetg_', '')
    if val == 'custom':
        msg = bot.send_message(call.message.chat.id, "✏️ Введите сумму ставки:")
        bot.register_next_step_handler(msg, process_custom_bet)
        return
    try:
        val_int = int(val)
        set_bet_amount(uid, val_int)
        bot.send_message(call.message.chat.id, rep(f"✅ {T(uid, 'bet_set')} <b>{val_int} ⭐</b>"))
    except:
        pass


def process_custom_bet(message):
    uid = message.from_user.id
    try:
        val = int(message.text.strip())
        if val < MIN_BET:
            bot.reply_to(message, rep(T(uid, 'bet_min')))
            return
        set_bet_amount(uid, val)
        bot.reply_to(message, rep(f"✅ {T(uid, 'bet_set')} <b>{val} ⭐</b>"))
    except:
        bot.reply_to(message, "❌ Введите число")


@bot.message_handler(content_types=['text'],
                     func=lambda m: m.chat.type in ['group', 'supergroup'] and (m.text or '').lower().strip() in ['играть', 'play', 'игра'])
def play_group_handler(message):
    uid = message.from_user.id
    user = get_user(uid)
    if not user:
        create_user(uid, message.from_user.username, message.from_user.first_name)
        user = get_user(uid)
    uname = message.from_user.username or message.from_user.first_name
    bet, err = check_bet(uid)
    if err:
        bot.reply_to(message, f"@{uname}, " + err)
        return
    text, m = get_play_menu(uid)
    bot.reply_to(message, text, reply_markup=m)


@bot.message_handler(content_types=['text'],
                     func=lambda m: m.chat.type == 'private' and (m.text or '').lower().strip() in ['ставка', 'бет', 'bet'])
def bet_command_private(message):
    uid = message.from_user.id
    user = get_user(uid)
    if not user:
        create_user(uid, message.from_user.username, message.from_user.first_name)
        user = get_user(uid)
    cur = user.get('bet_amount', 0)
    m = get_bet_keyboard("setbetp", uid)
    bot.send_message(uid, rep(f"🎯 {T(uid, 'bet_show')} <b>{cur} ⭐</b>"), reply_markup=m)


@bot.callback_query_handler(func=lambda c: c.data.startswith('setbetp_'))
def setbetp_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    val = call.data.replace('setbetp_', '')
    if val == 'custom':
        msg = bot.send_message(uid, "✏️ Введите сумму ставки:")
        bot.register_next_step_handler(msg, process_custom_bet)
        return
    try:
        val_int = int(val)
        set_bet_amount(uid, val_int)
        bot.send_message(uid, rep(f"✅ {T(uid, 'bet_set')} <b>{val_int} ⭐</b>"))
    except:
        pass


@bot.message_handler(content_types=['text'],
                     func=lambda m: m.chat.type == 'private' and m.text and m.text.strip() in
                     ['👤 Профиль', '👤 Profile', '👤 Профіль', '👤 پروفایل'])
def profile_btn(message):
    uid = message.from_user.id
    user = get_user(uid)
    if not user:
        create_user(uid, message.from_user.username, message.from_user.first_name)
        user = get_user(uid)
    bal = user.get('balance', 0)
    wins = user.get('total_wins', 0)
    losses = user.get('total_losses', 0)
    turnover = user.get('total_bets', 0)
    dep = user.get('total_deposits', 0)
    wd = user.get('total_withdraws', 0)
    refs = get_ref_count(uid)
    text = rep(f"""{T(uid, 'profile')}

🆔 <code>{uid}</code>
💰 {T(uid, 'balance')}: <b>{bal} ⭐</b>

{T(uid, 'stats')}
📊 {T(uid, 'turnover')}: <b>{turnover} ⭐</b>
✅ {T(uid, 'wins')}: <b>{wins}</b>
❌ {T(uid, 'losses')}: <b>{losses}</b>
📥 {T(uid, 'deposits')}: <b>{dep} ⭐</b>
📤 {T(uid, 'withdraws')}: <b>{wd} ⭐</b>
👥 Рефералов: <b>{refs}</b>""")
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton(T(uid, 'deposit_btn_short'), callback_data="deposit"),
        InlineKeyboardButton(T(uid, 'withdraw_btn'), callback_data="withdraw_start")
    )
    m.add(InlineKeyboardButton(T(uid, 'bonus_btn'), callback_data="bonus"))
    m.add(InlineKeyboardButton(T(uid, 'ref_system_btn'), callback_data="ref_menu"))
    bot.send_message(uid, text, reply_markup=m)


@bot.callback_query_handler(func=lambda c: c.data == "back_profile")
def back_profile_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    user = get_user(uid)
    if not user:
        return
    bal = user.get('balance', 0)
    wins = user.get('total_wins', 0)
    losses = user.get('total_losses', 0)
    turnover = user.get('total_bets', 0)
    dep = user.get('total_deposits', 0)
    wd = user.get('total_withdraws', 0)
    refs = get_ref_count(uid)
    text = rep(f"""{T(uid, 'profile')}

🆔 <code>{uid}</code>
💰 {T(uid, 'balance')}: <b>{bal} ⭐</b>

{T(uid, 'stats')}
📊 {T(uid, 'turnover')}: <b>{turnover} ⭐</b>
✅ {T(uid, 'wins')}: <b>{wins}</b>
❌ {T(uid, 'losses')}: <b>{losses}</b>
📥 {T(uid, 'deposits')}: <b>{dep} ⭐</b>
📤 {T(uid, 'withdraws')}: <b>{wd} ⭐</b>
👥 Рефералов: <b>{refs}</b>""")
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton(T(uid, 'deposit_btn_short'), callback_data="deposit"),
        InlineKeyboardButton(T(uid, 'withdraw_btn'), callback_data="withdraw_start")
    )
    m.add(InlineKeyboardButton(T(uid, 'bonus_btn'), callback_data="bonus"))
    m.add(InlineKeyboardButton(T(uid, 'ref_system_btn'), callback_data="ref_menu"))
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=m)
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data == "ref_menu")
def ref_menu_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    link = f"https://t.me/{BOT_USERNAME}?start=ref_{uid}"
    refs = get_ref_count(uid)
    text = rep(f"""{T(uid, 'ref_title')}

<blockquote>{T(uid, 'ref_desc')}</blockquote>

{T(uid, 'your_link')}
<code>{link}</code>

{T(uid, 'invited')}: <b>{refs}</b>""")
    m = InlineKeyboardMarkup(row_width=1)
    m.add(InlineKeyboardButton(T(uid, 'share'),
                               url=f"https://t.me/share/url?url={link}&text=Играй в XStars!"))
    m.add(InlineKeyboardButton(T(uid, 'back_btn'), callback_data="back_profile"))
    try:
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=m)
    except:
        pass


@bot.message_handler(content_types=['text'],
                     func=lambda m: m.chat.type == 'private' and m.text and m.text.strip() in
                     ['🎮 Играть', '🎮 Play', '🎮 Грати', '🎮 بازی'])
def play_btn(message):
    uid = message.from_user.id
    user = get_user(uid)
    if not user:
        create_user(uid, message.from_user.username, message.from_user.first_name)
        user = get_user(uid)
    text, m = get_play_menu(uid)
    bot.send_message(uid, text, reply_markup=m)


@bot.message_handler(content_types=['text'],
                     func=lambda m: m.chat.type == 'private' and m.text and m.text.strip() in
                     ['🌐 Язык', '🌐 Language', '🌐 Мова', '🌐 زبان'])
def lang_btn(message):
    uid = message.from_user.id
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
    )
    m.add(
        InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_uk"),
        InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa")
    )
    bot.send_message(uid, T(uid, 'choose_lang'), reply_markup=m)


@bot.callback_query_handler(func=lambda c: c.data.startswith('lang_'))
def lang_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    lang = call.data.replace('lang_', '')
    set_language(uid, lang)
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
    bot.send_message(uid, T(uid, 'lang_changed'), reply_markup=get_reply_keyboard(lang))


# ==================== ПЕРЕДАЧА ЗВЁЗД (НК реплаем) ====================
nk_pending = {}


def parse_nk_amount(text):
    if not text:
        return None
    t = text.lower().strip()
    for prefix in ('нк', 'nk'):
        if t == prefix:
            return 'ask'
        if t.startswith(prefix + ' '):
            try:
                return int(t[len(prefix):].strip().split()[0])
            except:
                return None
    return None


@bot.message_handler(
    content_types=['text'],
    func=lambda m: m.reply_to_message is not None and parse_nk_amount(m.text) is not None
)
def nk_reply_handler(message):
    uid = message.from_user.id
    user = get_user(uid)
    if not user:
        create_user(uid, message.from_user.username, message.from_user.first_name)
        user = get_user(uid)

    target = message.reply_to_message.from_user
    to_uid = target.id
    to_uname = target.username or target.first_name or str(to_uid)

    if to_uid == uid:
        bot.reply_to(message, "❌ Нельзя передать самому себе")
        return

    if not get_user(to_uid):
        bot.reply_to(message, f"❌ @{to_uname} ещё не запускал бота. Пусть нажмёт /start.")
        return

    parsed = parse_nk_amount(message.text)

    if parsed == 'ask':
        msg = bot.reply_to(message, rep(f"💸 Сколько ⭐ передать @{to_uname}? Напиши число."))
        bot.register_next_step_handler(msg, nk_ask_amount_step, to_uid, to_uname)
        return

    amount = parsed
    if not isinstance(amount, int) or amount < 1:
        bot.reply_to(message, rep("❌ Минимум 1 ⭐"))
        return

    if user.get('balance', 0) < amount:
        bot.reply_to(message, rep(T(uid, 'nk_no_money').format(balance=user.get('balance', 0))))
        return

    nk_pending[uid] = {'to_uid': to_uid, 'to_uname': to_uname, 'amount': amount}
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton(T(uid, 'nk_yes'), callback_data=f"nk_yes_{uid}"),
        InlineKeyboardButton(T(uid, 'nk_no'), callback_data=f"nk_no_{uid}")
    )
    bot.reply_to(
        message,
        rep(T(uid, 'nk_confirm').format(name=to_uname, amount=amount)),
        reply_markup=m
    )


def nk_ask_amount_step(message, to_uid, to_uname):
    uid = message.from_user.id
    try:
        amount = int(message.text.strip())
    except:
        bot.reply_to(message, "❌ Введите число")
        return
    if amount < 1:
        bot.reply_to(message, rep("❌ Минимум 1 ⭐"))
        return
    user = get_user(uid)
    if not user or user.get('balance', 0) < amount:
        bal = user.get('balance', 0) if user else 0
        bot.reply_to(message, rep(T(uid, 'nk_no_money').format(balance=bal)))
        return
    nk_pending[uid] = {'to_uid': to_uid, 'to_uname': to_uname, 'amount': amount}
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton(T(uid, 'nk_yes'), callback_data=f"nk_yes_{uid}"),
        InlineKeyboardButton(T(uid, 'nk_no'), callback_data=f"nk_no_{uid}")
    )
    bot.reply_to(
        message,
        rep(T(uid, 'nk_confirm').format(name=to_uname, amount=amount)),
        reply_markup=m
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith('nk_yes_'))
def nk_yes_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    owner_id = int(call.data.split('_')[-1])
    if uid != owner_id:
        bot.answer_callback_query(call.id, T(uid, 'not_your_game'), show_alert=True)
        return
    p = nk_pending.get(uid)
    if not p:
        bot.answer_callback_query(call.id, "❌ Заявка устарела", show_alert=True)
        return
    amount = p['amount']
    to_uid = p['to_uid']
    to_uname = p['to_uname']
    if get_balance(uid) < amount:
        bot.answer_callback_query(call.id, "❌ Недостаточно средств", show_alert=True)
        nk_pending.pop(uid, None)
        return
    add_balance(uid, -amount)
    add_balance(to_uid, amount)
    nk_pending.pop(uid, None)
    sender = get_user(uid)
    sender_uname = (sender.get('username') or sender.get('first_name') or 'user') if sender else 'user'
    try:
        bot.edit_message_text(
            rep(T(uid, 'nk_sent').format(amount=amount, name=to_uname)),
            call.message.chat.id, call.message.message_id
        )
    except:
        bot.send_message(call.message.chat.id, rep(T(uid, 'nk_sent').format(amount=amount, name=to_uname)))
    try:
        bot.send_message(to_uid, rep(T(to_uid, 'nk_received').format(amount=amount, name=sender_uname)))
    except:
        pass


@bot.callback_query_handler(func=lambda c: c.data.startswith('nk_no_'))
def nk_no_cb(call):
    bot.answer_callback_query(call.id)
    uid = call.from_user.id
    owner_id = int(call.data.split('_')[-1])
    if uid != owner_id:
        bot.answer_callback_query(call.id, T(uid, 'not_your_game'), show_alert=True)
        return
    nk_pending.pop(uid, None)
    try:
        bot.edit_message_text(T(uid, 'nk_cancelled'), call.message.chat.id, call.message.message_id)
    except:
        bot.send_message(call.message.chat.id, T(uid, 'nk_cancelled'))


# ==================== ЗАПУСК ====================
if __name__ == '__main__':
    print("=" * 50)
    print(f"🎰 {BRAND_NAME} Bot запущен!")
    print(f"📌 @{BOT_USERNAME}")
    print(f"👑 Админы: {ADMIN_IDS}")
    print("=" * 50)
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=60)
        except Exception as e:
            logger.error(f"Polling error: {e}")
            time.sleep(5)