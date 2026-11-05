import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ===== НАСТРОЙКИ (ЗАМЕНИТЕ НА СВОИ) =====
BOT_TOKEN = "import os
BOT_TOKEN = os.environ.get("BOT_TOKEN")"
ADMIN_ID = 123456789          # ← ваш Telegram ID
SELLER_CONTACT = "@your_username"  # ← ваш юзернейм

# ===== БАЗА АККАУНТОВ =====
ACCOUNTS = {
    "cs2": {
        "name": "CS2",
        "items": [
            {"id": 1, "title": "Global Elite | 500 ч", "price": 3500,
             "desc": "Ранг: Global Elite\nЧасы: 500+\nСкины: AK-47 Redline, AWP Asiimov\nFaceit: 8 уровень"},
            {"id": 2, "title": "Supreme | 1200 ч", "price": 5000,
             "desc": "Ранг: Supreme\nЧасы: 1200+\nСкины: Нож Бабочка, AK Neon Rider\nFaceit: 10 уровень"},
            {"id": 3, "title": "Silver | 100 ч", "price": 800,
             "desc": "Ранг: Silver 4\nЧасы: 100+\nPrime: есть\nСкины: базовые"},
        ]
    },
    "genshin": {
        "name": "Genshin Impact",
        "items": [
            {"id": 4, "title": "AR 58 | 20 пятёрок", "price": 7000,
             "desc": "AR: 58\nПерсонажи: Нахида C2, Ху Тао C1, Райдэн C2\nОружие 5★: 8 шт\nПримогемы: 12000"},
            {"id": 5, "title": "AR 55 | 10 пятёрок", "price": 3000,
             "desc": "AR: 55\nПерсонажи: Чжун Ли, Аяка, Казуха\nОружие 5★: 3 шт\nПримогемы: 5000"},
        ]
    },
    "fortnite": {
        "name": "Fortnite",
        "items": [
            {"id": 6, "title": "OG | Renegade Raider", "price": 15000,
             "desc": "Скины: Renegade Raider, Ghoul Trooper\nV-Bucks: 2500\nСезон: 1\nПобед: 350+"},
            {"id": 7, "title": "50 скинов", "price": 2500,
             "desc": "Скины: 50+\nV-Bucks: 800\nBattle Pass: текущий\nПобед: 100+"},
        ]
    },
    "valorant": {
        "name": "Valorant",
        "items": [
            {"id": 8, "title": "Immortal 3 | 15 скинов", "price": 6000,
             "desc": "Ранг: Immortal 3\nСкины: Vandal Prime, Phantom Reaver\nАгенты: все\nVP: 1500"},
        ]
    }
}

# ===== ОТЗЫВЫ =====
REVIEWS = [
    "⭐⭐⭐⭐⭐ Купил аккаунт CS2 Global, всё пришло за 5 минут. Рекомендую! — @gamer228",
    "⭐⭐⭐⭐⭐ Genshin AR 58, все персонажи на месте. Продавец адекватный! — @anime_fan",
    "⭐⭐⭐⭐⭐ Fortnite OG аккаунт, Renegade Raider реально есть. Спасибо! — @fortnite_king",
    "⭐⭐⭐⭐ Быстро и честно, но хотелось бы больше способов оплаты. — @player_one",
]

# ===== FAQ =====
FAQ_TEXT = (
    "❓ <b>Частые вопросы</b>\n\n"
    "<b>🔹 Как происходит покупка?</b>\n"
    "Вы выбираете аккаунт, нажимаете «Купить», связываетесь с продавцом. "
    "После оплаты получаете логин и пароль.\n\n"
    "<b>🔹 Какие способы оплаты?</b>\n"
    "Перевод на карту, СБП, криптовалюта, ЮMoney.\n\n"
    "<b>🔹 Есть ли гарантия?</b>\n"
    "Да, гарантия 24 часа после покупки. Если аккаунт не работает — "
    "вернём деньги или заменим.\n\n"
    "<b>🔹 Как быстро я получу аккаунт?</b>\n"
    "Обычно в течение 5–30 минут после оплаты.\n\n"
    "<b>🔹 Можно ли сменить данные после покупки?</b>\n"
    "Да, после получения вы полностью меняете почту, пароль и привязки."
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ===== ГЛАВНОЕ МЕНЮ =====
def main_menu_keyboard():
    kb = InlineKeyboardBuilder()
    for key, game in ACCOUNTS.items():
        kb.button(text=f"🎮 {game['name']}", callback_data=f"game_{key}")
    kb.button(text="❓ Частые вопросы", callback_data="faq")
    kb.button(text="⭐ Отзывы", callback_data="reviews")
    kb.button(text="💬 Связь с админом", callback_data="contact")
    kb.adjust(2)
    return kb.as_markup()


# ===== /start =====
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать в магазин игровых аккаунтов!\n\n"
        "🎮 Более 500 аккаунтов в наличии\n"
        "⚡ Моментальная доставка\n"
        "🛡 Гарантия 24 часа\n\n"
        "Выберите игру или воспользуйтесь меню ниже:",
        reply_markup=main_menu_keyboard()
    )


