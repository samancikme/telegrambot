from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
import database
import keyboards

router = Router()

QUIZ_TOTAL = 10  # Bolalar uchun 10 savol

CATEGORY_MAP = {
    # Qaraqalpaq
    "👋 Sálemlesiw": "salemlesiw",
    "🏠 Kúndelikli turmıs": "kundelikli",
    "🕒 Waqıt hám kúnler": "waqit",
    "👨‍👩‍👧‍👦 Shańaraq aǵzaları": "shanaraq",
    "🔢 Sanlar": "sanlar",
    "🍎 Azıq-awqat": "aziq_awqat",
    "🎨 Reńler": "renler",
    "🌳 Tábiyaat": "tabiyaat",
    "📚 Oqıw hám mektep": "oqiw",
    "👕 Kiyimler": "kiyimler",
    "🐾 Janiwarlar": "janiwarlar",
    "🍊 Miyweler": "miyweler",
    "🎮 Oyınshıqlar": "oyinshiqlar",
    "🦴 Dene aǵzaları": "dene_agzalari",

    # O'zbek
    "👋 Salomlashuv": "salemlesiw",
    "🏠 Kundalik hayot": "kundelikli",
    "🕒 Vaqt va kunlar": "waqit",
    "👨‍👩‍👧‍👦 Oila a'zolari": "shanaraq",
    "🔢 Sonlar": "sanlar",
    "🍎 Oziq-ovqat": "aziq_awqat",
    "🎨 Ranglar": "renler",
    "🌳 Tabiat": "tabiyaat",
    "📚 O'qish va maktab": "oqiw",
    "👕 Kiyimlar": "kiyimler",
    "🐾 Hayvonlar": "janiwarlar",
    "🍊 Mevalar": "miyweler",
    "🎮 O'yinchoqlar": "oyinshiqlar",
    "🦴 Tana a'zolari": "dene_agzalari",
}

def make_progress_bar(current, total):
    """Vizual progress bar: 🟢🟢🟢⚪⚪⚪"""
    filled = min(current, total)
    bar = '🟢' * filled + '⚪' * (total - filled)
    return f"{bar}  {current}/{total}"

def format_word_text(word, current, total, user_lang):
    progress = make_progress_bar(current, total)
    if user_lang == 'uz':
        return (
            f"🇺🇿 <b>{word[3]}</b>\n"
            f"🏳️ <b>{word[2]}</b>\n\n"
            f"💬 <i>{word[4]}</i>\n"
            f"💬 <i>{word[5]}</i>\n\n"
            f"{progress}"
        )
    else:
        return (
            f"🏳️ <b>{word[2]}</b>\n"
            f"🇺🇿 <b>{word[3]}</b>\n\n"
            f"💬 <i>{word[4]}</i>\n"
            f"💬 <i>{word[5]}</i>\n\n"
            f"{progress}"
        )

def get_score_stars(score, total):
    """Ball asosida yulduzcha qaytaradi"""
    ratio = score / total if total > 0 else 0
    if ratio >= 0.9:
        return "⭐⭐⭐"
    elif ratio >= 0.6:
        return "⭐⭐"
    else:
        return "⭐"

@router.message(CommandStart())
async def cmd_start(message: Message):
    is_new_user = database.add_user(message.from_user.id)

    if is_new_user:
        text = (
            "🌈 <b>Salom, do'stim!</b> 👋\n\n"
            "Men senga yangi so'zlar o'rgataman! 🎓\n"
            "Iltimos, tilni tanlang 👇\n\n"
            "〰️〰️〰️\n\n"
            "🌈 <b>Sálem, dosım!</b> 👋\n\n"
            "Men sagan jaña sózler úyretemın! 🎓\n"
            "Bot tılin saylań 👇"
        )
        await message.answer(text, reply_markup=keyboards.get_language_keyboard())
    else:
        user_lang = database.get_user_language(message.from_user.id)
        text = "🏠 Asosiy menyu" if user_lang == 'uz' else "🏠 Tiykarǵı menyu"
        await message.answer(text, reply_markup=keyboards.get_main_menu(user_lang))

