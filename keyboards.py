from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu(user_lang='uz'):
    if user_lang == 'uz':
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📚 So'zlarni o'rganish")],
                [KeyboardButton(text="🎮 O'yin (10 savol)"), KeyboardButton(text="🏆 Mening natijam")],
                [KeyboardButton(text="📸 Suratli lug'at")],
                [KeyboardButton(text="🔄 Tilni o'zgartirish")]
            ],
            resize_keyboard=True
        )
    else:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📚 Sózlerdi úyreniw")],
                [KeyboardButton(text="🎮 Oyın (10 soraw)"), KeyboardButton(text="🏆 Meniń nátiyjem")],
                [KeyboardButton(text="📸 Súwretli sózlik")],
                [KeyboardButton(text="🔄 Tildi ózgertiw")]
            ],
            resize_keyboard=True
        )
    return keyboard

def get_categories_menu(user_lang='uz'):
    if user_lang == 'uz':
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👋 Salomlashuv"), KeyboardButton(text="🏠 Kundalik hayot")],
                [KeyboardButton(text="🕒 Vaqt va kunlar"), KeyboardButton(text="👨‍👩‍👧‍👦 Oila a'zolari")],
                [KeyboardButton(text="🔢 Sonlar"), KeyboardButton(text="🍎 Oziq-ovqat")],
                [KeyboardButton(text="🎨 Ranglar"), KeyboardButton(text="🌳 Tabiat")],
                [KeyboardButton(text="📚 O'qish va maktab"), KeyboardButton(text="👕 Kiyimlar")],
                [KeyboardButton(text="🐾 Hayvonlar"), KeyboardButton(text="🍊 Mevalar")],
                [KeyboardButton(text="🎮 O'yinchoqlar"), KeyboardButton(text="🦴 Tana a'zolari")],
                [KeyboardButton(text="⬅️ Ortqa")]
            ],
            resize_keyboard=True
        )
    else:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="👋 Sálemlesiw"), KeyboardButton(text="🏠 Kúndelikli turmıs")],
                [KeyboardButton(text="🕒 Waqıt hám kúnler"), KeyboardButton(text="👨‍👩‍👧‍👦 Shańaraq aǵzaları")],
                [KeyboardButton(text="🔢 Sanlar"), KeyboardButton(text="🍎 Azıq-awqat")],
                [KeyboardButton(text="🎨 Reńler"), KeyboardButton(text="🌳 Tábiyaat")],
                [KeyboardButton(text="📚 Oqıw hám mektep"), KeyboardButton(text="👕 Kiyimler")],
                [KeyboardButton(text="🐾 Janiwarlar"), KeyboardButton(text="🍊 Miyweler")],
                [KeyboardButton(text="🎮 Oyınshıqlar"), KeyboardButton(text="🦴 Dene aǵzaları")],
                [KeyboardButton(text="⬅️ Arqaǵa")]
            ],
            resize_keyboard=True
        )
    return keyboard

def get_language_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbek tili", callback_data="lang:uz"),
                InlineKeyboardButton(text="🏳️ Qaraqalpaq tili", callback_data="lang:qq")
            ]
        ]
    )
    return keyboard

def get_pagination_keyboard(category_code, current_index, total_words, user_lang='uz'):
    buttons = []

    prev_text = "⬅️"
    next_text = "➡️"

    if current_index > 0:
        buttons.append(InlineKeyboardButton(text=prev_text, callback_data=f"word:{category_code}:{current_index - 1}"))

    if current_index < total_words - 1:
        buttons.append(InlineKeyboardButton(text=next_text, callback_data=f"word:{category_code}:{current_index + 1}"))

    rows = []
    if buttons:
        rows.append(buttons)

    # 🎲 Tasodifiy so'z tugmasi
    random_text = "🎲 Tasodifiy" if user_lang == 'uz' else "🎲 Tasadıypı"
    rows.append([InlineKeyboardButton(text=random_text, callback_data=f"random_word:{category_code}")])

    return InlineKeyboardMarkup(inline_keyboard=rows)

def get_quiz_keyboard(options, correct_id, q_num, score, user_lang='uz'):
    import random

    inline_keyboard = []
    random.shuffle(options)

    LETTERS = ["🅐", "🅑", "🅒", "🅓"]

    for i, option in enumerate(options):
        opt_id = option['id']
        opt_text = option['text']
        is_correct = 1 if opt_id == correct_id else 0
        letter = LETTERS[i] if i < len(LETTERS) else "▪️"

        btn = InlineKeyboardButton(
            text=f"{letter}  {opt_text}",
            callback_data=f"quiz:{is_correct}:{q_num}:{score}"
        )
        inline_keyboard.append([btn])

    stop_text = "🛑 To'xtatish" if user_lang == 'uz' else "🛑 Toqtatıw"
    inline_keyboard.append([InlineKeyboardButton(text=stop_text, callback_data=f"quiz_stop:{score}:{q_num}")])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

def get_picture_dictionary_keyboard(words, user_lang='uz'):
    inline_keyboard = []
    current_row = []

    for word in words:
        word_id = word[0]
        word_text = word[3] if user_lang == 'uz' else word[2]

        btn = InlineKeyboardButton(
            text=word_text,
            callback_data=f"pic:{word_id}"
        )
        current_row.append(btn)

        if len(current_row) == 2:
            inline_keyboard.append(current_row)
            current_row = []

    if current_row:
        inline_keyboard.append(current_row)

    home_text = "🏠 Asosiy menyu" if user_lang == 'uz' else "🏠 Tiykarǵı menyu"
    inline_keyboard.append([InlineKeyboardButton(text=home_text, callback_data="main_menu")])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