# ===== ВЫБОР ИГРЫ → СПИСОК АККАУНТОВ =====
@dp.callback_query(F.data.startswith("game_"))
async def show_accounts(callback: types.CallbackQuery):
    game_key = callback.data.replace("game_", "")
    game = ACCOUNTS.get(game_key)
    if not game:
        return await callback.answer("Не найдено")

    kb = InlineKeyboardBuilder()
    for item in game["items"]:
        kb.button(
            text=f"{item['title']} — {item['price']}₽",
            callback_data=f"acc_{item['id']}"
        )
    kb.button(text="⬅️ Назад", callback_data="back_main")
    kb.adjust(1)

    await callback.message.edit_text(
        f"🎮 <b>{game['name']}</b>\n\nДоступные аккаунты:",
        reply_markup=kb.as_markup(), parse_mode="HTML"
    )
    await callback.answer()


# ===== КАРТОЧКА АККАУНТА =====
@dp.callback_query(F.data.startswith("acc_"))
async def show_account(callback: types.CallbackQuery):
    acc_id = int(callback.data.replace("acc_", ""))
    account = None
    for game in ACCOUNTS.values():
        for item in game["items"]:
            if item["id"] == acc_id:
                account = item
                break
    if not account:
        return await callback.answer("Не найдено")

    kb = InlineKeyboardBuilder()
    kb.button(text="💰 Купить", callback_data=f"buy_{acc_id}")
    kb.button(text="⬅️ Назад", callback_data="back_main")
    kb.adjust(1)

    await callback.message.edit_text(
        f"📋 <b>{account['title']}</b>\n\n"
        f"{account['desc']}\n\n"
        f"💵 Цена: <b>{account['price']} ₽</b>",
        reply_markup=kb.as_markup(), parse_mode="HTML"
    )
    await callback.answer()


# ===== ПОКУПКА + УВЕДОМЛЕНИЕ АДМИНУ =====
@dp.callback_query(F.data.startswith("buy_"))
async def buy_account(callback: types.CallbackQuery):
    acc_id = int(callback.data.replace("buy_", ""))
    account = None
    for game in ACCOUNTS.values():
        for item in game["items"]:
            if item["id"] == acc_id:
                account = item
                break

    # 🔔 Отправляем уведомление админу
    user = callback.from_user
    try:
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🔔 <b>НОВЫЙ ЗАКАЗ!</b>\n\n"
                 f"👤 Клиент: @{user.username or 'нет юзернейма'}\n"
                 f"🆔 ID: {user.id}\n"
                 f"📛 Имя: {user.full_name}\n\n"
                 f"🎮 Товар: {account['title']}\n"
                 f"💵 Цена: {account['price']} ₽\n\n"
                 f"⏰ Напиши клиенту как можно скорее!",
            parse_mode="HTML"
        )
    except Exception:
        pass  # Если админ не найден, просто пропускаем

    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ В каталог", callback_data="back_main")
    kb.adjust(1)

    await callback.message.edit_text(
        f"✅ Вы выбрали: <b>{account['title']}</b>\n"
        f"💵 Цена: <b>{account['price']} ₽</b>\n\n"
        f"📩 Для покупки напишите продавцу:\n"
        f"👉 {SELLER_CONTACT}\n\n"
        f"Укажите название аккаунта — поможем с оплатой!\n"
        f"⚡ Обычно отвечаем в течение 5 минут.",
        reply_markup=kb.as_markup(), parse_mode="HTML"
    )
    await callback.answer("✅ Заявка отправлена!")


# ===== FAQ =====
@dp.callback_query(F.data == "faq")
async def show_faq(callback: types.CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Назад", callback_data="back_main")
    kb.adjust(1)

    await callback.message.edit_text(
        FAQ_TEXT,
        reply_markup=kb.as_markup(), parse_mode="HTML"
    )
    await callback.answer()


# ===== ОТЗЫВЫ =====
@dp.callback_query(F.data == "reviews")
async def show_reviews(callback: types.CallbackQuery):
    reviews_text = "⭐ <b>Отзывы наших клиентов</b>\n\n"
    for r in REVIEWS:
        reviews_text += f"{r}\n\n"
    reviews_text += f"📊 Всего продано: <b>500+</b> аккаунтов"

    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Назад", callback_data="back_main")
    kb.adjust(1)

    await callback.message.edit_text(
        reviews_text,
        reply_markup=kb.as_markup(), parse_mode="HTML"
    )
    await callback.answer()


# ===== СВЯЗЬ С АДМИНОМ =====
@dp.callback_query(F.data == "contact")
async def show_contact(callback: types.CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Назад", callback_data="back_main")
    kb.adjust(1)

    await callback.message.edit_text(
        f"💬 <b>Связь с администратором</b>\n\n"
        f"👉 {SELLER_CONTACT}\n\n"
        f"🕐 Время ответа: обычно 5–15 минут\n"
        f"⏰ Работаем: с 10:00 до 23:00 (МСК)\n\n"
        f"По всем вопросам — пишите, не стесняйтесь! 😊",
        reply_markup=kb.as_markup(), parse_mode="HTML"
    )
    await callback.answer()


# ===== НАЗАД В МЕНЮ =====
@dp.callback_query(F.data == "back_main")
async def back_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "👋 Добро пожаловать в магазин игровых аккаунтов!\n\n"
        "🎮 Более 500 аккаунтов в наличии\n"
        "⚡ Моментальная доставка\n"
        "🛡 Гарантия 24 часа\n\n"
        "Выберите игру или воспользуйтесь меню ниже:",
        reply_markup=main_menu_keyboard()
    )
    await callback.answer()


# ===== ЗАПУСК =====
async def main():
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