@router.callback_query(F.data.startswith("lang:"))
async def language_selection_handler(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    database.set_user_language(callback.from_user.id, lang)

    await callback.message.delete()

    if lang == 'uz':
        await callback.message.answer(
            "🎉 Zo'r! O'zbek tili tanlandi!\nQuyidagi menyudan biror narsani tanla 👇",
            reply_markup=keyboards.get_main_menu(user_lang=lang)
        )
    else:
        await callback.message.answer(
            "🎉 Jaqsı! Qaraqalpaq tili saylındı!\nTómendegi menyudan nárse saylań 👇",
            reply_markup=keyboards.get_main_menu(user_lang=lang)
        )

    await callback.answer()

@router.message(F.text.in_(CATEGORY_MAP.keys()))
async def category_handler(message: Message):
    category_code = CATEGORY_MAP[message.text]
    total_words = database.get_words_count(category_code)
    user_lang = database.get_user_language(message.from_user.id)

    if total_words == 0:
        msg = "😔 Bu kategoriyada so'zlar topilmadi." if user_lang == 'uz' else "😔 Bul kategoriyada sózler tabilmadi."
        await message.answer(msg)
        return

    # Quvnoq kirish xabari
    intro = f"🎒 Tayyor bo'l! {total_words} ta so'z bor! ➡️" if user_lang == 'uz' else f"🎒 Tayar bol! {total_words} sóz bar! ➡️"
    await message.answer(intro)

    word = database.get_word(category_code, 0)
    text = format_word_text(word, 1, total_words, user_lang)
    markup = keyboards.get_pagination_keyboard(category_code, 0, total_words, user_lang=user_lang)

    if word[6] and word[7]:
        await message.answer_photo(photo=word[6], caption=text, reply_markup=markup)
        await message.answer_voice(voice=word[7])
    elif word[6]:
        await message.answer_photo(photo=word[6], caption=text, reply_markup=markup)
    elif word[7]:
        await message.answer_voice(voice=word[7], caption=text, reply_markup=markup)
    else:
        await message.answer(text=text, reply_markup=markup)

@router.callback_query(F.data.startswith("word:"))
async def pagination_handler(callback: CallbackQuery):
    data_parts = callback.data.split(":")
    category_code = data_parts[1]
    index = int(data_parts[2])
    user_lang = database.get_user_language(callback.from_user.id)

    total_words = database.get_words_count(category_code)
    word = database.get_word(category_code, index)

    if not word:
        err_msg = "❌ So'z topilmadi." if user_lang == 'uz' else "❌ Sóz tabilmadi."
        await callback.answer(err_msg, show_alert=True)
        return

    text = format_word_text(word, index + 1, total_words, user_lang)
    markup = keyboards.get_pagination_keyboard(category_code, index, total_words, user_lang=user_lang)

    # Oxirgi so'zga yetganda tabriklash
    if index == total_words - 1:
        congrats = "🎉 Zo'r! Barcha so'zlarni ko'rding!" if user_lang == 'uz' else "🎉 Jaqsı! Barlıq sózlerdi kórdiń!"
        await callback.answer(congrats, show_alert=True)
    else:
        await callback.answer()

    if callback.message.photo or callback.message.video or callback.message.document:
        await callback.message.edit_caption(caption=text, reply_markup=markup)
    else:
        await callback.message.edit_text(text=text, reply_markup=markup)

@router.callback_query(F.data.startswith("random_word:"))
async def random_word_handler(callback: CallbackQuery):
    import random as _random
    user_lang = database.get_user_language(callback.from_user.id)
    category_code = callback.data.split(":")[1]
    total_words = database.get_words_count(category_code)
    if total_words == 0:
        await callback.answer()
        return
    rand_index = _random.randint(0, total_words - 1)
    word = database.get_word(category_code, rand_index)
    if not word:
        await callback.answer()
        return
    text = format_word_text(word, rand_index + 1, total_words, user_lang)
    markup = keyboards.get_pagination_keyboard(category_code, rand_index, total_words, user_lang=user_lang)
    surprise = "🎲 Yangi so'z!" if user_lang == 'uz' else "🎲 Jaña sóz!"
    await callback.answer(surprise)
    if callback.message.photo or callback.message.video or callback.message.document:
        await callback.message.edit_caption(caption=text, reply_markup=markup)
    else:
        await callback.message.edit_text(text=text, reply_markup=markup)

@router.message(F.text.in_(["📚 So'zlarni o'rganish", "📚 Sózlerdi úyreniw"]))
async def words_menu_handler(message: Message):
    user_lang = database.get_user_language(message.from_user.id)
    text = "📚 Qaysi mavzuni o'rganmoqchisan? 🌟\nBitta tanlang, o'rganamiz! 👇" if user_lang == 'uz' else "📚 Qaysı temadan úyreniwdi qálersen? 🌟\nBirin saylań, úyrenemiz! 👇"
    await message.answer(text, reply_markup=keyboards.get_categories_menu(user_lang))

@router.message(F.text.in_(["⬅️ Ortqa", "⬅️ Arqaǵa"]))
async def back_menu_handler(message: Message):
    user_lang = database.get_user_language(message.from_user.id)
    text = "🏠 Asosiy menyuga qaytdik!" if user_lang == 'uz' else "🏠 Tiykarǵı menyuge qayttıq!"
    await message.answer(text, reply_markup=keyboards.get_main_menu(user_lang))

@router.message(F.text.in_(["🏆 Mening natijam", "🏆 Meniń nátiyjem"]))
async def stats_handler(message: Message):
    stats = database.get_user_stats(message.from_user.id)
    correct = stats[0]
    total = stats[1]
    user_lang = database.get_user_language(message.from_user.id)

    stars = get_score_stars(correct, total)

    if user_lang == 'uz':
        text = (
            f"🏆 <b>Sening natijang:</b>\n\n"
            f"Jami savollar: {total}\n"
            f"To'g'ri javoblar: {correct} ✅\n\n"
            f"{stars} Zo'r ketmoqda!"
        )
    else:
        text = (
            f"🏆 <b>Siziń nátiyjeń:</b>\n\n"
            f"Jámi sorawlar: {total}\n"
            f"Durıs juwaplar: {correct} ✅\n\n"
            f"{stars} Jaqsı ketpekte!"
        )

    await message.answer(text)

@router.message(F.text.in_(["🎮 O'yin (10 savol)", "🎮 Oyın (10 soraw)"]))
async def start_quiz_handler(message: Message):
    words = database.get_random_words(4)
    if len(words) < 4:
        user_lang = database.get_user_language(message.from_user.id)
        msg = "😔 Test uchun yetarli so'z yo'q." if user_lang == 'uz' else "😔 Test ushın jetkilikli sóz joq."
        await message.answer(msg)
        return

    import random
    correct_word = random.choice(words)
    user_lang = database.get_user_language(message.from_user.id)

    options = []
    for w in words:
        opt_text = w[2] if user_lang == 'uz' else w[3]
        options.append({'id': w[0], 'text': opt_text})

    correct_id = correct_word[0]
    question_text = correct_word[3] if user_lang == 'uz' else correct_word[2]

    if user_lang == 'uz':
        text = (
            f"🎮 <b>O'yin boshlandi! (1/{QUIZ_TOTAL})</b>\n\n"
            f"<b>{question_text}</b> — bu so'zning qoraqalpoqcha tarjimasi qaysi? 🤔"
        )
    else:
        text = (
            f"🎮 <b>Oyın baslandı! (1/{QUIZ_TOTAL})</b>\n\n"
            f"<b>{question_text}</b> — bul sózdiń ózbekshe awdarması qaysı? 🤔"
        )

    markup = keyboards.get_quiz_keyboard(options, correct_id, 1, 0, user_lang=user_lang)

    progress = '🟡' * 1 + '⬜' * (QUIZ_TOTAL - 1)
    if user_lang == 'uz':
        text = (
            f"🎮 <b>O'yin boshlandi!</b>\n"
            f"{progress}  1/{QUIZ_TOTAL}\n\n"
            f"❓ <b>{question_text}</b>\n"
            f"<i>qoraqalpoqcha tarjimasi qaysi?</i>"
        )
    else:
        text = (
            f"🎮 <b>Oyın baslandı!</b>\n"
            f"{progress}  1/{QUIZ_TOTAL}\n\n"
            f"❓ <b>{question_text}</b>\n"
            f"<i>ózbekshe awdarması qaysı?</i>"
        )

    await message.answer(text, reply_markup=markup)

@router.callback_query(F.data.startswith("quiz:"))
async def quiz_answer_handler(callback: CallbackQuery):
    data_parts = callback.data.split(":")
    is_correct = int(data_parts[1])
    q_num = int(data_parts[2])
    score = int(data_parts[3])

    user_lang = database.get_user_language(callback.from_user.id)

    score += is_correct

    if is_correct:
        msg = "🌟 Ajoyib! Zo'r ekansan!" if user_lang == 'uz' else "🌟 Ajayıp! Jaqsı ekensin!"
    else:
        msg = "😊 Xafa bo'lma, keyingisini ur!" if user_lang == 'uz' else "😊 Xáp bolma, keyingisine ur!"

    await callback.answer(msg, show_alert=False)

    if q_num >= QUIZ_TOTAL:
        database.update_bulk_user_stats(callback.from_user.id, score, QUIZ_TOTAL)

        stars = get_score_stars(score, QUIZ_TOTAL)

        if user_lang == 'uz':
            if score == QUIZ_TOTAL:
                praise = "🎉 Mukammal natija! Sen dahosан!"
            elif score >= QUIZ_TOTAL * 0.7:
                praise = "🎊 Juda yaxshi! Davom et!"
            else:
                praise = "💪 Harakat qilgansan! Yana bir marta o'yna!"

            final_text = (
                f"🏆 <b>O'yin tugadi!</b>\n\n"
                f"{stars}\n"
                f"Sen {QUIZ_TOTAL} ta savoldan <b>{score}</b> tasiga to'g'ri javob berding!\n\n"
                f"{praise}"
            )
            btn_text = "🏠 Asosiy menyu"
        else:
            if score == QUIZ_TOTAL:
                praise = "🎉 Kámil nátiyje! Sen dahısan!"
            elif score >= QUIZ_TOTAL * 0.7:
                praise = "🎊 Júdá jaqsı! Dawam et!"
            else:
                praise = "💪 Háreketlendin! Yana bir mártе oyına!"

            final_text = (
                f"🏆 <b>Oyın tamamlandı!</b>\n\n"
                f"{stars}\n"
                f"Sen {QUIZ_TOTAL} sorawdan <b>{score}</b>ewine durıs juwap berdiń!\n\n"
                f"{praise}"
            )
            btn_text = "🏠 Tiykarǵı menyu"

        markup = keyboards.InlineKeyboardMarkup(
            inline_keyboard=[[keyboards.InlineKeyboardButton(text=btn_text, callback_data="main_menu")]]
        )

        await callback.message.edit_text(text=final_text, reply_markup=markup)
        return

    words = database.get_random_words(4)
    import random
    correct_word = random.choice(words)
    options = []

    for w in words:
        opt_text = w[2] if user_lang == 'uz' else w[3]
        options.append({'id': w[0], 'text': opt_text})

    correct_id = correct_word[0]
    question_text = correct_word[3] if user_lang == 'uz' else correct_word[2]

    next_q_num = q_num + 1
    progress = '🟡' * next_q_num + '⬜' * (QUIZ_TOTAL - next_q_num)

    if user_lang == 'uz':
        status_emoji = "✅" if is_correct else "❌"
        text = (
            f"{status_emoji}  Hisob: <b>{score}/{q_num}</b>\n"
            f"{progress}  {next_q_num}/{QUIZ_TOTAL}\n\n"
            f"❓ <b>{question_text}</b>\n"
            f"<i>qoraqalpoqcha tarjimasi qaysi?</i>"
        )
    else:
        status_emoji = "✅" if is_correct else "❌"
        text = (
            f"{status_emoji}  Upey: <b>{score}/{q_num}</b>\n"
            f"{progress}  {next_q_num}/{QUIZ_TOTAL}\n\n"
            f"❓ <b>{question_text}</b>\n"
            f"<i>ózbekshe awdarması qaysı?</i>"
        )

    markup = keyboards.get_quiz_keyboard(options, correct_id, next_q_num, score, user_lang=user_lang)
    await callback.message.edit_text(text=text, reply_markup=markup)

@router.callback_query(F.data.startswith("quiz_stop:"))
async def quiz_stop_handler(callback: CallbackQuery):
    data_parts = callback.data.split(":")
    score = int(data_parts[1])
    q_num = int(data_parts[2])

    user_lang = database.get_user_language(callback.from_user.id)

    if q_num > 0:
        database.update_bulk_user_stats(callback.from_user.id, score, q_num)

    stars = get_score_stars(score, q_num) if q_num > 0 else ""

    if user_lang == 'uz':
        text = (
            f"🛑 <b>O'yin to'xtatildi!</b>\n\n"
            f"{stars}\n"
            f"Sen {q_num} ta savoldan <b>{score}</b> tasiga to'g'ri javob berding.\n"
            f"💪 Keyingi safar ko'proq urinib ko'r!"
        )
        btn_text = "🏠 Asosiy menyu"
    else:
        text = (
            f"🛑 <b>Oyın toqtatıldı!</b>\n\n"
            f"{stars}\n"
            f"Sen {q_num} sorawdan <b>{score}</b>ewine durıs juwap berdiń.\n"
            f"💪 Keyingi jola kóbirek urınıp kór!"
        )
        btn_text = "🏠 Tiykarǵı menyu"

    markup = keyboards.InlineKeyboardMarkup(
        inline_keyboard=[[keyboards.InlineKeyboardButton(text=btn_text, callback_data="main_menu")]]
    )

    await callback.message.edit_text(text=text, reply_markup=markup)
    await callback.answer()

@router.callback_query(F.data == "main_menu")
async def main_menu_inline_handler(callback: CallbackQuery):
    user_lang = database.get_user_language(callback.from_user.id)
    text = "🏠 Asosiy menyuga qaytdik!" if user_lang == 'uz' else "🏠 Tiykarǵı menyuge qayttıq!"

    await callback.message.delete()
    await callback.message.answer(text, reply_markup=keyboards.get_main_menu(user_lang))
    await callback.answer()

@router.message(F.text.in_(["🔄 Tilni o'zgartirish", "🔄 Tildi ózgertiw"]))
async def change_language_handler(message: Message):
    text = (
        "🌐 Tilni tanlang / Tıldı saylań:\n\n"
        "〰️〰️〰️"
    )
    await message.answer(text, reply_markup=keyboards.get_language_keyboard())

@router.message(F.text.in_(["📸 Suratli lug'at", "📸 Súwretli sózlik"]))
async def pixture_dict_menu_handler(message: Message):
    user_lang = database.get_user_language(message.from_user.id)

    words = database.get_picture_dictionary_words(limit_per_category=2)

    if not words:
        await message.answer("😔 Lug'atda so'zlar yetarli emas / Sózlikte sózler jetkiliksiz.")
        return

    markup = keyboards.get_picture_dictionary_keyboard(words, user_lang)

    if user_lang == 'uz':
        text = "📸 <b>Suratli lug'at</b>\n\nQaysi so'zning rasmini ko'rmoqchisan? 👇🎨"
    else:
        text = "📸 <b>Súwretli sózlik</b>\n\nQaysı sózdiń súwretin kórmekshisin? 👇🎨"

    await message.answer(text, reply_markup=markup)

@router.callback_query(F.data.startswith("pic:"))
async def process_picture_dictionary(callback: CallbackQuery):
    import os
    from aiogram.types import FSInputFile

    user_lang = database.get_user_language(callback.from_user.id)
    word_id = int(callback.data.split(":")[1])

    word_data = database.get_word_by_id(word_id)
    if not word_data:
        await callback.answer("So'z topilmadi / Sóz tabılmadı")
        return

    word_uz = word_data[3]
    word_qq = word_data[2]
    word_text = word_uz if user_lang == 'uz' else word_qq

    IMAGE_MAP = {
        # Salomlashuv
        "Assalomu alaykum": "assalomualeykum.png",
        "Xayrli tong":      "hayirlitong.png",
        # Kundalik hayot
        "Uy":               "uy.png",
        # Vaqt va kunlar
        "Bugun":            "bugun.png",
        # Oila a'zolari
        "Bobo":             "bobo.png",
        "Buvi":             "buvi.png",
        # Sonlar
        "Bir":              "bir.png",
        "Ikki":             "ikki.png",
        # Oziq-ovqat
        "Non":              "non.png",
        "Suv":              "suv.png",
        # Ranglar
        "Qizil":            "qizil.png",
        "Yashil":           "yashil.png",
        # Tabiat
        "Osmon":            "osmon.png",
        "Quyosh":           "quyosh.png",
        # O'qish
        "Kitob":            "kitob.png",
        "Qalam":            "qalam.png",
        # Kiyimlar
        "Ko'ylak":                  "koylak.png",
        "Oyoq kiyim / Poyabzal":   "oyoqkiyim.png",
        # Hayvonlar
        "Mushuk":           "mushuk.png",
        "Kuchuk":           "kuchuk.png",
        # Mevalar
        "Olma":             "olma.png",
        "Banan":            "banan.png",
        # O'yinchoqlar
        "Koptok":           "koptok.png",
        "Mashina":          "mashina.png",
        # Tana a'zolari
        "Bosh":             "bosh.png",
        "Ko'z":             "koz.png",
    }

    import os as _os
    base_dir = _os.path.dirname(_os.path.abspath(__file__))
    image_filename = IMAGE_MAP.get(word_uz)
    image_path = _os.path.join(base_dir, "images", image_filename) if image_filename else None

    await callback.answer()

    if image_path and _os.path.exists(image_path):
        caption_text = f"🖼 <b>{word_text}</b> 🎨"
        await callback.message.delete()
        await callback.message.answer_photo(photo=FSInputFile(image_path), caption=caption_text)
    else:
        no_photo_text = "⚠️ Bu so'z uchun rasm yuklanmagan." if user_lang == 'uz' else "⚠️ Bul sóz ushın súwret júklenbegenіi."
        await callback.message.edit_text(f"🔤 <b>{word_text}</b>\n\n{no_photo_text}")
